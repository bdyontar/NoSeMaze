"""
This module contains method to input pulse parameters to 
get desired pulse.
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

from PyPulse import PulseGeneration
import numpy as np


def make_pulse(sampling_rate : int, global_onset : float, global_offset : float, params_list : list[dict]):
    """
    Parameters
    ----------
    sampling_rate : int
        Sampling rate defined in hardware configuration

    global_onset : float
        Number of element set to be an onset.

    global_offset : float
        Number of element set to be an offset.

    params_list : list
        List of pulse parameters.

    Returns
    -------
    pulse_matrix : 2d-list
        List of pulse.

    t : ndarray
        Time axis.
    """

    longest_t = []
    pulses = list()
    total = len(params_list)

    for i, params in enumerate(params_list):
        if params['type'] == 'Simple':
            this_pulse, t = PulseGeneration.simple_pulse(sampling_rate, params)
        elif params['type'] == 'Noise':
            this_pulse, t = PulseGeneration.noise_pulse(sampling_rate, params)
        elif params['type'] == 'DummyNoise':
            this_pulse, t = PulseGeneration.dummy_noise_pulse(
                sampling_rate, params)
        elif params['type'] == 'RandomNoise':
            this_pulse, t = PulseGeneration.random_simple_pulse(
                sampling_rate, params)
        elif params['type'] == 'Plume':
            this_pulse, t = PulseGeneration.plume_pulse(sampling_rate, params)
        elif params['type'] == 'ContCorr':
            this_pulse, t = PulseGeneration.spec_time_pulse(
                sampling_rate, params)
        elif params['type'] == 'Concatenate':
            this_pulse, t = PulseGeneration.concatenated_pulse(
                sampling_rate, params, i, total)
        else:
            raise ValueError

        pulses.append(this_pulse)
        if len(t) > len(longest_t):
            longest_t = t

    pulse_matrix = np.zeros((len(pulses), len(
        longest_t) + int((global_onset + global_offset) * sampling_rate)))

    for p, pulse in enumerate(pulses):
        pulse_matrix[p][int(global_onset * sampling_rate)
                            :int(global_onset * sampling_rate)+len(pulse)] = pulse

    t = np.linspace(
        0, pulse_matrix.shape[1] / sampling_rate, pulse_matrix.shape[1])

    return pulse_matrix, t
