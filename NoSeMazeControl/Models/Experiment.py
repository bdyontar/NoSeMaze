"""
This module contains the experiment class, mouse class, schedule class, and 
trial class.
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


from collections import deque
import numpy as np
import pickle
import csv
import os

# imports for type hinting
import datetime as dt

# MAX_NUM_TRIALS in a queue. Queue-algorithmus using deque-collections
MAX_NUM_TRIALS = 1500

# QUANTITY_OF_APPENDED_SCHEDULES indicate the number of last schedules will be
# appended if end of the last schedule is reached.
QUANTITY_OF_APPENDED_SCHEDULES = 4


class Experiment:
    """
    Contains all information of the experiment up to the last MAX_NUM_TRIALS

    Attributes
    ----------
    animal_list : dict[str, Mouse]
        List of animal in experiment.

    default_row : deque
        Default table row for the trials.

    trials : deque
        Trials executed by all animals.

    name : str
        Name of the experiment.

    save_path : str
        Path to last saved file.

    logs_path : str
        Path to saved logs file of each animal.

    date : str
        String of datetime.datetime.now()

    last_data_l : NDArray[float64]
        Last data from analog input assign to the left lick port.

    last_data_r : NDArray[float64]
        Last data from analog input assign to the right lick port.
    """

    def __init__(self):
        """Initiate animal list with _'default'_ mouse and initiate trials with _'default'_ row."""
        self.animal_list: dict[str, Mouse] = {'default': Mouse('default')}
        self.default_row: deque = deque(
            [['', '', '', '', '', '', '', '', '', '', '', '']], MAX_NUM_TRIALS)
        self.trials: deque = self.default_row.copy()
        self.name: str = None
        self.save_path: str = None
        self.logs_path: str = None
        self.date: str = None
        self.last_data_l: np.ndarray = None
        self.last_data_r: np.ndarray = None

    def add_mouse(self, id):
        """Add mouse in animal_list with key of id."""
        if id not in self.animal_list.keys():
            self.animal_list[id] = Mouse(id)

    def add_trial(self, animal_id, timestamp, schedule, trial,
                  rewarded, wait_response, response, correct, timeout, licks):
        """
        Append trial in 'trials'-list.

        Parameters
        ----------
        animal_id : str
            Id of animal

        timestamp : datetime.datetime
            Timestamp of trial start.

        schedule : int
            Current schedule index.

        trial : int
            Current trial index.

        rewarded : list
            Parameter of reward (reward probability and amount of reward).

        wait_response : list
            List of indicator of response in wait window at left port and right
            port

        response : list
            List of indicator of response in lick window at left port and 
            right port.

        correct : bool
            Indicator if hit or correct rejection at GNG trials is performed.
            Currently, correct only shows if water is given. That means,
            correct rejection is labeled falsely as 'False'.

        timeout : bool
            Indicator if timeout was executed. Currently not used and should
            always be False.

        licks : list
            Number of licks at left port and right port.
        """

        if self.trials == self.default_row.copy():
            self.trials[0] = [animal_id, timestamp, schedule, trial, rewarded[5],
                              rewarded[4], rewarded[0:4], wait_response, response, correct, timeout, licks]
        else:
            self.trials.append([animal_id, timestamp, schedule, trial, rewarded[5], rewarded[4],
                               rewarded[0:4], wait_response, response, correct, timeout, licks])

    def save(self):
        """Save experiment."""

        fname = self.save_path + '/' + self.name

        with open(fname, 'wb') as fn:
            pickle.dump(self, fn)


class Mouse:
    """Contains information of a mouse.
    
    Attributes
    ----------
    id : str
        ID of the mouse.
    
    licks_list : list
        List of licks made by the mouse.
    
    current_schedule_idx : int
        Index of current schedule.
    
    schedule_list : list
        List of schedule assign to the mouse.

    total_licks : int
        Total licks made by the mouse.
    
    fname : str
        Name of the log file(s) of the mouse.
    """

    def __init__(self, id):
        """
        Parameters
        ----------
        id : str
            ID of the mouse.
        """

        self.id : str = id
        self.licks_list : list = list()
        self.current_schedule_idx : int = 0
        self.schedule_list : list = list()
        self.total_licks : int = 0
        self.fname : str = None

    def update_licks(self, timestamp, rewarded, licks_before, licks_after,
                     save_path, water_given, correct, timeout):
        """
        Update licks in log file.

        Parameters
        ----------
        timestamp : datetime.datetime
            Time of trial start.

        rewarded : list
            List of reward parameters (reward probability and amount of reward)

        licks_before : list
            List of number of licks before odor presentation at left and right
            port.

        licks_after : list
            List of number of licks after odor presentation at left and right
            port.

        save_path : str
            Path for saving licks logs.

        water_given : list or 2d-list
            List of indicator if water is given at left and/or right port.

        correct : bool
            Indicator if trial is performed correctly. Currently only indicates
            if water is given at left or right port.

        timeout : bool
            Indicator if timeout is executed. Currently not used and should
            always be 'False'.
        """

        self.total_licks = self.total_licks + \
            np.sum(licks_before) + np.sum(licks_after)

        if type(rewarded[2]) is np.float64:  # then it is normal schedule
            amount_l = rewarded[2]
            amount_r = rewarded[3]
        elif type(rewarded[2]) is type(np.array([])):  # then it is concatenate schedule
            amount_l = rewarded[2]*np.array(water_given[0])
            amount_r = rewarded[3]*np.array(water_given[1])
#            amount_l = list(map(lambda x,y: x*y, list(map(int, water_given[0])), rewarded[2]))
#            amount_r = list(map(lambda x,y: x*y, list(map(int, water_given[1])), rewarded[3]))

        wl, wr = [0, 0]
        if np.sum(water_given[0]) and not np.sum(water_given[1]):
            wl = 1
        elif not np.sum(water_given[0]) and np.sum(water_given[1]):
            wr = 1
        elif np.sum(water_given[0]) and np.sum(water_given[1]):
            wl, wr = 1, 1
        # 0.22 microliter is given, if water vent opened for 0.4 seconds.
        water_amount = (wl*amount_l + wr*amount_r)/0.4*0.022

        # change into text separated with |
        odour = str(rewarded[5])
        delay = str(rewarded[4])
        rewarded = '|'.join(list(map(str, rewarded[0:4])))
        licks_before = '|'.join(list(map(str, licks_before)))
        licks_after = '|'.join(list(map(str, licks_after)))

        self.licks_list = [timestamp, odour, delay, rewarded, licks_before,
                           licks_after, self.total_licks, water_amount, correct, timeout]

        self.fname = save_path + '/licks_log_'+self.id+'.csv'
        if os.path.isfile(self.fname):
            should_write_header = False
        else:
            should_write_header = True

        with open(self.fname, 'a+', newline='') as fn:
            writer = csv.writer(fn, delimiter=';')
            if should_write_header:
                writer.writerow(['timestamp', 'odour', 'delay', 'rewarded', 'licks at waiting',
                                'licks after odour', 'total licks', 'water amount', 'correct', 'timeout'])
            writer.writerow(self.licks_list)

    def add_schedule(self, schedule_name, schedule_data, schedule_headers,
                     trial_parameters, idx):
        """
        Add schedule in schedule_list.

        Parameters
        ----------
        schedule_name : str
            Name of schedule.

        schedule_data : list[dict]
            Data of schedule.

        schedule_headers : list
            Schedule headers.

        trial_parameters : list[dict]
            Parameter of a trial.

        idx : int
            Index of current schedule.
        
        Notes
        -----
        For more information about the parameter of a trial or a schedule, see software documentation of NoSeMazeSchedule.
        """
        self.schedule_list.insert(idx+1, Schedule(schedule_name,
                                                  schedule_data,
                                                  schedule_headers,
                                                  trial_parameters))

    def current_trial(self):
        """Get current trial and returns it.
        
        Returns
        -------
        current_trial : list[list]
            Current trial in the current schedule to be executed.
        
        Notes
        -----
        For more information about the parameter of a trial or a schedule, see software documentation of NoSeMazeSchedule.
        """

        if len(self.schedule_list)-1 < self.current_schedule_idx:
            self.current_schedule_idx = len(self.schedule_list)-1
        current_schedule: Schedule = self.schedule_list[self.current_schedule_idx]
        current_trial: list[list] = current_schedule.schedule_trials[current_schedule.current_trial]
        return current_trial

    def current_trial_pulse(self):
        """Get current trial pulse and returns it.
        
        Returns
        -------
        pulse_params : list[dict]
            Current trial param of the current trial.
        
        Notes
        -----
        For more information about the parameter of a trial or a schedule, see software documentation of NoSeMazeSchedule.
        """

        while len(self.schedule_list) - 1 < self.current_schedule_idx:
            self.current_schedule_idx = len(self.schedule_list)-1
        current_schedule: Schedule = self.schedule_list[self.current_schedule_idx]
        pulse_params: list[dict] = current_schedule.trial_params[current_schedule.current_trial]
        return pulse_params

    @property
    def current_trial_idx(self):
        """Get current trial index.
        
        Returns
        -------
        current_trial_idx : int
            Index of current trial in the schedule.
        """
        return self.schedule_list[self.current_schedule_idx].current_trial

    def advance_trial(self):
        """Advance trial in a schedule if a trial is finished."""

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
                for i in range(QUANTITY_OF_APPENDED_SCHEDULES):
                    current_schedule = self.schedule_list[self.current_schedule_idx -
                                                          QUANTITY_OF_APPENDED_SCHEDULES + 1 + i]
                    fail_safe_schedule = Schedule(current_schedule.id, current_schedule.schedule_trials,
                                                  current_schedule.schedule_headers, current_schedule.trial_params)
                    self.schedule_list.append(fail_safe_schedule)

                self.current_schedule_idx += 1


class Schedule:
    """Contains information in a schedule.
    
    Attributes
    ----------
    id : str
        Name of the schedule.
    
    current_trial : int
        Current trial index.
    
    schedule_trials : list[list]
        Data of the trials in a schedule.
    
    schedule_headers : list
        Headers of the schedule.
    
    trial_params : list[dict]
        Parameter of a trial.
    """

    def __init__(self, id, schedule_trials, schedule_headers, trial_params):
        """
        Parameters
        ----------
        id : str
            Name of the schedule.
        
        schedule_trials : list[list]
            Data of the schedule.

        schedule_headers : list
            Header of the schedule.

        trial_params : list[dict]
            Parameter of a trial.
        
        Notes
        -----
        For more information about the parameter of a trial or a schedule, see software documentation of NoSeMazeSchedule.
        """
        self.id : str = id
        self.current_trial : int = 0
        self.schedule_trials : list[list] = schedule_trials
        self.schedule_headers : list = schedule_headers
        self.trial_params : list[dict] = trial_params

        self.trial_list : list = list()

    def add_trial_data(self, timestamp, wait_response, response, correct,
                       timeout, licks, rewarded):
        """
        Add trial data.

        Parameters
        ----------
        timestamp : datetime.datetime
            Start time of the trial.

        wait_response : list
            List of indicator if mouse has licked before odor is presented.

        response : list
            List of indicator if mouse has licked after odor is presented.

        correct : bool
            Indicator if trials is performed correctly. Currently, it shows 
            only if water is given.

        timeout : bool
            Indicator if timeout is given. Currently not used and should always
            be 'False'

        licks : list
            Number of licks at left port and right port.

        rewarded : list
            List of reward parameters (reward probability and amount of reward)
        """
        self.trial_list.append(Trial(timestamp, wait_response, response,
                                     correct, timeout, licks, rewarded))

    def n_trials(self):
        """Total number of trials that should be performed in the schedule.
        
        Returns
        -------
        len : int
            Number of trials available in the schedule. 
        """

        return len(self.schedule_trials)

    def trials_left(self):
        """Number of trials left in a schedule.
        
        Returns
        -------
        trial_left : bool
            Return true if current trial index is not the last index; else return false.
        """

        return self.current_trial < self.n_trials() - 1


class Trial:
    """Contains information of a trial.
    
    Attributes
    ----------
    timestamp : datetime.datetime
        Start time of the trial.

    wait_response : list
        List of indicator if mouse has licked before odor is presented.

    response : list
        List of indicator if mouse has licked after odor is presented.

    correct : bool
        Indicator if trials is performed correctly. Currently, it shows 
        only if water is given.

    timeout : bool
        Indicator if timeout is given. Currently not used and should always
        be 'False'

    licks : list
        Number of licks at left port and right port.

    rewarded : list
        List of reward parameters (reward probability and amount of reward)
    """

    def __init__(self, timestamp, wait_response, response, correct,
                 timeout, licks, rewarded):
        """
        Parameters
        ----------
        timestamp : datetime.datetime
            Start time of the trial.

        wait_response : list
            List of indicator if mouse has licked before odor is presented.

        response : list
            List of indicator if mouse has licked after odor is presented.

        correct : bool
            Indicator if trials is performed correctly. Currently, it shows 
            only if water is given.

        timeout : bool
            Indicator if timeout is given. Currently not used and should always
            be 'False'

        licks : list
            Number of licks at left port and right port.

        rewarded : list
            List of reward parameters (reward probability and amount of reward)
        """

        self.timestamp : dt.datetime = timestamp
        self.rewarded : list = rewarded
        self.wait_response : list = wait_response
        self.response : list = response
        self.correct : bool = correct
        self.timeout : bool = timeout
        self.licks : list = licks
