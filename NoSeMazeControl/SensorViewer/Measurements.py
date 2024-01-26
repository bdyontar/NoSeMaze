import csv
import time
from SensorViewer import constants
import os
import threading
from queue import Queue
import pandas as pd
import random

from pathlib import Path

from SensorViewer.SensorNode import sensornode as SensorNode


meas_samples = Queue(16)


class MeasObj:
    def __init__(self):
        t = time.localtime()
        self.timestamp = time.strftime("%y%m%d_%H%M", t)

        self.SensorNodes = []
        for SNId in constants.SNIds:
            self.SensorNodes.append((SNId, SensorNode(SNId)))
            path_name = Path.cwd() / constants.outputfolder / "SNID_{:02X}".format(SNId)
            if not path_name.exists():
                path_name.mkdir(parents=True)

                for file in constants.files:
                    filename = path_name / f"{file[0]}.csv"
                    with open(filename, "w", newline="") as csvfile:
                        output = csv.writer(
                            csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
                        )
                        output.writerow(file[1])

    @staticmethod
    def write_csv_row_to_file(file_path, csv_row):
        try:
            with open(file_path, "a", newline="") as csvfile:
                output = csv.writer(
                    csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
                )
                output.writerow(csv_row)
        except FileNotFoundError:
            print("csv not found")

    def meas_loop(self):
        results_list = list()
        for i, SN in enumerate(self.SensorNodes):

            try:    
                #res = SN[1].getMeasurement()
                z = random.randint(1, 100)
                z2 = random.randint(-1, 2)

                res= {'timestamp': 2, 'apds': {'timestamp': 1705406821874.3547, 'als': z}, 
                      'spg': {'timestamp': z2, 'voc_raw': z, 'voc_index': z}, 'microphone': {'timestamp': 2, 'sound': z}, 
                      'mics': {'timestamp': z2, 'nh3': z}, 'scd41': {'timestamp': z2, 'co2': z, 'temp': z, 'rh': z}}              
                               

            except:
                print("Port to SNId {:02X} not open".format(SN[0]))
                SN[1].reset_node(SN[0])
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


