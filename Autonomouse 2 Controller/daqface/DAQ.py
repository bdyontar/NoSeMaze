# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 13:51:48 2015

@author: Andrew Erskine
"""

#TODO ES IST SEHR UNÜBERSCHAULICH: EIN UMORDNUNG ERFORDERLICH!!!

# region [Import]
from PyDAQmx import *
from ctypes import *
import daqface.Utils as Util
import numpy
import matplotlib.pyplot as plt
import time
import datetime
import math
from HelperFunctions import Reward as reward
from TrialLogic import TrialConditions as trial


# region [DigitalTasks]


#class DigitalInput(Task):
#    def __init__(self, device, channels, samprate, secs, clock=''):
#        Task.__init__(self)
#        self.CreateDIChan(device, "", DAQmx_Val_ChanPerLine)
#
#        self.read = int32()
#        self.channels = channels
#        self.totalLength = numpy.uint32(samprate * secs)
#        self.digitalData = numpy.ones((channels, self.totalLength), dtype=numpy.uint32)
#
#        self.CfgSampClkTiming(clock, samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, numpy.uint64(self.totalLength))
#        self.WaitUntilTaskDone(-1)
#        self.AutoRegisterDoneEvent(0)
#
#    def DoTask(self):
#        print('Starting digital input')
#        self.StartTask()
#        self.ReadDigitalU32(self.totalLength, -1, DAQmx_Val_GroupByChannel, self.digitalData,
#                            self.totalLength * self.channels, byref(self.read), None)
#
#    def DoneCallback(self, status):
#        print(status)
#        self.StopTask()
#        self.ClearTask()
#        return 0


class TriggeredDigitalInput(Task):
    def __init__(self, device, channels, samprate, secs, trigger_source, clock=''):
        Task.__init__(self)
        self.CreateDIChan(device, "", DAQmx_Val_ChanPerLine)

        self.read = int32()
        self.channels = channels
        self.totalLength = numpy.uint32(samprate * secs)
        self.digitalData = numpy.zeros((channels, self.totalLength), dtype=numpy.uint32)

        self.CfgSampClkTiming(clock, samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, numpy.uint64(self.totalLength))
        self.WaitUntilTaskDone(-1)
        self.CfgDigEdgeStartTrig(trigger_source, DAQmx_Val_Rising)
        self.AutoRegisterDoneEvent(0)

    def DoTask(self):
        self.StartTask()
        self.ReadDigitalU32(self.totalLength, -1, DAQmx_Val_GroupByChannel, self.digitalData,
                            self.totalLength * self.channels, byref(self.read), None)

    def DoneCallback(self, status):
        print(status.value)
        self.StopTask()
        self.ClearTask()
        return 0


class DigitalOut(Task):
    def __init__(self, device, samprate, secs, write, clock=''):
        Task.__init__(self)
        self.CreateDOChan(device, "", DAQmx_Val_ChanPerLine)

        self.sampsPerChanWritten = int32()
        self.totalLength = samprate * secs
        self.CfgSampClkTiming(clock, samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, numpy.uint64(self.totalLength))

        self.AutoRegisterDoneEvent(0)

        self.write = Util.binaryToDigitalMap(write)

    def DoTask(self):
        print ('Starting digital output')
        self.WriteDigitalU32(self.write.shape[1], 0, -1, DAQmx_Val_GroupByChannel, self.write,
                             byref(self.sampsPerChanWritten), None)

        self.StartTask()

    def DoneCallback(self, status):
        print(status)
        self.StopTask()
        self.ClearTask()
        return 0

class NiUsbDigitalOutTwoDevices:
    def __init__(self, device1, device2, secs1, secs2, on1, on2):
        self.do1_handle = TaskHandle(0)
        self.do2_handle = TaskHandle(1)
        
        DAQmxCreateTask("",byref(self.do1_handle))
        DAQmxCreateTask("",byref(self.do2_handle))
        
        DAQmxCreateDOChan(self.do1_handle, device1, '', DAQmx_Val_ChanPerLine)
        DAQmxCreateDOChan(self.do2_handle, device2, '', DAQmx_Val_ChanPerLine)
        self.secs1 = secs1
        self.secs2 = secs2
        self.sampsPerChanWritten = int32()
        self.on1 = numpy.uint32([on1])
        self.on2 = numpy.uint32([on2])
        self.off = numpy.uint32([0])
        self.SampsPerChan = 1
        
    def DoTask(self):
        DAQmxStartTask(self.do1_handle)
        DAQmxStartTask(self.do2_handle)
        
        if self.secs1 == self.secs2:
            DAQmxWriteDigitalU32(self.do1_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on1,
                                 byref(self.sampsPerChanWritten), None)
            DAQmxWriteDigitalU32(self.do2_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on2,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(self.secs1)
            DAQmxWriteDigitalU32(self.do1_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.sampsPerChanWritten), None)
            DAQmxWriteDigitalU32(self.do2_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(float(self.secs1/100))
        elif self.secs1 > self.secs2:
            DAQmxWriteDigitalU32(self.do1_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on1,
                                 byref(self.sampsPerChanWritten), None)
            DAQmxWriteDigitalU32(self.do2_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on2,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(self.secs2)
            DAQmxWriteDigitalU32(self.do2_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(self.secs1-self.secs2)
            DAQmxWriteDigitalU32(self.do1_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(float(self.secs1/100))
        elif self.secs2 > self.secs1:
            DAQmxWriteDigitalU32(self.do1_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on1,
                                 byref(self.sampsPerChanWritten), None)
            DAQmxWriteDigitalU32(self.do2_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on2,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(self.secs1)
            DAQmxWriteDigitalU32(self.do1_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(self.secs2-self.secs1)
            DAQmxWriteDigitalU32(self.do2_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(float(self.secs2/100))
        
        self.ClearTask()
        
    def ClearTask(self):
        time.sleep(0.005)
        DAQmxStopTask(self.do1_handle)
        DAQmxStopTask(self.do2_handle)
        
        DAQmxClearTask(self.do1_handle)
        DAQmxClearTask(self.do2_handle)
        

class NiUsbDigitalOut:
    def __init__(self, device, secs, on):
        self.do_handle = TaskHandle(0)

        DAQmxCreateTask("", byref(self.do_handle))

        DAQmxCreateDOChan(self.do_handle, device, '', DAQmx_Val_ChanPerLine)
        self.secs = secs
        self.sampsPerChanWritten = int32()
        self.on = numpy.uint32([on])
        self.off = numpy.uint32([0])
        self.SampsPerChan = 1

    def DoTask(self):
        
        DAQmxStartTask(self.do_handle)
        
        DAQmxWriteDigitalU32(self.do_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on, 
                             byref(self.sampsPerChanWritten), None)
        
        time.sleep(self.secs)
        DAQmxWriteDigitalU32(self.do_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                             byref(self.sampsPerChanWritten), None)
        time.sleep(float(self.secs/100))
        
        self.ClearTasks()

    def ClearTasks(self):
        time.sleep(0.05)
        DAQmxStopTask(self.do_handle)

        DAQmxClearTask(self.do_handle)

class ThreadSafeDigitalOut:
    def __init__(self, device, samprate, secs, write, clock, ai_channels):
        self.do_handle = TaskHandle(0)
        self.ai_handle = TaskHandle(1)
        self.ai_channels = ai_channels
        DAQmxCreateTask("", byref(self.do_handle))
        DAQmxCreateTask("", byref(self.ai_handle))
        
        DAQmxCreateDOChan(self.do_handle, device, '', DAQmx_Val_ChanPerLine)
        DAQmxCreateAIVoltageChan(self.ai_handle, 'Dev2/ai0','', DAQmx_Val_Diff, -10.0, 10.0, DAQmx_Val_Volts, None)
        
        self.ai_read = int32()
        self.sampsPerChanWritten = int32()
        self.write = Util.binary_to_digital_map(write)

        self.totalLength = numpy.uint64(samprate * secs)
        self.analogData = numpy.zeros((self.ai_channels, self.totalLength), dtype=numpy.float64)
        
        DAQmxCfgSampClkTiming(self.ai_handle, '', samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                              numpy.uint64(self.totalLength))
        DAQmxCfgSampClkTiming(self.do_handle, clock, samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                              numpy.uint64(self.totalLength))

    def DoTask(self):
        DAQmxWriteDigitalU32(self.do_handle, self.write.shape[1], 0, -1, DAQmx_Val_GroupByChannel, self.write,
                             byref(self.sampsPerChanWritten), None)
        
        DAQmxStartTask(self.ai_handle)
        DAQmxStartTask(self.do_handle)
        
        DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogData,
                           numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
        
        DAQmxWaitUntilTaskDone(self.do_handle, DAQmx_Val_WaitInfinitely)

        self.ClearTasks()

    def ClearTasks(self):
        time.sleep(0.05)
        DAQmxStopTask(self.do_handle)
        DAQmxStopTask(self.ai_handle)

        DAQmxClearTask(self.do_handle)
        DAQmxClearTask(self.ai_handle)


# region [AnalogTasks]


class AnalogInput(Task):
    def __init__(self, device, channels, samprate, secs, clock=''):
        Task.__init__(self)
        self.CreateAIVoltageChan(device, "", DAQmx_Val_Cfg_Default, -10.0, 10.0, DAQmx_Val_Volts, None)

        self.read = int32()
        self.channels = channels
        self.totalLength = numpy.uint32(samprate * secs)
        self.analogRead = numpy.zeros((channels, self.totalLength), dtype=numpy.float64)

        self.CfgSampClkTiming(clock, samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, numpy.uint64(self.totalLength))
        self.WaitUntilTaskDone(-1)
        self.AutoRegisterDoneEvent(0)

    def DoTask(self):
        self.StartTask()
        self.ReadAnalogF64(self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogRead,
                           self.totalLength * self.channels, byref(self.read), None)

    def DoneCallback(self, status):
        self.StopTask()
        self.ClearTask()
        return 0


class ThreadSafeAnalogInput: #Für Pretraining-Schedule
    def __init__(self, ai_device, channels, samp_rate, secs, clock=''):
        self.ai_handle = TaskHandle(0)

        DAQmxCreateTask("", byref(self.ai_handle))

        DAQmxCreateAIVoltageChan(self.ai_handle, ai_device, "", DAQmx_Val_Diff, -10.0, 10.0, DAQmx_Val_Volts, None)

        self.ai_read = int32()
        self.ai_channels = channels
        self.totalLength = numpy.uint64(samp_rate * secs)
        self.analogData = numpy.zeros((self.ai_channels, self.totalLength), dtype=numpy.float64)

        DAQmxCfgSampClkTiming(self.ai_handle, '', samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                              numpy.uint64(self.totalLength))

    def DoTask(self):
        DAQmxStartTask(self.ai_handle)
        DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogData,
                           numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
        self.ClearTasks()
        return self.analogData

    def ClearTasks(self):
        time.sleep(0.05)
        DAQmxStopTask(self.ai_handle)
        DAQmxClearTask(self.ai_handle)


class TriggeredAnalogInput(Task):
    def __init__(self, device, channels, samprate, secs, trigger_source, clock=''):
        Task.__init__(self)
        self.CreateAIVoltageChan(device, "", DAQmx_Val_Cfg_Default, -10.0, 10.0, DAQmx_Val_Volts, None)

        self.read = int32()
        self.channels = channels
        self.totalLength = numpy.uint32(samprate * secs)
        self.analogRead = numpy.zeros((channels, self.totalLength), dtype=numpy.float64)

        self.CfgSampClkTiming(clock, samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, numpy.uint64(self.totalLength))
        self.WaitUntilTaskDone(-1)
        self.CfgDigEdgeStartTrig(trigger_source, DAQmx_Val_Rising)
        self.AutoRegisterDoneEvent(0)

    def DoTask(self):
        self.StartTask()
        self.ReadAnalogF64(self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogRead,
                           self.totalLength * self.channels, byref(self.read), None)

    def DoneCallback(self, status):
        print(status)
        self.StopTask()
        self.ClearTask()
        return 0


class AnalogOutput(Task):
    def __init__(self, device, samprate, secs, write, clock=''):
        Task.__init__(self)
        self.CreateAOVoltageChan(device, "", -10.0, 10.0, DAQmx_Val_Volts, None)

        self.sampsPerChanWritten = int32()
        self.write = write
        self.totalLength = numpy.uint32(samprate * secs)

        self.CfgSampClkTiming(clock, samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, numpy.uint64(self.totalLength))
        self.AutoRegisterDoneEvent(0)

    def DoTask(self):
        self.WriteAnalogF64(self.write.shape[1], 0, -1, DAQmx_Val_GroupByChannel,
                            self.write, byref(self.sampsPerChanWritten), None)
        self.StartTask()

    def DoneCallback(self, status):
        print(status)
        self.StopTask()
        self.ClearTask()
        return 0


# region [MultiTasks]
class DoAiMultiTask:
    def __init__(self, ai_device, ai_channels, do_device, fv_device, reward_device_l, reward_device_r, samp_rate, secs, odor_write, fv_write, sync_clock, static, thorax_delay, lick_delay, lick_channel_l, lick_channel_r, beam_channel, rewarded):
        self.ai_handle = TaskHandle(0)
        self.do_handle = TaskHandle(1)
        self.fv_handle = TaskHandle(2)
        self.static = static
        self.thorax_delay = thorax_delay
        self.lick_delay = lick_delay
        self.reward_device = [reward_device_l,reward_device_r]
        self.reward_prob = rewarded[0:2]
        self.water = rewarded[2:4]
        self.lick_channel = [lick_channel_l,lick_channel_r]
        self.beam_channel = beam_channel
#        print(self.static,self.thorax_delay,self.lick_delay,self.reward_device,self.reward_prob,self.water,self.lick_channel,self.beam_channel)
        DAQmxCreateTask('', byref(self.ai_handle))
        DAQmxCreateTask('', byref(self.do_handle))
        DAQmxCreateTask('', byref(self.fv_handle))
        
        DAQmxCreateAIVoltageChan(self.ai_handle, ai_device, '', DAQmx_Val_Diff, -5.0, 5.0, DAQmx_Val_Volts, None)
        DAQmxCreateDOChan(self.do_handle, do_device, '', DAQmx_Val_ChanForAllLines)
        DAQmxCreateDOChan(self.fv_handle, fv_device, '', DAQmx_Val_ChanPerLine)
        
        self.ai_read = int32()
        self.ai_channels = ai_channels
        self.odorSampsPerChanWritten = int32()
        self.fvSampsPerChanWritten = int32()
        self.secs = secs
        self.samp_rate = samp_rate
        
        if self.static:
            self.on = numpy.uint32([1])
            self.off = numpy.uint32([0])
            self.valve8on = math.pow(2,8)
            self.valve8on = numpy.uint32([self.valve8on])
            self.onset = odor_write[1]
            self.odor_length = odor_write[2]
            self.offset = odor_write[3]
            
            self.odor_pulse = Util.binary_to_digital_map(odor_write[0])
            self.odorSampsPerChan = self.odor_pulse.shape[1]
            self.odor_pulse = numpy.sum(self.odor_pulse, axis = 0)
            

            self.fv_onset_pulse = fv_write[0]
            self.fvSampsPerChan = fv_write.shape[0]
            
            #print("write : ", self.odor_pulse)
            #print("odor samps :",self.odorSampsPerChan)
            #print("fv samps :", self.fvSampsPerChan)
            
        else:
            self.totalLength = numpy.uint64(samp_rate * secs)
            self.analogData = numpy.zeros((self.ai_channels, self.totalLength), dtype=numpy.float64)
            self.write = numpy.vstack((odor_write,fv_write))
            self.write = Util.binary_to_digital_map(self.write)
            self.SampsPerChan = self.write.shape[1]
            self.write = numpy.sum(self.write, axis=0)
            
            DAQmxCfgSampClkTiming(self.do_handle, sync_clock, samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                  numpy.uint64(self.totalLength))
            DAQmxCfgSampClkTiming(self.ai_handle, '', samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                  numpy.uint64(self.totalLength))

    def DoTask(self):
        
        if self.static:
            """onset"""
#            print('onset')
            self.totalLength = numpy.uint64(self.samp_rate*self.onset)
            self.analogDataOnset = numpy.zeros((self.ai_channels,self.totalLength),dtype=numpy.float64)

            DAQmxStartTask(self.do_handle)
            DAQmxStartTask(self.fv_handle)

            DAQmxWriteDigitalU32(self.do_handle, self.odorSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.odorSampsPerChanWritten), None)
            DAQmxWriteDigitalU32(self.fv_handle, self.fvSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.fvSampsPerChanWritten), None)

            DAQmxStopTask(self.do_handle)
            DAQmxStopTask(self.fv_handle)
            time.sleep(self.onset)
     
            """fvonset"""
            timestamp2 = datetime.datetime.now()
#            print('timestamp2')
            if self.fv_onset_pulse != 0:
                self.totalLength = numpy.uint64(self.samp_rate*self.fv_onset_pulse)
                self.analogDataFvOnset = numpy.zeros((self.ai_channels,self.totalLength),dtype=numpy.float64)
                DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                      numpy.uint64(self.totalLength))
                DAQmxStartTask(self.ai_handle)
                DAQmxStartTask(self.do_handle)
                valve8write = numpy.sum([self.odor_pulse,self.valve8on],axis=0)
                DAQmxWriteDigitalU32(self.do_handle, self.odorSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, valve8write,
                                     byref(self.odorSampsPerChanWritten), None)
                DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataFvOnset,
                                   numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
                DAQmxStopTask(self.ai_handle)
                DAQmxStopTask(self.do_handle)
            else:
                self.analogDataFvOnset = numpy.zeros((self.ai_channels,1),dtype=numpy.float64)
            
            """odor application"""
#            print('odor application')
            self.totalLength = numpy.uint64(self.samp_rate*self.odor_length)
            self.analogDataOdorOn = numpy.zeros((self.ai_channels,self.totalLength),dtype=numpy.float64)
            DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                  numpy.uint64(self.totalLength))
            DAQmxStartTask(self.ai_handle)
            DAQmxStartTask(self.fv_handle)
            DAQmxStartTask(self.do_handle)
            DAQmxWriteDigitalU32(self.fv_handle, self.fvSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on,
                                 byref(self.fvSampsPerChanWritten), None)
            DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataOdorOn,
                               numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
            DAQmxWriteDigitalU32(self.do_handle, self.odorSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                     byref(self.odorSampsPerChanWritten), None)
            DAQmxWriteDigitalU32(self.fv_handle, self.fvSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                     byref(self.fvSampsPerChanWritten), None)
            DAQmxStopTask(self.ai_handle)
            DAQmxStopTask(self.fv_handle)
            DAQmxStopTask(self.do_handle)
            
#            reward.deliver_reward_static('dev1/port2/line1', 0.07)
            
            """odor off, wait for baseline"""
            timestamp1 = datetime.datetime.now()
            if self.thorax_delay != 0:
                self.totalLength = numpy.uint64(self.samp_rate*self.thorax_delay)
                self.analogDataOdorOff = numpy.zeros((self.ai_channels,self.totalLength),dtype=numpy.float64)
                DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                      numpy.uint64(self.totalLength))
                DAQmxStartTask(self.do_handle)
                DAQmxStartTask(self.fv_handle)
                DAQmxStartTask(self.ai_handle)
                DAQmxWriteDigitalU32(self.do_handle, self.odorSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                     byref(self.odorSampsPerChanWritten), None)
                DAQmxWriteDigitalU32(self.fv_handle, self.fvSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                     byref(self.fvSampsPerChanWritten), None)
                DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataOdorOff,
                                   numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read),None)
                DAQmxStopTask(self.do_handle)
                DAQmxStopTask(self.fv_handle)
                DAQmxStopTask(self.ai_handle)
            else:
                self.analogDataOdorOff = numpy.zeros((self.ai_channels,1),dtype=numpy.float64)
            
            #DONE 2 Lick-Ports implementieren.
            check_l = self.analogDataOdorOff[self.lick_channel[0]]
            check_r = self.analogDataOdorOff[self.lick_channel[1]]
#            print(check_l)
#            print(check_r)
##            print(check)
            check_beam = numpy.hstack((self.analogDataFvOnset[self.beam_channel], self.analogDataOdorOn[self.beam_channel]))
#            print(check_beam)
            
            lick_response_l = numpy.zeros(len(check_l))
            lick_response_l[numpy.where(check_l > 2)] = 1
            lick_response_r = numpy.zeros(len(check_r))
            lick_response_r[numpy.where(check_r > 2)] = 1
            
            beam_response = numpy.zeros(len(check_beam))
            beam_response[numpy.where(check_beam > 1)] = 1
            
            if numpy.sum(beam_response) == 0:
                beam = 5
            else:
                beam_nz = numpy.nonzero(beam_response)[0]
                beam = 0
                for i,v in enumerate(beam_nz):
                    if i == 0:
                        beam = beam
                    elif (v-beam_nz[i-1])>1:
                        beam = beam + 1
                if len(beam_response) - 1 > beam_nz[-1]:
                    beam = beam + 1
            
            print('\nbeam : ', str(beam))
            
            if numpy.sum(lick_response_l) == 0:
                licks_l = 0
            else:
                licks_nz_l = numpy.nonzero(lick_response_l)[0]
                licks_l = 0
                for i,v in enumerate(licks_nz_l):
                    if i == 0:
                        licks_l = licks_l + 1
                    elif (v-licks_nz_l[i-1])>1:
                        licks_l = licks_l + 1
            
            if numpy.sum(lick_response_r) == 0:
                licks_r= 0
            else:
                licks_nz_r = numpy.nonzero(lick_response_r)[0]
                licks_r = 0
                for i,v in enumerate(licks_nz_r):
                    if i == 0:
                        licks_r = licks_r + 1
                    elif (v-licks_nz_r[i-1])>1:
                        licks_r = licks_r + 1
            
#            print(licks_l)
#            print(licks_r)
            water_given = [False,False]
            if self.reward_prob[0] > 0 and self.reward_prob[1] == 0:
#                print('a')
                if licks_l > 0 and licks_r == 0 and beam < 2:
#                    print('b')
                    if numpy.random.rand() < self.reward_prob[0]:
                        reward.deliver_reward_static(self.reward_device[0], self.water[0])
                        water_given[0] = True
            if self.reward_prob[0] == 0 and self.reward_prob[1] > 0:
#                print('c')
                if licks_r > 0 and licks_l == 0 and beam < 2:
#                    print('d')
                    if numpy.random.rand() < self.reward_prob[1]:
                        reward.deliver_reward_static(self.reward_device[1], self.water[1])
                        water_given[1] = True
            if self.reward_prob[0] > 0 and self.reward_prob[1] > 0:
#                print('e')
                if licks_l > 0 and licks_r == 0 and beam < 2:
#                    print('f')
                    if numpy.random.rand() < self.reward_prob[0]:
                        reward.deliver_reward_static(self.reward_device[0], self.water[0])
                        water_given[0] = True
                if licks_l == 0 and licks_r > 0 and beam < 2:
#                    print('g')
                    if numpy.random.rand() < self.reward_prob[1]:
                        reward.deliver_reward_static(self.reward_device[1], self.water[1])
                        water_given[1] = True
            
#            print(water_given)
            """read lick"""
            if self.lick_delay != 0:
                self.totalLength = numpy.uint64(self.samp_rate*self.lick_delay)
                self.analogDataLick = numpy.zeros((self.ai_channels,self.totalLength),dtype=numpy.float64)
                DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                      numpy.uint64(self.totalLength))
                DAQmxStartTask(self.ai_handle)
                DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataLick,
                                   numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read),None)
                DAQmxStopTask(self.ai_handle)
            else:
                self.analogDataLick = numpy.zeros((self.ai_channels,1),dtype=numpy.float64)
            
            """offset"""
            self.totalLength = numpy.uint64(self.samp_rate*self.offset)
            self.analogDataOffset = numpy.zeros((self.ai_channels, self.totalLength),dtype=numpy.float64)
            time.sleep(self.offset)
            
            
            """saving analog data and free tasks"""
            analogData = numpy.hstack((self.analogDataOnset,self.analogDataFvOnset,self.analogDataOdorOn,self.analogDataOdorOff, self.analogDataLick, self.analogDataOffset))
            shouldLickData = self.analogDataOdorOff
            waitData = numpy.hstack((self.analogDataFvOnset,self.analogDataOdorOn))
            self.ClearTasks()

            return analogData, waitData, shouldLickData, timestamp1, timestamp2, water_given
            
        
        else:
            #TODO Implement all sequences
            DAQmxWriteDigitalU32(self.do_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.write,
                                 byref(self.odorSampsPerChanWritten), None)
            
            DAQmxStartTask(self.do_handle)
            DAQmxStartTask(self.ai_handle)
            DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogData,
                               numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
            self.ClearTasks()
            return self.analogData
        
    def ClearTasks(self):
        time.sleep(0.05)
        DAQmxStopTask(self.do_handle)
        DAQmxStopTask(self.ai_handle)
        DAQmxStopTask(self.fv_handle)

        DAQmxClearTask(self.do_handle)
        DAQmxClearTask(self.ai_handle)
        DAQmxClearTask(self.fv_handle)

class DoAiMultiTaskWaitTraining:
    def __init__(self, ai_device, ai_channels, do_device, fv_device, reward_device_l, reward_device_r, samp_rate, secs, odor_write, fv_write, sync_clock, static, thorax_delay, lick_delay, lick_channel_l, lick_channel_r, beam_channel, rewarded):
        self.ai_handle = TaskHandle(0)
        self.do_handle = TaskHandle(1)
        self.fv_handle = TaskHandle(2)
        self.static = static
        self.thorax_delay = thorax_delay
        self.lick_delay = lick_delay
        self.reward_device = [reward_device_l, reward_device_r]
        self.reward_prob = rewarded[0:2]
        self.water = rewarded[2:4]
        self.lick_channel = [lick_channel_l,lick_channel_r]
        self.beam_channel = beam_channel
        
        DAQmxCreateTask('', byref(self.ai_handle))
        DAQmxCreateTask('', byref(self.do_handle))
        DAQmxCreateTask('', byref(self.fv_handle))
        
        DAQmxCreateAIVoltageChan(self.ai_handle, ai_device, '', DAQmx_Val_Diff, -5.0, 5.0, DAQmx_Val_Volts, None)
        DAQmxCreateDOChan(self.do_handle, do_device, '', DAQmx_Val_ChanForAllLines)
        DAQmxCreateDOChan(self.fv_handle, fv_device, '', DAQmx_Val_ChanPerLine)
        
        self.ai_read = int32()
        self.ai_channels = ai_channels
        self.odorSampsPerChanWritten = int32()
        self.fvSampsPerChanWritten = int32()
        self.secs = secs
        self.samp_rate = samp_rate
        
        if self.static:
            self.on = numpy.uint32([1])
            self.off = numpy.uint32([0])
            self.valve8on = math.pow(2,8)
            self.valve8on = numpy.uint32([self.valve8on])
            self.onset = odor_write[1]
            self.odor_length = odor_write[2]
            self.offset = odor_write[3]
            
            self.odor_pulse = Util.binary_to_digital_map(odor_write[0])
            self.odorSampsPerChan = self.odor_pulse.shape[1]
            self.odor_pulse = numpy.sum(self.odor_pulse, axis = 0)
            

            self.fv_onset_pulse = fv_write[0]
            self.fvSampsPerChan = fv_write.shape[0]
            
            #print("write : ", self.odor_pulse)
            #print("odor samps :",self.odorSampsPerChan)
            #print("fv samps :", self.fvSampsPerChan)
            
        else:
            self.totalLength = numpy.uint64(samp_rate * secs)
            self.analogData = numpy.zeros((self.ai_channels, self.totalLength), dtype=numpy.float64)
            self.write = numpy.vstack((odor_write,fv_write))
            self.write = Util.binary_to_digital_map(self.write)
            self.SampsPerChan = self.write.shape[1]
            self.write = numpy.sum(self.write, axis=0)
            
            DAQmxCfgSampClkTiming(self.do_handle, sync_clock, samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                  numpy.uint64(self.totalLength))
            DAQmxCfgSampClkTiming(self.ai_handle, '', samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                  numpy.uint64(self.totalLength))

    def DoTask(self):
        
        if self.static:
            """onset"""
            self.totalLength = numpy.uint64(self.samp_rate*self.onset)
            self.analogDataOnset = numpy.zeros((self.ai_channels,self.totalLength),dtype=numpy.float64)

            DAQmxStartTask(self.do_handle)
            DAQmxStartTask(self.fv_handle)

            DAQmxWriteDigitalU32(self.do_handle, self.odorSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.odorSampsPerChanWritten), None)
            DAQmxWriteDigitalU32(self.fv_handle, self.fvSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.fvSampsPerChanWritten), None)

            DAQmxStopTask(self.do_handle)
            DAQmxStopTask(self.fv_handle)
            time.sleep(self.onset)
     
            """fvonset"""
            timestamp_2 = datetime.datetime.now()
            if self.fv_onset_pulse != 0:
                self.totalLength = numpy.uint64(self.samp_rate*self.fv_onset_pulse)
                self.analogDataFvOnset = numpy.zeros((self.ai_channels,self.totalLength),dtype=numpy.float64)
                DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                      numpy.uint64(self.totalLength))
                DAQmxStartTask(self.ai_handle)
                DAQmxStartTask(self.do_handle)
                valve8write = numpy.sum([self.odor_pulse,self.valve8on],axis=0)
                DAQmxWriteDigitalU32(self.do_handle, self.odorSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, valve8write,
                                     byref(self.odorSampsPerChanWritten), None)
                DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataFvOnset,
                                   numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
                DAQmxStopTask(self.ai_handle)
                DAQmxStopTask(self.do_handle)
            else:
                self.analogDataFvOnset = numpy.zeros((self.ai_channels,1),dtype=numpy.float64)
            
            """odor application"""
            self.totalLength = numpy.uint64(self.samp_rate*self.odor_length)
            self.analogDataOdorOn = numpy.zeros((self.ai_channels,self.totalLength),dtype=numpy.float64)
            DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                  numpy.uint64(self.totalLength))
            DAQmxStartTask(self.ai_handle)
            DAQmxStartTask(self.fv_handle)
            DAQmxStartTask(self.do_handle)
            DAQmxWriteDigitalU32(self.fv_handle, self.fvSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on,
                                 byref(self.fvSampsPerChanWritten), None)
            DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataOdorOn,
                               numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
            DAQmxWriteDigitalU32(self.do_handle, self.odorSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.odorSampsPerChanWritten), None)
            DAQmxWriteDigitalU32(self.fv_handle, self.fvSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.fvSampsPerChanWritten), None)
            DAQmxStopTask(self.do_handle)
            DAQmxStopTask(self.ai_handle)
            DAQmxStopTask(self.fv_handle)
            
            check_l = numpy.hstack((self.analogDataFvOnset[self.lick_channel[0]], self.analogDataOdorOn[self.lick_channel[0]]))
            check_r = numpy.hstack((self.analogDataFvOnset[self.lick_channel[1]], self.analogDataOdorOn[self.lick_channel[1]]))
            check_beam = numpy.hstack((self.analogDataFvOnset[self.beam_channel], self.analogDataOdorOn[self.beam_channel]))
            
            wait_lick_response_l = numpy.zeros(len(check_l))
            wait_lick_response_r = numpy.zeros(len(check_r))
            wait_lick_response_l[numpy.where(check_l > 2)] = 1
            wait_lick_response_r[numpy.where(check_r > 2)] = 1
            
            beam_response = numpy.zeros(len(check_beam))
            beam_response[numpy.where(check_beam > 1)] = 1
            
            if numpy.sum(beam_response) == 0:
                beam = 5
            else:
                beam_nz = numpy.nonzero(beam_response)[0]
                beam = 0
                for i,v in enumerate(beam_nz):
                    if i == 0:
                        beam = beam
                    elif (v-beam_nz[i-1])>1:
                        beam = beam + 1
                if len(beam_response) - 1 > beam_nz[-1]:
                    beam = beam + 1
            
            print('\nbeam : ', str(beam))
            
            if numpy.sum(wait_lick_response_l) == 0:
                licks_l = 0
                timestamps_l = 'not licked'
            else:
                licks_nz_l = numpy.nonzero(wait_lick_response_l)[0]
                licks_l = 0
                timestamps_l = list()
                for i,v in enumerate(licks_nz_l):
                    if i == 0:
                        licks_l = licks_l + 1
                        timestamps_l.append(str(v/self.samp_rate))
                    elif (v-licks_nz_l[i-1])>1:
                        licks_l = licks_l + 1
                        timestamps_l.append(str(v/self.samp_rate))
                timestamps_l = '|'.join(timestamps_l)
            
            if numpy.sum(wait_lick_response_r) == 0:
                licks_r = 0
                timestamps_r = 'not licked'
            else:
                licks_nz_r = numpy.nonzero(wait_lick_response_r)[0]
                licks_r = 0
                timestamps_r = list()
                for i,v in enumerate(licks_nz_r):
                    if i == 0:
                        licks_r = licks_r + 1
                        timestamps_r.append(str(v/self.samp_rate))
                    elif (v-licks_nz_r[i-1])>1:
                        licks_r = licks_r + 1
                        timestamps_r.append(str(v/self.samp_rate))
                timestamps_r = '|'.join(timestamps_r)
            
            water_given = [False,False]            
            if self.reward_prob[0] != 0 and self.reward_prob[1] == 0:
                if numpy.random.rand() < self.reward_prob[0]:
                    reward.deliver_reward_static(self.reward_device[0], self.water[0])
                    water_given[0] = True
            elif self.reward_prob[0] == 0 and self.reward_prob[1] != 0:
                if numpy.random.rand() < self.reward_prob[1]:
                    reward.deliver_reward_static(self.reward_device[1], self.water[1])
                    water_given[1] = True
            elif self.reward_prob[0] != 0 and self.reward_prob[1] != 0:
                idx = numpy.random.randint(2) #TODO How about wait training with Reward-Risk?
#                print('idx:', idx)
                if numpy.random.rand() < self.reward_prob[idx]:
                    reward.deliver_reward_static(self.reward_device[idx], self.water[idx])
                    water_given[idx] = True
            
#                if beam < 2 and licks < 16:
#                    reward.deliver_reward_static(self.reward_device, self.water)
#                    water_given = True
            
            """odor off, wait for baseline"""
            if self.thorax_delay != 0:
                self.totalLength = numpy.uint64(self.samp_rate*self.thorax_delay)
                self.analogDataOdorOff = numpy.zeros((self.ai_channels,self.totalLength),dtype=numpy.float64)
                DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                      numpy.uint64(self.totalLength))
                DAQmxStartTask(self.ai_handle)
                DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataOdorOff,
                                   numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read),None)
                DAQmxStopTask(self.ai_handle)
            else:
                self.analogDataOdorOff = numpy.zeros((self.ai_channels,1),dtype=numpy.float64)
            
            """read lick"""
            timestamp_1 = datetime.datetime.now()
            if self.lick_delay != 0:
                self.totalLength = numpy.uint64(self.samp_rate*self.lick_delay)
                self.analogDataLick = numpy.zeros((self.ai_channels,self.totalLength),dtype=numpy.float64)
                DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                      numpy.uint64(self.totalLength))
                DAQmxStartTask(self.ai_handle)
                DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataLick,
                                   numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read),None)
                DAQmxStopTask(self.ai_handle)
            else:
                self.analogDataLick = numpy.zeros((self.ai_channels,1),dtype=numpy.float64)
            
            """offset"""
            self.totalLength = numpy.uint64(self.samp_rate*self.offset)
            self.analogDataOffset = numpy.zeros((self.ai_channels, self.totalLength),dtype=numpy.float64)
            time.sleep(self.offset)
            
            
            """saving analog data and free tasks"""
            analogData = numpy.hstack((self.analogDataOnset,self.analogDataFvOnset,self.analogDataOdorOn,self.analogDataOdorOff, self.analogDataLick, self.analogDataOffset))
            shouldLickData = numpy.hstack((self.analogDataOdorOff, self.analogDataLick))
            waitData = numpy.hstack((self.analogDataFvOnset,self.analogDataOdorOn))
            licks = [licks_l,licks_r]
            timestamps = [timestamps_l, timestamps_r]
            self.ClearTasks()
            
            return analogData, waitData, shouldLickData, timestamp_1, water_given, licks, timestamps, timestamp_2
            
        
        else:
            #TODO Implement all sequences
            DAQmxWriteDigitalU32(self.do_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.write,
                                 byref(self.odorSampsPerChanWritten), None)
            
            DAQmxStartTask(self.do_handle)
            DAQmxStartTask(self.ai_handle)
            DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogData,
                               numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
            self.ClearTasks()
            return self.analogData
        
    def ClearTasks(self):
        time.sleep(0.05)
        DAQmxStopTask(self.do_handle)
        DAQmxStopTask(self.ai_handle)
        DAQmxStopTask(self.fv_handle)

        DAQmxClearTask(self.do_handle)
        DAQmxClearTask(self.ai_handle)
        DAQmxClearTask(self.fv_handle)

class DoAiTriggeredMultiTask:
    def __init__(self, ai_device, ai_channels, do_device, samp_rate, secs, write, sync_clock, trigger_source):
        self.ai_handle = TaskHandle(0)
        self.do_handle = TaskHandle(1)

        DAQmxCreateTask('', byref(self.ai_handle))
        DAQmxCreateTask('', byref(self.do_handle))

        DAQmxCreateAIVoltageChan(self.ai_handle, ai_device, '', DAQmx_Val_Diff, -10.0, 10.0, DAQmx_Val_Volts, None)
        DAQmxCreateDOChan(self.do_handle, do_device, '', DAQmx_Val_ChanForAllLines)
        # DAQmxCfgAnlgEdgeStartTrig(self.ai_handle, trigger_source, DAQmx_Val_RisingSlope, 4.0)
        DAQmxCfgDigEdgeStartTrig(self.ai_handle, trigger_source, DAQmx_Val_Rising)

        self.ai_read = int32()
        self.ai_channels = ai_channels
        self.sampsPerChanWritten = int32()

        self.write = Util.binary_to_digital_map(write)
        self.sampsPerChan = self.write.shape[1]
        self.write = numpy.sum(self.write, axis=0)

        self.totalLength = numpy.uint64(samp_rate * secs)
        self.analogData = numpy.zeros((self.ai_channels, self.totalLength), dtype=numpy.float64)

        DAQmxCfgSampClkTiming(self.ai_handle, '', samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                              numpy.uint64(self.totalLength))
        DAQmxCfgSampClkTiming(self.do_handle, sync_clock, samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                              numpy.uint64(self.totalLength))

    def DoTask(self):
        DAQmxWriteDigitalU32(self.do_handle, self.sampsPerChan, 0, -1, DAQmx_Val_GroupByChannel, self.write,
                             byref(self.sampsPerChanWritten), None)

        DAQmxStartTask(self.do_handle)
        DAQmxStartTask(self.ai_handle)

        DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogData,
                           numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)

        self.ClearTasks()
        return self.analogData

    def ClearTasks(self):
        time.sleep(0.05)
        DAQmxStopTask(self.do_handle)
        DAQmxStopTask(self.ai_handle)

        DAQmxClearTask(self.do_handle)
        DAQmxClearTask(self.ai_handle)


class AoAiMultiTask:
    def __init__(self, ai_device, ai_channels, ao_device, samprate, secs, write, sync_clock):
        self.ai_handle = TaskHandle(0)
        self.ao_handle = TaskHandle(1)

        DAQmxCreateTask("", byref(self.ai_handle))
        DAQmxCreateTask("", byref(self.ao_handle))

        self.sampsPerChanWritten = int32()
        self.write = write
        self.totalLength = numpy.uint32(samprate * secs)

        self.ai_read = int32()
        self.ai_channels = ai_channels
        self.analogData = numpy.zeros((self.ai_channels, self.totalLength), dtype=numpy.float64)

        DAQmxCreateAIVoltageChan(self.ai_handle, ai_device, "", DAQmx_Val_Cfg_Default, -10.0, 10.0, DAQmx_Val_Volts,
                                 None)
        DAQmxCreateAOVoltageChan(self.ao_handle, ao_device, "", -10.0, 10.0, DAQmx_Val_Volts, None)

        DAQmxCfgSampClkTiming(self.ai_handle, '', samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                              numpy.uint64(self.totalLength))
        DAQmxCfgSampClkTiming(self.ao_handle, sync_clock, samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                              numpy.uint64(self.totalLength))

    def DoTask(self):
        DAQmxWriteAnalogF64(self.ao_handle, self.write.shape[1], 0, -1, DAQmx_Val_GroupByChannel,
                            self.write, byref(self.sampsPerChanWritten), None)

        DAQmxStartTask(self.ao_handle)
        DAQmxStartTask(self.ai_handle)

        DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogData,
                           numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)

        self.ClearTasks()
        return self.analogData

    def ClearTasks(self):
        time.sleep(0.05)
        DAQmxStopTask(self.ao_handle)
        DAQmxStopTask(self.ai_handle)

        DAQmxClearTask(self.ao_handle)
        DAQmxClearTask(self.ai_handle)



class MultiTask:
    def __init__(self, ai_device, ai_channels, di_device, di_channels, do_device, samprate, secs, write, sync_clock):
        self.ai_handle = TaskHandle(0)
        self.di_handle = TaskHandle(1)
        self.do_handle = TaskHandle(2)

        DAQmxCreateTask("", byref(self.ai_handle))
        DAQmxCreateTask("", byref(self.di_handle))
        DAQmxCreateTask("", byref(self.do_handle))

        # NOTE - Cfg_Default values may differ for different DAQ hardware
        DAQmxCreateAIVoltageChan(self.ai_handle, ai_device, "", DAQmx_Val_Cfg_Default, -10.0, 10.0, DAQmx_Val_Volts,
                                 None)
        DAQmxCreateDIChan(self.di_handle, di_device, "", DAQmx_Val_ChanPerLine)

        self.ai_read = int32()
        self.di_read = int32()
        self.ai_channels = ai_channels
        self.di_channels = di_channels
        self.totalLength = numpy.uint32(samprate * secs)
        self.analogData = numpy.zeros((self.ai_channels, self.totalLength), dtype=numpy.float64)
        self.digitalData = numpy.ones((self.di_channels, self.totalLength), dtype=numpy.uint32)

        DAQmxCfgSampClkTiming(self.ai_handle, '', samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                              numpy.uint64(self.totalLength))
        DAQmxCfgSampClkTiming(self.di_handle, sync_clock, samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                              numpy.uint64(self.totalLength))

    def DoTask(self):
        DAQmxStartTask(self.di_handle)
        DAQmxStartTask(self.ai_handle)

        DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogData,
                           self.totalLength * self.ai_channels, byref(self.ai_read), None)
        DAQmxReadDigitalU32(self.di_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.digitalData,
                            self.totalLength * self.di_channels, byref(self.di_read), None)



# TODO TESTING #
# region DoAiMultiTaskTest
# a = DoAiMultiTask('cDAQ1Mod3/ai0', 1, 'cDAQ1Mod1/port0/line0', 1000.0, 1.0, numpy.zeros((2, 1000)),
#                   '/cDAQ1/ai/SampleClock')
# analog = a.DoTask()
#
# plt.plot(analog[0])
# plt.show()
# endregion

# region simple digital test
# DigitalOutput test
# a = DigitalOut('cDAQ1Mod1/port0/line0:1', 1, 1000, numpy.zeros((2, 1000)), clock='')
# a.DoTask()

# DigitalInput test
# a = DigitalInput('cDAQ1Mod2/port0/line0', 1, 1000, 1)
# a.DoTask()
# endregion

# MultiTask test
# a = MultiTask('cDAQ1Mod3/ai0', 1, 'cDAQ1Mod2/port0/line0', 1, 'cDAQ1Mod1/port0/line0', 1000, 2, numpy.zeros((1, 2000),
#               dtype=numpy.uint32), '/cDAQ1/ai/SampleClock')
#
# a.DoTask()
#
# plt.plot(a.digitalData[0])
# plt.show()

# AnalogInput
# a = AnalogInput('cDAQ1Mod3/ai0', 1, 1000, 1)
# a.DoTask()
#
# plt.plot(a.analogRead[0])
# plt.show()
