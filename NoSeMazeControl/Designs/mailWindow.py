# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/MailWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(522, 385)
        self.centralwidget: QtWidgets.QWidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout(
            self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.addAddressButton: QtWidgets.QPushButton = QtWidgets.QPushButton(
            self.centralwidget)
        self.addAddressButton.setObjectName("addAddressButton")
        self.gridLayout.addWidget(self.addAddressButton, 0, 1, 1, 1)
        self.removeAddressButton: QtWidgets.QPushButton = QtWidgets.QPushButton(
            self.centralwidget)
        self.removeAddressButton.setObjectName("removeAddressButton")
        self.gridLayout.addWidget(self.removeAddressButton, 1, 1, 1, 1)
        self.mailingListWidget: QtWidgets.QListWidget = QtWidgets.QListWidget(
            self.centralwidget)
        self.mailingListWidget.setObjectName("mailingListWidget")
        self.gridLayout.addWidget(self.mailingListWidget, 0, 0, 3, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar: QtWidgets.QMenuBar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 522, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar: QtWidgets.QStatusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mailing List"))
        self.addAddressButton.setText(_translate("MainWindow", "Add"))
        self.removeAddressButton.setText(_translate("MainWindow", "Remove"))
