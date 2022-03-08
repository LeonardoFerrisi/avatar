# Sub package for Filter-Bank Canonical Correlation Analysis

import warnings
import scipy.signal
import numpy as np

"""
Class for Synchronous (Real Time)
Filter-Bank Canonical Correlation Analysis
"""
class filterbankCCA_sync:
    """
    Paramters:

    Return:

    """
    def __init__(self):
        pass

"""

"""
class filterbankCCA_async:

    def __init__(self):
        pass


def filterbank(eeg, samplingRate, fbIndex):
    """
    Creates a filterbank from eeg data

    Parameters:
    eeg (multidimensional ndarray: float64): The input eeg data from the eeg data stream
    samplingRate ():
    index (int): The current index of the filterbank

    """
    if fbIndex == None:
        warnings.warn('stats:filterbank:MissingInput '\
                      +'Missing filter index. Default value (idx_fb = 0) will be used.')
        fbIndex = 0
    elif (fbIndex < 0 or 9 < fbIndex):
        raise ValueError('stats:filterbank:InvalidInput '\
                          +'The number of sub-bands must be 0 <= idx_fb <= 9.')
            
    if (len(eeg.shape)==2): # if 2d
        num_chans = eeg.shape[0]
        num_trials = 1
    else: #if shape > 2d
        num_chans, _, num_trials = eeg.shape # eeg.shape
    
    # Nyquist Frequency = Fs/2N
    Nq = samplingRate/2
    
    passband = [6, 14, 22, 30, 38, 46, 54, 62, 70, 78]
    stopband = [4, 10, 16, 24, 32, 40, 48, 56, 64, 72]
    Wp = [passband[fbIndex]/Nq, 90/Nq]
    Ws = [stopband[fbIndex]/Nq, 100/Nq]
    [N, Wn] = scipy.signal.cheb1ord(Wp, Ws, 3, 40) # band pass filter StopBand=[Ws(1)~Ws(2)] PassBand=[Wp(1)~Wp(2)]
    [B, A] = scipy.signal.cheby1(N, 0.5, Wn, 'bandpass') # Wn passband edge frequency
    
    y = np.zeros(eeg.shape)
    if (num_trials == 1):
        for ch_i in range(num_chans):
            #apply filter, zero phass filtering by applying a linear filter twice, once forward and once backwards.
            # to match matlab result we need to change padding length
            y[ch_i, :] = scipy.signal.filtfilt(B, A, eeg[ch_i, :], padtype = 'odd', padlen=3*(max(len(B),len(A))-1))
        
    else:
        for trial_i in range(num_trials):
            for ch_i in range(num_chans):
                y[ch_i, :, trial_i] = scipy.signal.filtfilt(B, A, eeg[ch_i, :, trial_i], padtype = 'odd', padlen=3*(max(len(B),len(A))-1))
           
    return y