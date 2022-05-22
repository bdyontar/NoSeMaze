# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/AnalysisWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from pyqtgraph import PlotWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class RiskWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.gridLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout(self)
        self.groupbox: QtWidgets.QGroupBox = QtWidgets.QGroupBox(self)
        self.groupLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout(
            self.groupbox)
        self.textbox: QtWidgets.QLabel = QtWidgets.QLabel(
            "Not implemented yet.")
        self.groupLayout.addWidget(self.textbox)
        self.gridLayout.addWidget(self.groupbox)


class GNGWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.gridLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.animalPerformanceView: PlotWidget = PlotWidget(self)
        self.animalPerformanceView.setObjectName("animalPerformanceView")
        self.gridLayout.addWidget(self.animalPerformanceView, 0, 0, 1, 1)

        self.groupPerformanceView: PlotWidget = PlotWidget(self)
        self.groupPerformanceView.setObjectName("groupPerformanceView")
        self.gridLayout.addWidget(self.groupPerformanceView, 0, 1, 1, 1)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)

        self.centralwidget: QtWidgets.QWidget = QtWidgets.QWidget(MainWindow)
        self.gridLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout(
            self.centralwidget)

        self.experimentStatsTable: QtWidgets.QTableWidget = QtWidgets.QTableWidget(
            self.centralwidget)
        self.experimentStatsTable.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.experimentStatsTable.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.experimentStatsTable.setObjectName("experimentStatsTable")
        self.experimentStatsTable.setColumnCount(3)
        self.experimentStatsTable.setRowCount(0)
        item: QtWidgets.QTableWidgetItem = QtWidgets.QTableWidgetItem()
        self.experimentStatsTable.setHorizontalHeaderItem(0, item)
        item: QtWidgets.QTableWidgetItem = QtWidgets.QTableWidgetItem()
        self.experimentStatsTable.setHorizontalHeaderItem(1, item)
        item: QtWidgets.QTableWidgetItem = QtWidgets.QTableWidgetItem()
        self.experimentStatsTable.setHorizontalHeaderItem(2, item)
        self.experimentStatsTable.horizontalHeader().setDefaultSectionSize(135)
        self.gridLayout.addWidget(self.experimentStatsTable, 0, 0, 1, 2)

        self.groupBox: QtWidgets.QGroupBox = QtWidgets.QGroupBox(
            self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2: QtWidgets.QGridLayout = QtWidgets.QGridLayout(
            self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.label: QtWidgets.QLabel = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)

        self.binSizeSpin: QtWidgets.QSpinBox = QtWidgets.QSpinBox(
            self.groupBox)
        self.binSizeSpin.setMinimum(1)
        self.binSizeSpin.setMaximum(200)
        self.binSizeSpin.setProperty("value", 20)
        self.binSizeSpin.setObjectName("binSizeSpin")
        self.gridLayout_2.addWidget(self.binSizeSpin, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 2)

        self.tabWidget: QtWidgets.QTabWidget = QtWidgets.QTabWidget(
            self.centralwidget)
        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 2)
        self.gngLWidget: GNGWidget = GNGWidget()
        self.gngRWidget: GNGWidget = GNGWidget()
        self.riskWidget: RiskWidget = RiskWidget()

        MainWindow.setCentralWidget(self.centralwidget)
        self.tabWidget.addTab(self.gngLWidget, "GNG Left")
        self.tabWidget.addTab(self.gngRWidget, "GNG Right")
        self.tabWidget.addTab(self.riskWidget, "Risk")

        self.menubar: QtWidgets.QMenuBar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar: QtWidgets.QStatusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionExport_To_MATLAB: QtWidgets.QAction = QtWidgets.QAction(
            MainWindow)
        self.actionExport_To_MATLAB.setObjectName("actionExport_To_MATLAB")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Experiment Analysis"))
        item = self.experimentStatsTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Animal"))
        item = self.experimentStatsTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Total Trials"))
        item = self.experimentStatsTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Trials in Last 24hrs"))
        self.actionExport_To_MATLAB.setText(
            _translate("MainWindow", "Export To MATLAB"))
        self.groupBox.setTitle(_translate("MainWindow", "Parameters"))
        self.label.setText(_translate("MainWindow", "Bin Size"))
