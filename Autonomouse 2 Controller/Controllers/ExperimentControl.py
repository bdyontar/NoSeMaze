from PyQt5 import QtCore, QtWidgets
from time import sleep, time
from PyPulse import PulseInterface, PulseGeneration
import daqface.DAQ as daq
from TrialLogic import TrialConditions
import datetime
from PyQt5.QtCore import QReadWriteLock
#import scipy.io as sio
import os
import csv
import HelperFunctions.RFID as rfid
import HelperFunctions.Reward as reward
import HelperFunctions.BeamCheck as beam
#import HelperFunctions.Filter as filt
import HelperFunctions.Email as email
import numpy as np

class ExperimentWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    trial_end = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(None)
        self.parent = parent
        self.lock_llog = QReadWriteLock()
        self.hardware_prefs = self.parent.parent.hardware_prefs
        self.experiment = self.parent.parent.experiment
        self.save_timestamp = datetime.datetime.now()
        self.cut = 0 # for debugging
        self.morning_mail_sent = False
        self.evening_mail_sent = False
        self.night_mail_sent = False
        self.mail_sent = False
        
    def trial(self):
        self.start_timestamp = [self.parent.start_timestamp, self.parent.start_timestamp]
        self.today = datetime.date.today()
        while self.parent.should_run:
            start = time()
            
            """ Is there an animal present? """
            
            if self.animal_present():
                """ Check which animal is present and get a reference to it """
                animal = self.get_present_animal()
                
                """ Look up current trial for this mouse """
                current_trial = animal.current_trial()
                
                """ Parse this trial into a set of DAQ commands """
                current_trial_pulse = animal.current_trial_pulse()
                
                if self.hardware_prefs['static']:
                    pulses = []
                    
                    for params in current_trial_pulse:
                        this_pulse = PulseGeneration.simple_pulse_static(self.hardware_prefs['samp_rate'],params)
                        pulses.append(this_pulse)
                        onset = params['onset']
                        offset = params['offset']
                    
                    if current_trial_pulse[0]['fromLength']:
                        duration = current_trial_pulse[0]['length']
                    else:
                        duration = current_trial_pulse[0]['pulse_width']
                    
                    odor_pulses = np.zeros((len(pulses),1))
                    
                    for p, pulse in enumerate(pulses):
                        odor_pulses[p] = pulse
                    
                    total_length = round(duration + onset + offset,10)
                    t = np.linspace(0, total_length, total_length*self.hardware_prefs['samp_rate'])
                    odor_pulses = [odor_pulses, onset, duration, offset]
                    fv_pulse = np.array([self.hardware_prefs['fv_delay']])
                else:
                    odor_pulses, t = PulseInterface.make_pulse(self.hardware_prefs['samp_rate'], 0.0, 0.0, current_trial_pulse)
                    length = len(t)/self.hardware_prefs['samp_rate'] - self.hardware_prefs['fv_delay'] - current_trial_pulse[0]['offset'] - current_trial_pulse[0]['offset']
                    fv_pulse = PulseGeneration.fv_pulse(self.hardware_prefs['samp_rate'], current_trial_pulse, length, self.hardware_prefs['fv_delay'])
                
                """ Checking if pretraining """
                if not ('pretraining' in current_trial_pulse[0]):
                    pretraining = False
                else:
                    pretraining = current_trial_pulse[0]['pretraining']
                
                if not 'wait_training' in current_trial_pulse[0]:
                    wait_training = False
                else:
                    wait_training = current_trial_pulse[0]['wait_training']
                
                """ Send the data to the DAQ """
                if pretraining:
                    self.reward(animal) 
                    water_given = [True, True]
                    trial_daq = daq.ThreadSafeAnalogInput(self.hardware_prefs['analog_input'], self.hardware_prefs['analog_channels'], self.hardware_prefs['samp_rate'], 2)
                    start_time = datetime.datetime.now()
                    analog_data = trial_daq.DoTask()
                    
                    lick_time_l, licks_l = TrialConditions.licks_number(analog_data[self.hardware_prefs['lick_channel_l']], 2, self.hardware_prefs['samp_rate'], start_time)
                    lick_time_r, licks_r = TrialConditions.licks_number(analog_data[self.hardware_prefs['lick_channel_r']], 2, self.hardware_prefs['samp_rate'], start_time)
                    
                    lick_time = [lick_time_l,lick_time_r]
                    licks = [licks_l,licks_r]
                    
                    self.experiment.last_data_l = analog_data[self.hardware_prefs['lick_channel_l']]
                    self.experiment.last_data_r = analog_data[self.hardware_prefs['lick_channel_r']]
                    
                    response_l = TrialConditions.lick_detect(analog_data[self.hardware_prefs['lick_channel_l']], 2, float(current_trial_pulse[0]['lick_fraction']))
                    response_r = TrialConditions.lick_detect(analog_data[self.hardware_prefs['lick_channel_r']], 2, float(current_trial_pulse[0]['lick_fraction']))
                    response = [response_l,response_r]
                    
                    wait_response_l = 0
                    wait_response_r = 0
                    wait_response = [wait_response_l,wait_response_r]
                    
                    rewarded = current_trial[0:4]
                    
                    result, correct, timeout = TrialConditions.trial_result(rewarded, response_l, response_r)
                    
                    wait_time_l = 'wait timestamp ist gleich lick timestamp'
                    wait_time_r = 'wait timestamp ist gleich lick timestamp'
                    wait_time = [wait_time_l, wait_time_r]
                    
                    timestamp = datetime.datetime.now()
                
                else:
                    if wait_training:
                        trial_daq = daq.DoAiMultiTaskWaitTraining(self.hardware_prefs['analog_input'],
                                                                  self.hardware_prefs['analog_channels'],
                                                                  self.hardware_prefs['odour_output'],
                                                                  self.hardware_prefs['finalvalve_output'],
                                                                  self.hardware_prefs['reward_output1'],
                                                                  self.hardware_prefs['reward_output2'],
                                                                  self.hardware_prefs['samp_rate'],
                                                                  len(t)/ self.hardware_prefs['samp_rate'],
                                                                  odor_pulses, fv_pulse,
                                                                  self.hardware_prefs['sync_clock'],
                                                                  self.hardware_prefs['static'],
                                                                  self.hardware_prefs['thorax_delay'],
                                                                  self.hardware_prefs['lick_delay'],
                                                                  self.hardware_prefs['lick_channel_l'],
                                                                  self.hardware_prefs['lick_channel_r'],
                                                                  self.hardware_prefs['beam_channel'],
                                                                  current_trial[0:4])
                    
                        analog_data, wait_data, should_lick_data, start_time, water_given, wait_response, wait_time, start_time_2 = trial_daq.DoTask()
                        
                        self.experiment.last_data_l = analog_data[self.hardware_prefs['lick_channel_l']]
                        self.experiment.last_data_r = analog_data[self.hardware_prefs['lick_channel_r']]
                        
                        """ Analyse the lick response """
                        rewarded = current_trial[0:4]
                        
                        response_l = TrialConditions.lick_detect(should_lick_data[self.hardware_prefs['lick_channel_l']], 2, float(current_trial_pulse[0]['lick_fraction']))
                        response_r = TrialConditions.lick_detect(should_lick_data[self.hardware_prefs['lick_channel_r']], 2, float(current_trial_pulse[0]['lick_fraction']))
                        response = [response_l, response_r]
                        
                        result, correct, timeout = TrialConditions.trial_result(rewarded, response_l, response_r)
                        
                        """ Analyse the number of licks """
                        lick_time_l, licks_l = TrialConditions.licks_number(should_lick_data[self.hardware_prefs['lick_channel_l']], 2, self.hardware_prefs['samp_rate'], start_time)
                        lick_time_r, licks_r = TrialConditions.licks_number(should_lick_data[self.hardware_prefs['lick_channel_r']], 2, self.hardware_prefs['samp_rate'], start_time)
                        lick_time = [lick_time_l, lick_time_r]
                        licks = [licks_l, licks_r]
                        
                        print('water given :', str(water_given))
                        print('wait response :', str(wait_response))
                        
                        timestamp = start_time_2
#                        if timeout or wait_response > 15:
#                            self.timeout()
                        
                    else:
                        trial_daq = daq.DoAiMultiTask(self.hardware_prefs['analog_input'],
                                                      self.hardware_prefs['analog_channels'],
                                                      self.hardware_prefs['odour_output'],
                                                      self.hardware_prefs['finalvalve_output'],
                                                      self.hardware_prefs['reward_output1'],
                                                      self.hardware_prefs['reward_output2'],
                                                      self.hardware_prefs['samp_rate'],
                                                      len(t) / self.hardware_prefs['samp_rate'],
                                                      odor_pulses, fv_pulse, 
                                                      self.hardware_prefs['sync_clock'], 
                                                      self.hardware_prefs['static'], 
                                                      self.hardware_prefs['thorax_delay'],
                                                      self.hardware_prefs['lick_delay'],
                                                      self.hardware_prefs['lick_channel_l'],
                                                      self.hardware_prefs['lick_channel_r'],
                                                      self.hardware_prefs['beam_channel'],
                                                      current_trial[0:4])
                    
                        analog_data, wait_data, should_lick_data, start_time1, start_time2, water_given = trial_daq.DoTask()
                        
                        self.experiment.last_data_l = analog_data[self.hardware_prefs['lick_channel_l']]
                        self.experiment.last_data_r = analog_data[self.hardware_prefs['lick_channel_r']]
                        
                        """ Analyse the wait response """
                        wait_time_l, wait_response_l = TrialConditions.licks_number(wait_data[self.hardware_prefs['lick_channel_l']], 2, self.hardware_prefs['samp_rate'], start_time2)
                        wait_time_r, wait_response_r = TrialConditions.licks_number(wait_data[self.hardware_prefs['lick_channel_r']], 2, self.hardware_prefs['samp_rate'], start_time2)
                        
                        wait_time = [wait_time_l, wait_time_r]
                        wait_response = [wait_response_l, wait_response_r]
                        
                        """ Analyse the lick response """#DONE : have to build a new trial_result method according to the new trial structure
                        rewarded = current_trial[0:4]
                        response_l = TrialConditions.lick_detect(should_lick_data[self.hardware_prefs['lick_channel_l']], 2, float(current_trial_pulse[0]['lick_fraction']))
                        response_r = TrialConditions.lick_detect(should_lick_data[self.hardware_prefs['lick_channel_r']], 2, float(current_trial_pulse[0]['lick_fraction']))
                        result, correct, timeout = TrialConditions.trial_result(rewarded, response_l, response_r) #DONE change trial result
                        response = [response_l, response_r]
                        
                        """ Analyse the number of licks """
                        lick_time_l, licks_l = TrialConditions.licks_number(should_lick_data[self.hardware_prefs['lick_channel_l']], 2, self.hardware_prefs['samp_rate'], start_time1)
                        lick_time_r, licks_r = TrialConditions.licks_number(should_lick_data[self.hardware_prefs['lick_channel_r']], 2, self.hardware_prefs['samp_rate'], start_time1)
                        
                        lick_time = [lick_time_l, lick_time_r]
                        licks = [licks_l, licks_r]

                        """ Determine reward conditions and enact """
                        if result == TrialConditions.TrialResult.false_alarm:
                            self.timeout()
                        
                        print('water given :', str(water_given))
                        print('wait_response :', str(wait_response))
                        timestamp = start_time2
                
                length = time() - start
                """ Update database """
                animal.schedule_list[animal.current_schedule_idx].add_trial_data(timestamp, wait_response, response, correct, timeout, licks, rewarded)
                self.experiment.add_trial(animal.id, timestamp, animal.current_schedule_idx, animal.current_trial_idx,
                                          list(map(str,rewarded)), wait_response, response, correct, timeout, licks)
                """updating licks"""
                print('updating licks')
                self.lock_llog.lockForWrite()
                animal.update_licks(timestamp, rewarded, wait_response, licks, self.experiment.logs_path, water_given, int(correct), int(timeout))
                self.lock_llog.unlock()
                
                """checking licks and status"""
                self.check_licks()
                sleep(0.005)
                self.check_status()
            
                """ Advance animal to next trial """
                animal.advance_trial()
                
                """ Save bulkiest part of data to disk and save experiment if necessary """
                self.save_data(animal.id, timestamp, rewarded, wait_response, response, correct, timeout, odor_pulses, t, self.save_timestamp, lick_time , licks, wait_time)
                
                if len(self.experiment.trials) % 10 == 0:
                    self.experiment.save()
                
                """ Signal that trial has finished """
                print("Trial index : {0}".format(len(self.experiment.trials)-1))
                print("Length of trial : {0:.2f} s".format(length))
                print("Trial at ", timestamp.strftime('%X'))
                
                self.trial_end.emit()
            else:
                self.check_licks()
                sleep(0.005)
                self.check_status()
            
            sleep(0.5)
        self.finished.emit()
    
    def check_status(self):
        if datetime.date.today() != self.today:
            self.today = datetime.date.today()
            self.morning_mail_sent = False
            self.evening_mail_sent = False
            self.night_mail_sent = False
            
        morning = datetime.datetime.combine(self.today, datetime.time(hour=8))
        evening = datetime.datetime.combine(self.today, datetime.time(hour=17))
        night = datetime.datetime.combine(self.today, datetime.time(hour=22))
        now = datetime.datetime.now()
        if now > morning and now <= evening and not self.morning_mail_sent:
            print('sending morning mail')
            email.deadmans_switch(self.experiment)
            self.morning_mail_sent = True
        elif now > evening and now <= night and not self.evening_mail_sent:
            print('sending evening mail')
            email.deadmans_switch(self.experiment)
            self.evening_mail_sent = True
        elif now > night and not self.night_mail_sent:
            email.deadmans_switch(self.experiment)
            self.night_mail_sent = True
        elif now < morning and not self.mail_sent:
            email.deadmans_switch(self.experiment)
            self.mail_sent = True
        
            
    def check_licks(self):
        self.lock_llog.lockForRead()
        interval = datetime.timedelta(hours=6)
        if (datetime.datetime.now() - self.start_timestamp[0]) > interval:
            print('check_licks')
            self.start_timestamp[0] = datetime.datetime.now()
            problem_list = list()
            for animal in self.experiment.animal_list:
                if animal != 'default':
                    fname = self.experiment.animal_list[animal].fname
                    if fname is not None and os.path.isfile(fname):
                        with open(fname,'r',newline='') as f:
                            licks_list = f.readlines()
                            licks_list = licks_list[1:]
                        for i,row in enumerate(licks_list):
                            licks_list[i] = row.split(',')
                    else:
                        licks_list = list()
                        
                    if len(licks_list) == 0:
                        last_hour_low_licked = True
                    else:
                        licks_T = list(map(list, zip(*licks_list)))
                        time = list()
                        for x in range(len(licks_T[0])):
                            time.append(datetime.datetime.strptime(licks_T[0][x].strip('\n'),'%Y-%m-%d %H:%M:%S.%f'))
                        try:
                            licks = licks_T[4]
                        except:
                            licks = [0]

                        if self.start_timestamp[0] - time[-1] > interval or licks[-1] == 0 or licks[-1] == None:
                            last_hour_low_licked = True
                        else:
                            if time[-1] - time[0] < interval:
                                licks_per_trial_last_hour = (int(licks[-1])- int(licks[0]))/len(licks)
                            else:
                                i = 2
                                while time[-1] - time[-i] < interval:
                                    i+=1
                                licks_per_trial_last_hour = (int(licks[-1])-int(licks[-i]))/i
                            last_hour_low_licked = licks_per_trial_last_hour < self.hardware_prefs['low_lickrate']
                    
                    if last_hour_low_licked: 
                        problem_list.append(animal)    
            if len(problem_list) > 0:
                problem_list.append('default')
                email.warning_licks(self.experiment.logs_path, problem_list)
        self.lock_llog.unlock()

    def animal_present(self):
        # checks whether animal is present in the port - DEBUG
        # return np.random.rand() > 0.5
        return beam.check_beam(self.hardware_prefs['analog_input'], self.hardware_prefs['analog_channels'],
                               self.hardware_prefs['beam_channel'])
            

    def get_present_animal(self):
        # returns the animal in the port - DEBUG just chooses a random animal
#        animals = list(self.experiment.animal_list.keys())
#        animal = np.random.choice(animals)

        animal = rfid.check_rfid(self.hardware_prefs['rfid_port'], 10)
        try:
            if animal in self.experiment.animal_list.keys():
                return self.experiment.animal_list[animal]
            else:
                return self.experiment.animal_list['default']
        except:
            return self.experiment.animal_list['default']

    def reward(self, animal):
        if self.hardware_prefs['static']: #DONE reward for pretraining should be together from both port
            rewarded = animal.current_trial()
            if rewarded[0] > 0 and rewarded[1] > 0:
                reward.deliver_reward_static_two(self.hardware_prefs['reward_output1'], self.hardware_prefs['reward_output2'], rewarded[2], rewarded[3])
            elif rewarded[0] > 0 and rewarded[1] == 0:
                reward.deliver_reward_static(self.hardware_prefs['reward_output1'], rewarded[2])
            elif rewarded[0] == 0 and rewarded[1] > 0:
                reward.deliver_reward_static(self.hardware_prefs['reward_output2'], rewarded[3])
        
    def timeout(self):
        sleep(self.hardware_prefs['timeout'])
        
#    def filter_data(self, data):
#        fcut = 20
#        self.cut = int(self.hardware_prefs['samp_rate']/fcut)
#        fData = filt.Square_Filter(data, self.hardware_prefs['samp_rate'],fcut)
#        return fData

    def save_data(self, animal_id, timestamp, rewarded, wait_response, response, correct, timeout, pulses, time_axis, file_timestamp, lick_time, licks, wait_time):
        strTimestamp = str(timestamp)
        file_timestamp = str(file_timestamp).replace('/','-')
        file_timestamp = file_timestamp.replace(' ','T')
        file_timestamp = file_timestamp.replace(':','')
        file_timestamp = file_timestamp.split('.')[0]
        
        file_name = self.experiment.save_path + '/' + 'trials_'+file_timestamp 
        
        rewarded = '|'.join(list(map(str,rewarded))) #change rewarded into a str variable
        
        newData = { 
                    'a_animal_id': animal_id,
                    'b_timestamp': strTimestamp,
                    'c_licks_number_l' : licks[0],
                    'd_licks_number_r' : licks[1],
                    'e_rewarded': rewarded,
                    'f_wait_response_l' : wait_response[0],
                    'g_wait_response_r' : wait_response[1],
                    'h_response_l': response[0],
                    'i_response_r': response[1],
                    'j_correct': correct,
                    'k_timeout': timeout,
                    'l_wait_timestamps_l': wait_time[0],
                    'm_wait_timestamps_r': wait_time[1],
                    'n_lick_timestamp_l': lick_time[0],
                    'o_lick_timestamp_r': lick_time[1]
                  }
        
        #save in .mat
        #if len(self.experiment.trials) % 10 == 0:
        #sio.savemat(file_name+'.mat', data)
        
        #save in .csv
        fn = sorted(newData.keys())
        if os.path.isfile(file_name+'.csv'):
            should_write_header = False
        else:
            should_write_header = True
        with open(file_name+'.csv','a+',newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fn)
            if should_write_header:
                writer.writeheader()
            writer.writerow(newData)
                     
        
class ExperimentController:
    def __init__(self, parent):
        self.parent = parent
        self.thread = QtCore.QThread()
        self.trial_job = ExperimentWorker(self)
        self.trial_job.moveToThread(self.thread)

        self.thread.finished.connect(self.thread.quit)
        self.thread.started.connect(self.trial_job.trial)

        self.should_run = False
        
    def update_pref(self, new_pref):
        self.trial_job.hardware_prefs = new_pref
        
    def start(self):
        #checking if any animal does not have a schedule
        check = []
        for animal in self.parent.experiment.animal_list:
            if len(self.parent.experiment.animal_list[animal].schedule_list) > 0:
                check.append(1)
            else:
                check.append(0)
        check = np.nonzero(np.array(check))[0]
        if len(self.parent.experiment.animal_list)>len(check):
            QtWidgets.QMessageBox.about(self.parent, "Error", "An animal does not have a schedule! Please update the Animal List")
        elif self.parent.experiment.save_path is not None:
            if not self.should_run:
                self.should_run = True
                self.start_timestamp = datetime.datetime.now()
                self.count = time()
                self.thread.start()
                print('thread started')
        else:
            QtWidgets.QMessageBox.about(self.parent, "Error", "Experiment not saved! Please save before starting")

    def stop(self):
        if self.should_run:
            self.should_run = False
            self.thread.terminate()
            self.thread.wait()
            print('thread ended')
