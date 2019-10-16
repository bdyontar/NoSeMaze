from collections import deque
import numpy as np

import pickle
import csv
import os

MAX_NUM_TRIALS = 5000 # MAX_NUM_TRIALS in a queue. Queue-algorithmus using deque-collections
QUANTITY_OF_APPENDED_SCHEDULES = 4

class Experiment:
    def __init__(self):
#        self.animal_list = {'default': Mouse('default', 0.40)}
        self.animal_list = {'default': Mouse('default')}
        self.default_row = deque([['', '', '', '', '', '', '', '','','']], MAX_NUM_TRIALS)
        self.trials = self.default_row.copy()

        self.name = None
        self.save_path = None
        self.logs_path = None
        self.date = None

        self.last_data_l = None
        self.last_data_r = None
            
#    def add_mouse(self, id, water):
#        if id in self.animal_list.keys():
#            self.animal_list[id].water = water
#        else:
#            self.animal_list[id] = Mouse(id, water)
        
    def add_mouse(self, id):
        if id not in self.animal_list.keys():
            self.animal_list[id] = Mouse(id)

    def add_trial(self, animal_id, timestamp, schedule, trial, rewarded, wait_response, response, correct, timeout, licks):
        if self.trials == self.default_row.copy():
            self.trials[0] = [animal_id, timestamp, schedule, trial, rewarded, wait_response, response, correct, timeout, licks]
        else:
            self.trials.append([animal_id, timestamp, schedule, trial, rewarded, wait_response, response, correct, timeout, licks])

    def save(self):
        fname = self.save_path + '/' + self.name

        with open(fname, 'wb') as fn:
            pickle.dump(self, fn)


class Mouse:
#    def __init__(self, id, water):
    def __init__(self, id):
        self.id = id
#        self.water = water
        self.licks_list = list() 
        self.current_schedule_idx = 0
        self.schedule_list = list()
        self.total_licks = 0
        self.fname = None
    
    def update_licks(self, timestamp, rewarded, licks_before, licks_after, save_path, water_given, correct, timeout):
        self.total_licks = self.total_licks + np.sum(licks_before) + np.sum(licks_after)
        
        wl, wr = [0, 0]
        if water_given[0]:
            wl = 1
        elif water_given[1]:
            wr = 1
        elif water_given[0] and water_given[1]:
            wl, wr = [1, 1]
        water_amount = (wl*rewarded[2] + wr*rewarded[3])/0.4*0.022 #0.22 microliter is given, if water vent opened for 0.4 seconds.
        
        #change into text separated with |
        rewarded = '|'.join(list(map(str,rewarded)))
        licks_before = '|'.join(list(map(str,licks_before)))
        licks_after = '|'.join(list(map(str,licks_after)))
        
        self.licks_list = [timestamp, rewarded, licks_before, licks_after, self.total_licks, water_amount, correct, timeout]
        
        self.fname = save_path + '/licks_log_'+self.id+'.txt'
        if os.path.isfile(self.fname):
            should_write_header = False
        else:
            should_write_header = True
        
        with open(self.fname, 'a+', newline = '') as fn:
            writer = csv.writer(fn)
            if should_write_header:
                writer.writerow(['timestamp','rewarded','licks at waiting', 'licks after odour', 'total licks','water amount','correct','timeout'])
            writer.writerow(self.licks_list)
    
    def add_schedule(self, schedule_name, schedule_data, schedule_headers, trial_parameters, idx):
#        print('idx :',idx)
        self.schedule_list.insert(idx+1, Schedule(schedule_name, schedule_data, schedule_headers, trial_parameters))

    def current_trial(self):
        if len(self.schedule_list)-1 < self.current_schedule_idx:
            self.current_schedule_idx = len(self.schedule_list)-1
        current_schedule = self.schedule_list[self.current_schedule_idx]
        current_trial = current_schedule.schedule_trials[current_schedule.current_trial]
        return current_trial

    def current_trial_pulse(self):
        while len(self.schedule_list) - 1 < self.current_schedule_idx:
            self.current_schedule_idx = len(self.schedule_list)-1
        current_schedule = self.schedule_list[self.current_schedule_idx]
        pulse_params = current_schedule.trial_params[current_schedule.current_trial]
        return pulse_params

    @property
    def current_trial_idx(self):
        return self.schedule_list[self.current_schedule_idx].current_trial

    def advance_trial(self):
        # end of schedule and schedules available to move to? advance to the next
        if not self.schedule_list[self.current_schedule_idx].trials_left() and \
                (self.current_schedule_idx + 1) < len(self.schedule_list):
            self.current_schedule_idx += 1

        # still trials left? advance to the next?
        elif self.schedule_list[self.current_schedule_idx].trials_left():
            self.schedule_list[self.current_schedule_idx].current_trial += 1

        # else we have reached the end of available trials - add a repeat of the current schedule
        else:
            if self.current_schedule_idx == 0 or len(self.schedule_list) < 4:
                current_schedule = self.schedule_list[self.current_schedule_idx]
                fail_safe_schedule = Schedule(current_schedule.id, current_schedule.schedule_trials,
                                              current_schedule.schedule_headers, current_schedule.trial_params)
                self.schedule_list.append(fail_safe_schedule)
                self.current_schedule_idx += 1
            else:
#                current_schedule = self.schedule_list[self.current_schedule_idx]
#                last_schedule = self.schedule_list[self.current_schedule_idx - 1]
#                fail_safe_schedule_1 = Schedule(last_schedule.id, last_schedule.schedule_trials,
#                                                last_schedule.schedule_headers, last_schedule.trial_params)
#                fail_safe_schedule_2 = Schedule(current_schedule.id, current_schedule.schedule_trials,
#                                                current_schedule.schedule_headers, current_schedule.trial_params)
#                self.schedule_list.append(fail_safe_schedule_1)
#                self.schedule_list.append(fail_safe_schedule_2)
                
                for i in range(QUANTITY_OF_APPENDED_SCHEDULES):
                    current_schedule = self.schedule_list[self.current_schedule_idx - QUANTITY_OF_APPENDED_SCHEDULES + 1 + i]
                    fail_safe_schedule = Schedule(current_schedule.id, current_schedule.schedule_trials,
                                                current_schedule.schedule_headers, current_schedule.trial_params)
                    self.schedule_list.append(fail_safe_schedule)
                    
                self.current_schedule_idx += 1

class Schedule:
    def __init__(self, id, schedule_trials, schedule_headers, trial_params):
        self.id = id
        self.current_trial = 0
        self.schedule_trials = schedule_trials
        self.schedule_headers = schedule_headers
        self.trial_params = trial_params

        self.trial_list = list()

    def add_trial_data(self, timestamp, wait_response, response, correct, timeout, licks, rewarded):
        self.trial_list.append(Trial(timestamp, wait_response, response, correct, timeout, licks, rewarded))

    def n_trials(self):
        return len(self.schedule_trials)

    def trials_left(self):
        return self.current_trial < self.n_trials() - 1

class Trial:
    def __init__(self, timestamp, wait_response, response, correct, timeout, licks, rewarded):
        self.timestamp = timestamp
        self.rewarded = rewarded
        self.wait_response = wait_response
        self.response = response
        self.correct = correct
        self.timeout = timeout
        self.licks = licks
