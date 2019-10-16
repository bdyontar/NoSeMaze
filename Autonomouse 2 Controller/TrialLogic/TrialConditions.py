import numpy as np
import datetime
from enum import Enum


class TrialResult(Enum):
    correct_response = 1
    correct_rejection = 2
    miss = 3
    false_alarm = 4

def licks_number(lick_data, threshold, samp_rate, start_time):
    lick_response = np.zeros(len(lick_data))
    lick_response[np.where(lick_data > threshold)] = 1
    
#    print('lick_response',lick_response)
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