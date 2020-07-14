# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 16:49:56 2019

@author: Anwender

Synchronising clock of RFID-Readers
"""

from Control import LogController as lc
import serial

def main():
    with serial.Serial("COM2",baudrate=19200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=2) as ser:
        worker = lc.LogWorker()
        worker.synchronise_clock(ser)
        
main()