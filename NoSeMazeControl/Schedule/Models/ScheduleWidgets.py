"""
This module contains the implementation of the schedule widgets. If a new trial
sequence is needed, then a new schedule widget is also needed. The new schedule
must be also implemented in DAQ.py and ExperimentControl.py in NoSeMazeControl.

All classes defined here will be shown in the schedule widget combo box in the main
window.

Methods needed in a class implementation of a schedule widget is:
generate_schedule() and pulse_parameters().
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

from PyQt5 import QtWidgets
import numpy as np

from Schedule.Designs import NoSeMazeScheduleDesign
from Schedule.Generation import Gen
import Schedule.Exceptions as e

# import for type hinting
# TODO: type hinting parentUI as MainApp. Circular import issue occured.
import types as t

# TODO: Describe attributes of all class in docstring?

class NoSeMazeScheduleWidget(QtWidgets.QWidget, NoSeMazeScheduleDesign.Ui_Form):
    """Widget for configuring the schedule and trials parameters."""
    def __init__(self, parentUi = None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.parentUi = parentUi
        self.valence_map : t.NoneType = None # not used
        self.nValveSpin.valueChanged.connect(self.change_reward_map)

    def flatten_value(self, value : int) -> int:
        if value < 0:
            return 0
        else:
            return value

    def change_reward_map(self):
        self.rewardMapTable.setColumnCount(int(self.nValveSpin.value()))
        label = []
        for i in range(self.nValveSpin.value()-1):
            label.append(str(i+1))
        self.rewardMapTable.setHorizontalHeaderLabels(label)

    def generate_schedule(self, valence_map : list) -> tuple[list, list]:
        # getting maps
        try:
            reward_map = [[self.flatten_value(float(self.rewardMapTable.item(x, y).text())) for y in range(
                self.rewardMapTable.columnCount())] for x in range(self.rewardMapTable.rowCount())]
        except:
            reward_map = []

        reward_map = np.array(reward_map)
        valence_map = np.array(valence_map)

        # proving faulty inputs
        if len(valence_map) > 3:
            QtWidgets.QMessageBox.about(
                self.parentUi, "Error", "Number of valves is limited to 3 or less")
        elif len(reward_map) == 0:
            QtWidgets.QMessageBox.about(
                self.parentUi, "Error", "Reward map does not permit NAN value")
        elif self.pretrainingCheck.isChecked() and len(np.where(reward_map[2] > 0)[0]) + len(np.where(reward_map[3] > 0)[0]) == 0:
            QtWidgets.QMessageBox.about(
                self.parentUi, "Error", "At least the amount of reward on one lick port is needed")
        elif not self.pretrainingCheck.isChecked() and len(np.where(reward_map[0] > 0)[0])+len(np.where(reward_map[1] > 0)[0]) == 0:
            QtWidgets.QMessageBox.about(
                self.parentUi, "Error", "At least one odour should be rewarded")
        else:
            lick_fraction = float(self.lickFractionEdit.text())
            n_trials = int(self.nTrialsEdit.text())

            # getting valence map and valve index
            valve_index = (np.where(valence_map == 0)[0],
                           np.where(valence_map == 1)[0],
                           np.where(valence_map == 2)[0],
                           np.where(valence_map == 3)[0])

            # getting valve_index nonzero map
            viMap = []
            for i in range(len(valve_index)):
                viMap.append(len(valve_index[i]))
            viMap = np.array(viMap)
            vinzMap = np.nonzero(viMap)[0]

            to_delete = list()
            for i, v in enumerate(vinzMap):
                if v not in range(reward_map.shape[1]+1):
                    to_delete.append(i)

            if len(to_delete) == 0:
                odour_choice = vinzMap
            else:
                odour_choice = np.delete(vinzMap, np.array(to_delete))

            if odour_choice.shape[0] == 0:
                QtWidgets.QMessageBox.about(
                    self.parentUi, "Error", "The odour selected in valve valence map does not exist in reward map.")
                raise e.RewardMapError
            else:
                # generate random sequence
                odour_sequence = Gen.odor_sequence(odour_choice, n_trials)

                schedule = []
                for t in range(n_trials):
                    odour = odour_sequence[t]
                    valve = valve_index[odour]+1
                    prob_left = reward_map[0][odour-1]
                    prob_right = reward_map[1][odour-1]
                    amount_left = reward_map[2][odour-1]
                    amount_right = reward_map[3][odour-1]
                    delay = reward_map[4][odour-1]
                    schedule.append([prob_left, prob_right, amount_left, amount_right,
                                    delay, odour, valve, valence_map, lick_fraction])

                return schedule, ['Probability Left', 'Probabilty Right', 'Reward Left', 'Reward Right', ' Delay', 'Odour', 'Valve', 'Valence Map', 'Lick Fraction']

    def pulse_parameters(self, trial : list) -> list[dict]:
        params : list = list()

        onset = float(self.trialOnsetEdit.text())
        offset = float(self.trialOffsetEdit.text())
        length = float(self.trialLengthEdit.text())
        valve = trial[6]
        valence_map = trial[7]
        lick_fraction = trial[8]

        for p in range(len(valence_map)):
            param = {'type': 'Simple',
                     'pretraining': bool(self.pretrainingCheck.isChecked()),
                     'odour_training': bool(self.odourTrainingCheck.isChecked()),
                     'fromDuty': False,
                     'fromValues': True,
                     'pulse_width': length,
                     'pulse_delay': 0.0,
                     'fromLength': False,
                     'fromRepeats': True,
                     'repeats': 1,
                     'length': 0.0,
                     'isClean': True,
                     'onset': onset,
                     'offset': offset,
                     'lick_fraction': lick_fraction
                     }

            if p + 1 in valve:
                param['repeats'] = 1

            params.append(param)

        return params

# Implementation of concatenated schedules. Not yet supported in the latest NoSeMaze Controller. It
# save here for archive purpose.

# from ScheduleDesigns import NoSeMazeConcatenatedScheduleDesign
# class NoSeMazeConcatenatedScheduleWidget(QtWidgets.QWidget, NoSeMazeConcatenatedScheduleDesign.Ui_Form):
#     def __init__(self, parentUi=None):
#         super(self.__class__, self).__init__()
#         self.setupUi(self)

#         self.parentUi = parentUi

#         self.valence_map = None
#         self.nValveSpin.valueChanged.connect(self.change_reward_map)

#     def flatten_value(self, value):
#         if value < 0: return 0
#         else: return value

#     def change_reward_map(self):
#         self.rewardMapTable.setColumnCount(int(self.nValveSpin.value()))
#         label = []
#         for i in range(self.nValveSpin.value()-1):
#             label.append(str(i+1))
#         self.rewardMapTable.setHorizontalHeaderLabels(label)

#     def generate_schedule(self, valence_map):
#         #getting maps
#         try:
#             reward_map = [[self.flatten_value(float(self.rewardMapTable.item(x,y).text())) for y in range(self.rewardMapTable.columnCount())] for x in range(self.rewardMapTable.rowCount())]
#         except:
#             reward_map = []

#         reward_map = np.array(reward_map)
#         valence_map = np.array(valence_map)
#         #proving faulty inputs
#         if len(valence_map) > 3:
#             QtWidgets.QMessageBox.about(self.parentUi, "Error", "Number of valves is limited to 3 or less")
#         elif len(reward_map) == 0:
#             QtWidgets.QMessageBox.about(self.parentUi, "Error", "Reward map does not permit NAN value")
#         else:
#             lick_fraction = float(self.lickFractionEdit.text())
#             n_trials = int(self.nTrialsEdit.text())

#             #getting valence map and valve index
#             valve_index = (np.where(valence_map == 0)[0],
#                            np.where(valence_map == 1)[0],
#                            np.where(valence_map == 2)[0],
#                            np.where(valence_map == 3)[0])

#             #getting valve_index nonzero map
#             viMap = []
#             for i in range(len(valve_index)):
#                 viMap.append(len(valve_index[i]))
#             viMap = np.array(viMap)
#             vinzMap = np.nonzero(viMap)[0]

#             #generate random sequence
#             to_delete = list()
#             for i,v in enumerate(vinzMap):
#                 if v not in range(reward_map.shape[1]+1):
#                     to_delete.append(i)
#             odour_choice = np.delete(vinzMap,np.array(to_delete))

#             schedule = []
#             for t in range(n_trials):
#                 odour = odour_choice
#                 valve = list()
#                 for o in odour:
#                     for i,v in enumerate(valve_index):
#                         if len(v) == 0:
#                             continue
#                         elif i == o:
#                             valve.extend(list(v))
#                             continue
#                 valve = np.array(valve, dtype=np.int32)+1
#                 length = reward_map[0]
#                 prob_left = 1
#                 prob_right = 1
#                 amount_left = reward_map[1]
#                 amount_right = reward_map[1]
#                 delay = 0
#                 schedule.append([prob_left, prob_right, amount_left, amount_right, delay, odour ,valve , valence_map, lick_fraction, length])

#             return schedule, ['Probability Left', 'Probabilty Right', 'Reward Left', 'Reward Right', ' Delay', 'Odour', 'Valve', 'Valence Map', 'Lick Fraction', 'Length of Odours']

#     def pulse_parameters(self, trial):
#         params = list()

#         onset = float(self.trialOnsetEdit.text())
#         offset = float(self.trialOffsetEdit.text())
#         valve = trial[6]
#         valence_map = trial[7]
#         lick_fraction = trial[8]
#         length = trial[9]

#         for p in range(len(valence_map)):
#             param = {'type': 'Concatenate',
#                      'concatenate_wait_training':True,
#                      'pretraining':bool(self.pretrainingCheck.isChecked()),
#                      'fromDuty': False,
#                      'fromValues': True,
#                      'pulse_width': length,
#                      'pulse_delay': 0.0,
#                      'fromLength': False,
#                      'fromRepeats': True,
#                      'repeats': 0,
#                      'length': 0.0,
#                      'isClean': True,
#                      'onset': onset,
#                      'offset': offset,
#                      'lick_fraction' : lick_fraction
#                      }

#             if p + 1 in valve:
#                 param['repeats'] = 1

#             params.append(param)

#         return params
