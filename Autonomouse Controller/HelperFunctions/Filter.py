# -*- coding: utf-8 -*-
"""
This module is used to filter analog data read from NI-Board.

Created on Fri Oct 26 12:07:45 2018

@author: jir-mb
"""

import numpy as np
import scipy.signal as spsig

def Gauss_Filter(data, k, fs, fcut):
    length = int(fs/fcut)
    std = k*length
    rf_gauss = spsig.gaussian(length,std)
    rf_gauss = rf_gauss/np.sum(rf_gauss)
    
    fData = np.convolve(rf_gauss,data, mode='same')
    fData = fData[length:(len(fData)-length)]
    
    return fData
    
def Square_Filter(data, fs, fcut):
    length = int(fs/fcut)
    rf_square = np.ones(length)
    rf_square = rf_square/np.sum(rf_square)
    
    fData = np.convolve(rf_square,data,mode ='same')
    fData = fData[length:(len(fData)-length)]
    
    return fData