# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 10:54:56 2018

@author: jir-mb

"""

#%%
from scipy.io import loadmat

data = loadmat('1_2018-09-19_10_20_02.964480_default.mat')

data

#%%
#from enum import Enum
import csv
import time
import numpy as np

timestamps = time.ctime()
timestamps = timestamps.replace(' ','_')
timestamps = timestamps.replace(':','_')

#%%
with open('testing_Wed_Sep_19_14_01_38_2018.csv', newline='') as file:
    reader = csv.reader(file)
    c = list(reader)
    #a = ([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]])
    #i = 0
    #for row in reader:  
    #   if i == 0:
    #       a[i] = row
    #       i = i+1
    #   else:
    #       a[i][0] = str(row[0])
    #       a[i][1] = str(row[1])
    #       a[i][2] = list(row[2])
           #row_prefix = '['
           #row_suffix = ']'
           #a[i][2] = a[i][2].remove(row_prefix)
           #a[i][2] = a[i][2].remove(row_suffix)
           #a[i][2] = list(map(int,row[2].split(',')))
    #       a[i][3] = int(row[3])
    #       a[i][4] = bool(row[4])
    #       a[i][5] = bool(row[5])
    #       a[i][6] = bool(row[6])
    #       a[i][7] = str(row[7])
    #       a[i][8] = float(row[8])
    #b = np.array(a, dtype=object)
    #print(b)
#%%
with open('testing_'+timestamps+'.csv', 'w', newline = '') as f:
            #fnames = ['animal_id','timestamp', 'analog_data', 'rewarded','response','correct','timeout','pulses','time_axis']
            
            #i = 0
            #l = len(fnames)
            #for i in range(l):
            #    fnames.append('name_'+fnames[i])
            #    i = i + 1
            
            #writer = csv.DictWriter(f, fieldnames = fnames, dialect = 'excel')
            
            writer = csv.writer(f, dialect = 'excel',quoting=csv.QUOTE_NONNUMERIC)
            
            animal_id = 'default'
            timestamp = '0:00:00'
            analog_data = list(np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]))
            rewarded = 1
            response = False
            correct = False
            timeout = False
            pulses = list(np.array([0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,]))
            time_axis = 5.0820
            
            data = [['animal_id', 'timestamp', 'analog_data', 'rewarded', 'response', 'correct', 'timeout', 'pulses', 'time_axis'],
                    [animal_id, timestamp, analog_data, rewarded, response, correct, timeout, pulses, time_axis]]
            
            writer.writerows(data)
            
            #data = {'animal_id': animal_id,
            #        'timestamp': timestamp,
            #        'analog_data': analog_data,
            #        'rewarded': rewarded,
            #        'response': response,
            #        'correct': correct,
            #        'timeout': timeout,
            #        'pulses': pulses,
            #        'time_axis': time_axis}
            # 
            #writer.writeheader()
            #writer.writerow({'animal_id':animal_id,
            #                 'timestamp':timestamp,
            #                 'analog_data':analog_data,
            #                 'rewarded':rewarded,
            #                 'response':response,
            #                 'correct':correct,
            #                 'timeout':timeout,
            #                 'pulses':pulses,
            #                 'time_axis':time_axis})

#%%

import pandas as pd
import time
import numpy as np
#from PyPulse import PulsePulse

timestamps = time.ctime()
timestamps = timestamps.replace(' ','_')
timestamps = timestamps.replace(':','_')

animal_id = 'default'
timestamp = '0:00:00'
analog_data = list(np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]))
rewarded = 1
response = False
correct = False
timeout = False
pulses = list(np.array([[0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0]]))
    
time_axis = 5.0820

data = {'animal_id':animal_id,
         'timestamp':timestamp,
         'analog_data':analog_data,
         'rewarded':rewarded,
         'response':response,
         'correct':correct,
         'timeout':timeout,
         'pulses':pulses,
         'time_axis':time_axis}

df = pd.DataFrame(dict([ (k, pd.Series(v)) for k,v in data.items() ]))
#s1 = pd.Series(pulses)
#s2 = pd.Series(analog_data)
#ds = s1.append(s2)
#ds.to_csv('testing_'+timestamps+'.csv', index=False)

#df=pd.DataFrame({'pulses':list(PulsePulse.pulses),'t':PulsePulse.t})
df.to_csv('testing_'+timestamps+'.csv', index = False, line_terminator = " ", quoting=csv.QUOTE_NONNUMERIC)
