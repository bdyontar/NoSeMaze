# -*- coding: utf-8 -*-
"""
This module is used to filter analog data read from NI-Board.
"""
"""
Copyright (c) 2022 [Insert name here]

This file is part of NoSeMaze.

NoSeMaze is free software: you can redistribute it and/or 
modify it under the terms of GNU General Public License as 
published by the Free Software Foundation, either version 3 
of the License, or (at your option) at any later version.

NoSeMaze is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public 
License along with NoSeMaze. If not, see https://www.gnu.org/licenses.
"""

import numpy as np
import scipy.signal as spsig


def Gauss_Filter(data, k, fs, fcut):
    length = int(fs/fcut)
    std = k*length
    rf_gauss = spsig.gaussian(length, std)
    rf_gauss = rf_gauss/np.sum(rf_gauss)

    fData = np.convolve(rf_gauss, data, mode='same')
    fData = fData[length:(len(fData)-length)]

    return fData


def Square_Filter(data, fs, fcut):
    length = int(fs/fcut)
    rf_square = np.ones(length)
    rf_square = rf_square/np.sum(rf_square)

    fData = np.convolve(rf_square, data, mode='same')
    fData = fData[length:(len(fData)-length)]

    return fData
