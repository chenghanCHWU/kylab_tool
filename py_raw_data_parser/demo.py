# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 14:52:28 2022

@author: kylab
"""

import numpy as np
import dataDecode
import math
from datetime import datetime, timedelta 


def get_data_complement(signal):
    np_signal=np.array(signal)
    for i in range(len(np_signal)):
        if np_signal[i]<32768:
            np_signal[i]+=65535
    np_signal-=65535      
    return np_signal



fname='Data/20711.RAW'
Raw_Data=open(fname, "rb").read()
Data,sampling_rate,timestr=dataDecode.DataDecode.rawdata_decode(Raw_Data)

data_duration=len(Data[0])/sampling_rate[0]

end_record_time=datetime.strptime(timestr, format)+timedelta(seconds = int(data_duration)) 
print('start record time: ',timestr)
print('end record time: ',datetime.strftime(end_record_time,format))
print('Record time: ', str(timedelta(seconds = int(data_duration)) ))



np_ECG=get_data_complement(Data[0])



