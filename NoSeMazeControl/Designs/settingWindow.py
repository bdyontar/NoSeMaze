# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/SettingWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(607, 415)
        self.centralwidget: QtWidgets.QWidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout(
            self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem: QtWidgets.QSpacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.applyButton: QtWidgets.QPushButton = QtWidgets.QPushButton(
            self.centralwidget)
        self.applyButton.setObjectName("applyButton")
        self.gridLayout.addWidget(self.applyButton, 3, 2, 1, 1)
        self.groupBox: QtWidgets.QGroupBox = QtWidgets.QGroupBox(
            self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(
            self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2: QtWidgets.QLabel = QtWidgets.QLabel(self.groupBox)
        font: QtGui.QFont = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.setCameraBox: QtWidgets.QComboBox = QtWidgets.QComboBox(
            self.groupBox)
        self.setCameraBox.setObjectName("setCameraBox")
        self.verticalLayout.addWidget(self.setCameraBox)
        self.label: QtWidgets.QLabel = QtWidgets.QLabel(self.groupBox)
        font: QtGui.QFont = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.resolutionComboBox: QtWidgets.QComboBox = QtWidgets.QComboBox(
            self.groupBox)
        self.resolutionComboBox.setObjectName("resolutionComboBox")
        self.verticalLayout.addWidget(self.resolutionComboBox)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 4)
        self.cancelButton: QtWidgets.QPushButton = QtWidgets.QPushButton(
            self.centralwidget)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 3, 3, 1, 1)
        self.okButton: QtWidgets.QPushButton = QtWidgets.QPushButton(
            self.centralwidget)
        self.okButton.setObjectName("okButton")
        self.gridLayout.addWidget(self.okButton, 3, 1, 1, 1)
        self.groupBox_2: QtWidgets.QGroupBox = QtWidgets.QGroupBox(
            self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(
            self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4: QtWidgets.QLabel = QtWidgets.QLabel(self.groupBox_2)
        font: QtGui.QFont = QtGui.QFont()
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.setCameraBox_2: QtWidgets.QComboBox = QtWidgets.QComboBox(
            self.groupBox_2)
        self.setCameraBox_2.setObjectName("setCameraBox_2")
        self.verticalLayout_2.addWidget(self.setCameraBox_2)
        self.label_3: QtWidgets.QLabel = QtWidgets.QLabel(self.groupBox_2)
        font: QtGui.QFont = QtGui.QFont()
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.resolutionComboBox_2: QtWidgets.QComboBox = QtWidgets.QComboBox(
            self.groupBox_2)
        self.resolutionComboBox_2.setObjectName("resolutionComboBox_2")
        self.verticalLayout_2.addWidget(self.resolutionComboBox_2)
        self.setCameraBox_2.raise_()
        self.resolutionComboBox_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.groupBox.raise_()
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 4)
        spacerItem1: QtWidgets.QSpacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar: QtWidgets.QMenuBar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 607, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar: QtWidgets.QStatusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Settings"))
        self.applyButton.setText(_translate("MainWindow", "Apply"))
        self.groupBox.setTitle(_translate("MainWindow", "Camera 1"))
        self.label_2.setText(_translate("MainWindow", "Set Camera"))
        self.label.setText(_translate("MainWindow", "Camera Resolution"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))
        self.okButton.setText(_translate("MainWindow", "Ok"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Camera 2"))
        self.label_4.setText(_translate("MainWindow", "Set Camera"))
        self.label_3.setText(_translate("MainWindow", "Camera Resolution"))
