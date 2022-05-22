# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'autonomouse-control(BEAST)/UI/ControlWindowGraphicsView.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from pyqtgraph import PlotWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1032, 814)
        self.centralwidget: QtWidgets.QWidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2: QtWidgets.QGridLayout = QtWidgets.QGridLayout(
            self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.cameraTwoBox: QtWidgets.QGroupBox = QtWidgets.QGroupBox(
            self.centralwidget)
        self.cameraTwoBox.setObjectName("cameraTwoBox")
        self.gridLayout_3: QtWidgets.QGridLayout = QtWidgets.QGridLayout(
            self.cameraTwoBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.camTwoView: QtWidgets.QGraphicsView = QtWidgets.QGraphicsView(
            self.cameraTwoBox)
        self.camTwoView.setObjectName("camTwoView")
        self.gridLayout_3.addWidget(self.camTwoView, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.cameraTwoBox, 0, 2, 1, 1)
        self.cameraOneBox: QtWidgets.QGroupBox = QtWidgets.QGroupBox(
            self.centralwidget)
        self.cameraOneBox.setObjectName("cameraOneBox")
        self.gridLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout(
            self.cameraOneBox)
        self.gridLayout.setObjectName("gridLayout")
        self.camOneView: QtWidgets.QGraphicsView = QtWidgets.QGraphicsView(
            self.cameraOneBox)
        self.camOneView.setObjectName("camOneView")
        self.gridLayout.addWidget(self.camOneView, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.cameraOneBox, 0, 1, 1, 1)
        self.licksView: PlotWidget = PlotWidget(self.centralwidget)
        self.licksView.setObjectName("licksView")
        self.gridLayout_2.addWidget(self.licksView, 1, 2, 1, 1)
        spacerItem: QtWidgets.QSpacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 0, 3, 1, 1)
        spacerItem1: QtWidgets.QSpacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.animalListTable: QtWidgets.QTableView = QtWidgets.QTableView(
            self.centralwidget)
        self.animalListTable.setObjectName("animalListTable")
        self.gridLayout_2.addWidget(self.animalListTable, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar: QtWidgets.QMenuBar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1032, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar: QtWidgets.QStatusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Video Control"))
        self.cameraTwoBox.setTitle(_translate("MainWindow", "Camera 2"))
        self.cameraOneBox.setTitle(_translate("MainWindow", "Camera 1"))
