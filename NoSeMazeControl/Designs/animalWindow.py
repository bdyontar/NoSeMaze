# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/AnimalWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(829, 600)
        MainWindow.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.centralwidget: QtWidgets.QWidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout(
            self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.scheduleTable: QtWidgets.QTableWidget = QtWidgets.QTableWidget(
            self.centralwidget)
        self.scheduleTable.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.scheduleTable.setObjectName("scheduleTable")
        self.scheduleTable.setColumnCount(3)
        self.scheduleTable.setRowCount(0)
        item: QtWidgets.QTableWidgetItem = QtWidgets.QTableWidgetItem()
        self.scheduleTable.setHorizontalHeaderItem(0, item)
        item: QtWidgets.QTableWidgetItem = QtWidgets.QTableWidgetItem()
        self.scheduleTable.setHorizontalHeaderItem(1, item)
        item: QtWidgets.QTableWidgetItem = QtWidgets.QTableWidgetItem()
        self.scheduleTable.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.scheduleTable, 0, 2, 3, 1)
        self.removeRowButton: QtWidgets.QPushButton = QtWidgets.QPushButton(
            self.centralwidget)
        self.removeRowButton.setObjectName("removeRowButton")
        self.gridLayout.addWidget(self.removeRowButton, 1, 1, 1, 1)
        self.addRowButton: QtWidgets.QPushButton = QtWidgets.QPushButton(
            self.centralwidget)
        self.addRowButton.setObjectName("addRowButton")
        self.gridLayout.addWidget(self.addRowButton, 0, 1, 1, 1)
        self.addScheduleButton: QtWidgets.QPushButton = QtWidgets.QPushButton(
            self.centralwidget)
        self.addScheduleButton.setObjectName("addScheduleButton")
        self.gridLayout.addWidget(self.addScheduleButton, 3, 2, 1, 1)
        self.removeScheduleButton: QtWidgets.QPushButton = QtWidgets.QPushButton(
            self.centralwidget)
        self.removeScheduleButton.setObjectName("removeScheduleButton")
        self.gridLayout.addWidget(self.removeScheduleButton, 4, 2, 1, 1)
        self.animalTable: QtWidgets.QTableWidget = QtWidgets.QTableWidget(
            self.centralwidget)
        self.animalTable.setObjectName("animalTable")
        self.animalTable.setColumnCount(1)
        self.animalTable.setRowCount(0)
        item: QtWidgets.QTableWidgetItem = QtWidgets.QTableWidgetItem()
        self.animalTable.setHorizontalHeaderItem(0, item)
        self.gridLayout.addWidget(self.animalTable, 0, 0, 5, 1)
        self.trialView: QtWidgets.QTableView = QtWidgets.QTableView(
            self.centralwidget)
        self.trialView.setObjectName("trialView")
        self.gridLayout.addWidget(self.trialView, 0, 3, 5, 1)
        spacerItem: QtWidgets.QSpacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 3, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar: QtWidgets.QMenuBar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 829, 26))
        self.menubar.setObjectName("menubar")
        self.menuUpdate_List: QtWidgets.QMenu = QtWidgets.QMenu(self.menubar)
        self.menuUpdate_List.setObjectName("menuUpdate_List")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar: QtWidgets.QStatusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionUpdate: QtWidgets.QAction = QtWidgets.QAction(MainWindow)
        self.actionUpdate.setObjectName("actionUpdate")
        self.menuUpdate_List.addAction(self.actionUpdate)
        self.menubar.addAction(self.menuUpdate_List.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Animal Management"))
        item = self.scheduleTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Schedule Name"))
        item = self.scheduleTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Number of Trials"))
        item = self.scheduleTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Progress (%)"))
        self.removeRowButton.setText(_translate("MainWindow", "-"))
        self.addRowButton.setText(_translate("MainWindow", "+"))
        self.addScheduleButton.setText(
            _translate("MainWindow", "Add Schedule"))
        self.removeScheduleButton.setText(
            _translate("MainWindow", "Remove Schedule"))
        item = self.animalTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        self.menuUpdate_List.setTitle(_translate("MainWindow", "Update List"))
        self.actionUpdate.setText(_translate("MainWindow", "Confirm"))
