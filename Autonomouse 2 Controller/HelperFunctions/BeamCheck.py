from daqface import DAQ as daq
import numpy as np
import time


def check_beam(device, channels, beam_channel):
    try:
        #s1 = time.time()
        check = daq.ThreadSafeAnalogInput(device, channels, 1000, 0.1)
        analog_data = check.DoTask()
        #l1 = time.time()-s1
        #s2 = time.time()
        check_mean = np.mean(analog_data[beam_channel])
        #l2 = time.time()-s2
        #print("check_mean : {0:.3f}\ncheck time : {1:.6f} s\ncompute time : {2:.6f} s".format(check_mean,l1,l2))
        return check_mean > 1
    except:
        return False