# -*- coding: utf-8 -*-
"""
Created on Mon May  6 17:48:41 2019

@author: jir-mb
"""

import sys
import traceback as tb
from time import sleep

from PyQt5 import QtWidgets
from Designs import mainWindow
from Control import LogController
from AppWindows import AppWindows

class MainApp(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)      
        self.mail_window = None
        self.actionMailing_List.triggered.connect(self.open_mail_window)
#        self.log_control = LogController.LogController(self)
#        self.actionStart.triggered.connect(self.log_control.start)
#        self.actionStop.triggered.connect(self.log_control.stop)
        
        self.start_log_control()
        
    def start_log_control(self):
        self.log_control = LogController.LogController(self)
        sleep(1)
        self.log_control.start()
    
    def open_mail_window(self):
        self.mail_window = AppWindows.MailWindow(self)
        self.mail_window.show()
    
    def closeEvent(self, event):
        answer = QtWidgets.QMessageBox.question(self, "Warning","Terminate logging?", QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            self.log_control.stop()
            sleep(2) #wait for thread to be terminated. #TODO it is not a solution and only a round about way to close the window without crashing  
            if self.mail_window is not None:
                self.mail_window.close()
            event.accept()
        else:
            event.ignore()

sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    exc = ''.join(tb.format_exception(exctype,value,traceback))
    print(exc)
    sys._excepthook()
    sys.exit(1)

sys.excepthook = my_exception_hook

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainApp()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()