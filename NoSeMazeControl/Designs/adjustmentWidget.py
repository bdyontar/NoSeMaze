# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/AdjustmentWidget.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(473, 152)
        DockWidget.setFloating(False)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.saturationSlider = QtWidgets.QSlider(self.dockWidgetContents)
        self.saturationSlider.setMinimum(-100)
        self.saturationSlider.setMaximum(100)
        self.saturationSlider.setOrientation(QtCore.Qt.Horizontal)
        self.saturationSlider.setObjectName("saturationSlider")
        self.gridLayout.addWidget(self.saturationSlider, 2, 1, 1, 1)
        self.brightnessSlider = QtWidgets.QSlider(self.dockWidgetContents)
        self.brightnessSlider.setMinimum(-100)
        self.brightnessSlider.setMaximum(100)
        self.brightnessSlider.setOrientation(QtCore.Qt.Horizontal)
        self.brightnessSlider.setObjectName("brightnessSlider")
        self.gridLayout.addWidget(self.brightnessSlider, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.contrastSlider = QtWidgets.QSlider(self.dockWidgetContents)
        self.contrastSlider.setMinimum(-100)
        self.contrastSlider.setMaximum(100)
        self.contrastSlider.setOrientation(QtCore.Qt.Horizontal)
        self.contrastSlider.setObjectName("contrastSlider")
        self.gridLayout.addWidget(self.contrastSlider, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "DockWidget"))
        self.label_2.setText(_translate("DockWidget", "Contrast"))
        self.label_3.setText(_translate("DockWidget", "Brightness"))
        self.label.setText(_translate("DockWidget", "Saturation"))

