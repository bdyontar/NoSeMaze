# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ScheduleUI/ValveMapUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(583,250)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.valveValenceTable = QtWidgets.QTableWidget(Form)
        self.valveValenceTable.setColumnCount(3)
        self.valveValenceTable.setObjectName("valveValenceTable")
        self.valveValenceTable.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.valveValenceTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.valveValenceTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.valveValenceTable.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.valveValenceTable.setItem(0, 2, item)
        self.valveValenceTable.horizontalHeader().setVisible(True)
        self.valveValenceTable.horizontalHeader().setCascadingSectionResizes(False)
        self.valveValenceTable.horizontalHeader().setDefaultSectionSize(31)
        self.valveValenceTable.horizontalHeader().setMinimumSectionSize(39)
        self.valveValenceTable.horizontalHeader().setSortIndicatorShown(False)
        self.valveValenceTable.horizontalHeader().setStretchLastSection(False)
        self.valveValenceTable.verticalHeader().setVisible(True)
        self.valveValenceTable.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.valveValenceTable, 4, 0, 1, 2)
        self.valveNumberSelect = QtWidgets.QSpinBox(Form)
        self.valveNumberSelect.setMinimum(1)
        self.valveNumberSelect.setMaximum(3)
        self.valveNumberSelect.setProperty("value", 3)
        self.valveNumberSelect.setObjectName("valveNumberSelect")
        self.gridLayout.addWidget(self.valveNumberSelect, 3, 1, 1, 1)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 2, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Number of Valves"))
        self.label.setText(_translate("Form", "Valve Valence Map"))
        self.valveValenceTable.setToolTip(_translate("Form", "<html><head/><body><p>The number of the column indicates the valve which is used</p></body></html>"))
        item = self.valveValenceTable.verticalHeaderItem(0)
        item.setText(_translate("Form", "Odours"))
        __sortingEnabled = self.valveValenceTable.isSortingEnabled()
        self.valveValenceTable.setSortingEnabled(False)
        item = self.valveValenceTable.item(0, 0)
        item.setText(_translate("Form", "1"))
        item = self.valveValenceTable.item(0, 1)
        item.setText(_translate("Form", "2"))
        item = self.valveValenceTable.item(0, 2)
        item.setText(_translate("Form", "3"))
        self.valveValenceTable.setSortingEnabled(__sortingEnabled)

