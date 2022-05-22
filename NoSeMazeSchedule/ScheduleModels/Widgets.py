"""
This module contains the ValveMapWidget, that is used in the UI.
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
from ScheduleDesigns import valveMapDesign

# import for type hinting
from ..scheduleMain import MainApp


class ValveMapWidget(QtWidgets.QWidget, valveMapDesign.Ui_Form):
    """Widget to configure valve map."""
    def __init__(self, parentUi : MainApp = None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.parentUi = parentUi
        self.valveNumberSelect.valueChanged.connect(self.change_valve_map)

    def flatten_value(self, value : int):
        if value < 0:
            return 0
        else:
            return value

    def change_valve_map(self):
        self.valveValenceTable.setColumnCount(
            int(self.valveNumberSelect.value()))

    def get_valence_map(self):
        try:
            vmap = []
            for i in range(self.valveValenceTable.columnCount()):
                vmap.append(int(self.valveValenceTable.item(0, i).text()))
            vmap = list(map(self.flatten_value, vmap))

            return vmap
        except:
            QtWidgets.QMessageBox.about(
                self.parentUi, "Error", "Valence map does not permit NAN value")
