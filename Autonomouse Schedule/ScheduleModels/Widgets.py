"""
This module contains the ValveMapWidget, that is used in the UI.
"""

from PyQt5 import QtWidgets
from ScheduleDesigns import valveMapDesign

class ValveMapWidget(QtWidgets.QWidget, valveMapDesign.Ui_Form):
    def __init__(self, parentUi=None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.parentUi = parentUi
        self.valveNumberSelect.valueChanged.connect(self.change_valve_map)
    
    def flatten_value(self, value):
        if value < 0: return 0
        else: return value 
    
    def change_valve_map(self):
        self.valveValenceTable.setColumnCount(int(self.valveNumberSelect.value()))

    def get_valence_map(self):
        try:
            vmap = []
            for i in range(self.valveValenceTable.columnCount()):
                vmap.append(int(self.valveValenceTable.item(0, i).text()))
            vmap = list(map(self.flatten_value, vmap))
            
            return vmap
        except:
            QtWidgets.QMessageBox.about(self.parentUi, "Error", "Valence map does not permit NAN value")