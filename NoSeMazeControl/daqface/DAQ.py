"""

"""
"""
Copyright (c) 2019, 2022 [copyright holders here]

This file is part of NoSeMaze.

NoSeMaze is free software: you can redistribute it and/or 
modify it under the terms of GNU General Public License as 
published by the Free Software Foundation, either version 3 
of the License, or (at your option) at any later version.

NoSeMaze is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public 
License along with NoSeMaze. If not, see https://www.gnu.org/licenses.
"""

from PyDAQmx import *
from ctypes import *

import numpy
import time
import datetime
import math

import daqface.Utils as Util
from HelperFunctions import Reward as reward

# TODO: describe attributes in classes as well? All classes?


class NiUsbDigitalOutTwoDevices:
    """Send digital signals out to two devices simultaneously. For giving 
    reward."""

    def __init__(self, device1: str, device2: str, secs1: float, secs2: float, on1: int, on2: int) -> None:
        """
        Parameters
        ----------
        device1 : str
            Name of 1st device

        device2 : str
            Name of 2nd device

        secs1 : float
            Duration of the ventil 1 should be opened. It is the water amount 
            defined in the schedule. Ventil 1 is left port.

        secs2 : float
            Duration of the ventil 2 should be opened. It is the water amount 
            defined in the schedule. Ventil 2 is right port.

        on1 : int
            On-signal for device 1 (Left port).

        on2 : int
            On-signal for device 2 (Right port).
        """

        self.do1_handle = TaskHandle(0)
        self.do2_handle = TaskHandle(1)

        DAQmxCreateTask("", byref(self.do1_handle))
        DAQmxCreateTask("", byref(self.do2_handle))

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
        # Start task
        DAQmxStartTask(self.do1_handle)
        DAQmxStartTask(self.do2_handle)

        if self.secs1 == self.secs2:
            # Set devices both on
            DAQmxWriteDigitalU32(self.do1_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on1,
                                 byref(self.sampsPerChanWritten), None)
            DAQmxWriteDigitalU32(self.do2_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on2,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(self.secs1)

            # Set devices both off after duration of secs1
            DAQmxWriteDigitalU32(self.do1_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.sampsPerChanWritten), None)
            DAQmxWriteDigitalU32(self.do2_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(float(self.secs1/100))

        elif self.secs1 > self.secs2:
            # Set both devices on
            DAQmxWriteDigitalU32(self.do1_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on1,
                                 byref(self.sampsPerChanWritten), None)
            DAQmxWriteDigitalU32(self.do2_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on2,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(self.secs2)

            # After duration of secs2, set device 2 off.
            DAQmxWriteDigitalU32(self.do2_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(self.secs1-self.secs2)

            # After duration of secs1 from start, set device 1 off.
            DAQmxWriteDigitalU32(self.do1_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(float(self.secs1/100))

        elif self.secs2 > self.secs1:
            # Set both devices on
            DAQmxWriteDigitalU32(self.do1_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on1,
                                 byref(self.sampsPerChanWritten), None)
            DAQmxWriteDigitalU32(self.do2_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on2,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(self.secs1)

            # After duration of secs1, set device 1 off.
            DAQmxWriteDigitalU32(self.do1_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(self.secs2-self.secs1)

            # After duration of secs2 from start time, set device 2 off.
            DAQmxWriteDigitalU32(self.do2_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.sampsPerChanWritten), None)
            time.sleep(float(self.secs2/100))

        self.ClearTask()

    def ClearTask(self):
        """Stop task and clear it."""

        time.sleep(0.005)
        DAQmxStopTask(self.do1_handle)
        DAQmxStopTask(self.do2_handle)

        DAQmxClearTask(self.do1_handle)
        DAQmxClearTask(self.do2_handle)

class NiUsbDigitalOut:
    """Send digital signal out to one device."""

    def __init__(self, device: str, secs: float, on: int) -> None:
        """
        Parameters
        ----------
        device : str
            Name of device

        secs : float
            Duration of on-signal.

        on : int
            Signal to send to channel.
        """
        self.do_handle = TaskHandle(0)

        DAQmxCreateTask("", byref(self.do_handle))

        DAQmxCreateDOChan(self.do_handle, device, '', DAQmx_Val_ChanPerLine)
        self.secs = secs
        self.sampsPerChanWritten = int32()
        self.on = numpy.uint32([on])
        self.off = numpy.uint32([0])
        self.SampsPerChan = 1

    def DoTask(self):
        """Start task and execute sequence"""

        # Start task
        DAQmxStartTask(self.do_handle)

        # Set signal on
        DAQmxWriteDigitalU32(self.do_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on,
                             byref(self.sampsPerChanWritten), None)
        time.sleep(self.secs)

        # Set signal off after duration of secs
        DAQmxWriteDigitalU32(self.do_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                             byref(self.sampsPerChanWritten), None)
        time.sleep(float(self.secs/100))

        self.ClearTasks()

    def ClearTasks(self):
        """Stop task and clear it"""

        time.sleep(0.05)
        DAQmxStopTask(self.do_handle)
        DAQmxClearTask(self.do_handle)

class ThreadSafeAnalogInput:
    """Read thread safe analog input."""

    def __init__(self, ai_device: str, channels: int, samp_rate: int, secs: float, clock: str = '') -> None:
        """
        Parameters
        ----------
        ai_device : str
            Name of analog input device

        channels : int
            Number of analog input read.

        samp_rate : int
            Sample rate defined in hardware configuration.

        secs : float
            Duration of reading data in seconds.

        clock : str
            Clock preferred to be used.
        """

        self.ai_handle = TaskHandle(0)

        DAQmxCreateTask("", byref(self.ai_handle))

        DAQmxCreateAIVoltageChan(
            self.ai_handle, ai_device, "", DAQmx_Val_Diff, -10.0, 10.0, DAQmx_Val_Volts, None)

        self.ai_read = int32()
        self.ai_channels = channels
        self.totalLength = numpy.uint64(samp_rate * secs)
        self.analogData = numpy.zeros(
            (self.ai_channels, self.totalLength), dtype=numpy.float64)

        DAQmxCfgSampClkTiming(self.ai_handle, '', samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                              numpy.uint64(self.totalLength))

    def DoTask(self):
        """
        Start task and read input.

        Return
        ------
        analogData : ndarray
            Data measured.
        """

        DAQmxStartTask(self.ai_handle)
        DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogData,
                           numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
        self.ClearTasks()

        return self.analogData

    def ClearTasks(self):
        """Stop task and clear it"""

        time.sleep(0.05)
        DAQmxStopTask(self.ai_handle)
        DAQmxClearTask(self.ai_handle)

class ThreadSafeDigitalOut:
    """Send thread safe digital signal out to a device."""

    def __init__(self, device: str, samprate: int, secs: float, write: numpy.ndarray, clock: str, ai_channels: int) -> None:
        """
        Parameters
        ----------
        device : str
            Name of device

        samprate : int
            Sample rate. Defined in hardware preference window.

        secs : float
            Duration of on-signal.

        write : binary
            Signal to be written on the channel.

        clock : str
            Clock preferred. Usually the clock of analog input.

        ai_channels : int
            Number of analog input channels.
        """

        self.do_handle = TaskHandle(0)
        self.ai_handle = TaskHandle(1)
        self.ai_channels = ai_channels
        DAQmxCreateTask("", byref(self.do_handle))
        DAQmxCreateTask("", byref(self.ai_handle))

        DAQmxCreateDOChan(self.do_handle, device, '', DAQmx_Val_ChanPerLine)
        DAQmxCreateAIVoltageChan(
            self.ai_handle, 'Dev2/ai0', '', DAQmx_Val_Diff, -10.0, 10.0, DAQmx_Val_Volts, None)

        self.ai_read = int32()
        self.sampsPerChanWritten = int32()
        self.write = Util.binary_to_digital_map(write)

        self.totalLength = numpy.uint64(samprate * secs)
        self.analogData = numpy.zeros(
            (self.ai_channels, self.totalLength), dtype=numpy.float64)

        DAQmxCfgSampClkTiming(self.ai_handle, '', samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                              numpy.uint64(self.totalLength))
        DAQmxCfgSampClkTiming(self.do_handle, clock, samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                              numpy.uint64(self.totalLength))

    def DoTask(self):
        """Start task and execute sequence"""

        # Initialise digital output
        DAQmxWriteDigitalU32(self.do_handle, self.write.shape[1], 0, -1, DAQmx_Val_GroupByChannel, self.write,
                             byref(self.sampsPerChanWritten), None)

        # Start task
        DAQmxStartTask(self.ai_handle)
        DAQmxStartTask(self.do_handle)

        # Set analog read
        DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogData,
                           numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)

        # Wait until analog read is finished
        DAQmxWaitUntilTaskDone(self.do_handle, DAQmx_Val_WaitInfinitely)

        self.ClearTasks()

    def ClearTasks(self):
        """Stop task and clear it"""

        time.sleep(0.05)
        DAQmxStopTask(self.do_handle)
        DAQmxStopTask(self.ai_handle)

        DAQmxClearTask(self.do_handle)
        DAQmxClearTask(self.ai_handle)

class ThreadSafeDigitalInput:
    """Read thread safe digital input. Used for checking the light beam"""

    def __init__(self, beam_channel : str) -> None:
        """
        Parameters
        ----------
        beam_channel : str
            String of digital input channel for beam input

        """
        
        self.task = Task()
        lines = 10
        
        #TODO: Get port from hardware pref UI
        self.task.CreateDIChan(beam_channel, "", DAQmx_Val_ChanPerLine)

        # Array to read samples into
        self.data = numpy.zeros((lines,), dtype=numpy.uint8)
        # Number of samples requested
        self.samples = lines
        # Number of read samples
        self.n = int32()
        
        

    def DoTask(self):
        """
        Start task and read input.

        Return
        ------
        data : ndarray
            Data measured.
        """

        self.task.StartTask()
        self.task.ReadDigitalLines(self.samples, 1.0, 
            DAQmx_Val_GroupByChannel, self.data, self.samples, byref(self.n), None, None)
        self.ClearTasks()

        values = self.data.tolist()
        print("Digital input values:", values)

        return self.data

    def ClearTasks(self):
        """Stop task and clear it"""

        time.sleep(0.05)
        self.task.StopTask()
        self.task.ClearTask()

class DoAiMultiTask:
    """DAQ for normal GNG or risk trial"""
    #TODO: Change analog data to digital data

    def __init__(self, ai_device: str, ai_channels: int, do_device: str, fv_device: str,
                 reward_device_l: str, reward_device_r: str, samp_rate: int, secs: float, odor_write: list[object],
                 fv_write: numpy.ndarray, sync_clock: str, static: bool, wait_delay: float, lick_delay: float,
                 lick_channel_l: int, lick_channel_r: int, rewarded: list[float]):
        """
        Parameters
        ----------
        ai_device : str
            Name of analog device

        ai_channels : int
            Number of analog input channels.

        do_device : str
            Name of digital output device

        fv_device : str
            Name of digital output device to final falve.

        reward_device_l : str
            Name of digital output device to ventil on left port.

        reward_device_r : str
            Name of digital output device to ventil on right port.

        samp_rate : int
            Sample rate defined in hardware configuration.

        secs : float
            Duration of total analog input is read. It is not used under
            'static' option.

        odor_write : list of objects
            Odor pulses and durations of trial segments. [odor_pulses, onset, duration, offset]

        fv_write : ndarray
            Duration of delay before final valve is turned on.

        sync_clock : str
            Clock preferred for synchronisation.

        static : bool
            Indicator if 'static' option is used.

        wait_delay : float
            Obsolete.

        lick_delay : float
            Window to see if port is licked after water.

        lick_channel_l : int
            Index of channel of analog input of left port.

        lick_channel_r : int
            Index of channel of analog input of right port.

        rewarded : list
            List of reward parameters (reward probability and amount of 
            reward.)
        """

        self.ai_handle = TaskHandle(0)
        self.do_handle = TaskHandle(1)
        self.fv_handle = TaskHandle(2)
        self.static = static
        self.wait_delay = 0
        self.lick_delay = lick_delay
        self.reward_device = [reward_device_l, reward_device_r]
        self.reward_prob = rewarded[0:2]
        self.water = rewarded[2:4]
        self.lick_channel = [lick_channel_l, lick_channel_r]

        DAQmxCreateTask('', byref(self.ai_handle))
        DAQmxCreateTask('', byref(self.do_handle))
        DAQmxCreateTask('', byref(self.fv_handle))

        DAQmxCreateAIVoltageChan(
            self.ai_handle, ai_device, '', DAQmx_Val_Diff, -5.0, 5.0, DAQmx_Val_Volts, None)
        DAQmxCreateDOChan(self.do_handle, do_device,
                          '', DAQmx_Val_ChanForAllLines)
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
            self.valve8on = numpy.uint32([math.pow(2, 7)])
            self.onset = odor_write[1]
            self.odor_length = odor_write[2]
            self.offset = odor_write[3]

            self.odor_pulse = Util.binary_to_digital_map(odor_write[0])
            self.odorSampsPerChan = self.odor_pulse.shape[1]
            self.odor_pulse = numpy.sum(self.odor_pulse, axis=0)

            self.fv_onset_pulse = fv_write[0]
            self.fvSampsPerChan = fv_write.shape[0]


    def CheckLicks(self):
        """
        Check if reward should be given.

        Returns
        -------
        water_given : list
            List of indicator if water is given at left port and/or right port.
        """

        check_l = numpy.hstack(
            (self.analogDataOdorOn[self.lick_channel[0]], self.analogDataLickWindow[self.lick_channel[0]]))
        check_r = numpy.hstack(
            (self.analogDataOdorOn[self.lick_channel[1]], self.analogDataLickWindow[self.lick_channel[1]]))


        lick_response_l = numpy.zeros(len(check_l))
        lick_response_l[numpy.where(check_l > 2)] = 1
        lick_response_r = numpy.zeros(len(check_r))
        lick_response_r[numpy.where(check_r > 2)] = 1

        if numpy.sum(lick_response_l) == 0:
            licks_l = 0
        else:
            licks_nz_l = numpy.nonzero(lick_response_l)[0]
            licks_l = 0
            for i, v in enumerate(licks_nz_l):
                if i == 0:
                    licks_l = licks_l + 1
                elif (v-licks_nz_l[i-1]) > 1:
                    licks_l = licks_l + 1

        if numpy.sum(lick_response_r) == 0:
            licks_r = 0
        else:
            licks_nz_r = numpy.nonzero(lick_response_r)[0]
            licks_r = 0
            for i, v in enumerate(licks_nz_r):
                if i == 0:
                    licks_r = licks_r + 1
                elif (v-licks_nz_r[i-1]) > 1:
                    licks_r = licks_r + 1

        # region [GNG two ports]
        # GNG two ports
        water_given = [False, False]
        random_num = numpy.random.rand()
        if self.reward_prob[0] == 0 and self.reward_prob[1] > 0:
            if licks_r > 0:
                if random_num <= self.reward_prob[1]:
                    reward.deliver_reward_static(
                        self.reward_device[1], self.water[1])
                    water_given[1] = True
        elif self.reward_prob[0] > 0 and self.reward_prob[1] == 0:
            if licks_l > 0:
                if random_num <= self.reward_prob[0]:
                    reward.deliver_reward_static(
                        self.reward_device[0], self.water[0])
                    water_given[0] = True
        elif self.reward_prob[0] > 0 and self.reward_prob[1] > 0:
            if self.reward_prob[0] >= self.reward_prob[1]-0.000001 and self.reward_prob[0] <= self.reward_prob[1]+0.000001:
                if licks_l > 0 or licks_r > 0:
                    if random_num <= 0.5:
                        reward.deliver_reward_static(
                            self.reward_device[0], self.water[0])
                        water_given[0] = True
                    else:
                        reward.deliver_reward_static(
                            self.reward_device[1], self.water[1])
                        water_given[1] = True
            elif licks_l > 0 and licks_r == 0:
                if random_num <= self.reward_prob[0]:
                    reward.deliver_reward_static(
                        self.reward_device[0], self.water[0])
                    water_given[0] = True
            elif licks_l == 0 and licks_r > 0:
                if random_num <= self.reward_prob[1]:
                    reward.deliver_reward_static(
                        self.reward_device[1], self.water[1])
                    water_given[1] = True
        # endregion

        return water_given

    def DoTask(self):
        """
        Start task and execute sequences.

        Returns
        -------
        analogData : ndarray
            All measured data read during the trial

        waitData : ndarray
            Measured data read during the wait window

        shouldLickData : ndarray
            Measured data read durign the lick window

        timestamp1 : datetime.datetime
            Timestamp of the start of odour presentation

        timestamp2 : datetime.datetime
            Timestamp of the start of trial.

        water_given : list
            List of indicator if water are given on left port or right port.
        """

        if self.static:
            """onset"""
            # print('onset')
            self.totalLength = numpy.uint64(self.samp_rate*self.onset)
            self.analogDataOnset = numpy.zeros(
                (self.ai_channels, self.totalLength), dtype=numpy.float64)

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

            if self.fv_onset_pulse != 0:
                self.totalLength = numpy.uint64(
                    self.samp_rate*self.fv_onset_pulse)
                self.analogDataFvOnset = numpy.zeros(
                    (self.ai_channels, self.totalLength), dtype=numpy.float64)
                DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                      numpy.uint64(self.totalLength))
                DAQmxStartTask(self.ai_handle)
                DAQmxStartTask(self.do_handle)
                valve8write = numpy.sum(
                    [self.odor_pulse, self.valve8on], axis=0)
                DAQmxWriteDigitalU32(self.do_handle, self.odorSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, valve8write,
                                     byref(self.odorSampsPerChanWritten), None)
                DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataFvOnset,
                                   numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
                DAQmxStopTask(self.ai_handle)
                DAQmxStopTask(self.do_handle)
            else:
                self.analogDataFvOnset = numpy.zeros(
                    (self.ai_channels, 1), dtype=numpy.float64)

            """odor application"""
            DAQmxStartTask(self.fv_handle)
            DAQmxWriteDigitalU32(self.fv_handle, self.fvSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on,
                                 byref(self.fvSampsPerChanWritten), None)
            DAQmxStopTask(self.fv_handle)

            """wait delay"""
            if self.wait_delay > 0.01:
                self.totalLength = numpy.uint64(
                    self.samp_rate*self.wait_delay)
                self.analogDataOdorOn = numpy.zeros(
                    (self.ai_channels, self.totalLength), dtype=numpy.float64)
                DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                      numpy.uint64(self.totalLength))
                DAQmxStartTask(self.ai_handle)
                DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataOdorOn,
                                   numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
                DAQmxStopTask(self.ai_handle)
            else:
                self.analogDataOdorOn = numpy.zeros(
                    (self.ai_channels, 1), dtype=numpy.float64)

            """lick window"""
            timestamp1 = datetime.datetime.now()
            if self.odor_length != 0:
                self.totalLength = numpy.uint64(
                    self.samp_rate*self.odor_length)
                self.analogDataLickWindow = numpy.zeros(
                    (self.ai_channels, self.totalLength), dtype=numpy.float64)
                DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                      numpy.uint64(self.totalLength))
                DAQmxStartTask(self.ai_handle)
                DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataLickWindow,
                                   numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
                DAQmxStopTask(self.ai_handle)
            else:
                self.analogDataLickWindow = numpy.zeros(
                    (self.ai_channels, 1), dtype=numpy.float64)

            water_given = self.CheckLicks()

            DAQmxStartTask(self.do_handle)
            DAQmxStartTask(self.fv_handle)
            DAQmxWriteDigitalU32(self.do_handle, self.odorSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.odorSampsPerChanWritten), None)
            DAQmxWriteDigitalU32(self.fv_handle, self.fvSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.fvSampsPerChanWritten), None)
            DAQmxStopTask(self.fv_handle)
            DAQmxStopTask(self.do_handle)

            """after lick window"""
            if self.lick_delay != 0:
                self.totalLength = numpy.uint64(self.samp_rate*self.lick_delay)
                self.analogDataLick = numpy.zeros(
                    (self.ai_channels, self.totalLength), dtype=numpy.float64)
                DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                      numpy.uint64(self.totalLength))

                DAQmxStartTask(self.ai_handle)
                DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataLick,
                                   numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)

                DAQmxStopTask(self.ai_handle)
            else:
                self.analogDataLick = numpy.zeros(
                    (self.ai_channels, 1), dtype=numpy.float64)

            """offset"""
            self.totalLength = numpy.uint64(self.samp_rate*self.offset)
            self.analogDataOffset = numpy.zeros(
                (self.ai_channels, self.totalLength), dtype=numpy.float64)
            time.sleep(self.offset)

            """saving analog data and free tasks"""
            analogData = numpy.hstack((self.analogDataOnset, self.analogDataFvOnset, self.analogDataOdorOn,
                                      self.analogDataLickWindow, self.analogDataLick, self.analogDataOffset))
            shouldLickData = numpy.hstack(
                (self.analogDataOdorOn, self.analogDataLickWindow, self.analogDataLick))
            waitData = self.analogDataFvOnset
            self.ClearTasks()

            return analogData, waitData, shouldLickData, timestamp1, timestamp2, water_given


    def ClearTasks(self):
        """Stop task and clear it."""

        time.sleep(0.05)
        DAQmxStopTask(self.do_handle)
        DAQmxStopTask(self.ai_handle)
        DAQmxStopTask(self.fv_handle)

        DAQmxClearTask(self.do_handle)
        DAQmxClearTask(self.ai_handle)
        DAQmxClearTask(self.fv_handle)

class DoAiMultiTaskOdourTraining:
    """DAQ for normal GNG odor association training. That is reward is always given after 
    odor presentation regardless of performance."""
    
    #TODO: Change analog data to digital data
    def __init__(self, ai_device, ai_channels, do_device, fv_device,
                 reward_device_l, reward_device_r, samp_rate, secs,
                 odor_write, fv_write, sync_clock, static, thorax_delay,
                 lick_delay, lick_channel_l, lick_channel_r, rewarded):
        """
        Parameters
        ----------
        ai_device : str
            Name of analog device

        ai_channels : int
            Number of analog input channels.

        do_device : str
            Name of digital output device

        fv_device : str
            Name of digital output device to final falve.

        reward_device_l : str
            Name of digital output device to ventil on left port.

        reward_device_r : str
            Name of digital output device to ventil on right port.

        samp_rate : int
            Sample rate defined in hardware configuration.

        secs : float
            Duration of total analog input is read. It is not used under
            'static' option.

        odor_write : float
            Duration of odour should be presented.

        fv_write : float
            Duration of delay before final valve is turned on.

        sync_clock : str
            Clock preferred for synchronisation.

        static : bool
            Indicator if 'static' option is used.

        lick_channel_l : int
            Index of channel of analog input of left port.

        lick_channel_r : int
            Index of channel of analog input of right port.

        rewarded : list
            List of reward parameters (reward probability and amount of 
            reward.)
        """

        self.ai_handle = TaskHandle(0)
        self.do_handle = TaskHandle(1)
        self.fv_handle = TaskHandle(2)
        self.static = static
        self.thorax_delay = thorax_delay
        self.lick_delay = lick_delay
        self.reward_device = [reward_device_l, reward_device_r]
        self.reward_prob = rewarded[0:2]
        self.water = rewarded[2:4]
        self.lick_channel = [lick_channel_l, lick_channel_r]

        DAQmxCreateTask('', byref(self.ai_handle))
        DAQmxCreateTask('', byref(self.do_handle))
        DAQmxCreateTask('', byref(self.fv_handle))

        DAQmxCreateAIVoltageChan(
            self.ai_handle, ai_device, '', DAQmx_Val_Diff, -5.0, 5.0, DAQmx_Val_Volts, None)
        DAQmxCreateDOChan(self.do_handle, do_device,
                          '', DAQmx_Val_ChanForAllLines)
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
            self.valve8on = math.pow(2, 7)
            self.valve8on = numpy.uint32([self.valve8on])
            self.onset = odor_write[1]
            self.odor_length = self.thorax_delay
            if self.odor_length < 0.01:
                self.odor_length = 0.01
            self.thorax_delay = odor_write[2] - self.thorax_delay
            self.offset = odor_write[3]

            self.odor_pulse = Util.binary_to_digital_map(odor_write[0])
            self.odorSampsPerChan = self.odor_pulse.shape[1]
            self.odor_pulse = numpy.sum(self.odor_pulse, axis=0)

            self.fv_onset_pulse = fv_write[0]
            self.fvSampsPerChan = fv_write.shape[0]

    def CheckLicks(self):
        """
        Check how reward should be presented. Reward is always given after 
        odor presentation regardless of performance.

        Returns
        -------
        licks_l : int
            Number of licks in lick window at left port during trial.

        licks_r : int
            Number of licks in lick window at right port during trial.

        timestamps_l: list
            Timestamps of licks in lick window.

        timestamps_r : list
            Timestamps of licks in lick window.

        water_given : list
            List of indicator if water is given at left port and/or right port.
        """
        check_wait_l = self.analogDataOdorOn[self.lick_channel[0]]
        check_wait_r = self.analogDataOdorOn[self.lick_channel[1]]
        check_l = self.analogDataLickWindow[self.lick_channel[0]]
        check_r = self.analogDataLickWindow[self.lick_channel[1]]

        lick_response_l = numpy.zeros(len(check_l))
        lick_response_r = numpy.zeros(len(check_r))
        lick_response_l[numpy.where(check_l > 2)] = 1
        lick_response_r[numpy.where(check_r > 2)] = 1

        wait_lick_response_l = numpy.zeros(len(check_wait_l))
        wait_lick_response_r = numpy.zeros(len(check_wait_r))
        wait_lick_response_l[numpy.where(check_wait_l > 2)] = 1
        wait_lick_response_r[numpy.where(check_wait_r > 2)] = 1

        if numpy.sum(wait_lick_response_l) == 0:
            wait_licks_l = 0
            timestamps_l = 'not licked'
        else:
            wait_licks_nz_l = numpy.nonzero(wait_lick_response_l)[0]
            wait_licks_l = 0
            wait_timestamps_l = list()
            for i, v in enumerate(wait_licks_nz_l):
                if i == 0:
                    wait_licks_l = wait_licks_l + 1
                    wait_timestamps_l.append(str(v/self.samp_rate))
                elif (v-wait_licks_nz_l[i-1]) > 1:
                    wait_licks_l = wait_licks_l + 1
                    wait_timestamps_l.append(str(v/self.samp_rate))
            wait_timestamps_l = '|'.join(wait_timestamps_l)

        if numpy.sum(wait_lick_response_r) == 0:
            wait_licks_r = 0
            wait_timestamps_r = 'not licked'
        else:
            wait_licks_nz_r = numpy.nonzero(wait_lick_response_r)[0]
            wait_licks_r = 0
            wait_timestamps_r = list()
            for i, v in enumerate(wait_licks_nz_r):
                if i == 0:
                    wait_licks_r = wait_licks_r + 1
                    wait_timestamps_r.append(str(v/self.samp_rate))
                elif (v-wait_licks_nz_r[i-1]) > 1:
                    wait_licks_r = wait_licks_r + 1
                    wait_timestamps_r.append(str(v/self.samp_rate))
            wait_timestamps_r = '|'.join(wait_timestamps_r)

        if numpy.sum(lick_response_l) == 0:
            licks_l = 0
            timestamps_l = 'not licked'
        else:
            licks_nz_l = numpy.nonzero(lick_response_l)[0]
            licks_l = 0
            timestamps_l = list()
            for i, v in enumerate(licks_nz_l):
                if i == 0:
                    licks_l = wait_licks_l + 1
                    timestamps_l.append(str(v/self.samp_rate))
                elif (v-licks_nz_l[i-1]) > 1:
                    licks_l = licks_l + 1
                    timestamps_l.append(str(v/self.samp_rate))
            timestamps_l = '|'.join(timestamps_l)

        if numpy.sum(lick_response_r) == 0:
            licks_r = 0
            timestamps_r = 'not licked'
        else:
            licks_nz_r = numpy.nonzero(lick_response_r)[0]
            licks_r = 0
            timestamps_r = list()
            for i, v in enumerate(licks_nz_r):
                if i == 0:
                    licks_r = licks_r + 1
                    timestamps_r.append(str(v/self.samp_rate))
                elif (v-licks_nz_r[i-1]) > 1:
                    licks_r = licks_r + 1
                    timestamps_r.append(str(v/self.samp_rate))
            timestamps_r = '|'.join(timestamps_r)

        water_given = [False, False]
        if self.reward_prob[0] > 0 and self.reward_prob[1] == 0:
            reward.deliver_reward_static(self.reward_device[0], self.water[0])
            water_given[0] = True
        elif self.reward_prob[0] == 0 and self.reward_prob[1] > 0:
            reward.deliver_reward_static(self.reward_device[1], self.water[1])
            water_given[1] = True
        elif self.reward_prob[0] > 0 and self.reward_prob[1] > 0:
            # GNG one port
            # reward.deliver_reward_static(self.reward_device[0], self.water[0])
            # water_given[0] = True
            # reward.deliver_reward_static(self.reward_device[1], self.water[1])
            # water_given[1] = True

            # GNG two ports
            if numpy.random.rand() < 0.5:
                reward.deliver_reward_static(
                    self.reward_device[0], self.water[0])
                water_given[0] = True
            else:
                reward.deliver_reward_static(
                    self.reward_device[1], self.water[1])
                water_given[1] = True

        return licks_l, licks_r, timestamps_l, timestamps_r, water_given

    def DoTask(self):
        """
        Start task and execute sequences.

        Returns
        -------
        analogData : ndarray
            All measured data read during the trial

        waitData : ndarray
            Measured data read during the wait window

        shouldLickData : ndarray
            Measured data read durign the lick window

        timestamp_1 : datetime.datetime
            Timestamp of the start of odour presentation

        water_given : list
            List of indicator if water are given on left port or right port.

        licks : list of int
            List of number of licks at left port and right port.

        timestamps : 2d-list
            List of timestamps of licks at left port and right port.

        timestamp_2 : datetime.datetime
            Timestamp of the start of trial.
        """

        if self.static:
            """onset"""
            self.totalLength = numpy.uint64(self.samp_rate*self.onset)
            self.analogDataOnset = numpy.zeros(
                (self.ai_channels, self.totalLength), dtype=numpy.float64)

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
            DAQmxStartTask(self.do_handle)
            valve8write = numpy.sum([self.odor_pulse, self.valve8on], axis=0)
            DAQmxWriteDigitalU32(self.do_handle, self.odorSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, valve8write,
                                 byref(self.odorSampsPerChanWritten), None)
            DAQmxStopTask(self.do_handle)

            if self.fv_onset_pulse != 0:
                self.totalLength = numpy.uint64(
                    self.samp_rate*self.fv_onset_pulse)
                self.analogDataFvOnset = numpy.zeros(
                    (self.ai_channels, self.totalLength), dtype=numpy.float64)
                DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                      numpy.uint64(self.totalLength))
                DAQmxStartTask(self.ai_handle)

                DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataFvOnset,
                                   numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
                DAQmxStopTask(self.ai_handle)

            else:
                self.analogDataFvOnset = numpy.zeros(
                    (self.ai_channels, 1), dtype=numpy.float64)

            """odor application"""
            DAQmxStartTask(self.fv_handle)
            DAQmxWriteDigitalU32(self.fv_handle, self.fvSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.on,
                                 byref(self.fvSampsPerChanWritten), None)
            DAQmxStopTask(self.fv_handle)
            if self.odor_length > 0.01:
                self.totalLength = numpy.uint64(
                    self.samp_rate*self.odor_length)
                self.analogDataOdorOn = numpy.zeros(
                    (self.ai_channels, self.totalLength), dtype=numpy.float64)
                DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                      numpy.uint64(self.totalLength))
                DAQmxStartTask(self.ai_handle)
                DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataOdorOn,
                                   numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
                DAQmxStopTask(self.ai_handle)

            else:
                self.analogDataOdorOn = numpy.zeros(
                    (self.ai_channels, 1), dtype=numpy.float64)

            """lick window"""
            if self.thorax_delay != 0:
                self.totalLength = numpy.uint64(
                    self.samp_rate*self.thorax_delay)
                self.analogDataLickWindow = numpy.zeros(
                    (self.ai_channels, self.totalLength), dtype=numpy.float64)
                DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                      numpy.uint64(self.totalLength))
                DAQmxStartTask(self.ai_handle)

                DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataLickWindow,
                                   numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)

                DAQmxStopTask(self.ai_handle)

            else:
                self.analogDataLickWindow = numpy.zeros(
                    (self.ai_channels, 1), dtype=numpy.float64)

            licks_l, licks_r, timestamps_l, timestamps_r, water_given = self.CheckLicks()

            DAQmxStartTask(self.fv_handle)
            DAQmxStartTask(self.do_handle)
            DAQmxWriteDigitalU32(self.do_handle, self.odorSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.odorSampsPerChanWritten), None)
            DAQmxWriteDigitalU32(self.fv_handle, self.fvSampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.off,
                                 byref(self.fvSampsPerChanWritten), None)
            DAQmxStopTask(self.fv_handle)
            DAQmxStopTask(self.do_handle)

            """read lick"""
            timestamp_1 = datetime.datetime.now()
            if self.lick_delay != 0:
                self.totalLength = numpy.uint64(self.samp_rate*self.lick_delay)
                self.analogDataLick = numpy.zeros(
                    (self.ai_channels, self.totalLength), dtype=numpy.float64)
                DAQmxCfgSampClkTiming(self.ai_handle, '', self.samp_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                                      numpy.uint64(self.totalLength))
                DAQmxStartTask(self.ai_handle)
                DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogDataLick,
                                   numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
                DAQmxStopTask(self.ai_handle)
            else:
                self.analogDataLick = numpy.zeros(
                    (self.ai_channels, 1), dtype=numpy.float64)

            """offset"""
            self.totalLength = numpy.uint64(self.samp_rate*self.offset)
            self.analogDataOffset = numpy.zeros(
                (self.ai_channels, self.totalLength), dtype=numpy.float64)
            time.sleep(self.offset)

            """saving analog data and free tasks"""
            analogData = numpy.hstack((self.analogDataOnset, self.analogDataFvOnset, self.analogDataOdorOn,
                                      self.analogDataLickWindow, self.analogDataLick, self.analogDataOffset))
            shouldLickData = numpy.hstack(
                (self.analogDataLickWindow, self.analogDataLick))
            waitData = self.analogDataOdorOn
            licks = [licks_l, licks_r]
            timestamps = [timestamps_l, timestamps_r]
            self.ClearTasks()

            return analogData, waitData, shouldLickData, timestamp_1, water_given, licks, timestamps, timestamp_2

        else:
            # TODO Implement all sequences if not using static NI board
            DAQmxWriteDigitalU32(self.do_handle, self.SampsPerChan, False, -1, DAQmx_Val_GroupByChannel, self.write,
                                 byref(self.odorSampsPerChanWritten), None)

            DAQmxStartTask(self.do_handle)
            DAQmxStartTask(self.ai_handle)
            DAQmxReadAnalogF64(self.ai_handle, self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogData,
                               numpy.uint32(self.ai_channels*self.totalLength), byref(self.ai_read), None)
            self.ClearTasks()
            return self.analogData

    def ClearTasks(self):
        """Stop task then clear it"""

        time.sleep(0.05)
        DAQmxStopTask(self.do_handle)
        DAQmxStopTask(self.ai_handle)
        DAQmxStopTask(self.fv_handle)

        DAQmxClearTask(self.do_handle)
        DAQmxClearTask(self.ai_handle)
        DAQmxClearTask(self.fv_handle)
