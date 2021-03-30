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
from GuiDev.ldc_pf_ui import 
import numpy
from ds1054z import DS1054Z



SCOPE_IP   = True

if(SCOPE_IP):
    oscope = DS1054Z('10.10.10.232')
else:
    oscope = rigol_ds1054z.rigol_ds1054z()

#scope = DS1054Z('TCPIP::192.168.1.104::INSTR')


dataWindow = tk_simple.valueWindow(label1_str='RPM', label2_str='FORCE[N]', label3_str='NA')




device_id = "ENTER ID"


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
    script_active = False
    print('Closed Figure!')
    plt.close()

    dataWindow.close()




class Serial_Data():
    def __init__(self, portStr='COM5'):
        self.portID = portStr
        ## Port setup
        self.ser = serial.Serial(self.portID, 2400, timeout=1, rtscts=False)  # open the serial on COM
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



def fetch_data():
    '''
    wda Function to log data into excel
    '''
    global error_flag
    global test_active
    global battVolts
    global gv_min, gv_max
    global frequency
    global motor_rpm
    global radians_per_sec
    global erm_mass_kg
    global erm_rad_mm
    global angular_force

    # get frequency
    if(SCOPE_IP):
        frequency = oscope.get_channel_measurement(1, item='frequency', type='current')
    else:
        frequency = oscope.get_measurement(channel=1, meas_type=oscope.frequency)

    if(type(frequency)!=float):
        frequency = 0.0


    motor_rpm = frequency * 60
    motor_rpm = round(motor_rpm, 3)
    frequency = round(frequency, 3)
    angular_force = erm_mass_kg * erm_rad_mm * (((2 * numpy.pi) * frequency)**2)
    angular_force = round(angular_force, 3)
    frequency = str(frequency) + 'Hz'


    print(time_clock, end=' ')
    print("Frequency:", end='')
    print(frequency, end=' ')
    print("RPM:", end='')
    print(motor_rpm, end=' ')
    print("Force:", end=' ')
    print(angular_force)

    error_flag = False


data1 = []
data2 = []


#plt.connect('close_event', handle_close)

# wda generate instance of serial communication to HiRes
# e = Serial_Data(portStr = comPort)

time_clock = time.strftime("%Y-%m-%d %H:%M:%S", gmtime())
#f.write("{}, \n".format(time_clock))

test_active = True
test_cnt = 0

# Now just loop on Data-fetch and Gui-Update
while True:  # While loop that loops forever
    # while (serialData.inWaiting() == 0):  # Wait here until there is data
    #     pass  # do nothing
    # arduinoString = serialData.readline()  # read the line of text from the serial port
    # dataArray = arduinoString.split(',')  # Split it into an array called dataArray
    # temp = float(dataArray[0])  # Convert first element to floating number and put in temp
    # P = float(dataArray[1])  # Convert second element to floating number and put in P
    if(script_active == True):
        fetch_data()
        dataWindow.update(value1=str(motor_rpm), value2=str(angular_force))
        sample_data1 = motor_rpm
        sample_data2 = angular_force


        data1.append(sample_data1)  # Build our tempF array by appending temp readings
        data2.append(sample_data2)  # Building our pressure array by appending P readings
        drawnow(makeFig)  # Call drawnow to update our live graph


        cnt = cnt + 1
        if (cnt > 50):  # If you have 50 or more points, delete the first one from the array
            cnt = 0


