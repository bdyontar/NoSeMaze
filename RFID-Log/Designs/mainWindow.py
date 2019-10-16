# -*- coding: utf-8 -*-
"""
Created on Mon May  6 15:29:26 2019

@author: jir-mb
"""

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(600,240)
        self.centralwidget= QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.statusLabel = QtWidgets.QLabel(self.groupBox)
        self.statusLabel.setObjectName("statusLabel")
        self.lastsavedLabel = QtWidgets.QLabel(self.groupBox)
        self.lastsavedLabel.setObjectName("lastsavedLabel")
        self.gridLayout_2.addWidget(self.statusLabel,0,0,1,1)
        self.gridLayout_2.addWidget(self.lastsavedLabel,1,0,1,1)
        self.statusText = QtWidgets.QLabel(self.groupBox)
        self.statusText.setObjectName("statusText")
        self.lastsavedText = QtWidgets.QLabel(self.groupBox)
        self.lastsavedText.setObjectName("lastsavedText")
        self.gridLayout_2.addWidget(self.statusText,0,1,1,1)
        self.gridLayout_2.addWidget(self.lastsavedText,1,1,1,1)
        self.gridLayout.addWidget(self.groupBox,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QtCore.QRect(0,0,600,26))
        self.menuE_Mails = QtWidgets.QMenu(self.menubar)
        self.menuE_Mails.setObjectName("menuE_Mails")
#        self.menuLog = QtWidgets.QMenu(self.menubar)
#        self.menuLog.setObjectName("menuLog")
        MainWindow.setMenuBar(self.menubar)
#        self.actionStart = QtWidgets.QAction(MainWindow)
#        self.actionStart.setObjectName("actionStart")
#        self.actionStop = QtWidgets.QAction(MainWindow)
#        self.actionStop.setObjectName("actionStop")
        self.actionMailing_List = QtWidgets.QAction(MainWindow)
        self.actionMailing_List.setObjectName("actionMailing_List")
        self.menuE_Mails.addAction(self.actionMailing_List)
#        self.menuLog.addAction(self.actionStart)
#        self.menuLog.addAction(self.actionStop)
        self.menubar.addAction(self.menuE_Mails.menuAction())
#        self.menubar.addAction(self.menuLog.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self,MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RFID Logs"))
        self.groupBox.setTitle(_translate("MainWindow", "Status"))
        self.statusLabel.setText(_translate("MainWindow","Status : "))
        self.statusText.setText(_translate("MainWindow","..."))
        self.lastsavedLabel.setText(_translate("MainWindow", "Logs were last saved at : "))
        self.lastsavedText.setText(_translate("MainWindow", "..."))
        self.menuE_Mails.setTitle(_translate("MainWindow", "E-Mails"))
        self.actionMailing_List.setText(_translate("MainWindow","Mailing List"))
#        self.menuLog.setTitle(_translate("MainWindow", "Log"))
#        self.actionStart.setText(_translate("MainWindow","Start Log"))
#        self.actionStop.setText(_translate("MainWindow","Stop Log"))
        