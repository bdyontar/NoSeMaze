# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/ControlWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from pyqtgraph import PlotWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(986, 829)
        self.centralwidget: QtWidgets.QWidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout(
            self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2: QtWidgets.QGroupBox = QtWidgets.QGroupBox(
            self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2: QtWidgets.QGridLayout = QtWidgets.QGridLayout(
            self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.viewfinderTwo = QCameraViewfinder(self.groupBox_2)
        self.viewfinderTwo.setObjectName("viewfinderTwo")
        self.gridLayout_2.addWidget(self.viewfinderTwo, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 2, 2, 1, 1)
        spacerItem: QtWidgets.QSpacerItem = QtWidgets.QSpacerItem(
            480, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.groupBox: QtWidgets.QGroupBox = QtWidgets.QGroupBox(
            self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3: QtWidgets.QGridLayout = QtWidgets.QGridLayout(
            self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.viewfinderOne: QCameraViewfinder = QCameraViewfinder(
            self.groupBox)
        self.viewfinderOne.setObjectName("viewfinderOne")
        self.gridLayout_3.addWidget(self.viewfinderOne, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 2, 1, 1)
        spacerItem1: QtWidgets.QSpacerItem = QtWidgets.QSpacerItem(
            640, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.licksView: PlotWidget = PlotWidget(self.centralwidget)
        self.licksView.setObjectName("licksView")
        self.gridLayout.addWidget(self.licksView, 2, 0, 1, 1)
        self.animalListTable: QtWidgets.QTableView = QtWidgets.QTableView(
            self.centralwidget)
        self.animalListTable.setObjectName("animalListTable")
        self.animalListTable.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.gridLayout.addWidget(self.animalListTable, 0, 0, 1, 1)
        spacerItem2: QtWidgets.QSpacerItem = QtWidgets.QSpacerItem(
            5, 480, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3: QtWidgets.QSpacerItem = QtWidgets.QSpacerItem(
            5, 480, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar: QtWidgets.QMenuBar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 986, 26))
        self.menubar.setObjectName("menubar")
        self.menuSetting: QtWidgets.QMenu = QtWidgets.QMenu(self.menubar)
        self.menuSetting.setObjectName("menuSetting")
        self.menuSet_Cameras: QtWidgets.QMenu = QtWidgets.QMenu(
            self.menuSetting)
        self.menuSet_Cameras.setObjectName("menuSet_Cameras")
        self.menuSet_Resolutions: QtWidgets.QMenu = QtWidgets.QMenu(
            self.menuSetting)
        self.menuSet_Resolutions.setObjectName("menuSet_Resolutions")
        self.menuAdjustment: QtWidgets.QMenu = QtWidgets.QMenu(
            self.menuSetting)
        self.menuAdjustment.setObjectName("menuAdjustment")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar: QtWidgets.QStatusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionCamera_1: QtWidgets.QAction = QtWidgets.QAction(MainWindow)
        self.actionCamera_1.setObjectName("actionCamera_1")
        self.actionCamera_2: QtWidgets.QAction = QtWidgets.QAction(MainWindow)
        self.actionCamera_2.setObjectName("actionCamera_2")
        self.actionRes_Camera_1: QtWidgets.QAction = QtWidgets.QAction(
            MainWindow)
        self.actionRes_Camera_1.setObjectName("actionRes_Camera_1")
        self.actionRes_Camera_2: QtWidgets.QAction = QtWidgets.QAction(
            MainWindow)
        self.actionRes_Camera_2.setObjectName("actionRes_Camera_2")
        self.actionAdj_Camera_1: QtWidgets.QAction = QtWidgets.QAction(
            MainWindow)
        self.actionAdj_Camera_1.setObjectName("actionAdj_Camera_1")
        self.actionAdj_Camera_2: QtWidgets.QAction = QtWidgets.QAction(
            MainWindow)
        self.actionAdj_Camera_2.setObjectName("actionAdj_Camera_2")
        self.menuSet_Cameras.addAction(self.actionCamera_1)
        self.menuSet_Cameras.addAction(self.actionCamera_2)
        self.menuSet_Resolutions.addAction(self.actionRes_Camera_1)
        self.menuSet_Resolutions.addAction(self.actionRes_Camera_2)
        self.menuAdjustment.addAction(self.actionAdj_Camera_1)
        self.menuAdjustment.addAction(self.actionAdj_Camera_2)
        self.menuSetting.addAction(self.menuSet_Cameras.menuAction())
        self.menuSetting.addAction(self.menuSet_Resolutions.menuAction())
        self.menuSetting.addAction(self.menuAdjustment.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Video Control"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Camera 2"))
        self.groupBox.setTitle(_translate("MainWindow", "Camera 1"))
        self.menuSetting.setTitle(_translate("MainWindow", "Setting"))
        self.menuSet_Cameras.setTitle(_translate("MainWindow", "Set Cameras"))
        self.menuSet_Resolutions.setTitle(
            _translate("MainWindow", "Set Resolutions"))
        self.menuAdjustment.setToolTip(_translate(
            "MainWindow", "Adjust Brightness, Contrast and Saturation"))
        self.menuAdjustment.setTitle(_translate("MainWindow", "Adjustment"))
        self.actionCamera_1.setText(_translate("MainWindow", "Camera 1"))
        self.actionCamera_2.setText(_translate("MainWindow", "Camera 2"))
        self.actionRes_Camera_1.setText(
            _translate("MainWindow", "Res Camera 1"))
        self.actionRes_Camera_2.setText(
            _translate("MainWindow", "Res Camera 2"))
        self.actionAdj_Camera_1.setText(
            _translate("MainWindow", "Adj. Camera 1"))
        self.actionAdj_Camera_2.setText(
            _translate("MainWindow", "Adj. Camera 2"))
