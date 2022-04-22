"""
This module contains method to check if beam is broken, which signals the start
of a trial.
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

from daqface import DAQ as daq
import numpy as np


def check_beam(device, channels, beam_channel):
    """
    Check if beam is broken. If beam is broken, TTL is high and data is 
    measured at 5 V. If beam is not broken, TTL is low and data is measured at
    0 V. If mean of data > 1, means that in 0.1 s there is a TTL high, ergo
    beam was broken.

    Parameters
    ----------
    device : str
        Name of device in NI-board where beam sensor is connected.

    channels : int
        Number of analog input channels read.

    beam_channel : int
        Index of beam channel.

    Return
    ------
    broken : bool
        Indicator if beam is broken or not.
    """

    try:
        check = daq.ThreadSafeAnalogInput(device, channels, 1000, 0.1)
        analog_data = check.DoTask()
        check_mean = np.mean(analog_data[beam_channel])

        return check_mean > 1
    except:
        return False
