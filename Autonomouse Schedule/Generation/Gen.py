"""
This module contains methods to generate randomise sequence of trials.
"""

import numpy as np


def odor_sequence(odour_choice, n_trials):
    """
    Randomized sequence after odour.

    Parameters
    ----------
    odour_choice : list
        List of odours to be randomised from.

    n_trials : int
        Number of trials in a schedule defined in UI.
    """

    sequence = np.empty(n_trials, dtype=int)
    length = len(odour_choice)
    rest = n_trials % length

    for i in range(int(n_trials/length)):
        sequence[i*length:(i+1)*length] = np.random.choice(odour_choice,
                                                           length,
                                                           replace=False)
    if rest != 0:
        sequence[-rest:] = np.random.choice(odour_choice, rest, replace=False)

    return sequence


def reward_sequence(n_trials):
    """
    Generate sequence after reward.

    Parameter
    ---------
    n_trials : int
        Number of trials in a schedule defined in UI.
    """

    sequence = [0]
    while sum(sequence) != int(n_trials/2):
        # initialise reward vector
        # with this method, the reward sequence has no more than 3 same values after one another
        sequence = np.empty(n_trials, dtype=int)
        sequence[0:3] = 1
        sequence[3:6] = 0

        for t in range(6, n_trials):
            preceding_sum = sum(sequence[t-3:t])
            if preceding_sum == 0:
                sequence[t] = 1
            elif preceding_sum == 3:
                sequence[t] = 0
            else:
                sequence[t] = np.random.randint(0, 2)

    return sequence
