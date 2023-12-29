#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 09:15:13 2019
@author: WY Li, CH Wu, IXuan Wu 
"""
import math
from datetime import datetime, timedelta
from itertools import zip_longest

class DataDecode:
    @staticmethod
    def _decode_header(raw_data):
        header = raw_data[0:512]
        header_str = [chr(s) for s in header]
        return header_str

    @staticmethod
    def _get_time_string(raw_data):
        time_bytes = raw_data[320:324]
        time_format = '%Y-%m-%d %H:%M:%S'
        time_delta = int.from_bytes(time_bytes, byteorder='little')
        timestr = (datetime.strptime("2000-01-01 00:00:00", time_format) + timedelta(seconds=time_delta)).strftime(time_format)
        return timestr

    @staticmethod
    def _calculate_sampling_rates(header_str, Chn):
        base_sampling_rate = float(''.join(header_str[39:54]))
        sr_array = []
        for i in range(Chn):
            sr_temp = header_str[55 + i * 16:70 + i * 16]
            sr_float = float(''.join(sr_temp))
            sr_array.append(base_sampling_rate / sr_float)

        return sr_array, base_sampling_rate

    @staticmethod
    def rawdata_decode(raw_data):
        header_str = DataDecode._decode_header(raw_data)
        timestr = DataDecode._get_time_string(raw_data)
        sr_array, base_sampling_rate = DataDecode._calculate_sampling_rates(header_str, raw_data[36])
        sr_float = [base_sampling_rate / sr for sr in sr_array]


        res = 2 if raw_data[12] == 33 else 1

        channel_count = raw_data[36]
        channel = [j for i in range(int(max(sr_array))) for j in range(channel_count) if i % sr_array[j] == 0]

        data = [[] for _ in range(channel_count)]
        raw_data_segment = raw_data[512:math.floor((len(raw_data)-512)/len(channel))*len(channel)+512]

        if res == 2:
            for i in range(0, len(raw_data_segment), 2 * len(channel)):
                chunk = raw_data_segment[i:i + 2 * len(channel)]
                paired_chunk = zip_longest(*[iter(chunk)]*2, fillvalue=None)
                for channel_idx, (low_byte, high_byte) in zip_longest(channel, paired_chunk, fillvalue=(None, (None, None))):
                    if low_byte is not None and high_byte is not None:
                        data[channel_idx].append(high_byte * 256 + low_byte)
        elif res == 1:
            for i in range(0, len(raw_data_segment), len(channel)):
                chunk = raw_data_segment[i:i+len(channel)]
                for channel_idx, byte in zip_longest(channel, chunk, fillvalue=None):
                    data[channel_idx].append(byte)

        return data, sr_float, timestr


# import math
# from datetime import datetime,timedelta
# from itertools import zip_longest

# class dataDecode:
#     def HeaderDataDecode(rawtxt):
#         Raw_Data = rawtxt
#         header = Raw_Data[0:512]             #RAW files header
#         #RAW = RAW[512:len(RAW)]         #RAW data
        
#         header2 = []                    #RAW files header to String
#         for s in header:
#             header2.append(chr(s))
        
        
#         time=Raw_Data[320:324]

#         timeformat='%Y-%m-%d %H:%M:%S'
#         timestr=(datetime.strptime("2000-01-01 00:00:00", timeformat)+timedelta(seconds=int.from_bytes(time, byteorder='little'))).strftime(timeformat)
#         #%% Acquisition sampling rate ratio
            
#         splr = header2[39:54]   
#         splr2 = ''.join(splr)
#         splr2 = float(splr2)        #Sampling Rate
        
#         start = 55
#         SRn = []
#         for i in range(header[36]):     #Acquisition sampling rate ratio SRn
#             SRtemp = header2[start+i*15+i:start+(i+1)*15+i]
#             splrtemp = ''.join(SRtemp)
#             splr_float = float(splrtemp)
#             SRn.append(splr2/splr_float)
        
#         maxi = int(max(SRn))
        
#         SR_array=[]
#         for i in range(len(SRn)):
#             SR_array.append(splr2/SRn[i])
            
#         return SR_array, timestr
                    
        
#     def rawdataDecode(rawtxt):
#         '''
#         input:
#             -rawtxt: a list in binary read from kylab raw file format
#         output:
#             -Data: a list with channel recorded by kylab sensor
#             -SR_array: a list with sampling rate of each channel
#             -timestr: file established time, not available for TD1/3, rat & mice sensor
#             if use TD1/3, rat & mice sensor, you can read file established time by datetime.fromtimestamp(os.path.getmtime(filename+'.RAW')) command
#         '''
#         Raw_Data = rawtxt

        
#         header = Raw_Data[0:512]             #RAW files header
#         #RAW = RAW[512:len(RAW)]         #RAW data
        
#         header2 = []                    #RAW files header to String
#         for s in header:
#             header2.append(chr(s))
        
        
#         time=Raw_Data[320:324]

#         timeformat='%Y-%m-%d %H:%M:%S'
#         timestr=(datetime.strptime("2000-01-01 00:00:00", timeformat)+timedelta(seconds=int.from_bytes(time, byteorder='little'))).strftime(timeformat)
        
#         if header[12]==33:
#             res=2 
#         elif header[12]==35:
#             res=1
#         #%% Acquisition sampling rate ratio
            
#         splr = header2[39:54]   
#         splr2 = ''.join(splr)
#         splr2 = float(splr2)        #Sampling Rate
        
#         start = 55
#         SRn = []
#         for i in range(header[36]):     #Acquisition sampling rate ratio SRn
#             SRtemp = header2[start+i*15+i:start+(i+1)*15+i]
#             splrtemp = ''.join(SRtemp)
#             splr_float = float(splrtemp)
#             SRn.append(splr2/splr_float)
        
#         maxi = int(max(SRn))
        
#         SR_array=[]
#         for i in range(len(SRn)):
#             SR_array.append(splr2/SRn[i])
        
#         #%%  Find the Channel 
        
        
#         #matrix = np.zeros([maxi,header[36]])
#         channel=[]
#         for i in range(maxi) :
#             for j in range(header[36]):
#                 #matrix[i][j] = i
#                 if i % SRn[j] == 0:
#                     channel.append(j)
        
#         #%% Data segmentation
#         #Data = np.zeros([header[36],])
#         Data = []
#         cont = []
#         for i in range(header[36]):
#             Data.append([])
#             cont.append(1)
                   
#         Raw_Data = Raw_Data[512:math.floor((len(Raw_Data)-512)/len(channel))*len(channel)+512]
        
#         if res==2:
#             # print(datetime.utcnow(),"Method 1 start")
#             for i in range(0, len(Raw_Data), 2 * len(channel)):
#                 chunk = Raw_Data[i:i + 2 * len(channel)]
#                 # 創建一個迭代器，每次迭代提取兩個連續元素
#                 paired_chunk = zip_longest(*[iter(chunk)]*2, fillvalue=None)
        
#                 for channel_idx, (low_byte, high_byte) in zip_longest(channel, paired_chunk, fillvalue=(None, (None, None))):
#                     if low_byte is not None and high_byte is not None:
#                         Data[channel_idx].append(high_byte * 256 + low_byte)
#             # print(datetime.utcnow(),"Method 1 end")
#             # print(datetime.utcnow(),"Method 2 start")
#             # for i in range(0, len(Raw_Data), len(channel)*2):
#             #     for j in range(len(channel)):
#             #         try:
#             #             Data[channel[j]].append(Raw_Data[i + 2*j+1]*256+Raw_Data[i + 2*j])
#             #         except IndexError:
#             #             pass
#             #         except:
#             #             print('unknown error')
#             # print(datetime.utcnow(),"Method 2 end")
#         elif res==1:
#             for i in range(0, len(Raw_Data),len(channel)):
#                 chunk=Raw_Data[i:i+len(channel)]
#                 for channel_idx, data in zip_longest(channel,chunk, fillvalue=None):
#                     Data[channel_idx].append(data)
#             # for i in range(0, len(Raw_Data), len(channel)):
#             #     for j in range(len(channel)):
#             #             Data[channel[j]].append(Raw_Data[i+j])
#         return Data, SR_array, timestr