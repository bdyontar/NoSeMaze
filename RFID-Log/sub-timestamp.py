# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 00:09:39 2019

@author: Michael
"""

from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import os
import datetime as dt
import subprocess
import re

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.resize(500,300)
        self.setWindowTitle("Sub-Timestamp")
        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.centralwidget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QGridLayout(self.centralwidget)
        self.groupbox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupboxlayout = QtWidgets.QGridLayout(self.groupbox)
        self.button = QtWidgets.QPushButton("&Create Timestamp", self.centralwidget)
        self.button.setFont(self.font)
        self.label = QtWidgets.QLabel(self.groupbox)
        self.label2 = QtWidgets.QLabel(self.groupbox)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.font.setPointSize(16)
        self.label.setFont(self.font)
        self.label.setText("To create timestamp from video files, \n" +
                           "click the button below\n" +
                           "and choose the video files.\n\n")
        
        self.font.setPointSize(10)
        self.label2.setFont(self.font)
        self.label2.setText("Hint: Start time of the subtitles " +
                            "are deduced from the file names.\n" +
                            "If file names are changed, start time is deduced " + 
                            "from the last modified time.")
        
        
        self.groupboxlayout.addWidget(self.label, 0, 0, 1, 1)
        self.groupboxlayout.addWidget(self.label2, 1, 0, 1, 1)
        
        self.layout.addWidget(self.groupbox, 0, 0, 3, 1)
        self.layout.addWidget(self.button, 4, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        
        self.button.clicked.connect(self.make_timestamp)
        
    def make_timestamp(self):
        filenames, suff = QtWidgets.QFileDialog.getOpenFileNames(self, 
                                     "Select one or more files", 
                                     '', 
                                     "Video (*.avi)")
        
        for path in filenames:
            workdir = os.path.dirname(path)
            fn = os.path.basename(path)
            start_time = None
            modified_time = None
            try:
                datetime = fn.split("_")[-1].split("-")
                date = datetime[:3]
                start_time = datetime[3]
#                print(date)
#                print(start_time[:2])
#                print(start_time[2:4])
#                print(start_time[4:])
            except:
                modified_time = dt.datetime.fromtimestamp(os.path.getmtime(path)) #last modified = end of video
                print("getting start time from metadata instead of filename...")
            process = subprocess.Popen(['ffmpeg',  '-i', path], universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = process.communicate()
            matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()
            total_secs = 60*60*int(matches['hours'])+60*int(matches['minutes'])+int(float(matches['seconds']))
            print("total video length: ", total_secs, " s")
            
            if start_time != None:
                start_time = dt.datetime(year=int(date[0]),month=int(date[1]),day=int(date[2]),hour=int(start_time[:2]),minute=int(start_time[2:4]),second=int(start_time[4:]))
            elif start_time == None and modified_time != None:
                time = dt.timedelta(hours=int(matches['hours']), minutes=int(matches['minutes']), seconds=float(matches['seconds']))
                start_time = modified_time - time
            else:
                QtWidgets.QMessageBox.about(self,"Error","Cannot determine start time")
            
            print("saving to: ",workdir)
            print("converting",fn)
            print("recognised start time: ", start_time)
            
            srt_text = "{index}\r\n{x:02d}:{y:02d}:{z:02d},000 --> {x:02d}:{y:02d}:{z2:02d},000\r\n{datetime}\r\n\r\n"
            message = ""
            
            for i in range(total_secs):
                message = message + srt_text.format(index=i+1, x=i//3600, y=(i%3600)//60, z=i%3600%60, z2=i%3600%60 + 1,datetime=(start_time+dt.timedelta(seconds=i)))
            
            name = workdir + '/' + fn.split(".")[0]+ '.srt'
#            print(name)
            with open(name,"w",newline="") as f:
                f.write(message)
                print("srt file created")

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainApp()
    form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()