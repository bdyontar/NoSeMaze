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
import webbrowser
import inspect
from types import NoneType, TracebackType
import numpy as np
import pickle
import traceback
from typing import Type
from PyQt5 import QtWidgets, QtCore
from ScheduleDesigns import mainDesign
from ScheduleModels import Widgets
from ScheduleModels import ScheduleWidgets, ScheduleView
from ScheduleUI import ColorMap
from SchedulePyPulse import PulseInterface
from Exceptions import RewardMapError


class MainApp(QtWidgets.QMainWindow, mainDesign.Ui_MainWindow):
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


def main():
    """The main method to be runned."""

    app = QtWidgets.QApplication(sys.argv)
    form = MainApp()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
