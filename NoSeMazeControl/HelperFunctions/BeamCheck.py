"""
This module contains method to check if beam is broken, which signals the start
of a trial.
"""
"""
Copyright (c) 2019, 2022 [copyright holders here]

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


def check_beam(beam_channel):
    """
    Check if beam is broken. If beam is broken, TTL is high. 
    If beam is not broken, TTL is low.
    
    Parameters
    ----------

    beam_channel : str
        String of beam channel.

    Return
    ------
    broken : bool
        Indicator if beam is broken or not.
    """

    try:
        check = daq.ThreadSafeDigitalInput(beam_channel)
        digital_data = check.DoTask()
        
        # Check if any logical highs are contained
        contains_ones = np.any(digital_data == 1)

        return contains_ones
    except:
        return False
