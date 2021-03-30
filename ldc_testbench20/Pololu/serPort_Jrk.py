# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 15:40:56 2020

@author: wadre
"""


##print(list(serial.tools.list_ports.comports()))
import time
import serial
from serial.tools import list_ports

def get_measurement():
    result = ''
    ser.write('MEAS1? \r')
    #time.sleep(1)
    #while self.ser.inWaiting() < 1:
     #   pass                    
    #result = self.ser.readlines()
    result = ser.readline()
    ser.flushInput() 
    return result  

## Following will only print COM PORT Strings -- for convenience 
x = []

for a in list_ports.comports(): 
    print(a)
    print(a[0])
    x.append(a)
    #x = x+1
    print(x)
  

#############################################################################
## FIND AND OPEN COM PORT  
#############################################################################
COMPORT_STR =''

ports = list(serial.tools.list_ports.comports())
for p in ports:
    if 'Pololu' in str(p):
        #print(p)
        COMPORT_STR = p[0]



print ("your port is:")
print COMPORT_STR


ser = serial.Serial(COMPORT_STR, baudrate = 9600, timeout = 0.1)
serial.Serial()

ser.write(0xE1)
time.sleep(.01)
ser.write(0x7F)


ser.close()

# create instance of fluke_45 class with newly found com port
#dmm = fluke_45(COMPORT_STR)
