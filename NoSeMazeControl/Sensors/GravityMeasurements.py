"""
This module contains a sensornode measurement object to recieve and save sensor data. 
"""

import csv
import time
from Sensors import constants
import os
import threading
from queue import Queue
import pandas as pd
import serial
from datetime import datetime


from pathlib import Path



class GravitySensor:
    """
    Class to handle measurement reading and saving as csv

    Attributes
    ----------
    timestamp : str
        Current local time as datetime string
    """
    
    def __init__(self):
        """
        Initializes the measurement object with the current time and creates a folder with measurements CSVs for each sensornodes in constants
        Folders are not overwritten if they already exist
        """
        t = time.localtime()
        self.timestamp = time.strftime("%y%m%d_%H%M", t)
        
        file = constants.gravity_file

        # Create a gravity sensor object 
        path_name = Path.cwd() / constants.outputfolder / "gravity_NH3"
        if not path_name.exists():
            path_name.mkdir(parents=True)

            # Create the respective measurement csv files
            filename = path_name / "gravity_nh3.csv"
            try:
                with open(filename, "w", newline="") as csvfile:
                    output = csv.writer(
                        csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
                    )
                    output.writerow(file[1])
            except:
                print("Could not create file")
        
    def recreate_files(self):
        """
        Method the recreate the csv files in case the are deleted
        """
        file = constants.gravity_file

        path_name = Path.cwd() / constants.outputfolder / "gravity_NH3"
        if not path_name.exists():
            path_name.mkdir(parents=True)

            # Create the respective measurement csv files
            filename = path_name / "gravity_nh3.csv"
            try:
                with open(filename, "w", newline="") as csvfile:
                    output = csv.writer(
                        csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
                    )
                    output.writerow(file[1])
            except:
                print("Could not create file")            
                        
                        
    def write_csv_row_to_file(self, file_path: Path, csv_row: list):
        """
        Method to write one row into the csv files

        Parameters
        ----------
        file_path : str
            Path to csv files
        
        csv_row : str
            String to write
        """
        try:
            with open(file_path, "a", newline="") as csvfile:
                output = csv.writer(
                    csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
                )
                output.writerow(csv_row)
        except FileNotFoundError:
            print("Files not found, recreating...")
            self.recreate_files()
        except PermissionError:
            pass


    def meas_loop(self):
        """
        Method to recieve measurements and write them into their respective csv files
        """
        measurement = 0


        # Open the serial port
        try:
            ser = serial.Serial(f"COM{constants.gravity_port}", 115200, timeout=1)
        except serial.serialutil.SerialException:
            print("Could not open port [{}] with gravity sensor".format(constants.gravity_port))

        # Send the command 'measure' followed by a newline character
        try:
            ser.write(b'measure\n')

            # Wait for the measurement
            while True:
                if ser.in_waiting > 0:
                    measurement = float(ser.readline().decode('utf-8').rstrip())
                    timestamp = datetime.now().timestamp()
                    break
        except:
            pass
         
        # Close the serial port   
        try:
            ser.close()   
        except:
            pass         
        
        # Write the measurement data into the csv file
        path_name = Path.cwd() / constants.outputfolder / "gravity_NH3"

        csv_file_paths = {
            "gravity_nh3": path_name / "gravity_nh3.csv",
        }

        try:
            filename = csv_file_paths["gravity_nh3"]
            self.write_csv_row_to_file(filename, [timestamp, measurement])
        except:
            pass
        
        
        return measurement

