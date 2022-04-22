"""
This module contains methods used in analysis windows or in report in Email
module.

Calculation of d' is left as commentar down below in 
weighted_binned_performance method.
"""
"""
This file is part of NoSeMaze.

NoSeMaze is free software: you can redistribute it and/or modify it under the terms of GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) at any later version.

NoSeMaze is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NoSeMaze. If not, see [https://www.gnu.org/licenses](https://www.gnu.org/licenses).

"""

import numpy as np
import datetime
import scipy.stats as stats
from Models import Experiment

Z = stats.norm.ppf


def n_trials_performed(mouse: Experiment.Mouse) -> int:
    """
    Calculate number of trials performed by a mouse since the start of the 
    experiment.

    Parameters
    ----------
    mouse : Experiment.mouse class
        Instance of mouse to calculate total trials performed.

    Returns
    -------
    total_trials : int
        Total trials performed since experiment start.
    """
    total_trials = 0
    for schedule in mouse.schedule_list:
        total_trials += schedule.current_trial

    return total_trials


def binned_performance(mouse: Experiment.Mouse, bin_size: int, idx: int) -> list[float]:
    """
    Calculate hit rate and correct rejection rate and returns them.

    Parameters
    ----------
    mouse : Experiment.mouse class
        Instance of Experiment.mouse class that is of interest.

    bin_size : int
        Size of bin. 

        It is the number of trials used to calculate hit rate or 
        correct rejection rate.

    idx : int
        Index of tab window selected on analysis window.

        It differentiate between left GNG or right GNG

    Returns
    -------
    binned_correct : list of float
        List of correct rate (hit and correct rejection altogether) to be shown
        in graphic view on analysis window.
    """

    # first get all performed trials as vector
    all_correct = list()
    all_rewarded = list()
    for schedule in mouse.schedule_list:
        for t, trial in enumerate(schedule.trial_list):
            if trial.rewarded[idx] == 0 and trial.licks[idx] == 0 and not trial.correct:
                all_correct.append(True)
            else:
                all_correct.append(trial.correct)
            all_rewarded.append(trial.rewarded)

    # then bin according to bin_size
    binned_correct = list()
    for i in range(1, len(all_correct)):
        if i < bin_size:
            binned_correct.append(np.mean(all_correct[0:i]))
        else:
            binned_correct.append(np.mean(all_correct[i-bin_size:i]))

    return binned_correct


def weighted_binned_performance(mouse: Experiment.Mouse, bin_size: int, idx: int) -> tuple[list[float], list[float]]:
    """
    In this function we examine performance by how many rewarded vs. 
    unrewarded trials there were.

    Parameters
    ----------
    mouse : Experiment.mouse class
        Instance of Experiment.mouse class that is of interest.

    bin_size : int
        Size of bin. 

        It is the number of trials used to calculate hit rate or 
        correct rejection rate.

    idx : int
        Index of tab window selected on analysis window.

        It differentiate between left GNG or right GNG

    Returns
    -------
    binned_perf_p : list of float
        List of hit rate in bin to be viewed in graphic view on analysis 
        window.

    binned_perf_m : list of float
        List of correct rejection rate in bin to be viewed in graphic view on
        analysis window.
    """

    # first get all performed trials as vector
    all_correct = list()
    all_rewarded = list()
    for schedule in mouse.schedule_list:
        for t, trial in enumerate(schedule.trial_list):
            if trial.rewarded[idx] == 0 and trial.licks[idx] == 0 and not trial.correct:
                all_correct.append(True)
            else:
                all_correct.append(trial.correct)
            all_rewarded.append(trial.rewarded)

    # then bin according to bin_size
    binned_perf_p = list()
    binned_perf_m = list()
    rewarded_count = 0
    unrewarded_count = 0

    # attributes for dprime. Actually not used.
#    left_count = 0
#    right_count = 0
#    correct_rewarded = 0
#    correct_rejection = 0
#    correct_left = 0
#    correct_right = 0

    for i in range(1, len(all_correct)):
        if i < bin_size:
            this_bin_correct = all_correct[0:i]
            this_bin_rewarded = all_rewarded[0:i]
        else:
            this_bin_correct = all_correct[i-bin_size:i]
            this_bin_rewarded = all_rewarded[i-bin_size:i]

        # dprime to see left and right. Actually not used.
#        for i in range(len(this_bin_rewarded)):
#            if this_bin_rewarded[i][0] > 0 and this_bin_rewarded[i][1] > 0:
#                rewarded_count += 1
#                if this_bin_correct:
#                    correct_rewarded += 1
#            elif this_bin_rewarded[i][0] == 0 and this_bin_rewarded[i][1] == 0:
#                unrewarded_count += 1
#                if this_bin_correct:
#                    correct_rejection += 1
#            elif this_bin_rewarded[i][0] > 0 and this_bin_rewarded[i][1] == 0:
#                left_count+= 1
#                if this_bin_correct:
#                    correct_left += 1
#            elif this_bin_rewarded[i][0] == 0 and this_bin_rewarded[i][1] > 0:
#                right_count += 1
#                if this_bin_correct:
#                    correct_right += 1
#
#        if rewarded_count + left_count == 0:
#            true_positive = 0.01
#        else:
#            true_positive = (correct_rewarded + correct_left)/(rewarded_count + left_count)
#
#        if unrewarded_count + right_count == 0:
#            true_negative = 0.01
#        else:
#            true_negative = (correct_rejection + correct_right)/(unrewarded_count + right_count)
#
#        if true_positive == 1:
#            true_positive = 0.99
#        if true_negative == 1:
#            true_negative = 0.99
#
#        false_positive = 1 - true_negative
#        dprime = Z(true_positive) - Z(false_positive)
#
#        binned_perf.append(dprime)

        this_bin_rewarded = np.array(this_bin_rewarded)[:, 0]
        rewarded_count = np.sum(this_bin_rewarded)
        unrewarded_count = len(this_bin_rewarded) - rewarded_count

        # if rewarded and correct are both True or 1,
        # then rewarded + correct > 1
        hit_count = len([t
                         for t in range(len(this_bin_correct))
                         if this_bin_rewarded[t] + this_bin_correct[t] > 1])

        # if rewarded is False or 0 and correct is True or 1, then
        # rewarded - correct < 0
        c_rejection_count = len([t
                                 for t in range(len(this_bin_correct))
                                 if this_bin_rewarded[t] - this_bin_correct[t] < 0])

        # set rate to 1 if rewarded count or unrewarded count is 0
        if rewarded_count > 0:
            sp_fraction = hit_count / rewarded_count
        else:
            sp_fraction = 1

        if unrewarded_count > 0:
            sm_fraction = c_rejection_count / unrewarded_count
        else:
            sm_fraction = 1

        binned_perf_p.append(sp_fraction)
        binned_perf_m.append(sm_fraction)

    return binned_perf_p, binned_perf_m


def n_trials_since(mouse: Experiment.Mouse, since: datetime.datetime) -> int:
    """
    Calculate number of trials since a time.

    Parameters
    ----------
    mouse : Experiment.mouse class
        Instance of mouse to calculate number of trials of.

    since : datetime.datetime
        Instance of datetime.datetime as start point to calculate number of 
        trials performed.

    Returns
    -------
    n_trials : int
        Number of trials since time given.
    """

    n_trials = 0

    for schedule in mouse.schedule_list:
        for trial in schedule.trial_list:
            if trial.timestamp > since:
                n_trials += 1

    return n_trials


def n_trials_last_24(mouse: Experiment.Mouse) -> int:
    """
    Calculate number of trials in last 24h.

    Parameters
    ----------
    mouse : Experiment.mouse class
        Instance of mouse to calculate number of trials.

    Returns
    -------
    n_trials : int
        Number of trials since 1 day.
    """

    return n_trials_since(mouse,
                          datetime.datetime.now() - datetime.timedelta(days=1))
