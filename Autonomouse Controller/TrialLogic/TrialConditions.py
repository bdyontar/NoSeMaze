"""
This module contains methods to analyse read data.
"""

import numpy as np
import datetime
from enum import Enum

class TrialResult(Enum):
    correct_response = 1
    correct_rejection = 2
    miss = 3
    false_alarm = 4

def licks_number(lick_data, threshold, samp_rate, start_time):
    """
    Get the number of licks from data.
    
    Parameters
    ----------
    lick_data : ndarray
        Read data to be analysed.
    
    threshold : int
        Threshold if data is considered TTL high.
    
    samp_rate : int
        Sample rate definded in hardware configuration.
    
    start_time : datetime.datetime
        Start time of a trial.
        
    Return
    ------
    lick_times : list
        Timestamps of licks.
    
    licks : int
        Number of licks.
    """
    
    lick_response = np.zeros(len(lick_data))
    lick_response[np.where(lick_data > threshold)] = 1
    
    if np.sum(lick_response) == 0:
        lick_time = 'not licked'
        licks = 0
    else:
        lick_nz = np.nonzero(lick_response)[0]
        lick_delta = []
        for i,v in enumerate(lick_nz):
            if i == 0:
                lick_delta.append(datetime.timedelta(seconds = (v/samp_rate)))
            elif (v-lick_nz[i-1])>1:
                lick_delta.append(datetime.timedelta(seconds = (v/samp_rate)))
        licks = len(lick_delta)
        lick_time = []
        for i in range(len(lick_delta)):
            lick_time.append((start_time+lick_delta[i]).strftime('%X.%f'))
        
        lick_time = "|".join(lick_time)
    
    return lick_time, licks

def lick_detect(lick_data, threshold, percent_accepted):
    """
    Detect lick and analyse it if it is considered licked or not.
    
    Parameters
    ----------
    lick_data : ndarray
        Read data to be analysed.
    
    threshold : int
        Threshold if data is considered TTL high.
    
    percent_accepted: float
        Ratio of TTL high in data to be considered licked.
    
    Return
    ------
    response : bool
        Response is true, if number of licks is greater than 2 or if the ratio
        is greater than indicated.
    """
    
    # first binarise the data
    lick_response = np.zeros(len(lick_data))
    lick_response[np.where(lick_data > threshold)] = 1
    
    if np.sum(lick_response) == 0:
        licks = 0
    else:
        licks_nz = np.nonzero(lick_response)[0]
        licks = 0
        for i,v in enumerate(licks_nz):
            if i == 0:
                licks = licks + 1
            elif (v-licks_nz[i-1])>1:
                licks = licks + 1

    # return whether this is accepted as a response or not
    return licks > 2 or np.sum(lick_response)/len(lick_response) > percent_accepted


def trial_result(_rewarded, _response_l, _response_r):
    """
    Analyse trial, if it is correct.
    
    Parameters
    ----------
    _rewarded : list
        List of reward parameteres (reward probability and amount of reward).
    
    _response_l : bool
        Indicator if left port is licked.
    
    _response_r : bool
        Indicator if right port is licked.
    
    Return
    ------
    TrialResult_enum : TrialResult
        Enum of trial result.
        
        4 indicators - correct response, correct rejection, miss, and 
        false alarm.
    
    correct : bool
        Indicator if correct response or correct rejection.
        
    timeout : bool
        Indicator if timeout is executed.
    """
    
    prob_l = _rewarded[0]
    prob_r = _rewarded[1]
    
    if _response_l and _response_r:
        return TrialResult.false_alarm, False, True
    elif _response_l and not _response_r:
        if prob_l == 0 and prob_r == 0:
            return TrialResult.false_alarm, False, True
        elif prob_l == 0 and prob_r != 0:
            return TrialResult.miss, False, False
        elif prob_l != 0:
            return TrialResult.correct_response, True, False
    elif not _response_l and _response_r:
        if prob_l == 0 and prob_r == 0:
            return TrialResult.false_alarm, False, True
        elif prob_l != 0 and prob_r == 0:
            return TrialResult.miss, False, False
        elif prob_r != 0:
            return TrialResult.correct_response, True, False
    elif not _response_l and not _response_r:
        if prob_l == 0 and prob_r == 0:
            return TrialResult.correct_rejection, True, False
        else:
            return TrialResult.miss, False, False
                
    # returns trial result enum, correct bool, timeout bool
#    rewarded = _rewarded == 1
#    if rewarded == 1 and _response_l:
#        return TrialResult.correct_response, True, False
#    elif rewarded == 1 and not _response_l:
#        return TrialResult.miss, False, False
#    elif not rewarded and not _response_l:
#        return TrialResult.correct_rejection, True, False
#    elif not rewarded and _response_l:
#        return TrialResult.false_alarm, False, True
#    else:
#        print('unknown trial condition')
#        return TrialResult.miss, False, False