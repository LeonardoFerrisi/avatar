# Sub package for Filter-Bank Canonical Correlation Analysis

from sklearn.cross_decomposition import CCA
from filterbank import filterbank
from scipy.stats import pearsonr
import numpy as np

def fbcca(eeg, list_freqs, fs, num_harms=3, num_fbs=5):

    fb_coefs = np.power(np.arange(1, num_fbs+1), (-1.25)) + 0.25

    num_targs, _, num_smpls = eeg.shape 