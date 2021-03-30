'''
LDC Sensor FFT script 050520
Basic Vibration/Accelaration evaluation tool
Processes Accellerometer Sensor Data using Time/Freq FFT tools

Adjust Following to match test application
DataFile =  Data file name

MAX_REQUESTS = Number of packets(of samples) to take from Sensor (250 samples/packet)
SAMPLE_SIZE  = Total size of array to process with FFT tools


STARTING TO FEEL THIS MIGHT NEED A FORMILIZED GUI??
Tkinter?? basic
PyQt?? qt4/5?


USING 2 AXIS DATA X AND Z from ADXL326 16G accel
Using channels 0 and 1


'''
from statistics import mean, median

#from __future__ import division
import numpy as np
import pylab as pl
import random
import xlrd

import xlwt
import time
from datetime import datetime

import sys
import traceback
from datetime import datetime
from scipy.signal import find_peaks

from PIL import Image
import csv



#FFT SAMPLE TIME -  Total time to sample data with accelerometer
SAMPLE_SECONDS = 10

# SCAN_FREQUENCY - Sensor Sample Rate-  WitMotion can go up to 200hz. Initially working at 100hz
SENSOR_SAMPLE_RATE = 100

#Replace following filename and directory to match WITMotion installation on test pc
#for each data file created on WITMotion- enter the filename below to process
RAW_SENSOR_FILE_NAME = r'201216122205.txt'
RAW_SENSOR_FILE_PATH = r'C:/Users/wadre/OneDrive/Desktop/WIT_Sensor/BWT901CL-20201207T194636Z-001/BWT901CL/Standard Software for Windows PC/Data/'

#Define How many Axes of Sensor Measurement X=1, X,
AXES_CNT = 3



DataFile = 'WITSensor_FFT'
SENSOR = "WIT_901CL"
# How many samples to process with FFT??
# Original value = 1000
#SAMPLE_SIZE = FFT_SAMPLE_SECONDS * SCAN_FREQUENCY
SAMPLE_SIZE = SAMPLE_SECONDS * SENSOR_SAMPLE_RATE



# use 'with' if the program isn't going to immediately terminate
# so you don't leave files open
# the 'b' is necessary on Windows
# it prevents \x1a, Ctrl-z, from ending the stream prematurely
# and also stops Python converting to / from different line terminators
# On other platforms, it has no effect
raw_x_array = []
raw_y_array = []
raw_z_array = []


with open(RAW_SENSOR_FILE_PATH+RAW_SENSOR_FILE_NAME, newline='') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        if(row[0]=='0x50'):
            raw_x_array.append(float(row[2]))
            raw_y_array.append(float(row[3]))
            raw_z_array.append(float(row[4]))


'''
AT THIS POINT-  CAN write function to export a seperate nicely formated excel file to send back to LDC?? 

For this version
We need to read in from an excel file- generated by WITMotion software
The timestamp provided is not accurate- though the samples/sec is accurate.
We can likely estimate a timestamp driven by set sampling frequency.

So---

first navigate and find the WIT motion file

Command Line?? 
or first start with 
#defines

We will actually have to first parse the txt file generated from WIT motion software


Lets build in steps-
first simplify by manually converting the WIT motion text file into a useable excel,csv file with timestamp




'''

'''CROP DATA IF NEEDED'''
if(len(raw_x_array) > SAMPLE_SIZE):
 raw_x_array = raw_x_array[0:SAMPLE_SIZE]

if(len(raw_y_array) > SAMPLE_SIZE):
 raw_y_array = raw_y_array[0:SAMPLE_SIZE]

if(len(raw_z_array) > SAMPLE_SIZE):
 raw_z_array = raw_z_array[0:SAMPLE_SIZE]

print(mean(raw_x_array))
print(median(raw_x_array))
print()
LW = 2 #line width
AC = 0.5 #alpha channel
pi = np.pi

def periodogramSS(inputsignal,fsamp):
 N = len(inputsignal)
 N_notnan = np.count_nonzero(~np.isnan(inputsignal))
 hr = fsamp/N #frequency resolution
 t = np.arange(0,N*Ts,Ts)
 #flow,fhih = -fsamp/2,(fsamp/2)+hr #Double-sided spectrum
 flow,fhih = 0,fsamp/2+hr #Single-sided spectrum
 #flow,fhih = hr,fsamp/2
 frange = np.arange(flow,fhih,hr)
 fN = len(frange)
 Aspec = np.zeros(fN)
 n = 0
 for f in frange:
  Aspec[n] = np.abs(np.nansum(inputsignal*np.exp(-2j*pi*f*t)))/N_notnan
  n+=1
 Aspec *= 2 #single-sided spectrum
 Aspec[0] /= 2 #DC component restored (i.e. halved)
 return (frange,Aspec)

#construct reference signal:
f1 = 10 #Hz
T = 1/f1
fs = 10*f1 #10*50 = 500
Ts = 1/fs # = 1/500 sampling period
#t = np.arange(0,20*T,Ts)
t = np.arange(0,(len(raw_x_array)/fs), Ts)
DC = 3.0
#x = DC + 1.5*np.cos(2*pi*f1*t)
#x = data1_array
x = raw_x_array


'''
vel_array = []

for k in range(0, (len(data1_array)-2)):
    vel_array.append(((data1_array[k]+data1_array[k+1])/2) * 0.002)

vel_array.append(0.0)
vel_array.append(0.0)

pos_array = []

for k in range(0, (len(vel_array)-2)):
    pos_array.append(((vel_array[k]+vel_array[k+1])/2) * 0.002)

pos_array.append(0.0)
pos_array.append(0.0)

'''
'''
#randomly delete values from signal x:
ndel = 10 #number of samples to replace with NaN
random.seed(0)
L = len(x)
randidx = random.sample(range(0,L),ndel)
for idx in randidx:
 x[idx] = np.nan
'''



(fax,Aspectrum) = periodogramSS(x,fs)

fig1 = pl.figure(1,figsize=(6*3.13,4*3.13)) #full screen
pl.ion()

pl.subplot(211)
pl.plot(t, x, 'b.-', lw=LW, ms=2, label='ref', alpha=AC)

x_np = np.array(raw_x_array)

x_max = np.max(x_np)
x_min = np.min(x_np)

filter_window_pos = x_max - 0.2
filter_window_neg = (x_min * -1) - 0.2

#x_np = np.arange(raw_x_array, .01)

inv_np = -1 * x_np


peaks, _ = find_peaks(x_np, height=filter_window_pos)



min_peaks, _ = find_peaks(inv_np, height=filter_window_neg)
#print(peaks)
#plt.plot(x)
pl.plot(t[peaks], x_np[peaks], "x")

pl.plot(t[min_peaks], x_np[min_peaks], "x")
print(x_np[peaks])
print(np.average(x_np[peaks]))
print(np.average(x_np[min_peaks]))

average_maxima = round(np.average(x_np[peaks]), 4)
average_minima = round(np.average(x_np[min_peaks]), 4)
average_bias = round(abs(average_maxima) - abs(average_minima), 4)

print("\n")
print("\n")
print("*********!!!!!!!!!  Test Complete    !!!!!!!!**********")
print("The Local Maxima Average(Positive G) = {}".format(average_maxima))
print("The Local Minima Average(Negative G) = {}".format(average_minima))

print("The Net Acceleration Bias [G] = {}".format(average_bias))
#plt.plot(np.zeros_like(x), "--", color="gray")
#plt.show()




#mark NaN values:
for (t_,x_) in zip(t,x):
 if np.isnan(x_):
  pl.axvline(x=t_,color='g',alpha=AC,ls='-',lw=2)

pl.grid()
pl.xlabel('Time [s]')
pl.ylabel('Reference signal')

pl.subplot(212)
pl.stem(fax, Aspectrum, basefmt=' ', markerfmt='r.', linefmt='r-')
pl.grid()
pl.xlabel('Frequency [Hz]')
pl.ylabel('Amplitude spectrum')

'''

pl.subplot(413)
pl.plot(t, vel_array, 'b.-', lw=LW, ms=2, label='ref', alpha=AC)


pl.subplot(414)
pl.plot(t, pos_array, 'b.-', lw=LW, ms=2, label='ref', alpha=AC)
'''


fig1name = './'+DataFile+'.png'
#fig1name = './signal.png'
print ('Saving Fig. 1 to:', end=' ')
print (fig1name)
fig1.savefig(fig1name)
image = Image.open(fig1name)
image.show()