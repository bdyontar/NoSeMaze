# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 08:13:09 2021

@author: jir
"""
import serial
import serial.tools.list_ports as s_ports
import time
import sys

timing_dbg = False

if timing_dbg:        
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1)

class sensornode:
    """Class to represent a sensornode. 
    Contains methods to communicate and request measurements from the node
    """
    def __init__(self, SNid : int):
        """Search for esp devices connected to the COM port.
        Check if their ID matches the saved ID and open a serial connection

        Args:
            SNid (int): _description_
        """
        self.start_ns = time.perf_counter_ns()
        self.start_ms = time.time()*1000 
        
        self.open_serial(SNid)
        
    def __del__(self):
        """Close the serial connection
        """
        try:
            self.ser.close() #close serial connection before instance is destroyed
        except:
            pass #nothing to do here. Either serial connection does not exist or is already closed
    
    def __sendCommand(self, send_buf : str):
        """Send a command to the node via serial interface

        Args:
            send_buf (str): message to send
        """
        self.ser.reset_input_buffer()
        self.ser.write(send_buf.encode())
        self.ser.flush()
        
    def __getValue(self) -> str:
        """Get the current serial message per line

        Returns:
            str: serial message
        """
        tmp = self.ser.readline().decode()

        return tmp

    def __getID(self, port : str) -> int:
        """get the ID of the sensor node connected to the port

        Args:
            port (str): COM port 

        Returns:
            int: sensornode ID
        """
        try:
            self.ser = serial.Serial(port, 115200, timeout = 5)
            time.sleep(3)
            if timing_dbg:
                tic = time.perf_counter_ns()
            self.__sendCommand("GetID\n")

            try:
                tmp_id = int(self.__getValue(), 16)
            except ValueError:
                tmp_id = -1
                
            if timing_dbg:
                toc = time.perf_counter_ns()
                print("Elapsed time GetID serial connection: {:.2f} ms".format((toc-tic)/1000000))
            self.ser.close()
        except serial.SerialException: #something went wrong maybe a Silicon Lab Bridge not used as SensorNode was present. Capture the exception
            try: #try to close serial connection. This might raise an exception if serial connection was never instanciated (e.g. if connection was already in use)
                if(self.ser.closed == False):
                    self.ser.close()
            except:
                pass # nothing to do, if serial connection does not exist
            tmp_id = -1 #return invalid id
        return tmp_id
    
    #%% public functions
    def getMeasurement(self) -> dict:
        """returns a measurement dictionary with the last measurement values

        Returns:
            dict: dictionary with sensor data and timestamps
        """
        res = dict()
        self.__sendCommand("MO\n")
        tmp = self.__getValue()
        i = 0
        while(tmp == ''):
            if(i > self.retries):
                print("SNID 0x{:02X}: getMeasurement failed! No new data this time.".format(self.id))
                tmp = "0;0;0;0;0;0;0;0;0;0;0;0;0;0\n" #create dummy message without new data
                #restart serial connection
                self.ser.close()
                self.ser = serial.Serial(self.port, 115200, timeout = 5)
                time.sleep(3)
                break
            i += 1
            print("Retry {:d}".format(i))
            self.__sendCommand('MO\n')
            tmp = self.__getValue()
            
        timestamp_os = self.start_ms + (time.perf_counter_ns() - self.start_ns)/1000000
        
        #0x003b236a;0x003b204a;0x00d3;0x00000000;0x0000;0x0000;0x00000000;0x00000000;0x00000000;0x0000;0x00000000;0x0000;0x0000;0x0000
        split_str = tmp.split(';')
        
        t0 = int(split_str[0], 16)
        res["timestamp"] = timestamp_os
        
        if(int(split_str[1], 16) != 0):
            tmp =  timestamp_os + (t0 - int(split_str[1], 16))
        else:
            tmp = -1
        res["apds"] = {"timestamp" : tmp,
                        "als": int(split_str[2], 16)}
        
        if(int(split_str[3], 16) != 0):
            tmp =  timestamp_os + (t0 - int(split_str[3], 16))
        else:
            tmp = -1
        res["spg"]= {"timestamp" : tmp,
                    "voc_raw" : int(split_str[4], 16),
                    "voc_index": int(split_str[5], 16)}
        
        if(int(split_str[6], 16) != 0):
            tmp =  timestamp_os + (t0 - int(split_str[6], 16))
        else:
            tmp = -1
        res["microphone"]= {"timestamp" : tmp,
                            "sound" : int(split_str[7], 16)}
        
        if(int(split_str[8], 16) != 0):
            tmp =  timestamp_os + (t0 - int(split_str[8], 16))
        else:
            tmp = -1
        res["mics"]= {"timestamp" : tmp,
                    "nh3" : int(split_str[9], 16)}
        
        if(int(split_str[10], 16) != 0):
            tmp =  timestamp_os + (t0 - int(split_str[10], 16))
        else:
            tmp = -1
        res["scd41"]= {"timestamp" : tmp,
                       "co2" : int(split_str[11], 16),
                       "temp" : (int(split_str[12], 16)/2**16)*175 - 45,
                        "rh":  ((int(split_str[13], 16))/2**16)*100}
        return res
        
        
    def open_serial(self, SNid):
        """Method to check for esp devices and opening of a serial port
        Used to reopen serial communication in case a node is disconnected and not found

        Args:
            SNid (_type_): ID of sensornode
        """
        ports = list(s_ports.comports())
        esp_list = list()
        self.id = -1
        for p in ports:
            if "Silicon Labs" in p.description:
                esp_list.append(p)
    
        for esp in esp_list:
            tmp_id = self.__getID(esp.device)
            if(tmp_id == SNid):
                working_port = esp.device
                self.id = tmp_id
                print("Sensor Node with ID 0x{:02X} found on {:s}".format(self.id, working_port))
        
        if(self.id == -1):
            print("Sensor Node with ID 0x{:02X} not found! Check connections and make sure no other applications blocks the Sensor Node!".format(SNid))
            self.InstanceExists = False
            return
        
        print("Opening " + working_port)

        self.ser = serial.Serial(working_port, 115200, timeout = 0.5)
        time.sleep(3)
        self.port = working_port
        self.InstanceExists = True
        self.calib_timeout = 60

        self.retries = 5
        self.pause = 0.1

    def close(self):
        try:
            self.ser.close() #close serial connection before instance is destroyed
        except:
            pass #nothing to do here. Either serial connection does not exist or is already closed
        

    