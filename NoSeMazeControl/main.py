"""
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

import sys
import os
from types import NoneType
import webbrowser
import pickle
import datetime
import numpy as np
from PyQt5 import QtWidgets, QtCore

from Designs import mainWindow
from Windows import AppWindows
from Models import GuiModels
import Models.Experiment as Experiment
from Controllers import ExperimentControl
from PyPulse import PulseInterface
from HelperFunctions import Email as email


class MainApp(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    """The main window class of the UI.

    Inherits QMainWindow from QtWidgest and uses UI design from
    mainWindow.py.

    Attributes
    ----------
    saved_status : bool
        Status if experiments already saved. Checked while closing the windows
        and changed if any trials are executed or experiment is saved.

    config_path : str
        Path to the config files.

    hardware_prefs : dict
        Hardware preferences.

    message_folder_path : str
        Path to message folder to save deadman-switch, warning and error messages.

    hardware_window : instance of AppWindows.HardwareWindow class
        Hardware window to configure hardware preferences.

    animal_window : instance of AppWindows.AnimalWindow class
        Animal window to input animals in the experiment and their schedules.

    analysis_window : instance of AppWindows.AnalysisWindow class
        Analysis window that shows the performance curve of the experiment and of
        each mouses respectively.

    mail_window : instance of AppWindows.MailWindow class
        Mail window to input the mailing list.

    control_window : instance of AppWindows.ControlWindow class
        Control window which shows video feed of usb cameras connected. Currently not maintained.

    experiment : instance of Experiment class
        Variable where data are saved.

    Note
    ----
    E-Mailing functionality is deprecated as messages are now saved in a cloud folder.
    """

    saved = QtCore.pyqtSignal()
    """QtCore.pyqtSignal: pyqtSignal sent if experiment is saved."""

    loaded = QtCore.pyqtSignal()
    """QtCore.pyqtSignal: pyqtSignal sent if experiment is loaded."""

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.saved_status : bool = True
        self.config_path : str = ".nosemazeconfig"

        # create config folder if folder does not exist
        if not os.path.isdir(self.config_path):
            os.makedirs(self.config_path)

        self.hardware_prefs : dict = self.load_config_data()
        self.message_folder_path : str = self.load_message_folder_path()
        email.message_folder_path = self.message_folder_path
        self.hardware_window : AppWindows.HardwareWindow = AppWindows.HardwareWindow(self)
        self.animal_window : AppWindows.AnimalWindow = None
        self.analysis_window : AppWindows.AnalysisWindow = None
        self.mail_window : NoneType = None
        self.control_window : AppWindows.ControlWindow = None
        self.setup_experiment_bindings(Experiment.Experiment())

        # binding functions to the signals
        self.actionAnimal_List.triggered.connect(self.open_animal_window)
        self.actionHardware_Preferences.triggered.connect(self.open_hardware_window)
        self.actionAnalyse_Experiment.triggered.connect(self.open_analysis_window)
        self.actionView_Data.triggered.connect(self.open_sensor_viewer)

        self.actionMailing_List.triggered.connect(self.open_mail_window)
        self.actionMessage_Folder.triggered.connect(self.set_message_folder_path)
        self.actionVideo_Control.triggered.connect(self.open_control_window)
        self.actionOpen_User_Guide.triggered.connect(self.open_user_guide)
        self.actionAbout.triggered.connect(self.show_about)
        self.actionSave_Experiment.triggered.connect(self.save_experiment)
        self.actionLoad_Experiment.triggered.connect(self.load_experiment)
        self.saved.connect(self.experiment_saved)

    def setup_experiment_bindings(self, experiment : Experiment.Experiment):
        """
        Set up experiment in the GUI and populate the experiment table in the GUI.

        Parameters
        ----------
        experiment : Experiment.Experiment
            Experiment to be set up.
        """
        self.experiment = experiment

        if self.experiment.default_row.maxlen != Experiment.Experiment().default_row.maxlen:
            self.experiment.default_row = Experiment.Experiment().default_row.copy()
            temp = self.experiment.trials.copy()
            self.experiment.trials = self.experiment.default_row.copy()
            for row in temp:
                self.experiment.trials.append(row)

        self.experiment_control = ExperimentControl.ExperimentController(self)

        self.model = GuiModels.TableModel(['Animal ID', 'Time Stamp', 'Schedule Idx', 'Trial Idx', 'Odour', 'Delay', 'Rewarded',
                                           'Wait Response', 'Response', 'Correct', 'Timeout', 'Number of Licks'],
                                          self.experiment.trials, parent=self)

        self.trialView.setModel(self.model)

        try:
            self.startButton.disconnect()
            self.stopButton.disconnect()
        except:
            pass
        self.startButton.clicked.connect(self.experiment_control.start)
        self.stopButton.clicked.connect(self.experiment_control.stop)

        self.hardware_window.new_pref.connect(
            self.experiment_control.update_pref)

        self.experiment_control.trial_job.trial_end.connect(
            self.update_trial_view)
        self.experiment_control.trial_job.trial_end.connect(
            self.update_data_view)
        self.experiment_control.trial_job.trial_end.connect(
            self.status_changed)

        self.trialView.selectionModel().selectionChanged.connect(self.on_trial_selected)

    def load_config_data(self):
        """Load hardware configuration data. Load files from path defined in config_path.

        Returns
        -------
        hardware_configs : dict
            Hardware configurations saved in hardware.config
        """
        hardware_config_path = self.config_path+"/hardware.config"
        if os.path.exists(hardware_config_path):
            with open(hardware_config_path, 'rb') as fn:
                return pickle.load(fn)
        else:
            return None

    def load_message_folder_path(self):
        """Load message folder path saved in messageFolder.txt to message_folder_path_file variable.

        Returns
        -------
        message_folder_path_file : str
            Path to message folder path file for messages to be written.
        """
        message_folder_path_file = self.config_path+"/messageFolder.txt"
        if os.path.exists(message_folder_path_file):
            with open(message_folder_path_file, 'r') as fn:
                return fn.readline().strip("\n")
        else:
            return None

    def open_animal_window(self):
        """Open animal window."""
        self.animal_window = AppWindows.AnimalWindow(self)
        self.animal_window.changed.connect(self.status_changed)
        self.animal_window.show()

    def open_hardware_window(self):
        """Open hardware window."""
        self.hardware_window.show()

    def open_control_window(self):
        """Open control window."""
        self.control_window = AppWindows.ControlWindow(
            self.experiment, parent=self)
        self.control_window.show()

    def open_mail_window(self):
        """Open mail window. E-Mailing is deprecated and not implemented 
        in current version. Open message box notifying about deprecation
        notice instead.
        """
        QtWidgets.QMessageBox(self, "Deprecation Notice",
                              "E-Mailing function is deprecated\nand not implemented in current version.")
        # Implementation of open_mail_window are commented out below
        # for archive purpose, in case there is a need to have
        # e-mailing implementation again
        #
        # region [mailWindow]
        # self.mail_window = AppWindows.MailWindow(self)
        # self.mail_window.show()
        # endregion

    def open_analysis_window(self):
        """Open analysis window."""
        self.analysis_window = AppWindows.AnalysisWindow(
            self.experiment, parent=self)
        self.analysis_window.show()

    def open_sensor_viewer(self):
        """Open sensor viewer window."""
        self.sensors_window = AppWindows.SensorsWindow(parent=self)
        self.sensors_window.show()
        
    def update_trial_view(self):
        """Update graph view of the trial if a trial is executed."""
        self.model.layoutChanged.emit()

    def update_data_view(self):
        """Update data view of the trial."""
        self.dataLView.plotItem.clear()
        self.dataRView.plotItem.clear()
        self.dataLView.plotItem.plot(np.arange(len(self.experiment.last_data_l)) / self.hardware_prefs['samp_rate'],
                                     np.array(self.experiment.last_data_l))
        self.dataRView.plotItem.plot(np.arange(len(self.experiment.last_data_r)) / self.hardware_prefs['samp_rate'],
                                     np.array(self.experiment.last_data_r))
        self.dataLView.setYRange(0, 6)
        self.dataRView.setYRange(0, 6)

    def update_graphics_view(self, trial : int):
        """Update graph view to the odour signal of the selected trial.

        Parameters
        ----------
        trial : int
            Trial index to be viewed.
        """
        animal = self.experiment.trials[trial][0]
        sched_idx = self.experiment.trials[trial][2]
        trial_idx = self.experiment.trials[trial][3]

        try:
            trial_data = self.experiment.animal_list[animal].schedule_list[sched_idx].trial_params[trial_idx]

            pulses, t = PulseInterface.make_pulse(
                self.hardware_prefs['samp_rate'], 0.0, 0.0, trial_data)

            onset = np.zeros(
                int(self.hardware_prefs['fv_delay']*self.hardware_prefs['samp_rate']))
            offset = np.zeros(int(
                (self.hardware_prefs['lick_delay']+self.hardware_prefs['thorax_delay'])*self.hardware_prefs['samp_rate']))
            t = np.arange(len(onset)+len(offset)+len(t)) / \
                self.hardware_prefs['samp_rate']

            self.graphicsView.plotItem.clear()
            for p, pulse in enumerate(pulses):
                self.graphicsView.plotItem.plot(t, np.hstack(
                    (onset, np.array(pulse), offset)) - (p * 1.1))
        except:
            pass

    def on_trial_selected(self):
        """Update trial if trial is selected."""
        try:
            selected_trial = self.trialView.selectionModel().selectedRows()[
                0].row()
        except:
            selected_trial = 0
        self.update_graphics_view(selected_trial)

    def update_experiment_info(self):
        """Update experiment labels in the GUI."""
        self.experimentNameLabel.setText(self.experiment.name)
        self.experimentDateLabel.setText(self.experiment.date)
        self.savePathLabel.setText(self.experiment.save_path)

    def save_experiment(self):
        """Save experiment."""
        try:
            # bit messy, what if the experiment class changes, should rather be saving the data in the class
            fname, suff = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save Experiment", '', "NoSeMaze Experiment (*.nosemaze)")
            tmpName = os.path.basename(fname)
            tmpSavePath = os.path.dirname(fname)
            self.experiment.name = tmpName
            self.experiment.save_path = tmpSavePath

            # We don't change the original date of creation
            if self.experiment.date is None:
                self.experiment.date = str(datetime.datetime.now())

            logs_path = os.path.dirname(
                fname) + '/Logs/logs_' + self.experiment.name.split(".")[0]
            self.experiment.logs_path = logs_path

            # check if there is still old format of logs dir
            i = 1
            if os.path.isdir(logs_path + '(' + str(i) + ')'):
                while os.path.isdir(logs_path + '(' + str(i+1) + ')'):
                    self.experiment.logs_path = logs_path + '('+str(i)+')'
                    i += 1

            # create dir if not created
            if not os.path.isdir(self.experiment.logs_path):
                os.makedirs(self.experiment.logs_path)

            self.update_experiment_info()

            with open(fname, 'wb') as fn:
                pickle.dump(self.experiment, fn)

            self.saved.emit()
        except:
            print('were not saved...')

    def set_message_folder_path(self):
        """Set message folder path in which the deadman-switch, warning and error messages to be saved."""
        message_folder_path = self.load_message_folder_path()

        try:
            dirname = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                 "Set message folder path",
                                                                 message_folder_path,
                                                                 QtWidgets.QFileDialog.Option.ShowDirsOnly)
            self.message_folder_path = dirname

            message_folder_path_file = self.config_path+"/messageFolder.txt"
            email.message_folder_path = dirname

            if dirname != '':
                with open(message_folder_path_file, 'w') as fn:
                    fn.write(dirname+"\n")
        except:
            print("were not saved...")

    def experiment_saved(self):
        """Changing status and name of window if experiment is saved."""
        self.saved_status = True
        self.setWindowTitle('NoSeMaze')

    def status_changed(self):
        """Changing status and name of window if a trial is executed."""
        self.saved_status = False
        self.setWindowTitle('NoSeMaze*')

    def load_experiment(self):
        """Load experiment."""
        try:
            fname, suff = QtWidgets.QFileDialog.getOpenFileName(
                self, "Open Experiment", '', "NoSeMaze Experiment (*.nosemaze)")

            if fname != '':
                with open(fname, 'rb') as fn:
                    experiment = pickle.load(fn)

                self.setup_experiment_bindings(experiment)
                self.update_experiment_info()
                self.update_trial_view()
        except:
            QtWidgets.QMessageBox.about(self, "Error", "Cannot load data")

    def open_user_guide(self):
        """Open User Guide. If user guide is not locally available, 
        open user guide in Github
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

        # Relative path to doc file.
        docsPath = "Documentation/Guides/userGuide.pdf"
        dPath = "../" + docsPath
        # If file not found, assuming current working directory is NoSeMazeControl
        if not _open_file_in(dPath):
            dPath = "./" + docsPath
            # If file not found, assuming current working directory is NoSeMaze
            if not _open_file_in(dPath):
                webbrowser.open(
                    "https://github.com/KelschLAB/NoSeMaze/blob/master/Documentation/Guides/userGuide.md#nosemazecontrol")

    def show_about(self):
        """Show the *about* message."""

        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setTextFormat(QtCore.Qt.TextFormat.RichText)
        msgBox.setWindowTitle("About")
        msgBox.setText(
            "<html><strong style=\"font-size:18px\">NoSeMaze Controller v1.0</strong>")
        infText = ("<html><em style=\"font-size:14px\">NoSeMaze Controller</em> is part of <em>NoSeMaze</em>." +
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

    def thread_control(self):
        """Stop experiment control thread."""
        self.experiment_control.stop()

    def windows_control(self):
        """Check if any window is opened, then close it."""
        if self.animal_window is not None:
            self.animal_window.close()
        if self.analysis_window is not None:
            self.analysis_window.close()
        if self.hardware_window is not None:
            self.hardware_window.close()
        if self.mail_window is not None:
            self.mail_window.close()
        if self.control_window is not None:
            self.control_window.close()

    def closeEvent(self, event : QtCore.QEvent):
        """Things to be executed if closeEvent occured (x in main window is clicked).
        
        Parameters
        ----------
        event : instance of QCloseEvent
            Events with close event information sent to the window.
        """
        if self.saved_status == False:
            answer = QtWidgets.QMessageBox.question(self, "Warning", "Data has not been saved.\nSave changes?", QtWidgets.QMessageBox.Yes |
                                                    QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)
            if answer == QtWidgets.QMessageBox.No:
                self.windows_control()
                self.saved_status = True
                self.thread_control()
                event.accept()
            elif answer == QtWidgets.QMessageBox.Yes:
                self.save_experiment()
                self.windows_control()
                if self.saved_status:
                    self.thread_control()
                    event.accept()
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            self.windows_control()
            self.thread_control()
            event.accept()


# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    """Custom exception hook.

    Parameters
    ----------
    exctype : type of BaseException
        Type of exception.
    value : BaseException
        Exception occured.
    traceback : TracebackType
        Traceback up to the exception.
    """
    email.crash_error(exctype, value, traceback)
    
    # Print the error and traceback
    # test = "".join(traceback.format_exception(exctype,value,traceback))
    # print(test)
    
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


def main():
    """Main method to be called."""
    app = QtWidgets.QApplication(sys.argv)
    form = MainApp()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
