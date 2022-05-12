"""
This module contains methods used for converting experiment data into matlab
data. It is not used and not supported in NoSeMaze but still saved here for 
archive purpose.
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

import scipy.io as sio
from Models import Experiment
from PyPulse import PulseInterface
import os
import pickle
import csv
import numpy as np
import collections as col


def load_experiment(path: str) -> tuple[Experiment.Experiment, list[str], dict]:
    """Read all experiment files in path and return the data.
    
    Parameters
    ----------
    path : str
        Path of the experiment files.

    Returns
    -------
    experiment : Experiment.Experiment
        Last experiment loaded from .autmaus file.
    data_files : list[str]
        List of .mat files filename.
    schedule_map : dict
        Last schedule read from .csv file.
    """
    data_files = list()
    for file in os.listdir(path):
        if file.endswith(".autmaus"):
            with open(path + file, 'rb') as fn:
                experiment = pickle.load(fn)

        if file.endswith(".mat"):
            data_files.append(path + file)

        if file.endswith(".csv"):
            schedule_map = read_schedule_map(path + file)

    return experiment, data_files, schedule_map


def read_schedule_map(path: str) -> dict:
    """Read schedule map from csv file.
    
    Parameters
    ----------
    path : str
        Path of the csv file.
    
    Returns
    -------
    schedule_map : dict
        Schedule map read from the csv file.
    """
    schedule_map = dict()
    with open(path, 'rt') as sched:
        reader = csv.reader(sched)
        for row in reader:
            schedule_map[row[0]] = row[1]
    return schedule_map


def batch_convert(paths: list[str], out_path: str, out_name: str, trial_parameter: int, verbose: bool = True, save_licks: bool = False):
    """Convert files in batch.
    
    Parameters
    ----------
    paths : list of str
        List of paths to convert experiment data from.
    out_path : str
        Path to save the converted data.
    out_name : str
        Name of the saved file of the converted data.
    trial_parameter : int
        Parameter for output.
    verbose : bool
        Check if verbose mode should be used.
    save_licks : bool
        Check if licks should be saved.
    """
    output = dict()
    for path in paths:
        if verbose:
            print('processing: ' + path)

        experiment, data_files, schedule_map = load_experiment(path)

        for animal_id in experiment.animal_list.keys():
            this_animal = experiment.animal_list[animal_id]
            save_id = 'maus' + this_animal.id
            if save_id not in output.keys():
                output[save_id] = col.OrderedDict()

            for schedule in this_animal.schedule_list:
                sched_id = schedule.id.split('.')[0]
                sched_id = schedule_map[sched_id]
                match_sched = [
                    sched for sched in output[save_id].keys() if sched_id in sched]
                sched_id = sched_id + '_' + str(len(match_sched) + 1)

                output[save_id][sched_id] = {'rewarded': list(), 'correct': list(), 'licked': list(),
                                             'data_file': list(), 'timestamp': list(),
                                             'schedule_name': schedule.id.split('.')[0],
                                             'schedule_params': list(), 'lick_on_times': list()}

                for t, trial in enumerate(schedule.trial_list):
                    time = str(trial.timestamp)
                    time = time.replace(' ', '_')
                    time = time.replace(':', '_')

                    output[save_id][sched_id]['rewarded'].append(
                        schedule.schedule_trials[t][0])
                    output[save_id][sched_id]['correct'].append(trial.correct)
                    output[save_id][sched_id]['licked'].append(trial.response)
                    output[save_id][sched_id]['timestamp'].append(time)

                    if len(schedule.schedule_trials[t]) > trial_parameter:
                        output[save_id][sched_id]['schedule_params'].append(
                            schedule.schedule_trials[t][trial_parameter])

                    match_file = [file for file in data_files if time in file]

                    if save_licks:
                        if len(match_file) > 0:
                            output[save_id][sched_id]['data_file'].append(
                                match_file[0])

                            if save_licks:
                                # now that we know where the data file is, get the lick data from it. 3 idx is just a known,
                                # need to change if hardware changes
                                try:
                                    lick_data = sio.loadmat(match_file[0])[
                                        'analog_data'][3]
                                except:
                                    lick_data = []
                                # reduce this data to a set of lick onsets to save storage space
                                lick_diff = np.diff(lick_data)
                                lick_onsets = np.where(lick_diff > 0.1)
                                output[save_id][sched_id]['lick_on_times'].append(
                                    lick_onsets)

    output = {out_name: output}

    sio.savemat(out_path + out_name, output)


def convert():
    """Converting in a batch files with defined paths."""
    batch_convert(['I:/Automated Behaviour/CorrelationStudy2/Pretrain/',
                   'I:/Automated Behaviour/CorrelationStudy2/GNG_5/',
                   'I:/Automated Behaviour/CorrelationStudy2/InitialCorrDiscrim/',
                   'I:/Automated Behaviour/CorrelationStudy2/CorrDiscrimControls/',
                   'I:/Automated Behaviour/CorrelationStudy2/CorrDiscrimControls2/',
                   'I:/Automated Behaviour/CorrelationStudy2/RandomisedFrequency_1/',
                   'I:/Automated Behaviour/CorrelationStudy2/RandomisedFrequency_2/',
                   'I:/Automated Behaviour/CorrelationStudy2/RandomisedFrequency_3/',
                   'I:/Automated Behaviour/CorrelationStudy2/RandomisedFrequency_4/',
                   'D:/CorrelationStudy2/RandomisedFrequency_5/',
                   'I:/Automated Behaviour/CorrelationStudy2/StaticTrain/',
                   'I:/Automated Behaviour/CorrelationStudy2/StaticTrainSwitch/',
                   'D:/LowHighSwitch/',
                   'E:/AutomatedBehaviour/CorrelationStudy2/OnsetDisrupt/',
                   'E:/AutomatedBehaviour/CorrelationStudy2/TrainCNvsACP_2Hz/',
                   'E:/AutomatedBehaviour/CorrelationStudy2/TrainCNvsACP_10Hz/'],
                  'C:/Users/ERSKINA/Repos/AutonoMouseDataSets/CorrelationStudy2/', 'allData2', 13, save_licks=False)

    # batch_convert(['D:/CorrelationStudy2/RandomisedFrequency_5/',
    #                'H:/Automated Behaviour/CorrelationStudy2/StaticTrain/',
    #                'H:/Automated Behaviour/CorrelationStudy2/StaticTrainSwitch/'],
    #               'C:/Users/ERSKINA/Repos/AutonoMouseDataSets/CorrelationStudy2/', 'allData_LickTest', 8, save_licks=True)

    # batch_convert(['H:/Automated Behaviour/CorrelationStudy2/RandomisedFrequency_1/'], 'H:/Automated Behaviour/CorrelationStudy2/RandomisedFrequency_1/', 'InitRandomHz', 8)


if __name__ == '__main__':
    convert()
