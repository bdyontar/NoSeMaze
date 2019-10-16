# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:31:27 2019

@author: jir-mb
"""

from PyQt5 import QtWidgets
from Designs import mailWindow

import os

class MailWindow(QtWidgets.QMainWindow, mailWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.mailingListWidget.setSortingEnabled
        self.mailingListWidget.setSelectionMode(3)
        
        #Get mailing list
        self.fn = os.getcwd() + '\\HelperFunctions\\Email\\mailing_list.txt'
        if os.path.isfile(self.fn):
            with open(self.fn, encoding='utf-8') as f: 
                self.mlist = f.readlines()
                for i,addr in enumerate(self.mlist):
                    self.mlist[i] = addr.strip("\n")
            self.populate_mailing_list(self.mlist)
        else:
            self.mlist=list()
            
        try:
            self.addAddressButton.clicked.connect(self.get_address)
            self.removeAddressButton.clicked.connect(self.remove_address)
        except:
            pass

    def get_address(self):
        text, okPressed = QtWidgets.QInputDialog.getText(self, "Add Address", "Please input the address. For multiple addresses, please separate them with a  \",\"", QtWidgets.QLineEdit.Normal, "")
        
        if okPressed and text is not "":
            text = text.replace(" ","")
            text = text.split(",")
            
            if len(text) > 0:
                i = 0
                for item in text:
                        if '@zi-mannheim.de' in item: 
                            i = i+1
                        if '.' not in item.split("@")[0]: 
                            i = i-1
                if i == len(text):
                    self.add_address(text)
                else:
                    QtWidgets.QMessageBox.about(self.parent,"Error", "Invalid Address")

    def populate_mailing_list(self, mlist):
        self.mailingListWidget.clear()
        self.mailingListWidget.addItems(mlist)
        self.mailingListWidget.sortItems()
        
    def remove_address(self):
        rem_list = self.mailingListWidget.selectedItems()
        # rem_list is QItemList and addr is QItem
        for addr in rem_list: self.mlist.remove(addr.text())
        self.populate_mailing_list(self.mlist)
        self.save(self.mlist)
        
    def add_address(self, new_addrs):
        for addr in new_addrs: 
            if not addr in self.mlist: self.mlist.append(addr)
        self.populate_mailing_list(self.mlist)
        self.save(self.mlist)
        
    def save(self, mlist):
        with open(self.fn,'w') as f:
            for addr in mlist: f.write(addr+'\n')