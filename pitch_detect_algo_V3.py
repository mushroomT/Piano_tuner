# Read in a WAV and find the freq's
from __future__ import division
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import time
from touch_screen_UI_V1 import *
from change_bitrate import *
from piano_config import Piano_keyname
from record import record_sound
import scipy.fftpack as sf
from scipy.fftpack import fft
from scipy.signal import argrelextrema
import xlwt
import winsound

low_cutoff = 20
high_cutoff = 4200

def save(data, data2, path):
    f = xlwt.Workbook()  # create workbook
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # create sheet
    l_ = len(data)
    for ii in range(l_):
        sheet1.write(ii+1, 1, data[ii])
        sheet1.write(ii+1, 2, data2[ii])
    f.save(path)

def plot_time_response(data_stream):
    plt.figure(0)
    plt.plot(range(len(data_stream)), data_stream)
    # plt.xlim([0, 4200])
    plt.title('Signal in time domain')
    plt.xlabel('time(s)')
    # plt.ylabel('Magnitude(dB)')
    # plt.xlim([0,60000])
    plt.show()

def plot_freq_response(fft_data,coef):
    plt.figure(1)
    num =len(fft_data)
    x = np.arange(0,num*coef,coef)
    plt.plot(x[:num], abs(fft_data))
    plt.xlim([0, 4200])
    plt.title('Frequency response after fft')
    plt.xlabel('Frequency(Hz)')
    plt.ylabel('Magnitude')
    plt.show()


#function to find the fundamental pitch frequency
def signal_process(file):
    # chunk = 2048 #increasing the size of these chunks can increase the accuracy but at a computational cost
    wf = wave.open(file,'rb')
    #we also extract the rate at which the sampling frames were recorded
    #and the total length of the sample
    chunk = wf.getnframes()
    rate = wf.getframerate()
    swidth = wf.getsampwidth()
    values=[]
    timestep = 1.0/rate #the sampling timestep in seconds
    #now we keep reading the frames contained in each chunk and apply the FFT
    #until we get to the end of the sample
    while True:
        signal = wf.readframes(chunk)
        if len(signal) < chunk*swidth:
            break
        else:
            signal = np.fromstring(signal, 'Int16')
            # plot_time_response(signal)
            n = signal.size
            #we apply the FFT, extract the frequencies and take their absolute value
            freqs = fft(signal)
            # plot_freq_response(freqs,rate/chunk)
            freq = np.fft.fftfreq(n, d=timestep)
            data = np.abs(freqs)
            #we find the frequency with maximum intensity
            max = [x for x in argrelextrema(data, np.greater)[0] if x<10000]
            maxInt = data[max]
            absMaxInt=np.max(maxInt)
            absMax=np.where(maxInt==absMaxInt)[0][0]
            number=max[absMax]*rate/chunk
            if number>=20 and number<=4000:
                values.append(number)
    #finally, here we consider only the results from the central part of the signal wave
    #discarding those values that could be affected mostly by noise at the beginnign
    #and at the end of the recording (the value of one third is completely arbitrary)
    l=int(len(values)/3)
    return np.mean(values)

# if __name__ == '__main__':
#     # record_sound()
#     # path = 'output.wav'
#     path = './key_sound_WAV/50-A#.wav'
#     # change_bitrate(path)
#     current_frequency = signal_process(path)
#     print(current_frequency)

    # current_freq = np.zeros(88)
    # stand_freq = np.zeros(88)
    # for i in range(len(current_freq)):
    #     try:
    #         path = './key_sound_WAV/' + str(i+1) + '-' + Piano[i+1] + '.wav'
    #         print(path)
    #         # change_bitrate(path)
    #         current_freq[i] = signal_process(path)
    #         stand_freq[i] = 440*2**((i+1-49)/12)
    #         print(current_freq[i],stand_freq[i])
    #     except:
    #         continue
    #
    # print(current_freq, stand_freq)
    # save(current_freq, stand_freq, 'current_freq.xlsx')
