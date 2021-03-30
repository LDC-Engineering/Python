#!/usr/bin/python
# Python code to plot amplitude spectrum of signal containing NaN values
# Python version 2.7.13

from __future__ import division
import numpy as np
import pylab as pl
import random
import xlrd


DataFile = 'Purple_T4_L3'
SAMPLE_SIZE = 1000


workbook = xlrd.open_workbook(DataFile+'.xls')
worksheet = workbook.sheet_by_name('Sheet1')
num_rows = worksheet.nrows - 1
curr_row = 0

#creates an array to store all the rows
row_array = []
data1_array = []
column=3

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