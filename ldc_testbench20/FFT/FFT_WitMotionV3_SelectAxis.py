'''
LDC Sensor FFT script 110520 WDA
Script format- not modular object code.
Basic Vibration/Accelaration evaluation tool
Processes Accellerometer Sensor Data using Time/Freq FFT tools

Having issues finding a low cost software/sensor combo to measure and provide something useful for characterizing thruster
Good tools exist- though many are quite expensive-- National Instruments etc.
Finding a sensor is easier than finding the right software- without spending $.
So while trying to source the ideal commercial software-
We will also try building something that can parse existing sensor data, and process into something useful.
Will start by building some simple python code to process accelerometer data.
- Try to find primary freq and amplitude on acceleration in +/- direction-  of simple thrust speed settings.

ACCELEROMETER SENSOR = WITMotion BWT901CL-E

SAMPLE_SECONDS = Total Time to capture accelerometer Data using WitMotion Software

!!!! TO USE - Follow these basic instructions !!!!
(Simplified - formal docs will be made if this path is continued still developing):'
1. Make sure Python3.4 ans supporting modules are properly installed on a windows machine with BLE capability
2. Configure and calibrate WItMotion Sensor. Install WitMotion onto PC
    - Set sensor to 4G, 100Hz.  Will increase to 200hz at somepoint- need to test.
3. Edit this python file with correct WitMotion 'Data' folder path- See below #RAW_SENSOR_FILE_PATH
4. Connect to Sensor bluetooth link using WitMotion software- should begin receiving data
5. Fixture the test thruster- Whatever method chosen. We are testing linear slides, and hanging swingset style
    - For now, Align the sensor X-axis inline with thrust motion, Positive X-Axis going into the body. Sensor on top of Thruster
    - May move sensor to the side of the thruster for curved thruster testing- in order to use X+Y axis-
    - Zaxis on Wimotion sensor is affected by magnetic fields- avoid using.
    - Will focus on single axis of sensor for straight thrusters- Use x or y.
    - Will focus on two axes for curved thruster measurement. Still to determine

6. Turn on Thruster product (fixtured and sensor attached)- set to appropriate test setting.

7. Goto 'Record' tab and begin recording data- Record for at least SAMPLE_SECONDS duration- Click 'Stop' once complete
    - For initial work on the test system, we have been sampling for at least 5seconds, SAMPLE_SECONDS = 5

8. After stopping the recording. Run this Python File- The latest WitMotion Datafile will be processed and results provided

9. The console will provide measurement values, along with matplotlib plots showing Time and Freq Domain Plots
    - Still very much playing around with this code- and libraries. I am not an expert at python data analysis.


!!!!! Adjust Following to match Test PC settings !!!!
DataFileName = WITMotion Saved data file name
Datafolderpath = windows path for WITMotion Data files








#####################################################################################################################
STARTING TO FEEL THIS MIGHT NEED A FORMILIZED GUI?? Dont have time to spend, will focus on data quality. 67777777777777777777777777777777777777777777777777777777777uuuuuuu
Tkinter?? basic
PyQt?? qt4/5?

- 3axis acceleration data captured from sensor
- Stored in text file array- tab delimited
- X=col2 Y=col3 Z=col4
- Note-  The sensor axis may not correlate to the LDC humanbody axis.
         We may optimize due to sensor sensitivity to magnetic fields(thruster slug)


todo:
1. create simple console UI - run from folder under windows command shell?
2. build function to auto process latest file date within data folder-- COMPLETE
3. Calibrate WIT sensor??
4. Change from pylab to pyplot-- pylab deprecated
5. Add second axis for curved thruster
'''
from statistics import mean, median
import numpy as np
import pylab as pl
import random
import xlrd
import xlwt
import time
from datetime import datetime
import sys
import traceback

from scipy.signal import find_peaks
import csv
from PIL import Image
import glob
import os

#####################################################################################################################
###################### EDIT THE FOLLOWING ONLY ######################################################################
#####################################################################################################################

#Replace following filename and directory to match WITMotion installation on test pc
#for each data file created on WITMotion- enter the filename below to process
RAW_SENSOR_FILE_NAME = r'201215172523.txt'
RAW_SENSOR_FILE_PATH = r'C:/Users/wadre/OneDrive/Desktop/WIT_Sensor/BWT901CL-20201207T194636Z-001/BWT901CL/Standard Software for Windows PC/Data/'

#SAMPLE SECONDS Total time to sample data with accelerometer- Record Data for AT LEAST this long (Seconds)
SAMPLE_SECONDS = 5

# SCAN_FREQUENCY - Sensor Sample Rate-  WitMotion can go up to 200hz. Initially working at 100hz- Set to sensor configuration
SENSOR_SAMPLE_RATE = 100

#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
AXES_TO_PROCESS = 'X'  #use this to process each axis independently??? 
#AXES_TO_PROCESS = 'Y'
#AXES_TO_PROCESS = 'Z'


#Define How many Axes of Sensor Measurement X=1, X,
AXES_CNT = 3

DataFile = 'WITSensor_FFT'
SENSOR = "WIT_901CL"
# How many samples to process with FFT??
# Original value = 1000
#SAMPLE_SIZE = FFT_SAMPLE_SECONDS * SCAN_FREQUENCY
SAMPLE_SIZE = SAMPLE_SECONDS * SENSOR_SAMPLE_RATE

pi = np.pi
datafile_path = ''
datafile_name = ''

raw_x_array = []
raw_y_array = []
raw_z_array = []

def fetch_data():
    '''
    Search for Accelerometer raw data file.
    load into local arrays for processing
    '''
    global raw_x_array,raw_y_array, raw_z_array
    locfilename = ''
    global datafile_name
    datafile_name = "Latest"

    if(datafile_name == "Latest"):
        #list_of_files = glob.glob('C:/Users/wadre/OneDrive/Desktop/WIT_Sensor/BWT901CL-20201207T194636Z-001/BWT901CL/Standard Software for Windows PC/Data/*')  # * means all if need specific format then *.csv
        list_of_files = glob.glob(RAW_SENSOR_FILE_PATH+'*')  # * means all if need specific
        latest_file = max(list_of_files, key=os.path.getctime)

        with open(latest_file, newline='') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if(row[0]=='0x50'):
                    raw_x_array.append(float(row[2]))
                    raw_y_array.append(float(row[3]))
                    raw_z_array.append(float(row[4]))
    else:
        locfilename = RAW_SENSOR_FILE_NAME

        with open(RAW_SENSOR_FILE_PATH + locfilename, newline='') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if(row[0]=='0x50'):
                    raw_x_array.append(float(row[2]))
                    raw_y_array.append(float(row[3]))
                    raw_z_array.append(float(row[4]))



    '''CROP DATA IF NEEDED'''
    if(len(raw_x_array) > SAMPLE_SIZE):
     raw_x_array = raw_x_array[0:SAMPLE_SIZE]

    if(len(raw_y_array) > SAMPLE_SIZE):
     raw_y_array = raw_y_array[0:SAMPLE_SIZE]

    if(len(raw_z_array) > SAMPLE_SIZE):
     raw_z_array = raw_z_array[0:SAMPLE_SIZE]

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

def cl_input():
    '''Simple Console GUI to get user input- Like Data file name to look for-- NOT BEING USED '''
    global datafile_name, datafile_path

    #path = input("Enter file path (leave empty and press enter to use path found in pyscript): ")
    filename = input("Press Enter to process Latest File.  2(enter): process file name in code  ")
    '''
    if(path == ''):
        datafile_path = "Latest"
    else:
        datafile_path = path
    '''

    if(filename == ''):
        datafile_name = "Latest"
    elif(filename == '2'):
        datafile_name = "Code"


############################################################################################################
####################  MAIN SCRIPT ##########################################################################
############################################################################################################
if __name__ == "__main__":
    #cl_input()
    fetch_data()

    #construct reference signal:
   # f1 = 10 #Hz
   # T = 1/f1
   # fs = 10*f1 #

    fs = SENSOR_SAMPLE_RATE
    Ts = 1/fs # = 1/500 sampling period
    #t = np.arange(0,20*T,Ts)
    t = np.arange(0,(len(raw_x_array)/fs), Ts)
    DC = 3.0
    #x = DC + 1.5*np.cos(2*pi*f1*t)
    #x = data1_array
    x = raw_x_array
    y = raw_y_array
    z = raw_z_array


    outputAxes = raw_y_array

    (fax,Aspectrum) = periodogramSS(outputAxes,fs)

    #Create Screen Figure Canvas
    fig1 = pl.figure(1,figsize=(6*3.13,4*3.13)) #full screen
    pl.ion() #make plot interactive - Note- this library is deprecated and not recommened- change to pyplot

    pl.subplot(211) #Top Plot#1

    LW = 2 #line width
    AC = 0.5 #alpha channel
    pl.plot(t, outputAxes, 'b.-', lw=LW, ms=2, label='ref', alpha=AC)

    #change type to np.array to use various np array features
    outputAxes_np = np.array(outputAxes)
    #calculate max and min values of time based acc data arrays, use to set threshold for local min/max finding
    outputAxes_max = np.max(outputAxes_np)
    outputAxes_min = np.min(outputAxes_np)

    #calculate a threshold to use in finding local mins/max's. Used in find_peaks
    amp_thresh_pos = outputAxes_max - 0.2
    amp_thresh_neg = (outputAxes_min * -1) - 0.2

    #mult sig by -1 to find negative peaks - used in min_peaks
    inv_np = -1 * outputAxes_np

    peaks, _ = find_peaks(outputAxes_np, height=amp_thresh_pos)

    min_peaks, _ = find_peaks(inv_np, height=amp_thresh_neg)


    #plot highlight peaks with 'x'
    pl.plot(t[peaks], outputAxes_np[peaks], "x")

    pl.plot(t[min_peaks], outputAxes_np[min_peaks], "x")
    print(outputAxes_np[peaks])
    print(np.average(outputAxes_np[peaks]))
    print(np.average(outputAxes_np[min_peaks]))

    #calc average maxima and minima. Will use these values for initial rough Acceleration PEAK (min/max) values.
    average_maxima = round(np.average(outputAxes_np[peaks]), 4)
    average_minima = round(np.average(outputAxes_np[min_peaks]), 4)
    average_bias = round(abs(average_maxima) - abs(average_minima), 4)


    #plt.plot(np.zeros_like(x), "--", color="gray")
    #plt.show()

    #mark NaN values:
    for (t_,x_) in zip(t,x):
     if np.isnan(x_):
      pl.axvline(x=t_,color='g',alpha=AC,ls='-',lw=2)

    pl.grid()
    pl.xlabel('Time [s]')
    pl.ylabel('Reference signal [g]')


    '''FIND LOCAL MAXIMA (PEAKS) FOR FREQ SPECTRUM FFT'''

    Aspectrum[0] = 0.0  #remove DC Component- No Need for now
    amp_thresh = np.max(Aspectrum)
    print("amp thresh = ", amp_thresh)
    amp_thresh = .9 * amp_thresh
    print(fax)
    print(Aspectrum)
    print("amp thresh = ", amp_thresh)


    #issue is occuring due to multiple peaks detected--!!! must fix
    freq_peak, _=find_peaks(Aspectrum, height=amp_thresh)
    print(freq_peak)
    prim_component_freq = round(float(fax[freq_peak]),3)
    prim_component_amp =  round(float(Aspectrum[freq_peak]),3)



    pl.subplot(212)
    pl.stem(fax, Aspectrum, basefmt=' ', markerfmt='r.', linefmt='r-')
    pl.grid()
    pl.xlabel('Frequency [Hz]')
    pl.ylabel('Amplitude spectrum [g]')
    pl.stem(fax[freq_peak], Aspectrum[freq_peak], "x")
    pl.text(fax[freq_peak], Aspectrum[freq_peak],'  Peak Component = {} hz'.format(prim_component_freq),horizontalalignment='left')


    fig1name = './'+DataFile+'.png'
    #fig1name = './signal.png'
    print ('Saving Fig. 1 to:', end=' ')
    print (fig1name)
    fig1.savefig(fig1name)
    image = Image.open(fig1name)
    image.show()

    print("Note: 1g = 9.8m/s^2")
    print("\n")
    print("*********!!!!!!!!!   PROCESS COMPLETE   !!!!!!!!**********")

    print("TIME DOMAIN >>>>")
    print("The Local Maxima Average(Positive g) = {}".format(average_maxima))
    print("The Local Minima Average(Negative g) = {}".format(average_minima))

    print("The Net Acceleration Bias [g] = {}".format(average_bias))

    print("")
    print("FFT >>>>")
    print("primary component Frequency[hz]= ", prim_component_freq)
    print("primary component Amplitude[g]= ", prim_component_amp)