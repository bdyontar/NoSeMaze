# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/AddWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(572, 120)
        MainWindow.setToolTip("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mailEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.mailEdit.setGeometry(QtCore.QRect(10, 40, 451, 22))
        self.mailEdit.setToolTip("")
        self.mailEdit.setText("")
        self.mailEdit.setObjectName("mailEdit")
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(470, 40, 93, 28))
        self.cancelButton.setObjectName("cancelButton")
        self.okButton = QtWidgets.QPushButton(self.centralwidget)
        self.okButton.setGeometry(QtCore.QRect(470, 10, 93, 28))
        self.okButton.setObjectName("okButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 441, 21))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 572, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Add Address"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))
        self.okButton.setText(_translate("MainWindow", "Ok"))
        self.label.setText(_translate("MainWindow", "Please input the address. For multiple addresses separate them with a  \",\""))

