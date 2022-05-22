# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/HardwareWindowEdited.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget: QtWidgets.QWidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout(
            self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.samplingRateEdit: QtWidgets.QLineEdit = QtWidgets.QLineEdit(
            self.centralwidget)
        self.samplingRateEdit.setObjectName("samplingRateEdit")
        self.gridLayout.addWidget(self.samplingRateEdit, 7, 1, 1, 1)
        self.label_5: QtWidgets.QLabel = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.fvOutputEdit: QtWidgets.QLineEdit = QtWidgets.QLineEdit(
            self.centralwidget)
        self.fvOutputEdit.setObjectName("fvOutputEdit")
        self.gridLayout.addWidget(self.fvOutputEdit, 2, 1, 1, 1)
        self.label_14: QtWidgets.QLabel = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 2, 0, 1, 1)
        self.usbBox: QtWidgets.QCheckBox = QtWidgets.QCheckBox(
            self.centralwidget)
        self.usbBox.setChecked(True)
        self.usbBox.setObjectName("usbBox")
        self.gridLayout.addWidget(self.usbBox, 2, 3, 1, 2)
        self.label_3: QtWidgets.QLabel = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.syncClockEdit: QtWidgets.QLineEdit = QtWidgets.QLineEdit(
            self.centralwidget)
        self.syncClockEdit.setObjectName("syncClockEdit")
        self.gridLayout.addWidget(self.syncClockEdit, 6, 1, 1, 1)
        self.label_7: QtWidgets.QLabel = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 7, 0, 1, 1)
        self.label_6: QtWidgets.QLabel = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 8, 0, 1, 1)
        self.analogChannelsSpin: QtWidgets.QSpinBox = QtWidgets.QSpinBox(
            self.centralwidget)
        self.analogChannelsSpin.setMinimum(1)
        self.analogChannelsSpin.setMaximum(10)
        self.analogChannelsSpin.setProperty("value", 4)
        self.analogChannelsSpin.setObjectName("analogChannelsSpin")
        self.gridLayout.addWidget(self.analogChannelsSpin, 0, 4, 1, 1)
        self.label_2: QtWidgets.QLabel = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 3, 1, 1)
        self.label: QtWidgets.QLabel = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_8: QtWidgets.QLabel = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 11, 0, 1, 1)
        self.label_4: QtWidgets.QLabel = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 3, 1, 1)
        self.rewardOutputEdit: QtWidgets.QLineEdit = QtWidgets.QLineEdit(
            self.centralwidget)
        self.rewardOutputEdit.setObjectName("rewardOutputEdit")
        self.gridLayout.addWidget(self.rewardOutputEdit, 4, 1, 1, 1)
        self.label_11: QtWidgets.QLabel = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 4, 0, 1, 1)
        self.lickChannelSpin: QtWidgets.QSpinBox = QtWidgets.QSpinBox(
            self.centralwidget)
        self.lickChannelSpin.setMaximum(31)
        self.lickChannelSpin.setProperty("value", 1)
        self.lickChannelSpin.setObjectName("lickChannelSpin")
        self.gridLayout.addWidget(self.lickChannelSpin, 11, 1, 1, 1)
        self.odourOutputEdit: QtWidgets.QLineEdit = QtWidgets.QLineEdit(
            self.centralwidget)
        self.odourOutputEdit.setObjectName("odourOutputEdit")
        self.gridLayout.addWidget(self.odourOutputEdit, 1, 1, 1, 1)
        self.rfidPortEdit: QtWidgets.QLineEdit = QtWidgets.QLineEdit(
            self.centralwidget)
        self.rfidPortEdit.setObjectName("rfidPortEdit")
        self.gridLayout.addWidget(self.rfidPortEdit, 8, 1, 1, 1)
        spacerItem: QtWidgets.QSpacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.analogInputEdit: QtWidgets.QLineEdit = QtWidgets.QLineEdit(
            self.centralwidget)
        self.analogInputEdit.setObjectName("analogInputEdit")
        self.gridLayout.addWidget(self.analogInputEdit, 0, 1, 1, 1)
        self.label_10: QtWidgets.QLabel = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 13, 0, 1, 1)
        self.label_9: QtWidgets.QLabel = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 14, 0, 1, 1)
        self.beamChannelSpin: QtWidgets.QSpinBox = QtWidgets.QSpinBox(
            self.centralwidget)
        self.beamChannelSpin.setMaximum(31)
        self.beamChannelSpin.setProperty("value", 0)
        self.beamChannelSpin.setObjectName("beamChannelSpin")
        self.gridLayout.addWidget(self.beamChannelSpin, 13, 1, 1, 1)
        self.odourChannelsSpin: QtWidgets.QSpinBox = QtWidgets.QSpinBox(
            self.centralwidget)
        self.odourChannelsSpin.setMinimum(1)
        self.odourChannelsSpin.setMaximum(32)
        self.odourChannelsSpin.setProperty("value", 8)
        self.odourChannelsSpin.setObjectName("odourChannelsSpin")
        self.gridLayout.addWidget(self.odourChannelsSpin, 1, 4, 1, 1)
        self.timeoutEdit: QtWidgets.QLineEdit = QtWidgets.QLineEdit(
            self.centralwidget)
        self.timeoutEdit.setObjectName("timeoutEdit")
        self.gridLayout.addWidget(self.timeoutEdit, 14, 1, 1, 1)
        self.line: QtWidgets.QFrame = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 10, 0, 1, 5)
        self.fvDelayEdit: QtWidgets.QLineEdit = QtWidgets.QLineEdit(
            self.centralwidget)
        self.fvDelayEdit.setObjectName("fvDelayEdit")
        self.gridLayout.addWidget(self.fvDelayEdit, 9, 1, 1, 1)
        self.label_12: QtWidgets.QLabel = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 9, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar: QtWidgets.QMenuBar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile: QtWidgets.QMenu = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar: QtWidgets.QStatusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave_Preferences: QtWidgets.QAction = QtWidgets.QAction(
            MainWindow)
        self.actionSave_Preferences.setObjectName("actionSave_Preferences")
        self.menuFile.addAction(self.actionSave_Preferences)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Hardware Preferences"))
        self.samplingRateEdit.setText(_translate("MainWindow", "1000"))
        self.label_5.setText(_translate("MainWindow", "Synchronisation Clock"))
        self.fvOutputEdit.setText(_translate("MainWindow", "Dev1/port2/line0"))
        self.label_14.setText(_translate(
            "MainWindow", "Final Valve Output Device"))
        self.usbBox.setToolTip(_translate(
            "MainWindow", "<html><head/><body><p>Set to check if using NI USB 6216 (BNC)</p></body></html>"))
        self.usbBox.setText(_translate("MainWindow", "NI USB 6216 (BNC)"))
        self.label_3.setText(_translate("MainWindow", "Odour Output Device"))
        self.syncClockEdit.setText(_translate(
            "MainWindow", "/Dev1/ai/SampleClock"))
        self.label_7.setText(_translate("MainWindow", "Sampling Rate"))
        self.label_6.setText(_translate("MainWindow", "RFID Port"))
        self.label_2.setText(_translate("MainWindow", "Analog Input Channels"))
        self.label.setText(_translate("MainWindow", "Analog Input Device"))
        self.label_8.setText(_translate("MainWindow", "Lick Channel"))
        self.label_4.setText(_translate("MainWindow", "Odour Output Channels"))
        self.rewardOutputEdit.setText(
            _translate("MainWindow", "Dev1/port2/line1"))
        self.label_11.setText(_translate("MainWindow", "Reward Output Device"))
        self.odourOutputEdit.setText(_translate(
            "MainWindow", "Dev1/port0/line0:7"))
        self.rfidPortEdit.setText(_translate("MainWindow", "COM2"))
        self.analogInputEdit.setText(_translate("MainWindow", "Dev1/ai0:3"))
        self.label_10.setText(_translate("MainWindow", "Beam Channel"))
        self.label_9.setText(_translate("MainWindow", "Timeout (s)"))
        self.timeoutEdit.setText(_translate("MainWindow", "6"))
        self.fvDelayEdit.setText(_translate("MainWindow", "1.0"))
        self.label_12.setToolTip(_translate(
            "MainWindow", "<html><head/><body><p>delay before final valve is activated</p></body></html>"))
        self.label_12.setText(_translate(
            "MainWindow", "Final Valve Delay (s)"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSave_Preferences.setText(
            _translate("MainWindow", "Save Preferences"))
