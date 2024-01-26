# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_design.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1202, 858)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.bu_stop = QtWidgets.QPushButton(self.centralwidget)
        self.bu_stop.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bu_stop.sizePolicy().hasHeightForWidth())
        self.bu_stop.setSizePolicy(sizePolicy)
        self.bu_stop.setMinimumSize(QtCore.QSize(200, 30))
        self.bu_stop.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bu_stop.setFont(font)
        self.bu_stop.setStyleSheet("background-color: rgb(255, 155, 155);\n"
"border-radius: 5px;\n"
"")
        self.bu_stop.setObjectName("bu_stop")
        self.gridLayout.addWidget(self.bu_stop, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.bu_start = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bu_start.sizePolicy().hasHeightForWidth())
        self.bu_start.setSizePolicy(sizePolicy)
        self.bu_start.setMinimumSize(QtCore.QSize(200, 30))
        self.bu_start.setMaximumSize(QtCore.QSize(200, 16777215))
        self.bu_start.setBaseSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.bu_start.setFont(font)
        self.bu_start.setStyleSheet("background-color: rgb(155, 255, 175);\n"
"border-radius: 5px;\n"
"\n"
"")
        self.bu_start.setObjectName("bu_start")
        self.gridLayout.addWidget(self.bu_start, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setContentsMargins(40, -1, -1, -1)
        self.formLayout.setHorizontalSpacing(30)
        self.formLayout.setVerticalSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.slider_value = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.slider_value.setFont(font)
        self.slider_value.setObjectName("slider_value")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.slider_value)
        self.sensors_slider = QtWidgets.QSlider(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sensors_slider.sizePolicy().hasHeightForWidth())
        self.sensors_slider.setSizePolicy(sizePolicy)
        self.sensors_slider.setMaximumSize(QtCore.QSize(200, 16777215))
        self.sensors_slider.setMinimum(1)
        self.sensors_slider.setMaximum(5)
        self.sensors_slider.setPageStep(1)
        self.sensors_slider.setOrientation(QtCore.Qt.Horizontal)
        self.sensors_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sensors_slider.setTickInterval(1)
        self.sensors_slider.setObjectName("sensors_slider")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.sensors_slider)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label)
        self.gridLayout.addLayout(self.formLayout, 6, 0, 2, 1)
        self.graphicsView = GraphicsLayoutWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setBaseSize(QtCore.QSize(0, -27008))
        self.graphicsView.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 1, 0, 1, 1)
        self.bu_reset = QtWidgets.QPushButton(self.centralwidget)
        self.bu_reset.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bu_reset.sizePolicy().hasHeightForWidth())
        self.bu_reset.setSizePolicy(sizePolicy)
        self.bu_reset.setMaximumSize(QtCore.QSize(300, 25))
        self.bu_reset.setObjectName("bu_reset")
        self.gridLayout.addWidget(self.bu_reset, 4, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sensornode Data"))
        self.bu_stop.setText(_translate("MainWindow", "Stop"))
        self.bu_start.setText(_translate("MainWindow", "Start"))
        self.label_2.setText(_translate("MainWindow", "Sensornode Data Viewer"))
        self.slider_value.setText(_translate("MainWindow", "1"))
        self.label.setText(_translate("MainWindow", "Sensors"))
        self.bu_reset.setText(_translate("MainWindow", "Reset"))
from pyqtgraph import GraphicsLayoutWidget