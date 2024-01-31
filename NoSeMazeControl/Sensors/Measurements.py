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
import random

from pathlib import Path

from Sensors.SensorNode import sensornode as SensorNode


meas_samples = Queue(16)


class MeasObj:
    """
    Class to handle measurement reading and saving as csv

    Attributes
    ----------
    timestamp : str
        Current local time as datetime string
    
    SensorNodes : list
        List to hold sensornode objects
    
    """
    
    def __init__(self):
        """
        Initializes the measurement object with the current time and creates a folder with measurements CSVs for each sensornodes in constants
        Folders are not overwritten if they already exist
        """
        t = time.localtime()
        self.timestamp = time.strftime("%y%m%d_%H%M", t)

        self.SensorNodes = []
        # Loop over all sensor IDs
        for SNId in constants.SNIds:
            # Create a sensornode object 
            self.SensorNodes.append((SNId, SensorNode(SNId)))
            path_name = Path.cwd() / constants.outputfolder / "SNID_{:02X}".format(SNId)
            if not path_name.exists():
                path_name.mkdir(parents=True)

                # Create the respective measurement csv files
                for file in constants.files:
                    filename = path_name / f"{file[0]}.csv"
                    try:
                        with open(filename, "w", newline="") as csvfile:
                            output = csv.writer(
                                csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
                            )
                            output.writerow(file[1])
                    except:
                        print("Could not create file")
        
    def recreate_files(self):
        for SNId in constants.SNIds:

                    path_name = Path.cwd() / constants.outputfolder / "SNID_{:02X}".format(SNId)
                    if not path_name.exists():
                        path_name.mkdir(parents=True)

                        # Create the respective measurement csv files
                        for file in constants.files:
                            filename = path_name / f"{file[0]}.csv"
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


    def meas_loop(self):
        """
        Method to recieve measurements and write them into their respective csv files

        Attributes
        ----------
        results_list : list
            List containing result dataframes


        Returns
        -------
        meas_samples : Queue 
            Queue containing result lists
        
        """
        results_list = list()
        for i, SN in enumerate(self.SensorNodes):

            # If connection is successful, get measurements
            try:    
                res = SN[1].getMeasurement()
            
            # If connection failed, reset sensornode
            except:
                print("Port to SNId {:02X} not open".format(SN[0]))
                SN[1].open_serial(SN[0])
                continue
                    
            path_name = Path(constants.outputfolder) / f"SNID_{SN[0]:02X}"

            csv_file_paths = {
                "scd41": path_name / f"{constants.scd41_file[0]}.csv",
                "apds": path_name / f"{constants.apds_file[0]}.csv",
                "spg": path_name / f"{constants.spg_file[0]}.csv",
                "microphone": path_name / f"{constants.mp_file[0]}.csv",
                "mics": path_name / f"{constants.mics_file[0]}.csv",
            }

            # SCD41 values
            if res["scd41"]["timestamp"] != -1:  # check if new data is available
                filename = csv_file_paths["scd41"]
                self.write_csv_row_to_file(
                    filename,
                    [
                        res["scd41"]["timestamp"],
                        res["scd41"]["temp"],
                        res["scd41"]["rh"],
                        res["scd41"]["co2"],
                    ],
                )

            # Light sensor
            if res["apds"]["timestamp"] != -1:  # check if new data is available
                filename = csv_file_paths["apds"]
                self.write_csv_row_to_file(
                    filename, [res["apds"]["timestamp"], res["apds"]["als"]]
                )

            # VOC sensor
            if res["spg"]["timestamp"] != -1:  # check if new data is available
                filename = csv_file_paths["spg"]
                self.write_csv_row_to_file(
                    filename,
                    [
                        res["spg"]["timestamp"],
                        res["spg"]["voc_raw"],
                        res["spg"]["voc_index"],
                    ],
                )

            # Microphone
            if res["microphone"]["timestamp"] != -1:  # check if new data is available
                filename = csv_file_paths["microphone"]
                self.write_csv_row_to_file(
                    filename, [res["microphone"]["timestamp"], res["microphone"]["sound"]]
                )

            # NH3
            if res["mics"]["timestamp"] != -1:  # check if new data is available
                filename = csv_file_paths["mics"]
                self.write_csv_row_to_file(
                    filename, [res["mics"]["timestamp"], res["mics"]["nh3"]]
                )
        
            results_list.append(res)

        if not meas_samples.full():
            meas_samples.put(results_list)
            return meas_samples


