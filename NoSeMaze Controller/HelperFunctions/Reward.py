"""
This module contains methods to deliver reward at different situations.
"""

from daqface import DAQ as daq
import numpy as np


def deliver_reward(do_device, samp_rate, secs, sync_clock, ai_channels):
    """
    Deliver reward to a device.
    
    Parameters
    ----------
    do_device : str
        Name of digital out device
    
    samp_rate : int
        Sample rate specified in hardware configuration.
    
    secs : float
        Duration that the ventil should be opened (water amount).
    
    sync_clock : str
        Clock preferred for synchronised reading.
    
    ai_channels : int
        Number of analog input channels read.
        
    Return
    ------
    out : None
        Currently, there is no analog data read.
    """
    
    on = np.ones((1, int(samp_rate*secs)))
    off = np.zeros((1, int(samp_rate/100)))
    
    vec = np.hstack((on, off))
    s1 = np.zeros((1,len(vec[0])))
    vec = np.vstack((s1,vec))
    reward = daq.ThreadSafeDigitalOut(do_device, samp_rate, secs, vec, sync_clock, ai_channels)
    out = reward.DoTask()

    return out

def deliver_reward_static_concatenate(device1, device2, secs, index):
    """
    Deliver reward for concetanted training.
    
    Parameters
    ----------
    device1 : str
        Name of device 1 (left port).
    
    device2 : str
        Name of device 2 (right port).
    
    secs : float
        Duration that the ventil should be opened (water amount).
    
    index : int
        Index of odour actually presented.
        
    Return
    ------
    out : None
        There is currently no analog input read.
    """
    
    on1 = 2**int(device1[-1])
    on2 = 2**int(device2[-1])
    reward = daq.NiUsbDigitalOutTwoDevicesC(device1, device2, secs[index], on1, on2)
    out = reward.DoTask()
    
    return out

def deliver_reward_static_two(device1, device2, secs1, secs2):
    """
    Deliver reward for concetanted training.
    
    Parameters
    ----------
    device1 : str
        Name of device 1 (left port).
    
    device2 : str
        Name of device 2 (right port).
    
    secs1 : float
        Duration that left ventil should be opened (water amount).
    
    secs2 : float
        Duration that right ventil should be opened (water amount).
        
    Return
    ------
    out : None
        There is currently no analog input read.
    """
    
    on1 = 2**int(device1[-1])
    on2 = 2**int(device2[-1])
    reward = daq.NiUsbDigitalOutTwoDevices(device1, device2, secs1, secs2, on1, on2)
    out = reward.DoTask()
    
    return out

def deliver_reward_static(do_device,secs):
    """
    Deliver reward from a ventil.
    
    Parameters
    ----------
    do_device : str
        Name of device.
    
    secs : float
        Duration that the ventil should be opened (water amount).
        
    Return
    ------
    out : None
        Currently no analog input is read.
    """
    on = 2**int(do_device[-1])
    reward = daq.NiUsbDigitalOut(do_device,secs,on)
    out = reward.DoTask()
    
    return out