# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:21:04 2020

@author: kylab
"""

import matplotlib.pyplot as plt
from dataDecode import dataDecode
import numpy as np
from scipy import signal


 
def fftpower(samplerate, sig):
    # FFT from matlab
    datalength = len(sig)
    index = np.arange(1, int(datalength/2)+1)
    hammingwindow = np.hamming(datalength)
    f_length = samplerate * np.linspace(0, 1, datalength)
    s_temp = signal.detrend(sig)
    s_temp = s_temp * hammingwindow
    sfft = np.fft.fft(s_temp, datalength)
    power_amp = abs(sfft[index])            # FFT output
    theta = np.mod(np.angle(sfft[index])*180 / np.pi, 360)
    f_length = f_length[index]
    
    return f_length, power_amp


fname="200401.152"

with open(fname,"rb") as f:
    RawData=f.read()
    Data,sampling_rate,strtemp=dataDecode.rawdataDecode(RawData)

windowsize=int(30*sampling_rate[0])
amp_total=[]
for i in range(len(Data[0])//windowsize):
    f_len,amp=fftpower(sampling_rate[0],Data[0][i*windowsize:(i+1)*windowsize])
    amp_total.append(amp)


amp_total=np.array(amp_total).T
x=np.linspace(0,len(Data[0])//windowsize*30,len(Data[0])//windowsize)

plt.pcolormesh(x,f_len,amp_total)
plt.ylim([f_len[0],1])
plt.colorbar()
#plt.imshow(amp_total, aspect='auto', interpolation='none',
#           origin='lower')