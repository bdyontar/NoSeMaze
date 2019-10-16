from daqface import DAQ as daq
import numpy as np


def deliver_reward(do_device, samp_rate, secs, sync_clock, ai_channels):
    on = np.ones((1, int(samp_rate*secs)))
    off = np.zeros((1, int(samp_rate/100)))
    
    vec = np.hstack((on, off))
    s1 = np.zeros((1,len(vec[0])))
    vec = np.vstack((s1,vec))
    reward = daq.ThreadSafeDigitalOut(do_device, samp_rate, secs, vec, sync_clock, ai_channels)
    out = reward.DoTask()

    return out

def deliver_reward_static_two(device1, device2, secs1, secs2):
    on1 = 2**int(device1[-1])
    on2 = 2**int(device2[-1])
    reward = daq.NiUsbDigitalOutTwoDevices(device1, device2, secs1, secs2, on1, on2)
    out = reward.DoTask()
    
    return out

def deliver_reward_static(do_device,secs):
    print('\nreward from device: ',do_device)
    on = 2**int(do_device[-1]) #TODO Prüfen ob es richtig in Hardware durchgeführt wird.
    print('on: ',on,'\n')
    reward = daq.NiUsbDigitalOut(do_device,secs,on)
    out = reward.DoTask()
    
    return out