import socket
import argparse
from threading import local
import time
import numpy as np

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations, NoiseTypes

from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams

import math
import socket
import zmq
import sys

from fbcca import filterbankCCA

"""
SFPR: Signal Filtering and Processing Relay
"""


class SFPR:

    def __init__(self, masterboardId : int):

        # Initilize the board for usage in local
        board_id = -2
        params = BrainFlowInputParams()
        params.ip_port = 6677
        params.other_info = str(masterboardId) # board id of master board (is a synth board)
        params.ip_address = '225.1.1.1'
        self.board_recv = BoardShim(board_id, input_params=params)

        self.master_board_id = masterboardId

        self.eeg_channels = BoardShim.get_eeg_channels(
            int(self.master_board_id))
        self.sampling_rate = BoardShim.get_sampling_rate(
            self.master_board_id)
        self.nfft = DataFilter.get_nearest_power_of_two(self.sampling_rate)
        # Init stream
        self.initStream = False

        # Data holders
        self.wholeData = 0
        self.currentData = 0

        # Relays - activate or deactivate these depending on what we want to measure
        self.relays = {'focus': False, 'relaxation': False, 'alpha': False,
                       'beta': False, 'gamma': False, 'delta': False, 'theta': False}

        # For sending commands to output (Module 3)
        # ZMQ Attempt
        self.ctx = zmq.Context()
        self.sock = self.ctx.socket(zmq.PUB)
        self.sock.bind("tcp://*:1234")
        ################

        # for controlling loop
        self.inf = False

        # predictions if using ml
        self.prediction = 0.0

        # On off switches for what to use (use the builtin methods to change them!)
        self.doFocus = False
        self.doSSVEPbool = False
        self.doRelaxation = False

    def recieve(self, isInf=True, runOnce=False):
        '''
        Recieves the stream of EEG data from a designated port {params.ip_address}:{params.ip_port}
        @param isInf: Determines whether or not we want to be running a infinite loop 
        @param runOnce: Determine whether or not we want to run only once (isInf cannot be on)
        '''
        self.board_recv.prepare_session()
        self.board_recv.start_stream(45000)

        self.inf = isInf # Whether or not loop runs forever

        time.sleep(5)

        # switches #####################
        modelPrepared = False

        keep_alive = self.inf

        sendOverSocket = True

        socketPrepared = False

        #############################

        useML = self.doFocus # Right now only checks for measuring ML metric for concentration
        useSVVEP = self.doSSVEPbool

        while keep_alive:

            # self.wholeData = self.board_recv.get_board_data()

            self.currentData = self.board_recv.get_current_board_data(
                self.sampling_rate*5)

            if self.currentData.size == 0:
                print("still empty")
                # print(self.currentData)

            else:
                
                # APPLY essential filters #######################

                # Do NOTCH filter
                
                try: 
                    for count, channel in enumerate(self.eeg_channels):
                        DataFilter.remove_environmental_noise(self.currentData[channel], self.sampling_rate, NoiseTypes.SIXTY.value)
                    # print("NOTCH FILTER SUCCESSFULLY APPLIED")
                
                except:
                    print("NOTCH FILTER FAILED TO EXECUTE")


                #################################################

                if useML:

                    bands = DataFilter.get_avg_band_powers(
                    self.currentData, self.eeg_channels, self.sampling_rate, True)
                    print('Bands size: %f' % len(bands))
                    feature_vector = np.concatenate((bands[0], bands[1]))

                    if modelPrepared == False:
                        self.prepareMLModel('focus')
                        modelPrepared = True
                    else:
                        # print('Bands: ', bands)
                        # print('Feature Vector: ', str(feature_vector))
                        self.prediction = self.concentration.predict(
                            feature_vector)
                        print("Concentration Lvl: %f" % self.prediction) 

                        if sendOverSocket:
                            toSend = str(self.prediction)
                            output = f"Calculated Focus value: {toSend}"
                            self.sock.send_string(output)

                if useSVVEP:

                    # Do all SSVEP values for 4 squares we want 
                    # wantedFreqs = [10, 15, 20, 25] # wanted values in HZ
                    wantedFreqs = np.arange(4.0, 15.0+1, 4.0) # wanted values in HZ
                    # wantedFreqs = [6.0, 9.0, 12.0, 15.0] # wanted values in HZ

                    self.doSSVEP(num_channels=self.eeg_channels, currentData=self.currentData, samplingRate=self.sampling_rate, sendOverSocket=False, desiredFreqs=wantedFreqs)

                    # FORMAT: doSSVEP(num_channels, currentData, samplingRate, sendOverSocket, valuesWeWant : list):

                    # For sending SSVEP values out


        if runOnce and not isInf:
            self.runOnce()

    '''
    Takes parameters from reciever function and sfpr class in order to get SSVEP values from a list
    @param num_channels: The number of eeg_channels our board has
    @param currentData: The current data being streamed from our board
    @param samplingRate: The sampling rate of our board
    @param sendOverSocket: Boolean value of whether or not we want to send over socket
    @param valuesWeWant: A list containing values of SSVEP we want to scan for (SSVEP values are in Hertz)
    '''
    def doSSVEP(self, num_channels, currentData, samplingRate, sendOverSocket, desiredFreqs):

        f = filterbankCCA()
        
        # totalResult = 0


        for chan in num_channels:
            result = f.asyncfbCCA(data=currentData, list_freqs=desiredFreqs, fs=samplingRate)
            print(f"Channel: {chan}, FILTERBANKCCA output: >> {str(result)}")    

        try: 
            if sendOverSocket:
                toSend = str("_ssvepTotals")
                # output = f"Calculated SSVEP values: {toSend}"
                output = toSend
                self.sock.send_string(output)
        except:
            print("Socket send FAILED")

    ###################################################################

    def activateFocus(self):
        '''
        Sets the focus value to true, any other values are true shuts them off.
        RUN THIS BEFORE YOU run recieve()
        '''
        if self.doFocus == False:
            if self.doSSVEP:
                self.doSSVEP = False
            if self.doRelaxation:
                self.doRelaxation = False
            print("\nMeasuring FOCUS value from data\n")
            self.doFocus = True


    # Theres a better way of doing this but whatever...

    def activateSSVEP(self):
        # TODO: Needs more info, activate SSVEP should as for a range of values that it can send out
        '''
        Sets the check for SSVEP value to true, any other values are true shuts them off.
        RUN THIS BEFORE YOU run recieve()
        '''
        if self.doSSVEPbool == False:
            if self.doFocus:
                self.doFocus = False
            if self.doRelaxation:
                self.doRelaxation = False
            print("\nMeasuring SSVEP value from data\n")

            self.doSSVEPbool = True

    def activateRelaxation(self):
        '''
        Sets the check for SSVEP value to true, any other values are true shuts them off.
        RUN THIS BEFORE YOU run recieve()
        '''
        if self.doRelaxation == False:
            if self.doFocus:
                self.doFocus = False
            if self.doSSVEP:
                self.doSSVEP = False

            print("\nMeasuring RELAXATION value from data\n")

            self.doRelaxation = True

    ########################################################

    def prepareMLModel(self, metric):
        '''
        Prepares the machine learning model to predict a value for. (Currently only accomadates concentration values)
        @param metric: The build in ML metric we are using. Choose among: 'focus'
        '''
        if metric == 'focus':
            MLModel.enable_dev_ml_logger()
            concentration_params = BrainFlowModelParams(
                BrainFlowMetrics.CONCENTRATION.value, BrainFlowClassifiers.REGRESSION.value)

            self.concentration = MLModel(concentration_params)
            self.concentration.prepare()

    def runOnce(self):
        '''
        Runs the SFPR only once
        '''
        self.currentData = self.board_recv.get_current_board_data(
            self.sampling_rate*5)
        bands = DataFilter.get_avg_band_powers(
            self.currentData, self.eeg_channels, self.sampling_rate, True)

        print(bands)
        print(len(bands))

    def endStream(self):
        '''
        Ends the board's data stream
        '''
        self.board_recv.stop_stream()

    def releaseSession(self):
        '''
        Releases the board stream session, in order to run board again... must re-prepare session
        '''
        self.board_recv.release_session()


if __name__ == "__main__":
    newRelay = SFPR(-1)
    # newRelay = SFPR(0)
    # newRelay.activateFocus()
    newRelay.activateSSVEP()
    # print('Do SSVEP value: ', newRelay.doSSVEP)
    newRelay.recieve()
    exit = input("Press ENTER to exit")