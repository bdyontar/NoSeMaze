# -*- coding: utf-8 -*-
"""
Created on Fri May 17 15:15:58 2019

@author: jir-mb
"""

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self,MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(522,385)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.mailingListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.mailingListWidget.setObjectName("mailingListWidget")
        self.gridLayout.addWidget(self.mailingListWidget, 0, 0, 3, 1)
        self.addAddressButton = QtWidgets.QPushButton(self.centralwidget)
        self.addAddressButton.setObjectName("addAddressButton")
        self.gridLayout.addWidget(self.addAddressButton, 0, 1, 1, 1)
        self.removeAddressButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeAddressButton.setObjectName("removeAddressButton")
        self.gridLayout.addWidget(self.removeAddressButton, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow","Mailing List"))
        self.addAddressButton.setText(_translate("MainWindow", "Add"))
        self.removeAddressButton.setText(_translate("MainWindow", "Remove"))