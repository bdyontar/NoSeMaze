"""

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

import numpy
import math


def binary_to_digital_map(bin_buffer: numpy.ndarray) -> numpy.ndarray:
    """
    If we have a sequence of 1s and 0s corresponding to digital ON 
    and OFF times, we want to map this to digital commands that the digital 
    ports can read and implement.

    Input should be mapped as a 2d numpy array (dtype=numpy.uint32), rows are 
    individual lines, columns are continuous time points. Ignores sampling 
    rate until we tell NIDAQmx what it is. 

    Parameters
    ----------
    bin_buffer : ndarray
        An integer array of zeros and ones to be converted.

    Returns
    -------
    digital : ndarray
        Mapped digital commands.
    """

    digital = numpy.zeros((bin_buffer.shape[0], bin_buffer.shape[1]))

    n_lines = digital.shape[0]

    for line in range(n_lines):
        digital[line] = bin_buffer[line] * math.pow(2, line)

    return numpy.uint32(digital)
