# -*- coding: utf-8 -*-
"""
Created on Mon May  6 17:21:35 2019

@author: jir-mb
"""

#TODO Implement a timeout or a watchdog thread and synchronised it with this thread

START = '1002'
STOP = '1003'
COMP = 'fe'
NUMBER_OF_RFID_DECODER = 4
LENGTH_ANSWER_CHECK_MEMORY = 12-2-2-1 #length of the answer of '41' command, without start code, stop code and checksum
LENGTH_ANSWER_TIMESTAMP = 19-2-2-1 #length of on row of the answer of '4d' command, without start code, stop code, and checksum

from PyQt5 import QtCore
from datetime import date as dt
from datetime import time as tm
from datetime import datetime as dtm
from datetime import timedelta as td
from time import sleep
#if __name__ != "__main__":
#    from HelperFunctions import Email as email
import os
import serial
import serial.tools.list_ports as lstport

class LogWorker(QtCore.QObject):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(None)
        self.parent = parent
        self.log_saved = None
        self.start_time = dtm.now().isoformat()
        self.date = dt.today()
        self.mail_sent = False
        self.error_sent = False
        self.dir_path = "C:\\Users\\Anwender\\Dropbox\\Autonomouse_2\\TubeTestLog\\logs_since_" + ''.join(self.start_time.split(':')[0:2])
        self.exception_num = 0
        self.saved = False
        self.synced = None
        self.should_delete = False
        if not os.path.isdir(self.dir_path):
            os.mkdir(self.dir_path)
        
    def check_comports(self):
        if lstport.comports() != []:
            self.PORT = 'No MOXA'
            for port in lstport.comports():
                if "MOXA" in port[1]:
                    self.PORT = port[0]
        else:
            self.PORT = 'No MOXA'
    
    def xor_checksum(self, to_write):
        check = to_write[0]
        for byte in to_write[1:]:
            check = check ^ byte
            
        return check

    def ser_command(self, to, command):
        to_write = bytes.fromhex(''.join([START,COMP,to,command,STOP]))
        checksum = self.xor_checksum(to_write)
        to_write = b''.join([to_write,bytes.fromhex(format(checksum,'02x'))])
        
        return to_write
    
    #TODO: Problem of synchronising clock if an error occured. Maybe synchronise it manually. Esspecially Clock number 2
    def synchronise_clock(self, ser):
        #synchronise with clock number 1
        now = dtm.now()
        hour = now.strftime('%H')
        minute = now.strftime('%M')
        second = now.strftime('%S')
        year = format(now.year%4,'02b')
        ten_days = format(int(now.day/10),'02b')
        day_unit = format(now.day%10, '04b')
        year_day = format(int(''.join([year,ten_days,day_unit]),2), '02x')
        weekday = format(now.weekday(), '03b')
        ten_months = str(int(now.month/10))
        month_unit = format(now.month%10, '04b')
        weekday_month = format(int(''.join([weekday,ten_months,month_unit]),2),'02x')
        
        time = [second,minute,hour,year_day,weekday_month]
        temp = list()
        for ele in time:
            if ele == '10':
                temp.extend(['10','10'])
            else:
                temp.append(ele)
        time = ''.join(temp)
#        time = ''.join([second,minute,hour,year_day,weekday_month])
        data_without_tags = bytes.fromhex(time)
#        rfid_add = format(1,'02x')
#        to_write = self.ser_command(rfid_add, '44')
#        ser.reset_input_buffer()
#        sleep(1)
#        ser.write(to_write)
#        sleep(0.2)
#        
#        while True:
#            if ser.in_waiting != 0:
#                all_data = ser.read_until(bytes.fromhex(STOP))
#                print(all_data)
#                check_sum = ser.read(1)
#                if self.xor_checksum(all_data) == check_sum[0]:
#                    data_without_tags = bytes.fromhex(time)+all_data[8:-2]
#                    print(data_without_tags)
#                break
                
        for i in range(NUMBER_OF_RFID_DECODER):
            rfid_add = format(i+1,'02x')
            to_write = b''.join([bytes.fromhex(''.join([START,COMP,rfid_add,'64'])),data_without_tags,bytes.fromhex(STOP)])
            check = to_write[0]
            for byte in to_write[1:]:
                check = check^byte
            to_write = b''.join([to_write,bytes.fromhex(format(check,'02x'))])
            print(to_write)
            ser.write(to_write)
            sleep(0.2)
    
    def send_report(self):
        """Deprecated. Newer version is using Dropbox."""
        
        if self.date != dt.today():
            self.date = dt.today()
            self.mail_sent = False
            self.exception_num = 0 #reset error counter everyday
            self.error_sent = False
        
        if dtm.now() > dtm.combine(self.date, tm(hour=8)) and self.saved and not self.mail_sent:
#            dates = [(self.date-td(hours=24)).isoformat(), self.date.isoformat()]
            logs = [file for file in os.listdir(self.dir_path) if 'LOG' in file and '.csv' in file]
#            try:
#                email.log_reports(dates,self.start_time, self.dir_path, logs)
#                self.mail_sent = True
#            except:
#                print('report cannot be sent\ntime: '+ dtm.now().isoformat())
        
        if self.exception_num > 11 and not self.error_sent:
            try:
#                email.connection_error()
                self.error_sent = True
                self.exception_num = 0
            except:
                print('error mail cannot be sent\ntime: '+dtm.now().isoformat())
    
    def save(self, csv_list):
        """Proprocess the data to be saved  than save it
        
        Parameters
        ----------
        csv_list : list
            List of timestamps data to be saved.
        """
            
        csv_list.sort() # sort after timestamp
        
        # saving files of one session in one folder
        if not os.path.isdir(self.dir_path):
            os.mkdir(self.dir_path)
        
        # get all saved files
        logs = [file for file in os.listdir(self.dir_path) if 'LOG' in file and '.csv' in file]
        
        # if there are saved files, saved data of saved files 
        # are taken out from csv_list
        if logs != list():
            for log in logs:
                with open(self.dir_path+'\\'+log,'r',newline='') as f:
                    saved_data = f.readlines()
                
                csv_list = [data_row for data_row in csv_list if data_row not in saved_data]
        
        to_save = ''.join(csv_list)
        
        save_name_yesterday = self.dir_path+'\\LOG_'+(dt.today()-td(days=1)).isoformat()+'.csv'
        save_name_today = self.dir_path+'\\LOG_'+dt.today().isoformat()+'.csv'
        
        # saved to file from yesterday before 9 a.m.
        if dtm.now().time() < tm(hour=9):
            save_name = save_name_yesterday
        else:
            save_name = save_name_today
        
        to_save = ''.join(csv_list)
        
        with open(save_name,'a+',newline='') as f:
            f.write(to_save)
    
    def log(self):
        
        while self.parent.should_run:        
            if not self.saved or (dtm.now() - self.log_saved) > td(hours = 1): #check if 1 hour has ellapsed or if csv file has been saved            
                
                self.parent.parent.statusText.setText('connecting ...') #print('connecting...')
                
                self.check_comports()
                
                if self.PORT != "No MOXA":
                    try:
                        with serial.Serial(self.PORT,baudrate=19200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=2) as ser:
                            if not ser.is_open:
                                raise Exception('cannot connect to port')
                            
                            # synchronised clock at logging begin and every 24h after
                            if self.synced == None:
                                self.synced = dtm.now()
                                self.synchronise_clock(ser)
                            elif dtm.now() > self.synced + td(days=1):
                                self.synced = dtm.now()
                                self.synchronise_clock(ser)
                            
                            sleep(3)
                            csv_list = list() #saving logs from all decoder in one file
                            
                            for i in range(NUMBER_OF_RFID_DECODER):
                                # check if ui is terminated
                                if not self.parent.should_run:
                                    break
                                
                                # check memory
                                finished = False
                                while not finished:
                                    if not self.parent.should_run:
                                        break
                                    rfid_add = format(i+1,'02x')
                                    print('rfid_id:',rfid_add)
                                    self.parent.parent.statusText.setText( 'reading decoder nr. '+rfid_add) #print('reading decoder nr. '+rfid_add)
                                    
                                    to_write = self.ser_command(rfid_add,'41')
                                    ser.reset_input_buffer()
                                    sleep(0.5)                                
                                    ser.write(to_write)
                                    sleep(3) #waiting for answer from decoder to be written in input buffer
                                    if ser.in_waiting != 0:
                                        all_data =  ser.read_until(bytes.fromhex(STOP))
                                        i = 0
                                        while len(all_data) < LENGTH_ANSWER_CHECK_MEMORY+4:
                                            i += 1
                                            if i > 100:
                                                raise Exception('Communication error. Please check if cable connected properly.')
                                            checksum = ser.read(1) #Irgednwie funktioniert das "ser.reset_input_buffer()"  nicht. Deswegen wird die Restdaten hier manuell gelöscht.
                                            del checksum
                                            all_data = ser.read_until(bytes.fromhex(STOP))
                                        print('all_data',all_data)
    #                                    print('length',len(all_data))
    #                                    print('should be :', LENGTH_ANSWER_CHECK_MEMORY+4)
                                        checksum = ser.read(1)
    #                                    print('checksum',checksum)
                                            
                                        if self.xor_checksum(all_data) == checksum[0]: #check if there is error in bytes
    #                                        data_without_tags = all_data.strip(bytes.fromhex(''.join([START,STOP])))
                                            data_without_tags = all_data[2:-2]
    #                                        print('data_without_tags', data_without_tags)
                                            z = 0
                                            n_id = list()
                                            for x in range(LENGTH_ANSWER_CHECK_MEMORY):
    #                                            print('iter x ',x)
                                                if x == 3:
                                                    n_id.append(format(data_without_tags[z],'02x'))
                                                if x == 4:
                                                    n_id.append(format(data_without_tags[z],'02x'))
                                                if data_without_tags[z] == int('10',16):
                                                    z += 1
                                                z += 1
                                            n_id = int(''.join(n_id), 16)
                                            finished = True
                                        else:
                                            self.parent.parent.statusText.setText('instability is detected\n\nnew attempt will be made')
                                            sleep(5)
                                    else:
                                        finished = True
                                        raise Exception('decoder nr. '+rfid_add+' is not connected')

                                # get data
                                finished = False
                                while not finished:
                                    if not self.parent.should_run:
                                        break
                                    self.parent.parent.statusText.setText( 'reading decoder nr. '+rfid_add) #print('reading decoder nr. '+rfid_add)
                                    sleep(1)
                                    to_write = self.ser_command(rfid_add,'4d')
                                    ser.reset_input_buffer()
                                    ser.write(to_write)
                                    sleep(3)
                                    
                                    print('n_id', n_id)
                                    if ser.in_waiting != 0:
                                        temp_list = list()
                                        for j in range(n_id):
                                            if not j%500:
                                                self.parent.parent.statusText.setText('decoder {} read : {:.2f}%'.format(rfid_add, j/n_id*100))
                                                print('percent read : {:.2f} %'.format(j/n_id*100))
    #                                        print('iter j ', j)
    #                                        print('n_id',n_id)
                                            all_data = ser.read_until(bytes.fromhex(STOP))
    #                                        print("all data: ", all_data)
                                            
                                            while len(all_data) < (LENGTH_ANSWER_TIMESTAMP + 2 + 2): #Length with START and STOP code
                                                rest = ser.read_until(bytes.fromhex(STOP))
    #                                            print("rest:",rest)
    #                                            print("len rest:", len(rest))
                                                if len(rest) > 0:
                                                    all_data = b''.join([all_data,rest])
                                                else:
                                                    break
                                            # print('all data :', all_data)
    #                                        print('length:',len(all_data))
    #                                        print('should be:', LENGTH_ANSWER_TIMESTAMP+4)
                                            checksum = ser.read(1)
                                            if len(checksum) == 0:
                                                checksum = rest
                                                break #checksum was in the rest beacuse it was end of message but message was smaller. Also all id codes are read -> break loop
    #                                        print('checksum:',checksum)
                                            
                                            if self.xor_checksum(all_data) == checksum[0]:
                                                if len(all_data) >= (LENGTH_ANSWER_TIMESTAMP+4):
        #                                            data_without_tags = all_data.strip(bytes.fromhex(''.join([START,STOP])))
                                                    data_without_tags = all_data[2:-2]
    #                                                print("data without tags:", data_without_tags)
                                                    z = 0
                                                    tag_id = list()
                                                    for y in range(LENGTH_ANSWER_TIMESTAMP):
    #                                                    print('iter y',y)
    #                                                    print('iter z', z)
                                                        if y == 4:
                                                            tag_id.append(format(data_without_tags[z],'02X'))
                                                        if y == 5:
                                                            tag_id.append(format(data_without_tags[z],'02X'))
                                                        if y == 6:
                                                            tag_id.append(format(data_without_tags[z],'02X'))
                                                        if y == 7:
                                                            tag_id.append(format(data_without_tags[z],'02X'))
                                                        if y == 8:
                                                            tag_id.append(format(data_without_tags[z],'02X'))
                                                        if y == 9:
                                                            second = format(data_without_tags[z],'02x')
                                                        if y == 10:
                                                            minute = format(data_without_tags[z],'02x')
                                                        if y == 11:
                                                            hour = format(data_without_tags[z],'02x')
                                                        if y == 12:
                                                            day_year = format(data_without_tags[z],'08b')
                                                            day = format(int(day_year[2:4],2)*10+int(day_year[4:8],2),'02d')
                                                            year_number = int(day_year[0:2],2)
                                                        if y == 13:
                                                            month_week = format(data_without_tags[z],'08b')
                                                            month = format(int(month_week[3],2)*10+int(month_week[4:8],2),'02d')
                                                        if data_without_tags[z] == int('10',16):
                                                            z += 1
                                                        z += 1
                                                    
                                                    
                                                    if year_number < dt.today().year%4:
                                                        year = str(dt.today().year-1)
                                                    elif year_number == 3 and dt.today().year%4 == 0:
                                                        year = str(dt.today().year-1)
                                                    else:
                                                        year = str(dt.today().year)
                                                    #year = dt.today().strftime('%Y')
                                                    timestamp = year+'-'+month+'-'+day+'T'+hour+':'+minute+':'+second
                                                    tag_id = ''.join(tag_id)
                                                    # print('tag_id :', tag_id)
                                                    # print("timestamp :", timestamp)
                                                    #datetime from pc
                                                    #date = dt.today().isoformat()
                                                    #timestamp = date+'T'+hour+':'+minute+':'+second
                                                    
                                                    try:
                                                        timestamp_dtm = dtm.strptime(timestamp,'%Y-%m-%dT%H:%M:%S')
                                                    except:
                                                        timestamp_dtm = dtm.now()-td(hours=10)
    #                                                print("timestamp_dtm :", timestamp_dtm)
                                                    if self.log_saved == None:
                                                        temp_list.append(';'.join([timestamp,rfid_add,tag_id])+'\n')
                                                    elif timestamp_dtm > (self.log_saved -td(minutes=30)): # write files from the last saved
                                                        temp_list.append(';'.join([timestamp,rfid_add,tag_id])+'\n')
    #                                                if timestamp_dtm > (dtm.now() - td(hours=1)): #write only log files with timestamp from 1 hour ago till now
    #                                                    csv_list.append(';'.join([timestamp,rfid_add,tag_id]))
                                                    finished = True
                                            else:
                                                self.parent.parent.statusText.setText('instability detected.\n\nnew attempt will be made')
                                                sleep(5)
                                    else:
                                        raise Exception('decoder nr. '+rfid_add+' is disconnected')
                                        finished = True
                                
                                csv_list.extend(temp_list)
                                #flush input buffer to erase unused data byte
                                #ser.reset_input_buffer()
                                #print("reset input buffer")
                                #print("len of csv_list: ",len(csv_list))
                            
                            # check if ui is terminated
                            if not self.parent.should_run:
                                break
                            
                            # save log file in csv
                            print('length of csv_list:', len(csv_list))
                            if csv_list != list(): #check if there is no acitivity in the last hour
                                self.parent.parent.statusText.setText('saving in csv ...') #print('saving in csv ...')
                                self.save(csv_list)
                                sleep(1)
                                self.parent.parent.statusText.setText('finished saving')
                                sleep(1)
#                                csv_list.sort() #sort after timestamp
#                                to_save = '\n'.join(csv_list)
#                                
#                                #saving files of one session in one folder
#                                if not os.path.isdir(self.dir_path):
#                                    os.mkdir(self.dir_path)
#                                    
#                                with open(self.dir_path+'\\LOG_'+self.date.isoformat()+'.csv','a+',newline='') as f:
#                                    self.parent.parent.statusText.setText('saving in csv ...') #print('saving in csv ...')
#                                    f.write(to_save+'\n')
#                                    sleep(1)
#                                    self.parent.parent.statusText.setText('finished saving') #print('finished saving')
#                                    sleep(1)
                                
                                        
                                #Erasing memory
                                #BUT there is a possibility of data lost if an instability occured.
                                #
                                if dt.today() > (self.date + td(days=2)) or self.should_delete:
                                    self.should_delete = False
                                    self.date = dt.today()
                                    for i in range(4):
                                        rfid_add = format(i+1,'02x')
                                        rest = b''
                                        ser.reset_input_buffer()
                                        sleep(0.5)
                                        to_write = self.ser_command(rfid_add,'65')
                                        ser.write(to_write)
                                        sleep(3)
                                        
                                        sta = dtm.now()
                                        while True:
                                            # check for timeout. Set for 5 seconds
                                            if (dtm.now() - sta) > td(seconds=5):
                                                self.should_delete = True
                                                self.parent.parent.statusText.setText('cannot delete data from decoder no. {}'.format(i+1))
                                                sleep(3)
                                                break
                                            if ser.in_waiting != 0:
                                                rest += ser.readline()
                                                if bytes.fromhex(STOP) in rest:
                                                    if bytes.fromhex('65') in rest:
                                                        print(rest)
                                                        break
                                        
                    
                        self.log_saved = dtm.now()
                        self.parent.parent.lastsavedText.setText(self.log_saved.isoformat())
                        self.parent.parent.statusText.setText('waiting till next cycle in 1 hour')
                        #save the timestamp if all sequences are done
                        self.saved = True
                        
                        #sending report if conditions are met
#                        self.send_report()
                        
                        # check if ui is terminated
                        if not self.parent.should_run:
                            break
                        
                        sleep(600)
                        
                    except Exception as inst:
                        self.parent.parent.statusText.setText(inst.args[0]+'\n\nnew attempt will be made in 1 minute\n\nlast try: '+dtm.now().isoformat().split('.')[0].replace('T',', '))
                        
                        # save available data
                        if csv_list != list():
                            self.save(csv_list)
                        
                        # label self.saved as false because not all data are saved
                        self.saved = False
                        
                        # closing port if an exception is raised
                        ser.close()
                        
                        # add exception num. After 12 attempts, an error email will be sent
                        self.exception_num += 1
                        
#                        self.send_report()
                        
                        sleep(60)
                else:
                    self.parent.parent.statusText.setText('there is no USB connection to MOXA detected\n\nnew attempt will be made in 10 minutes\n\nlast try: '+dtm.now().isoformat().split('.')[0].replace('T',', '))
                    self.saved = False
                    self.exception_num += 1
                    
#                    self.send_report()
                    # check if ui is terminated
                    if not self.parent.should_run:
                        break
                    
                    sleep(600)
            else:
                sleep(600)
                
class LogController:
    
    def __init__(self, parent=None):
        
        self.parent = parent
        self.thread = QtCore.QThread()
        self.log_job = LogWorker(self)
        self.log_job.moveToThread(self.thread)
        
        self.thread.started.connect(self.log_job.log)
        
        self.should_run = False
    
    def start(self):
        
        if not self.should_run:
            self.should_run = True
            self.thread.start()
            self.parent.statusText.setText("thread started") #print('thread started')
    
    def stop(self):
        
        if self.should_run:
            self.should_run = False
            self.thread.quit()
            self.parent.statusText.setText("thread terminated") #print('thread terminated')
            
if __name__ == "__main__":
    ser = serial.Serial("COM15", baudrate=19200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=2 )
    log = LogWorker()
    log.synchronise_clock(ser)
    ser.close()
            