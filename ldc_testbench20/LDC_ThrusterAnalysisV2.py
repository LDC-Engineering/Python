# -*- coding: utf-8 -*-
"""
Created on Wed Apr 09 11:17:13 2014

@author: adrewd
"""
import sys
#import u3
import serial, re
import math
import rigol_ds1054z
## from visa import instrument
# from time import sleep
import time
from time import gmtime, strftime
# sys.path.append('C:/Users/adrewd/Dropbox/PYTHON/LabJack_scripts/KB_ManfTest_Serial')
import numpy  # Import numpy
import matplotlib.pyplot as plt  # import matplotlib library
from drawnow import *
import random
import tk_simple
script_active = True

# io = u3.U3()
oscope = rigol_ds1054z.rigol_ds1054z()
#SENSOR = "ADXL_335"
SENSOR = "ADXL_326"
dataWindow = tk_simple.valueWindow()

comPort = 'COM4'
battVolts = 0.0
test_active = False
rest_period = 20
error_flag = False
error_id = 'none'
gv_min = 0.0
gv_max = 0.0
frequency = 0.0

# io.getFeedback(u3.BitDirWrite(IONumber = 5, Direction = 0))
# Number: 0-7=FIO, 8-15=EIO, 16-19=CIO Direction: 1 = Output, 0 = Input

title = 'LDC LOGTEST'  # wda [manf][chem][quant/type][simulation/emulation iteration]
softversion = 'BACI_V3_0601'  # general cell identity - branding etc

time_clock = time.strftime("%Y-%m-%d %H:%M:%S", gmtime())
# f = open('testdata.csv', 'w')
# f.write("Pressure Test - Full Batt Discharge, {}, {} \n".format(title, time_clock))
# f.write("Test Subject, %s \n" % softversion)
# f.write("Time, Pressure[psi], Batt Volts[V] \n")

#print("please enter first x-variable>>")
#print("please enter y-min")
#print(GetSerialPort())

def handle_close(evt):
    global script_active

    print('Closed Figure!')
    plt.close()
    script_active = False

def makeFig():  # Create a function that makes our desired plot
   # if(plt.)
    plt.ylim(-5, 5)  # Set y min and max values
    plt.title('LDC Thruster Sensor Data')  # Plot the title
    plt.grid(True)  # Turn the grid on
    plt.ylabel('Pos G')  # Set ylabels
    plt.plot(tempF, 'ro-', label='+Accel(+g)')  # plot the temperature
    plt.legend(loc='upper left')  # plot the legend
    plt2 = plt.twinx()  # Create a second y axis
    plt.ylim(-5, 5)  # Set limits of second y axis- adjust to readings you are getting
    plt2.plot(pressure, 'b^-', label='-Accel(-g)')  # plot pressure data
    plt2.set_ylabel('Neg G')  # label second y axis
    plt2.ticklabel_format(useOffset=False)  # Force matplotlib to NOT autoscale y axis
    plt2.legend(loc='upper right')  # plot the legend


class Serial_Data():
    def __init__(self, portStr='COM5'):
        self.portID = portStr
        ## Port setup
        self.ser = serial.Serial(self.portID, 9600, timeout=1, rtscts=False)  # open the serial on COM
        self.ser.flush()
        time.sleep(2)


    def get_data(self):
        result = ''
        # self.ser.write('*1B1 \r')
        # time.sleep(1)
        while self.ser.inWaiting() < 1:
            pass
        result = self.ser.readline()

        return result

def source_sample():
    '''
    check run_status flags, and log samples - current,voltages,cycles,
    '''
    pass

def fetch_data():
    '''
    wda Function to log data into excel
    '''
    global error_flag
    global test_active
    global battVolts  #not used yet
    global gv_min, gv_max
    global frequency

    global frequency_x, frequency_y, frequency_z
    global gv_min_x, gv_max_x, gv_min_z, gv_max_z

    battVolts = 3.5

    # get frequency x axis - Channel 1
    frequency = oscope.get_measurement(channel=1, meas_type=oscope.frequency)
    if(frequency):
        frequency = round(frequency, 3)
        frequency = str(frequency) + 'Hz'
    else:
        frequency = 0.0

    # get voltages x axis - Channel 1
    # -3g = 0v   3g= 3.3v
    # so 1.65v = 0 g

    vmax = oscope.get_measurement(channel=1, meas_type=oscope.max_voltage)
    vmin = oscope.get_measurement(channel=1, meas_type=oscope.min_voltage)
    vavg = oscope.get_measurement(channel=1, meas_type=oscope.average_voltage)

    #ADXL_326_XCAL = 15.525
    ADXL_326_XCAL = 16.5
    ADXL_326_YCAL = 16.5
    ADXL_326_ZCAL = 16.5

    ADXL_326_XZERO = 1.60
    ADXL_326_YZERO = 1.61
    ADXL_326_ZZERO = 1.60



    if(SENSOR == "ADXL_326"):
        gv_dif = (vavg - 1.60) * ADXL_326_XCAL

        gv_max = (vmax - 1.61) * ADXL_326_XCAL
        gv_min = (vmin - 1.61) * ADXL_326_XCAL
        #gv_dif = gv_max + gv_min


    elif(SENSOR == "ADXL_335"):
        gv_max = (vmax - 1.65) * 1.818
        gv_min = (vmin - 1.65) * 1.818
    else:
        gv_max = (vmax - 1.65) * 1.818
        gv_min = (vmin - 1.65) * 1.818


    gv_max = round(gv_max, 3)
    gv_min = round(gv_min, 3)
    gv_dif = round(gv_dif, 3)

    print(time_clock),
    print("Frequency:"),
    print(frequency),
    # print("Vmax[V]:"),
    # print(vmax),
    # print("Vmin[V]:"),
    # print(vmin)
    print("g+:" + str(gv_max) + " g-: " + str(gv_min)+ " g*: " + str(gv_dif))
    # if(log_data == True):
    #     log_data(Freq, Vmax, Vmin, gv_max, gv_min)

    # print time_clock.strip("\n"), j
    # print(time_clock+" "+"Pressure: "+ j)

    # f.write("{}, {}, {}, \n".format(time_clock, j, battVolts))
    # f.write("{}, {}, {}, \n".format(time_clock, j, battVolts))
    error_flag = False


tempF = []
pressure = []

plt.ion()  # Tell matplotlib you want interactive mode to plot live data
cnt = 0
plt.connect('close_event', handle_close)

# wda generate instance of serial communication to HiRes
# e = Serial_Data(portStr = comPort)

time_clock = time.strftime("%Y-%m-%d %H:%M:%S", gmtime())
#f.write("{}, \n".format(time_clock))

test_active = True
test_cnt = 0


while True:  # While loop that loops forever
    # while (serialData.inWaiting() == 0):  # Wait here until there is data
    #     pass  # do nothing
    # arduinoString = serialData.readline()  # read the line of text from the serial port
    # dataArray = arduinoString.split(',')  # Split it into an array called dataArray
    # temp = float(dataArray[0])  # Convert first element to floating number and put in temp
    # P = float(dataArray[1])  # Convert second element to floating number and put in P
    if(script_active == True):
        fetch_data()
        dataWindow.update(value1=str(frequency), value2=str(gv_max), value3=str(gv_min))
        temp = gv_max
        P = gv_min
        tempF.append(temp)  # Build our tempF array by appending temp readings
        pressure.append(P)  # Building our pressure array by appending P readings
        drawnow(makeFig)  # Call drawnow to update our live graph
        plt.pause(.000001)  # Pause Briefly. Important to keep drawnow from crashing
        cnt = cnt + 1
        if (cnt > 50):  # If you have 50 or more points, delete the first one from the array
            tempF.pop(0)  # This allows us to just see the last 50 data points
            pressure.pop(0)


# print("Test Finished - Check Data Log")
#f.write("Test Finished \n")

#f.close()

#e.ser.close()