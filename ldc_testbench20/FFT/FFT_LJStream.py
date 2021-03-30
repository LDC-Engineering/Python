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

'''

from __future__ import division
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

import u3
#import u6
#import ue9
from PIL import Image


DataFile = 'Sensor_FFT'

#Define How many Axes of Sensor Measurement X=1, X,
AXES_CNT = 2

#FFT SAMPLE TIME
FFT_SAMPLE_SECONDS = 8

# SCAN_FREQUENCY is the scan frequency of stream mode in Hz
SCAN_FREQUENCY = 500



# MAX_REQUESTS is the number of packets to be read.
# Original Value = 5
# 10 = 5000 samples
#MAX_REQUESTS = 10

MAX_REQUESTS = ((AXES_CNT*250)/SCAN_FREQUENCY)*FFT_SAMPLE_SECONDS*2

# How many samples to process with FFT??
# Original value = 1000
#SAMPLE_SIZE = FFT_SAMPLE_SECONDS * SCAN_FREQUENCY
SAMPLE_SIZE = FFT_SAMPLE_SECONDS * SCAN_FREQUENCY * 2

d = None

###############################################################################
# U3
# Uncomment these lines to stream from a U3
###############################################################################

# At high frequencies ( >5 kHz), the number of samples will be MAX_REQUESTS
# times 48 (packets per request) times 25 (samples per packet).
d = u3.U3()
# To learn the if the U3 is an HV
d.configU3()
# For applying the proper calibration to readings.
d.getCalibrationData()
# Set the FIO0 and FIO1 to Analog (d3 = b00000011)
d.configIO(FIOAnalog=3)
print("Configuring U3 stream")
d.streamConfig(NumChannels=2, PChannels=[0, 1], NChannels=[31, 31], Resolution=1, ScanFrequency=SCAN_FREQUENCY)


###############################################################################
# U6
# Uncomment these lines to stream from a U6
###############################################################################
'''
# At high frequencies ( >5 kHz), the number of samples will be MAX_REQUESTS
# times 48 (packets per request) times 25 (samples per packet).
d = u6.U6()
# For applying the proper calibration to readings.
d.getCalibrationData()
print("Configuring U6 stream")
d.streamConfig(NumChannels=2, ChannelNumbers=[0, 1], ChannelOptions=[0, 0], SettlingFactor=1, ResolutionIndex=1, ScanFrequency=SCAN_FREQUENCY)
'''

###############################################################################
# UE9
# Uncomment these lines to stream from a UE9
###############################################################################
'''
# At 96 Hz or higher frequencies, the number of samples will be MAX_REQUESTS
# times 8 (packets per request) times 16 (samples per packet).
# Currently over ethernet packets per request is 1.
d = ue9.UE9()
#d = ue9.UE9(ethernet=True, ipAddress="192.168.1.209")  # Over TCP/ethernet connect to UE9 with IP address 192.168.1.209
# For applying the proper calibration to readings.
d.getCalibrationData()
print("Configuring UE9 stream")
d.streamConfig(NumChannels=2, ChannelNumbers=[0, 1], ChannelOptions=[0, 0], SettlingTime=0, Resolution=12, ScanFrequency=SCAN_FREQUENCY)
'''

if d is None:
    print("""Configure a device first.
Please open streamTest.py in a text editor and uncomment the lines for your device.
Exiting...""")
    sys.exit(0)

try:
    print("Start stream")
    d.streamStart()
    start = datetime.now()
    print("Start time is %s" % start)

    missed = 0
    dataCount = 0
    packetCount = 0
    x_array = []
    z_array = []

    for r in d.streamData():
        if r is not None:
            # Our stop condition
            if dataCount >= MAX_REQUESTS:
                break

            if r["errors"] != 0:
                print("Errors counted: %s ; %s" % (r["errors"], datetime.now()))

            if r["numPackets"] != d.packetsPerRequest:
                print("----- UNDERFLOW : %s ; %s" %
                      (r["numPackets"], datetime.now()))

            if r["missed"] != 0:
                missed += r['missed']
                print("+++ Missed %s" % r["missed"])

            # Comment out these prints and do something with r
            print("Average of %s AIN0, %s AIN1 readings: %s, %s" %
                  (len(r["AIN0"]), len(r["AIN1"]), sum(r["AIN0"])/len(r["AIN0"]), sum(r["AIN1"])/len(r["AIN1"])))
            #
            x_array = x_array+r['AIN0']
            z_array = z_array+r['AIN1']
            dataCount += 1
            packetCount += r['numPackets']
        else:
            # Got no data back from our read.
            # This only happens if your stream isn't faster than the USB read
            # timeout, ~1 sec.
            print("No data ; %s" % datetime.now())
except:
    print("".join(i for i in traceback.format_exc()))
finally:
    stop = datetime.now()
    d.streamStop()
    print("Stream stopped.\n")
    d.close()

    sampleTotal = packetCount * d.streamSamplesPerPacket

    scanTotal = sampleTotal / 2  # sampleTotal / NumChannels
    print("%s requests with %s packets per request with %s samples per packet = %s samples total." %
          (dataCount, (float(packetCount)/dataCount), d.streamSamplesPerPacket, sampleTotal))
    print("%s samples were lost due to errors." % missed)
    sampleTotal -= missed
    print("Adjusted number of samples = %s" % sampleTotal)

    runTime = (stop-start).seconds + float((stop-start).microseconds)/1000000
    print("The experiment took %s seconds." % runTime)
    print("Actual Scan Rate = %s Hz" % SCAN_FREQUENCY)
    print("Timed Scan Rate = %s scans / %s seconds = %s Hz" %
          (scanTotal, runTime, float(scanTotal)/runTime))
    print("Timed Sample Rate = %s samples / %s seconds = %s Hz" %
          (sampleTotal, runTime, float(sampleTotal)/runTime))


for i in range(0, len(x_array)):
    x_array[i] -= 1.64

for i in range(0, len(z_array)):
    z_array[i] -= 1.63

print (x_array)
print (len(x_array))
print (z_array)
print (len(z_array))


'''
Now we need to write arrays to excel file with 1/freq timestamps'''





wb = xlwt.Workbook()
ws = wb.add_sheet('Sheet1')
t_stamp = 0

for samp in range(0, len(x_array)):
    ws.write(samp, 0, t_stamp)
    ws.write(samp, 1, x_array[samp])
    ws.write(samp, 2, x_array[samp])
    t_stamp+= .002


wb.save(DataFile+'.xls')


time.sleep(1)

workbook = xlrd.open_workbook(DataFile+'.xls')
worksheet = workbook.sheet_by_name('Sheet1')
num_rows = worksheet.nrows - 1
curr_row = 0

#creates an array to store all the rows
row_array = []
data1_array = []
column=1

while curr_row < num_rows:
    dataVal = worksheet.cell(curr_row, column)
    data1_array.append(dataVal.value)
    curr_row += 1


if(len(data1_array) > SAMPLE_SIZE):
 data1_array = data1_array[0:SAMPLE_SIZE]

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
f1 = 50 #Hz
T = 1/f1
fs = 10*f1 #10*50 = 500
Ts = 1/fs
#t = np.arange(0,20*T,Ts)
t = np.arange(0,(len(data1_array)/fs), Ts)
DC = 3.0
#x = DC + 1.5*np.cos(2*pi*f1*t)
x = data1_array

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

fig1name = './'+DataFile+'.png'
#fig1name = './signal.png'
print ('Saving Fig. 1 to:', end=' ')
print (fig1name)
fig1.savefig(fig1name)
image = Image.open(fig1name)
image.show()