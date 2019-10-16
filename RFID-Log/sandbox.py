# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 15:27:55 2019

@author: jir-mb
"""

START = '1002'
STOP = '1003'
COMP = 'fe'
NUMBER_OF_RFID_DECODER = 4

import serial
import time
from datetime import date as dt
from datetime import datetime as dtm
from datetime import timedelta as td

def xor_checksum(to_write):
    check = to_write[0]
    for byte in to_write[1:]:
        check = check ^ byte
        
    return check

def ser_command(to, command):
    to_write = bytes.fromhex(''.join([START,COMP,to, command, STOP]))
    checksum = xor_checksum(to_write)
    to_write = b''.join([to_write,bytes.fromhex(format(checksum,'02x'))])
    
    return to_write

log_start = dtm.now()
#connecting to port
print('connecting...')
ser = serial.Serial("COM1",
                    baudrate=19200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=2)
print('connected')

csv_list = list() #saving logs from all decoder in one file

for i in range(NUMBER_OF_RFID_DECODER):
    rfid_add = format(i+1,'02x')
    print('reading decoder nr. '+rfid_add)
    
    #check memory
    to_write = ser_command(rfid_add,'41')
    ser.write(to_write)
    time.sleep(0.002) #waiting for answer from decoder to be written in input buffer
    n_id = int(ser.read(ser.in_waiting)[5:7].hex(), 16)
    
    #get data
    to_write = ser_command(rfid_add,'4d')
    ser.write(to_write)
    print('getting data ...')
    
    time_to_wait = round(n_id*19/19200,3)+0.002
    time.sleep(time_to_wait)
    
    for row in range(n_id):
        read = ser.read(19)
        tag_id = read[6:11].hex().upper()
        second = format(read[11],'02x')
        minute = format(read[12],'02x')
        hour = format(read[13],'02x')
        
        #datetime from decoder
        #day_year = format(read[14],'08b')
        #day = format(int(day_year[2:4],2)*10+int(day_year[4:8],2),'02d')
        #month_week = format(read[15],'08b')
        #month = format(int(month_week[3],2)*10+int(month_week[4:8],2),'02d')
        #timestamp = month+day+'D'+hour+':'+minute+':'+second
        
        #datetime from pc
        date = dt.today().isoformat()
        timestamp = date+'D'+hour+':'+minute+':'+second
        
        timestamp_dtm = dtm.strptime(timestamp,'%Y-%m-%dD%H:%M:%S')
        
        #write only log files with timestamp from 1 hour ago till now
        if timestamp_dtm > (log_start - td(hours=1)):
            csv_list.append(';'.join([timestamp,rfid_add,tag_id]))
    
    #flush input buffer
    ser.reset_input_buffer()
    
    #erase memory - it is better to erase read memory to reduce read time at next cycle
    #to_write = ser_command(rfid_add,'65')
    #ser.write(to_write)
    
#save log file in csv
to_save = '\n'.join(csv_list)
with open('LOG_'+date,'a+',newline='') as f:
    print('saving...')
    f.write(to_save+'\n')
    print('finished saving')