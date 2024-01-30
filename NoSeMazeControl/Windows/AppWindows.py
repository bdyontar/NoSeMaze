"""
This module contains all implementation of windows in UI. There are adjustment
window, hardware window, control window, animal window, e-mail window, sensors window and 
analysis window.
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

import pickle
import os
import numpy as np
import datetime
import sys
import pandas as pd
import pyqtgraph as pg

import webbrowser
import inspect
from types import NoneType, TracebackType
import traceback
from typing import Type

from PyQt5 import QtWidgets, QtMultimedia, QtCore
from PyQt5.QtCore import pyqtSignal, Qt, QThread
from Designs import adjustmentWidget, animalWindow, hardwareWindow, prefsWindow, analysisWindow, mailWindow, controlWindow, sensorsWindow, scheduleMainWindow, sensorsWindow
from Models import GuiModels
from Schedule.Models import ScheduleWidgets, ScheduleView, Widgets
from Schedule.UI import ColorMap
from Schedule.PyPulse import PulseInterface
from Schedule.Exceptions import RewardMapError
from queue import Queue


from Sensors.MyWorker import MeasurementWorker, PlotWorker
from Sensors.PlotControl import plotter
from Sensors import constants

from Analysis import Analysis

# importing for type hinting
import typing
from main import MainApp
from Models import Experiment


# TODO: Type hinting ControlWindow as parent of AdjustmentWidget.
# TODO: Also describe attributes of all classes instead of only type hinting?



class AdjustmentWidget(QtWidgets.QDockWidget, adjustmentWidget.Ui_DockWidget):
    """Widget for adjusting camera control. """

    def __init__(self, cam: str, settings: dict[str, dict[str, typing.Any]], parent = None):
        QtWidgets.QDockWidget.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle('Adjustment ' + cam)
        self.floating = False
        self.parent = parent
        self.cam = cam
        if self.cam == 'Camera 1':
            if self.parent.camOne.imageProcessing().isAvailable():
                self.imgPro = self.parent.camOne.imageProcessing()
                self.saturationSlider.setValue(
                    int(settings['cam1']['saturation']))
                self.brightnessSlider.setValue(
                    int(settings['cam1']['brightness']))
                self.contrastSlider.setValue(int(settings['cam1']['contrast']))
                self.set_saturation(int(settings['cam1']['saturation']))
                self.set_brightness(int(settings['cam1']['brightness']))
                self.set_contrast(int(settings['cam1']['contrast']))
                self.saturationSlider.valueChanged.connect(self.set_saturation)
                self.brightnessSlider.valueChanged.connect(self.set_brightness)
                self.contrastSlider.valueChanged.connect(self.set_contrast)
            else:
                QtWidgets.QMessageBox.about(
                    self.parent, "Error", "Adjustment is not supported by Camera 1.")
        elif self.cam == 'Camera 2':
            if self.parent.camTwo.imageProcessing().isAvailable():
                self.imgPro = self.parent.camTwo.imageProcessing()
                self.saturationSlider.setValue(
                    int(settings['cam2']['saturation']))
                self.brightnessSlider.setValue(
                    int(settings['cam2']['brightness']))
                self.contrastSlider.setValue(
                    int(settings['cam2']['brightness']))
                self.set_saturation(int(settings['cam2']['saturation']))
                self.set_brightness(int(settings['cam2']['brightness']))
                self.set_contrast(int(settings['cam2']['contrast']))
                self.saturationSlider.valueChanged.connect(self.set_saturation)
                self.brightnessSlider.valueChanged.connect(self.set_brightness)
                self.contrastSlider.valueChanged.connect(self.set_contrast)
            else:
                QtWidgets.QMessageBox.about(
                    self.parent, "Error", "Adjustment is not supported by the Camera 2.")

    def set_brightness(self, value : int|None = None):
        if value is None:
            value = self.brightnessSlider.value()
        else:
            self.brightnessSlider.setValue(value)
        brightness = value/100
        self.imgPro.setBrightness(brightness)
        if self.cam == 'Camera 1':
            self.parent.settings['cam1']['brightness'] = value
        elif self.cam == 'Camera 2':
            self.parent.settings['cam2']['brightness'] = value

    def set_saturation(self, value):
        value = self.saturationSlider.value()
        saturation = value/100
        self.imgPro.setSaturation(saturation)
        if self.cam == 'Camera 1':
            self.parent.settings['cam1']['saturation'] = value
        elif self.cam == 'Camera 2':
            self.parent.settings['cam2']['saturation'] = value

    def set_contrast(self, value):
        value = self.contrastSlider.value()
        contrast = value/100
        self.imgPro.setContrast(contrast)
        if self.cam == 'Camera 1':
            self.parent.settings['cam1']['contrast'] = value
        elif self.cam == 'Camera 2':
            self.parent.settings['cam2']['contrast'] = value


class ControlWindow(QtWidgets.QMainWindow, controlWindow.Ui_MainWindow):
    """Window to view camera feedback."""

    def __init__(self, experiment: Experiment.Experiment, parent: MainApp = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.parent: MainApp = parent
        self.experiment: Experiment.Experiment = experiment
        self.setting_path: str = self.parent.config_path + "/cam.setting"
        self.camOne: QtMultimedia.QCamera | None = None
        self.camTwo: QtMultimedia.QCamera | None = None
        self.cameras_pos: dict = dict()
        self.settings: dict[str, dict[str, typing.Any]] = {
            'cam1': {
                'pos': None,
                'saturation': 0,
                'brightness': 0,
                'contrast': 0
            },
            'cam2': {
                'pos': None,
                'saturation': 0,
                'brightness': 0,
                'contrast': 0
            }
        }
        self.populate_table()

        cameras = QtMultimedia.QCameraInfo.availableCameras()
        for i, cam in enumerate(cameras):
            desc = cam.description()
            key = str(i)+' : '+desc
            self.cameras_pos[key] = cam

        if os.path.exists(self.setting_path):
            with open(self.setting_path, 'rb') as f:
                settings = pickle.load(f)
                self.configure_settings(settings)

        self.parent.experiment_control.trial_job.trial_end.connect(
            self.populate_table)
        self.actionCamera_1.triggered.connect(self.get_cam1)
        self.actionCamera_2.triggered.connect(self.get_cam2)
        self.actionRes_Camera_1.triggered.connect(self.get_res_cam1)
        self.actionRes_Camera_2.triggered.connect(self.get_res_cam2)
        self.actionAdj_Camera_1.triggered.connect(self.adjust_cam1)
        self.actionAdj_Camera_2.triggered.connect(self.adjust_cam2)

    def adjust_cam1(self):
        if self.camOne is not None:
            self.adjWidget1 : AdjustmentWidget = AdjustmentWidget(
                "Camera 1", self.settings, parent=self)
            self.addDockWidget(Qt.RightDockWidgetArea, self.adjWidget1)
        else:
            QtWidgets.QMessageBox.about(
                self, "Error", "Camera has not been set.")

    def adjust_cam2(self):
        if self.camTwo is not None:
            self.adjWidget2 : adjustmentWidget = AdjustmentWidget(
                "Camera 2", self.settings, parent=self)
            self.addDockWidget(Qt.RightDockWidgetArea, self.adjWidget2)
        else:
            QtWidgets.QMessageBox.about(
                self, "Error", "Camera has not been set.")

    def configure_settings(self, settings : dict[str, dict[str, typing.Any]]):
        for cam in settings.keys():
            if cam == 'cam1':
                if settings['cam1']['pos'] is not None:
                    key = settings['cam1']['pos']
                    self.settings['cam1']['pos'] = key
                    self.set_cam1(self.cameras_pos[key])
                    self.settings['cam1']['saturation'] = settings['cam1']['saturation']
                    self.settings['cam1']['brightness'] = settings['cam1']['brightness']
                    self.settings['cam1']['contrast'] = settings['cam1']['contrast']
                    self.camOne.imageProcessing().setBrightness(
                        settings['cam1']['brightness'])
                    self.camOne.imageProcessing().setSaturation(
                        settings['cam1']['saturation'])
                    self.camOne.imageProcessing().setContrast(
                        settings['cam1']['contrast'])
                    try:
                        self.settings['cam1']['res_x'] = settings['cam1']['res_x']
                        self.settings['cam1']['res_y'] = settings['cam1']['res_y']
                        self.set_res_cam1(
                            settings['cam1']['res_x'], settings['cam1']['res_y'])
                    except:
                        pass
            if cam == 'cam2':
                if settings['cam2']['pos'] is not None:
                    key = settings['cam2']['pos']
                    self.settings['cam2']['pos'] = key
                    self.set_cam2(self.cameras_pos[key])
                    self.settings['cam2']['saturation'] = settings['cam2']['saturation']
                    self.settings['cam2']['brightness'] = settings['cam2']['brightness']
                    self.settings['cam2']['contrast'] = settings['cam2']['contrast']
                    self.camTwo.imageProcessing().setBrightness(
                        settings['cam2']['brightness'])
                    self.camTwo.imageProcessing().setSaturation(
                        settings['cam2']['saturation'])
                    self.camTwo.imageProcessing().setContrast(
                        settings['cam2']['contrast'])
                    try:
                        self.settings['cam2']['res_x'] = settings['cam2']['res_x']
                        self.settings['cam2']['res_y'] = settings['cam2']['res_y']
                        self.set_res_cam2(
                            settings['cam2']['res_x'], settings['cam2']['res_y'])
                    except:
                        pass

    def get_cam1(self):
        key, okPressed = QtWidgets.QInputDialog.getItem(
            self, "Set Cameras", "<i>hardware position : camera description</i><br><br>Camera 1 Input:", list(self.cameras_pos.keys()), 1, False)

        if okPressed:
            self.settings['cam1']['pos'] = key
            self.set_cam1(self.cameras_pos[key])

    def set_cam1(self, cam : QtMultimedia.QCameraInfo):
        self.camOne : QtMultimedia.QCamera = QtMultimedia.QCamera(cam)
        if self.settings['cam2']['pos'] is not None and self.settings['cam1']['pos'][0] == self.settings['cam2']['pos'][0]:
            self.settings['cam2']['pos'] = None
            if self.camTwo is not None:
                self.camTwo.stop()
                self.camTwo = None

        self.camOne.setCaptureMode(QtMultimedia.QCamera.CaptureVideo)
        self.camOne.setViewfinder(self.viewfinderOne)
        self.camOne.start()

    def get_res_cam1(self):
        try:
            if self.camOne.state() is not QtMultimedia.QCamera.ActiveState:
                self.camOne.start()

            res_list = self.camOne.supportedViewfinderResolutions()

            str_list = list(map(self.qsize_to_string, res_list))

            res, okPressed = QtWidgets.QInputDialog.getItem(
                self, "Set Resolution", "Camera 1 Resolution:", str_list, 0, False)

            if okPressed:
                res = res.split("x")
                x = int(res[0])
                y = int(res[1])
                self.settings['cam1'].update({'res_x': x, 'res_y': y})
                self.set_res_cam1(x, y)
        except:
            QtWidgets.QMessageBox.about(
                self, "Error", "Camera has not been set.")

    def set_res_cam1(self, x : int, y : int):
        self.viewfinderOneSettings : QtMultimedia.QCameraViewfinderSettings = QtMultimedia.QCameraViewfinderSettings()
        self.viewfinderOneSettings.setResolution(x, y)
        self.camOne.setViewfinderSettings(self.viewfinderOneSettings)

    def get_cam2(self):
        key, okPressed = QtWidgets.QInputDialog.getItem(
            self, "Set Cameras", "<i>hardware position : camera description</i><br><br>Camera 2 Input:", list(self.cameras_pos.keys()), 2, False)

        if okPressed:
            self.settings['cam2']['pos'] = key
            self.set_cam2(self.cameras_pos[key])

    def set_cam2(self, cam : QtMultimedia.QCameraInfo):
        self.camTwo : QtMultimedia.QCamera = QtMultimedia.QCamera(cam)
        if self.settings['cam1']['pos'] is not None and self.settings['cam2']['pos'] == self.settings['cam1']['pos']:
            self.settings['cam1']['pos'] = None
            if self.camOne is not None:
                self.camOne.stop()
                self.camOne = None

        self.camTwo.setViewfinder(self.viewfinderTwo)
        self.camTwo.setCaptureMode(QtMultimedia.QCamera.CaptureVideo)
        self.camTwo.start()

    def get_res_cam2(self):
        try:
            if self.camTwo.state() is not QtMultimedia.QCamera.ActiveState:
                self.camTwo.start()

            res_list = self.camTwo.supportedViewfinderResolutions()

            str_list = list(map(self.qsize_to_string, res_list))

            res, okPressed = QtWidgets.QInputDialog.getItem(
                self, "Set Resolution", "Camera 2 Input:", str_list, 0, False)

            if okPressed:
                res = res.split("x")
                x = int(res[0])
                y = int(res[1])
                self.settings['cam2'].update({'res_x': x, 'res_y': y})
                self.set_res_cam2(x, y)
        except:
            QtWidgets.QMessageBox.about(
                self, "Error", "Camera has not been set.")

    def set_res_cam2(self, x : int, y : int):
        self.viewfinderTwoSettings = QtMultimedia.QCameraViewfinderSettings()
        self.viewfinderTwoSettings.setResolution(x, y)
        self.camTwo.setViewfinderSettings(self.viewfinderTwoSettings)

    def qsize_to_string(self, qsize : QtCore.QSize):
        string = str(qsize)
        string = string.strip("PyQt5.QtCore.QSize()")
        string = string.replace(", ", "x")
        return string

    def populate_table(self):
        self.table_list : list = list()
        for animal in self.experiment.animal_list:
            this_animal = self.experiment.animal_list[animal]
            self.table_list.append([animal, this_animal.total_licks])

        self.model = GuiModels.TableModel(['Animal ID', 'Total Licks'],
                                          self.table_list, parent=self)

        self.animalListTable.setModel(self.model)
        self.animalListTable.selectionModel().selectionChanged.connect(self.on_animal_selected)

    def on_animal_selected(self):
        try:
            selected_row = self.animalListTable.selectionModel().selectedRows()[
                0].row()
        except:
            selected_row = 0
        selected_animal = self.table_list[selected_row][0]
        self.update_licks_view(selected_animal)

    def update_licks_view(self, animal):
        fname = self.experiment.animal_list[animal].fname

        if fname is not None and os.path.isfile(fname):
            with open(fname, 'r', newline='') as f:
                licks_list = f.readlines()
                licks_list = licks_list[1:]
            for i, row in enumerate(licks_list):
                licks_list[i] = row.split(',')
        else:
            licks_list = list()
        licks_T = list(map(list, zip(*licks_list)))
        if len(licks_list) == 0:
            t = [0, 0.5]
            licks_data = [0, 0]
        else:
            t = licks_T[0]
            licks_data = licks_T[4]
            start = datetime.datetime.strptime(
                self.experiment.date, '%Y-%m-%d %H:%M:%S.%f')
            for i, time in enumerate(t):
                t[i] = (time - start)/datetime.timedelta(hours=1)

        self.licksView.plotItem.clear()
        self.licksView.plotItem.plot(t, licks_data)

    def closeEvent(self, event : QtCore.QEvent):
        if self.camOne is not None:
            self.camOne.stop()
            self.camOne.unload()
        if self.camTwo is not None:
            self.camTwo.stop()
            self.camTwo.unload()
        with open(self.setting_path, 'wb') as f:
            pickle.dump(self.settings, f)
            f.flush()
        event.accept()


class MailWindow(QtWidgets.QMainWindow, mailWindow.Ui_MainWindow):
    """Window for configuring mailing list."""

    def __init__(self, parent : MainApp = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.mailingListWidget.setSortingEnabled
        self.mailingListWidget.setSelectionMode(3)

        # Get mailing list
        self.fn = os.getcwd() + '\\HelperFunctions\\Email\\mailing_list.txt'
        if os.path.isfile(self.fn):
            with open(self.fn, encoding='utf-8') as f:
                self.mlist = f.readlines()
                for i, addr in enumerate(self.mlist):
                    self.mlist[i] = addr.strip("\n")
            self.populate_mailing_list(self.mlist)
        else:
            self.mlist = list()

        try:
            self.addAddressButton.clicked.connect(self.get_address)
            self.removeAddressButton.clicked.connect(self.remove_address)
        except:
            pass

    def get_address(self):
        text, okPressed = QtWidgets.QInputDialog.getText(
            self, "Add Address", "Please input the address. For multiple addresses, please separate them with a  \",\"", QtWidgets.QLineEdit.Normal, "")

        if okPressed and text != "":
            text = text.replace(" ", "")
            text = text.split(",")

            if len(text) > 0:
                i = 0
                for item in text:
                    if '@zi-mannheim.de' in item:
                        i = i+1
                    if '.' not in item.split("@")[0]:
                        i = i-1
                if i == len(text):
                    self.add_address(text)
                else:
                    QtWidgets.QMessageBox.about(
                        self.parent, "Error", "Invalid Address")

    def populate_mailing_list(self, mlist : list[str]):
        self.mailingListWidget.clear()
        self.mailingListWidget.addItems(mlist)
        self.mailingListWidget.sortItems()

    def remove_address(self):
        rem_list = self.mailingListWidget.selectedItems()
        # rem_list is QItemList and addr is QItem
        for addr in rem_list:
            self.mlist.remove(addr.text())
        self.populate_mailing_list(self.mlist)
        self.save(self.mlist)

    def add_address(self, new_addrs : list[str]):
        for addr in new_addrs:
            if not addr in self.mlist:
                self.mlist.append(addr)
        self.populate_mailing_list(self.mlist)
        self.save(self.mlist)

    def save(self, mlist : list[str]):
        with open(self.fn, 'w') as f:
            for addr in mlist:
                f.write(addr+'\n')


class AnimalWindow(QtWidgets.QMainWindow, animalWindow.Ui_MainWindow):
    """Window for configurin animal list."""
    changed = pyqtSignal()
    saved = pyqtSignal()

    def __init__(self, parent : MainApp = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.parent : MainApp = parent

        self.status = True
        self.populate_animal_table(parent.experiment.animal_list)

        # function bindings
        self.addRowButton.clicked.connect(self.add_row)
        self.removeRowButton.clicked.connect(self.remove_row)
        self.actionUpdate.triggered.connect(self.update_animals)
        self.addScheduleButton.clicked.connect(self.add_schedule)
        self.removeScheduleButton.clicked.connect(self.remove_schedule)
        self.changed.connect(self.change_false)
        self.saved.connect(self.change_true)

        self.animalTable.selectionModel().selectionChanged.connect(self.animal_selected)
        self.animalTable.itemDoubleClicked.connect(self.change_false)
        self.scheduleTable.selectionModel().selectionChanged.connect(self.schedule_selected)

    def add_row(self):
        self.animalTable.insertRow(self.animalTable.rowCount())
        self.changed.emit()

    def remove_row(self):
        selectedRows = self.animalTable.selectedIndexes()
        rows = [row.row() for row in selectedRows]
        if rows == []:
            rows = [self.animalTable.rowCount()-1]
        else:
            rows.sort()
            rows.reverse()
        for row in rows:
            animal = self.animalTable.item(row, 0).text(
            ) if self.animalTable.item(row, 0) is not None else ""
            
            if animal != 'default': # do nothing if it is default mouse
                if animal:
                    answer = QtWidgets.QMessageBox.question(
                        self,
                        "Warning",
                        ("All data of <strong> {animal} </strong> will be deleted.<br/>" +
                        "Are you sure?<br/><br/><em>Hint: You can also delete specific animal from<br/>" +
                        "the list by selecting the animal<br/>before clicking the minus button.</em>").format(
                            animal=animal), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                    if answer == QtWidgets.QMessageBox.Yes:
                        if animal in self.parent.experiment.animal_list.keys():
                            del self.parent.experiment.animal_list[animal]
                        self.animalTable.removeRow(row)
                else:
                    self.animalTable.removeRow(row)
        
        self.changed.emit()

    def populate_animal_table(self, animal_list):
        self.animalTable.clear()

        self.animalTable.setRowCount(len(animal_list.keys()))
        self.animalTable.setColumnCount(1)

        for a, animal in enumerate(sorted(list(animal_list.keys()))):
            id = QtWidgets.QTableWidgetItem(animal_list[animal].id)
            self.animalTable.setItem(a, 0, id)

    def current_animal(self):
        try:
            row = self.animalTable.selectedIndexes()[0].row()
            animal = self.parent.experiment.animal_list[self.animalTable.item(
                row, 0).text()]
            return animal
        except:
            return None

    def current_sched_index(self):
        try:
            row = self.scheduleTable.selectedIndexes()[0].row()
            return row
        except:
            return self.scheduleTable.rowCount()

    def update_animals(self):
        try:
            for row in range(self.animalTable.rowCount()):
                id = self.animalTable.item(row, 0).text()
                self.parent.experiment.add_mouse(id)
            self.saved.emit()
        except:
            QtWidgets.QMessageBox.about(
                self.parent, "Error", "Animal row must have the correct data type and must not be empty")

    def animal_selected(self):
        animal = self.current_animal()
        if animal is not None:
            self.scheduleTable.setRowCount(len(animal.schedule_list))
            self.scheduleTable.setColumnCount(3)

            for s, schedule in enumerate(animal.schedule_list):
                sched_name = QtWidgets.QTableWidgetItem(schedule.id)
                n_trials = QtWidgets.QTableWidgetItem(
                    str(len(schedule.schedule_trials)))
                perc_complete = round(
                    ((schedule.current_trial) / (len(schedule.schedule_trials) - 1)) * 100, 2)
                progress = QtWidgets.QTableWidgetItem(str(perc_complete))

                self.scheduleTable.setItem(s, 0, sched_name)
                self.scheduleTable.setItem(s, 1, n_trials)
                self.scheduleTable.setItem(s, 2, progress)

    def schedule_selected(self):
        try:
            animal = self.current_animal()
            schedule = animal.schedule_list[self.current_sched_index()]

            self.trialView.setModel(GuiModels.TableModel(
                schedule.schedule_headers, schedule.schedule_trials, parent=self))
        except:
            pass

    def add_schedule(self):
        animal = self.current_animal()
        if animal is not None:
            try:
                fname, suff = QtWidgets.QFileDialog.getOpenFileName(
                    self, "Load Schedule", '', '*.schedule')
                with open(fname, 'rb') as fn:
                    schedule_data = pickle.load(fn)

                animal.add_schedule(os.path.basename(fname), schedule_data['schedule'], schedule_data['headers'],
                                    schedule_data['params'], self.current_sched_index())

                self.animal_selected()
            except:
                pass
        else:
            QtWidgets.QMessageBox.about(
                self.parent, "Animal Management", "No animal selected\n\nPlease select an animal before clicking the Add Schedule button")

    def remove_schedule(self):
        try:
            animal = self.current_animal()
            del animal.schedule_list[self.current_sched_index()]
            if animal.current_schedule_idx >= self.current_sched_index():
                animal.current_schedule_idx -= 1
        except:
            pass
        self.animal_selected()

    def change_true(self):
        if self.status == False:
            self.status = True
            self.setWindowTitle('Animal Management')

    def change_false(self):
        animal = self.current_animal()
        if self.status == True:
            self.status = False
            self.setWindowTitle('Animal Management*')

    def closeEvent(self, event : QtCore.QEvent):
        if self.status == False:
            answer = QtWidgets.QMessageBox.question(self, "Warning", "<b>Animal Management</b> has been modified.<br>Do you want to save changes?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)
            if answer == QtWidgets.QMessageBox.Yes:
                self.update_animals()
                if self.status:
                    event.accept()
                else:
                    event.ignore()
            elif answer == QtWidgets.QMessageBox.No:
                self.status = True
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


class HardwareWindow(QtWidgets.QMainWindow, hardwareWindow.Ui_MainWindow):
    """Window for configurin hardware preferences."""
    new_pref = pyqtSignal(dict)
    saved = pyqtSignal()

    def __init__(self, parent : MainApp = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.status = True

        if self.parent.hardware_prefs is not None:
            self.set_preferences(self.parent.hardware_prefs)

        self.actionSave_Preferences.triggered.connect(self.save_preferences)
        self.saved.connect(self.saved_status)

        self.analogInputEdit.textEdited.connect(self.change)
        self.analogChannelsSpin.valueChanged.connect(self.change)
        self.odourOutputEdit.textEdited.connect(self.change)
        self.syncClockEdit.textEdited.connect(self.change)
        self.rewardOutput1Edit.textEdited.connect(self.change)
        self.rewardOutput2Edit.textEdited.connect(self.change)
        self.fvOutputEdit.textEdited.connect(self.change)
        self.rfidPortEdit.textEdited.connect(self.change)
        self.samplingRateEdit.textEdited.connect(self.change)
        self.lickChannelSpin.valueChanged.connect(self.change)
        self.timeoutEdit.textEdited.connect(self.change)
        self.beamChannelSpin.valueChanged.connect(self.change)
        self.lickChannel2Spin.valueChanged.connect(self.change)
        self.analogInput3Spin.valueChanged.connect(self.change)
        self.usbBox.stateChanged.connect(self.change)
        self.fvDelayEdit.textEdited.connect(self.change)
        self.thoraxMonitorDelayEdit.textEdited.connect(self.change)
        self.lickMonitorDelayEdit.textEdited.connect(self.change)
        self.lickrateEdit.textEdited.connect(self.change)

    def set_preferences(self, prefs):
        self.analogInputEdit.setText(prefs['analog_input'])
        self.analogChannelsSpin.setValue(prefs['analog_channels'])
        self.odourOutputEdit.setText(prefs['odour_output'])
        self.syncClockEdit.setText(prefs['sync_clock'])
        self.rewardOutput1Edit.setText(prefs['reward_output1'])
        self.rewardOutput2Edit.setText(prefs['reward_output2'])
        self.fvOutputEdit.setText(prefs['finalvalve_output'])
        self.rfidPortEdit.setText(prefs['rfid_port'])
        self.samplingRateEdit.setText(str(prefs['samp_rate']))
        self.lickChannelSpin.setValue(prefs['lick_channel_l'])
        self.timeoutEdit.setText(str(prefs['timeout']))
        self.beamChannelSpin.setValue(prefs['beam_channel'])
        self.lickChannel2Spin.setValue(prefs['lick_channel_r'])
        self.analogInput3Spin.setValue(prefs['analog_input_3'])
        self.usbBox.setChecked(prefs['static'])
        self.fvDelayEdit.setText(str(prefs['fv_delay']))
        self.thoraxMonitorDelayEdit.setText(
            str(prefs['thorax_delay']))  # TODO Namen ändern
        self.lickMonitorDelayEdit.setText(
            str(prefs['lick_delay']))  # TODO Namen ändern
        self.lickrateEdit.setText(str(prefs['low_lickrate']))

    def zero_edit(self):
        sl = len(self.samplingRateEdit.text())
        number = list(str(2/int(self.samplingRateEdit.text())))
        number[sl] = str(int(number[sl])+1)
        number = number[:(sl+1)]
        number = "".join(number)
        return number

    def save_preferences(self):

        try:
            prefs = {'analog_input': self.analogInputEdit.text(),
                     'analog_channels': int(self.analogChannelsSpin.value()),
                     'odour_output': self.odourOutputEdit.text(),
                     'reward_output1': self.rewardOutput1Edit.text(),
                     'reward_output2': self.rewardOutput2Edit.text(),
                     'sync_clock': self.syncClockEdit.text(),
                     'finalvalve_output': self.fvOutputEdit.text(),
                     'rfid_port': self.rfidPortEdit.text(),
                     'samp_rate': int(self.samplingRateEdit.text()),
                     'lick_channel': int(self.lickChannelSpin.value()),
                     'timeout': int(self.timeoutEdit.text()),
                     'beam_channel': int(self.beamChannelSpin.value()),
                     'lick_channel_l': int(self.lickChannelSpin.value()),
                     'lick_channel_r': int(self.lickChannel2Spin.value()),
                     'analog_input_3': int(self.analogInput3Spin.value()),
                     'static': bool(self.usbBox.isChecked()),
                     'fv_delay': float(self.fvDelayEdit.text()),
                     'thorax_delay': float(self.thoraxMonitorDelayEdit.text()),
                     'lick_delay': float(self.lickMonitorDelayEdit.text()),
                     'low_lickrate': float(self.lickrateEdit.text())}
        except ValueError:
            QtWidgets.QMessageBox.about(self.parent, "Error",
                                        "A value error has occured")
        else:
            self.parent.hardware_prefs = prefs
            self.new_pref.emit(prefs)

            hardware_config_path = self.parent.config_path+'/hardware.config'
            with open(hardware_config_path, 'wb') as fn:
                pickle.dump(prefs, fn)
                fn.flush()
            self.saved.emit()

    def saved_status(self):
        if self.status == False:
            self.status = True
            self.setWindowTitle('Hardware Preferences')

    def change(self):
        if self.status == True:
            self.status = False
            self.setWindowTitle('Hardware Preferences*')

    def closeEvent(self, event : QtCore.QEvent):
        if self.status == False:
            answer = QtWidgets.QMessageBox.question(self, "Warning", "<b>Hardware Preferences</b> has been modified.\nDo you want to save changes?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)
            if answer == QtWidgets.QMessageBox.No:
                self.status = True
                self.setWindowTitle('Hardware Preferences')
                event.accept()
            elif answer == QtWidgets.QMessageBox.Yes:
                self.save_preferences()
                if self.status:
                    event.accept()
                else:
                    event.ignore()
        else:
            event.accept()


class PreferencesWindow(QtWidgets.QMainWindow, prefsWindow.Ui_MainWindow):
    """Older version of hardware preference window."""
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent

        if self.parent.preferences is not None:
            self.set_preferences(self.parent.preferences)

        self.actionSave_Preferences.triggered.connect(self.save_preferences)
        self.savePathButton.clicked.connect(self.select_save_path)

    def set_preferences(self, prefs):
        self.savePathEdit.setText(prefs['save_path'])
        self.experimentNameEdit.setText(prefs['experiment_name'])

    def save_preferences(self):
        prefs = {'save_path': self.savePathEdit.text(),
                 'experiment_name': self.experimentNameEdit.text()}

        self.parent.preferences = prefs

        with open('preferences.config', 'wb') as fn:
            pickle.dump(prefs, fn)

    def select_save_path(self):
        save_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Choose Save Folder')
        self.savePathEdit.setText(save_path)


class AnalysisWindow(QtWidgets.QMainWindow, analysisWindow.Ui_MainWindow):
    """Window to see some analysis of trial results."""
    def __init__(self, experiment : Experiment.Experiment, parent : MainApp = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.experiment = experiment
        self.currWidget = self.tabWidget.widget(0)
        self.idx = self.tabWidget.currentIndex()

        self.populate_stats_table()

        self.experimentStatsTable.selectionModel(
        ).selectionChanged.connect(self.on_animal_selected)
        self.binSizeSpin.valueChanged.connect(self.on_animal_selected)
        self.tabWidget.currentChanged.connect(self.on_tab_selected)

    def on_tab_selected(self, index):
        self.currWidget = self.tabWidget.widget(index)
        self.idx = index

    def populate_stats_table(self):
        self.experimentStatsTable.setRowCount(
            len(self.experiment.animal_list.keys()))

        for m, mouse in enumerate(sorted(list(self.experiment.animal_list.keys()))):
            this_mouse = self.experiment.animal_list[mouse]

            id = QtWidgets.QTableWidgetItem(this_mouse.id)
            total_trials = QtWidgets.QTableWidgetItem(
                str(Analysis.n_trials_performed(this_mouse)))
            trials_last24h = QtWidgets.QTableWidgetItem(
                str(Analysis.n_trials_last_24(this_mouse)))

            self.experimentStatsTable.setItem(m, 0, id)
            self.experimentStatsTable.setItem(m, 1, total_trials)
            self.experimentStatsTable.setItem(m, 2, trials_last24h)

    def on_animal_selected(self):
        if self.idx < 2:
            self.display_animal_performance()
            self.display_group_performance()

    def display_animal_performance(self):
        animal = self.current_animal()
        if animal is not None:
            # binned_correct = Analysis.binned_performance(animal, int(self.binSizeSpin.value())) -
            # Non-weighted performance
            bin_size = int(self.binSizeSpin.value())

            binned_correct_hit, binned_correct_rejection = Analysis.weighted_binned_performance(animal,
                                                                                                bin_size,
                                                                                                self.idx)

            self.currWidget.animalPerformanceView.plotItem.clear()
            self.currWidget.animalPerformanceView.plotItem.setLabels(title='Animal Performance',
                                                                     left='Correct',
                                                                     bottom='Legend : ' +
                                                                     'yellow - hit, grey - c_rejection')
            self.currWidget.animalPerformanceView.plotItem.plot(
                binned_correct_hit, pen='y', name='hit')
            self.currWidget.animalPerformanceView.plotItem.plot(
                binned_correct_rejection, pen=0.8, name='c_rejection')

            # Guide lines
            N_x = len(binned_correct_hit)
            self.currWidget.animalPerformanceView.plotItem.plot(
                np.ones(N_x) * 0.5, pen='r')
            self.currWidget.animalPerformanceView.plotItem.plot(
                np.ones(N_x) * 0.8, pen='g')

            self.currWidget.animalPerformanceView.setYRange(-0.1, 1.1)

    def display_group_performance(self):
        n_longest = 0
        all_performance = list()
        bin_size = int(self.binSizeSpin.value())
        for animal_id in self.parent.experiment.animal_list.keys():
            animal = self.parent.experiment.animal_list[animal_id]
            if animal_id != 'default':
                this_performance = Analysis.binned_performance(animal,
                                                               bin_size,
                                                               self.idx)
                all_performance.append(this_performance)
                if len(this_performance) > n_longest:
                    n_longest = len(this_performance)

        performance_matrix = np.empty(
            (len(self.parent.experiment.animal_list)-1, n_longest))
        performance_matrix[:] = np.nan

        for p, perf in enumerate(all_performance):
            performance_matrix[p][0:len(perf)] = perf

        av_performance = np.nanmean(performance_matrix, 0)
        std_performance = np.nanstd(performance_matrix, 0)

        self.currWidget.groupPerformanceView.plotItem.clear()
        self.currWidget.groupPerformanceView.plotItem.setLabels(title='Group Performance',
                                                                left='Correct',
                                                                bottom='Legend: ' +
                                                                'grey - hit and c_rejection, ' +
                                                                'magenta - std. dev.')

        self.currWidget.groupPerformanceView.plotItem.plot(
            av_performance, name='hit and c_rejection')
        self.currWidget.groupPerformanceView.plotItem.plot(
            av_performance + std_performance, pen='m', name='std. dev.')
        self.currWidget.groupPerformanceView.plotItem.plot(
            av_performance - std_performance, pen='m')

        # Guide lines
        self.currWidget.groupPerformanceView.plotItem.plot(
            np.ones(len(av_performance)) * 0.5, pen='r')
        self.currWidget.groupPerformanceView.plotItem.plot(
            np.ones(len(av_performance)) * 0.8, pen='g')

        self.currWidget.groupPerformanceView.setYRange(-0.1, 1.1)

    def current_animal(self):
        try:
            row = self.experimentStatsTable.selectedIndexes()[0].row()
            animal = self.parent.experiment.animal_list[self.experimentStatsTable.item(
                row, 0).text()]
            return animal
        except:
            return None
        




class SchedulesWindow(QtWidgets.QMainWindow, scheduleMainWindow.Ui_MainWindow):
    """The MainApp of schedule generator UI. Inherits QMainWindow
    and uses design from mainDesign.

    Attributes
    ----------
    parent : NoneType
        Parent of the main window. MainApp does not have a parent widget.

    current_schedule_type : QWidget
        Current schedule type chosen in drop down menu.
    
    schedule : dict
        Schedule created.
    
    schedule_headers : list
        Header of the schedule.
    
    generated : bool, default=False
        Status if schedule is generated.

    schedule_types : dict
        Types of schedules available.
    """

    def __init__(self, parent : NoneType = None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.parent = parent

        self.current_schedule_type : str = None
        self.schedule : dict = dict()
        self.schedule_headers : list = []
        self.generated : bool= False

        # add the valence map
        self.valence_map : Widgets.ValveMapWidget = Widgets.ValveMapWidget(self.valveMapContents)
        self.valveMapContents.layout().addWidget(self.valence_map)

        # populate schedule types
        self.schedule_types = dict()
        for name, obj in inspect.getmembers(ScheduleWidgets):
            if inspect.isclass(obj):
                self.scheduleTypesCombo.addItem(name)
                self.schedule_types[name] = obj

        # initialise schedule model
        self.scheduleView.setModel(ScheduleView.ScheduleModel([], [[]]))

        # select first schedule widget
        self.select_schedule_type()

        # add function bindings
        self.actionSave.triggered.connect(self.save_schedule)
        self.actionOpenUserGuide.triggered.connect(self.open_user_guide)
        self.actionAbout.triggered.connect(self.show_about)
        self.generateScheduleButton.clicked.connect(self.generate)
        self.scheduleTypesCombo.activated.connect(self.select_schedule_type)
        self.scheduleView.selectionModel().selectionChanged.connect(self.draw_pulse)

    def generate(self):
        """Slot for generating schedule if generate button is clicked."""

        try:
            # get the schedule data and headers
            self.schedule, self.schedule_headers = self.current_schedule_type.generate_schedule(
                self.valence_map.get_valence_map())
        except RewardMapError:
            # Known error. Catch error here to avoid showing error message the 2nd time.
            pass
        except Exception as e:
            # Show exception and traceback in an error window if error has occured
            eStr = "".join(traceback.format_exception(e))
            QtWidgets.QMessageBox.about(
                self.parent, "Error", "An error has occured.\n\n{}".format(eStr))
        else:
            # Post to the schedule view
            self.schedule_model = ScheduleView.ScheduleModel(
                self.schedule_headers, self.schedule, parent=self)
            self.scheduleView.setModel(self.schedule_model)
            self.scheduleView.selectionModel().selectionChanged.connect(self.draw_pulse)
            self.generated = True
            QtWidgets.QMessageBox.about(
                self.parent, "Schedule", "Schedule is generated!")

    def select_schedule_type(self):
        """Slot for updating schedule view if a schedule type is selected."""

        self.generated = False
        schedule_name = self.scheduleTypesCombo.currentText()

        if self.current_schedule_type is not None:
            self.scheduleParamsContents.layout().removeWidget(self.current_schedule_type)
            self.current_schedule_type.deleteLater()

        self.current_schedule_type = self.schedule_types[schedule_name]()
        self.scheduleParamsContents.layout().addWidget(self.current_schedule_type)

        self.scheduleView.setModel(ScheduleView.ScheduleModel([], [[]]))

    def draw_pulse(self):
        """Slot for drawing or redrawing pulse in UI if a new trial is selected."""

        trial = self.schedule[self.scheduleView.selectionModel().selectedRows()[
            0].row()]
        params = self.current_schedule_type.pulse_parameters(trial)

        pulses, t = PulseInterface.make_pulse(1000.0, 0.0, 0.0, params)

        self.pulseView.plotItem.clear()
        for p, pulse in enumerate(pulses):
            color = ColorMap.c_list[self.valence_map.get_valence_map()[p]]
            self.pulseView.plotItem.plot(
                t, np.array(pulse) - (p*1.1), pen=color)

    def save_schedule(self):
        """Slot for saving schedule as .schedule"""

        if self.generated:
            params = list()
            for trial in self.schedule:
                params.append(
                    self.current_schedule_type.pulse_parameters(trial))

            fname, suff = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save Schedule", '', "Schedule File (*.schedule)")
            try:
                with open(fname, 'wb') as fn:
                    pickle.dump({'schedule': self.schedule,
                                 'headers': self.schedule_headers,
                                 'params': params}, fn)
            except:
                #QtWidgets.QMessageBox.about(self.parent,"Error","An error has occurred")
                pass
        else:
            QtWidgets.QMessageBox.about(
                self.parent, "Error", "Schedule is not yet generated!")

    def open_user_guide(self):
        """Open User Guide. If there is no user guide locally available, 
        open the user guide in Github.
        """

        def _open_file_in(dPath):
            """Check if file is available. If yes, then open file
            in default apps. Return true, if file is available; else 
            return false.
            """
            isFile = os.path.isfile(dPath)
            if isFile:
                os.startfile(dPath)

            return isFile

        # Relative path to user guide document.
        docsPath = "Documentation/Guides/userGuide.pdf"
        dPath = "../" + docsPath
        # If file not found, assuming current working directory is NoSeMazeSchedule
        if not _open_file_in(dPath):
            dPath = "./" + docsPath
            # If file not found, assuming current working directory is NoSeMaze
            if not _open_file_in(dPath):
                webbrowser.open(
                    "https://github.com/KelschLAB/NoSeMaze/blob/master/Documentation/Guides/userGuide.md#nosemazeschedule")

    def show_about(self):
        """Show the *about* message."""

        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setTextFormat(QtCore.Qt.TextFormat.RichText)
        msgBox.setWindowTitle("About")
        msgBox.setText(
            "<html><strong style=\"font-size:18px\">NoSeMaze Scheduler v1.0</strong>")
        infText = ("<html><em style=\"font-size:14px\">NoSeMaze Scheduler</em> is part of <em>NoSeMaze</em>." +
                   "<br /><div style=\"font-size:14px;white-space:nowrap\">NoSeMaze&nbsp;&nbsp;Copyright (c) 2019, 2022&nbsp;&nbsp;\"name of author(s)\"</div>" +
                   "<div style=\"font-size:14px;white-space:wrap;text-align:justify;text-justify:inter-word\">This program comes with ABSOLUTELY NO WARRANTY. " +
                   "This is free software, and you are welcome to redistribute it under certain conditions. " +
                   "Click <em style=\"white-space:nowrap\">Show Details...</em> below for more details.</div>")
        msgBox.setInformativeText(infText)
        detText = ("NoSeMaze is free software: you can redistribute it and/or " +
                   "modify it under the terms of GNU General Public License as " +
                   "published by the Free Software Foundation, either version 3 " +
                   "of the License, or (at your option) at any later version.\n\n" +

                   "NoSeMaze is distributed in the hope that it will be useful, " +
                   "but WITHOUT ANY WARRANTY; without even the implied warranty " +
                   "of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. " +
                   "See the GNU General Public License for more details.")
        msgBox.setDetailedText(detText)
        msgBox.exec()


# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook


def my_exception_hook(exctype: Type[BaseException], value: BaseException, traceback: TracebackType):
    """Custom exception hook.

    Parameters
    ----------
    exctype : type of exception
        Type of exception catch.
    value : BaseException
        Exception catched.
    traceback : TracebackType
        Traceback associated with the exception.
    """
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


# Main Window of the application
class SensorsWindow(QtWidgets.QMainWindow, sensorsWindow.Ui_MainWindow):
    """PyQt window to display sensor data
    """

    def __init__(self, parent : MainApp = None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.setWindowTitle("NoseMaze II")

        self.parent = parent
        self.setupUi(self)

        self.initalize_workers()

        # Connect buttons to start and stop the worker
        self.bu_start.clicked.connect(self.start_worker)
        self.bu_stop.clicked.connect(self.stop_worker)
        self.bu_reset.clicked.connect(self.reset)

        self.sensors_slider.valueChanged.connect(self.slider_value_changed)


    def initalize_workers(self):
        """Method to create two workers and their pyqt threads:
        worker 1 recieves the measurement data from the sensornodes.
        worker 2 plots the measurement data.
        """
        # Create a new worker == pseudo thread
        self.worker = MeasurementWorker()
        self.plot_worker = PlotWorker(self.graphicsView)

        self.worker_thread = QThread()
        self.plot_thread = QThread()

        # Move worker to thread
        self.worker.moveToThread(self.worker_thread)
        self.plot_worker.moveToThread(self.plot_thread)

        self.plot_thread.start()

        # Connect signals
        self.worker_thread.started.connect(self.worker.start)
        self.worker.finished.connect(self.worker_thread.quit)

        # Connect the worker's signal to the plot workers slot
        self.worker.measurementsReady.connect(self.plot_worker.plotMeasurement)

    
    def start_worker(self):

        if self.worker_thread.isRunning():
            self.worker.start()
        else:
            self.worker_thread.start()

        self.bu_start.setEnabled(False)
        self.bu_stop.setEnabled(True)
        self.sensors_slider.setEnabled(False)


    def stop_worker(self):
        if self.worker_thread.isRunning():
            self.worker.stop()   
            self.bu_stop.setEnabled(False)
            self.bu_start.setEnabled(True)
            #self.bu_reset.setEnabled(True)

    def reset(self):
        if self.worker_thread.isRunning():
            
            self.worker.reset()   
    
            self.graphicsView.clear()

            self.bu_start.setEnabled(True)       
            self.sensors_slider.setEnabled(True)

            self.sensors_slider.setValue(1)
            self.slider_value.setText("1")
            constants.SNIds = [1]

            self.plot_worker.setupPlots()
            print("Resetted")


    def slider_value_changed(self, value):
        self.slider_value.setText(f"{value}") 
        constants.SNIds = list(range(1, value+1))
        print(constants.SNIds)

        self.plot_worker.setupPlots()
        self.worker.reset()


    def closeEvent(self, event):
        print("Shutting down")
        self.stop_worker()