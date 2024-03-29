# Sub package for Filter-Bank Canonical Correlation Analysis

import warnings
import scipy.signal
from scipy.stats import pearsonr
import numpy as np
from sklearn.cross_decomposition import CCA

"""
Class for Synchronous (Real Time)
Filter-Bank Canonical Correlation Analysis
"""

class filterbankCCA:

    """
    Parameters:

    eeg (dtype: ndarray (dtype: float64)): The eeg data
    list_freqs (dtype: ): The list of existing frequencies
    s (dtype: int64): sampling rate

    """
    def __init__(self, eeg, list_freqs, s, num_harms=3, num_fbs=5):
        self.data = eeg 
        self.data_shape = eeg.shape
        self.freqs = list_freqs
        self.SAMPLINGRATE = s
        self.harmonicsQ = num_harms # The number of harmonics, idk what that is
        self.filterbanksQ = num_fbs # The quantity of filterbanks

    """
    Paramters:
    Return:
    """   
    def __init__(self):
        pass
    
    
    def syncfbCCA(self):
        
        pass
    
    """
    Parameters:
    @param data: EEG data
    @param list_freqs: frequencies we want
    @param fs: Sampling frequncy (of the board)
    @param: num_harams: idk
    @param: num_fbs: idk
    Return:
    """
    def asyncfbCCA(self, data, list_freqs, fs, num_harms=3, num_fbs=5):
        
        fb_coefs = np.power(np.arange(1, num_fbs + 1), (-1.25)) + 0.25

        num_targs = len(list_freqs)
        _, num_smpls = data.shape

        y_ref = cca_reference(list_freqs, fs, num_smpls, num_harms)
        cca = CCA(n_components=1)  # initialize CCA

        # result matrix
        r = np.zeros((num_fbs, num_targs))

        for fb_i in range(num_fbs):  # filter bank number, deal with different filter bank
            testdata = filterbank(data, fs, fb_i)  # data after filtering
            for class_i in range(num_targs):
                refdata = np.squeeze(y_ref[class_i, :, :])  # pick corresponding freq target reference signal
                test_C, ref_C = cca.fit_transform(testdata.T, refdata.T)
                r_tmp, _ = pearsonr(np.squeeze(test_C), np.squeeze(ref_C))  # return r and p_value
                if r_tmp == np.nan:
                    r_tmp = 0
                r[fb_i, class_i] = r_tmp

        rho = np.dot(fb_coefs, r)  # weighted sum of r from all different filter banks' result
        print("Rho: "+str(rho))  # print out the correlation
        result = np.argmax(
            rho)  # get maximum from the target as the final predict (get the index), and index indicates the maximum entry(most possible target)
        ''' Threshold '''
        THRESHOLD = 0.97
        if abs(rho[
                result]) < THRESHOLD:  # 2.587=np.sum(fb_coefs*0.8) #2.91=np.sum(fb_coefs*0.9) #1.941=np.sum(fb_coefs*0.6)
            return 999  # if the correlation isn't big enough, do not return any command
        else:
            return result

"""
Creates a filterbank from eeg data

Parameters:
eeg (multidimensional ndarray: float64): The input eeg data from the eeg data stream
samplingRate ():
index (int): The current index of the filterbank

"""
def filterbank(eeg, samplingRate, fbIndex):
    
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



'''
Generate reference signals for the canonical correlation analysis (CCA)
-based steady-state visual evoked potentials (SSVEPs) detection [1, 2].
function [ y_ref ] = cca_reference(listFreq, fs,  nSmpls, nHarms)
Input:
  listFreq        : List for stimulus frequencies
  fs              : Sampling frequency
  nSmpls          : # of samples in an epoch
  nHarms          : # of harmonics
Output:
  y_ref           : Generated reference signals
                   (# of targets, 2*# of channels, Data length [sample])
Reference:
  [1] Z. Lin, C. Zhang, W. Wu, and X. Gao,
      "Frequency Recognition Based on Canonical Correlation Analysis for 
       SSVEP-Based BCI",
      IEEE Trans. Biomed. Eng., 54(6), 1172-1176, 2007.
  [2] G. Bin, X. Gao, Z. Yan, B. Hong, and S. Gao,
      "An online multi-channel SSVEP-based brain-computer interface using
       a canonical correlation analysis method",
      J. Neural Eng., 6 (2009) 046002 (6pp).
'''      
def cca_reference(list_freqs, fs, num_smpls, num_harms=3):
    
    num_freqs = len(list_freqs)
    tidx = np.arange(1,num_smpls+1)/fs #time index
    
    y_ref = np.zeros((num_freqs, 2*num_harms, num_smpls))
    for freq_i in range(num_freqs):
        tmp = []
        for harm_i in range(1,num_harms+1):
            stim_freq = list_freqs[freq_i]  #in HZ
            # Sin and Cos
            tmp.extend([np.sin(2*np.pi*tidx*harm_i*stim_freq),
                       np.cos(2*np.pi*tidx*harm_i*stim_freq)])
        y_ref[freq_i] = tmp # 2*num_harms because include both sin and cos
    
    return y_ref

'''
Base on fbcca, but adapt to our input format
'''
def fbcca_realtime(data, list_freqs, fs, num_harms=3, num_fbs=5):
    fb_coefs = np.power(np.arange(1, num_fbs + 1), (-1.25)) + 0.25

    num_targs = len(list_freqs)
    _, num_smpls = data.shape

    y_ref = cca_reference(list_freqs, fs, num_smpls, num_harms)
    cca = CCA(n_components=1)  # initialize CCA

    # result matrix
    r = np.zeros((num_fbs, num_targs))

    for fb_i in range(num_fbs):  # filter bank number, deal with different filter bank
        testdata = filterbank(data, fs, fb_i)  # data after filtering
        for class_i in range(num_targs):
            refdata = np.squeeze(y_ref[class_i, :, :])  # pick corresponding freq target reference signal
            test_C, ref_C = cca.fit_transform(testdata.T, refdata.T)
            r_tmp, _ = pearsonr(np.squeeze(test_C), np.squeeze(ref_C))  # return r and p_value
            if r_tmp == np.nan:
                r_tmp = 0
            r[fb_i, class_i] = r_tmp

    rho = np.dot(fb_coefs, r)  # weighted sum of r from all different filter banks' result
    print("RHO: "+rho)  # print out the correlation
    result = np.argmax(
        rho)  # get maximum from the target as the final predict (get the index), and index indicates the maximum entry(most possible target)
    ''' Threshold '''
    THRESHOLD = 1.2
    if abs(rho[
               result]) < THRESHOLD:  # 2.587=np.sum(fb_coefs*0.8) #2.91=np.sum(fb_coefs*0.9) #1.941=np.sum(fb_coefs*0.6)
        return 999  # if the correlation isn't big enough, do not return any command
    else:
        return result