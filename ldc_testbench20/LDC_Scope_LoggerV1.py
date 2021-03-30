# -*- coding: utf-8 -*-
"""
Created on Wed Apr 09 11:17:13 2014

@author: adrewd
"""
import sys
import u3
import serial, re
import math
import rigol_ds1054z
## from visa import instrument
#from time import sleep
import time
from time import gmtime, strftime
#from KB_ManfTest_Serial import kbbus
#sys.path.append('C:/Users/adrewd/Dropbox/PYTHON/LabJack_scripts/KB_ManfTest_Serial')
#import kbbus
## import numpy as np
#import string


#io = u3.U3()
oscope = rigol_ds1054z.rigol_ds1054z()


comPort = 'COM4'

#d = u3.U3()



battVolts = 0.0

test_active = False 
rest_period = 20



error_flag = False
error_id = 'none'

#io.getFeedback(u3.BitDirWrite(IONumber = 5, Direction = 0))

#Number: 0-7=FIO, 8-15=EIO, 16-19=CIO Direction: 1 = Output, 0 = Input


title = 'LDC LOGTEST'      #wda [manf][chem][quant/type][simulation/emulation iteration]
softversion = 'BACI_V3_0601'  #general cell identity - branding etc

time_clock = time.strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    

f = open('testdata.csv','w')
    
f.write("Pressure Test - Full Batt Discharge, {}, {} \n".format(title, time_clock))
f.write("Test Subject, %s \n" %softversion)
f.write("Time, Pressure[psi], Batt Volts[V] \n")



class limit: #wda limit def enum
    lower = low = bottom = 1
    upper = up = top = 2
    stop = inter = 3
    current = 4
    ALL = 5
    

    def __init__(self, portStr='COM5'):
        self.portID = portStr
        ## Port setup
        self.ser = serial.Serial(self.portID,9600,timeout=1,rtscts=False) #open the serial on COM n+1
        

class HiRes():
    
    def __init__(self, portStr='COM5'):
        self.portID = portStr
        ## Port setup
        self.ser = serial.Serial(self.portID,2400,timeout=1,rtscts=False) #open the serial on COM
        self.ser.flush() 
        time.sleep(2)
       # self.ser.write('*1C1 \r')
        #sleep(5)
        
    def get_count(self):
        result = ''
        #self.ser.write('*1B1 \r')
        #time.sleep(1)
        while self.ser.inWaiting() < 1:
            pass            
        result = self.ser.readline()
        
        return result
  #  def get_count(self):

'''
def kb_wait(plimit):
    global error_flag
    global error_id
    global current_limit
    
    #wda wait until ready/busy bit goes low -- High = in movement
    while ((io.getFeedback(u3.BitStateRead(5)))[0] == 1):
        pass
    #wda grab copy of current position after movement stops.
        
    kb_currpos = (kbbus.limit_read(kbbus.limit.current))['A4']
    
    if plimit == limit.up:       
        current_limit = limit.up
        if (math.fabs(kb_currpos - kb_uplim) > limit_margin):
            retval = 0
            error_flag = True
            error_id = 'Uplim not reached'
        else:
            retval = 1
            
    if plimit == limit.low:
        current_limit = limit.low
        if (math.fabs(kb_currpos - kb_lowlim) > limit_margin):
            retval = 0
            error_flag = True
            error_id = 'Lowlim not reached'
        else:
            retval = 1
    time.sleep(1)      
    return retval

'''

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
    global battVolts
    
    '''
    #Get pressure
    j=""
    HiRes_currpos = e.get_count()
    j = HiRes_currpos.strip('\n')
    j  = j.strip('\r')
    
    
    
    #get battery volts
    battVolts = io.getAIN(0)
    battVolts = round(battVolts, 4)
    '''
    j='NA'
    battVolts = 3.5
    
    #get frequency
    frequency = oscope.get_measurement(channel=1, meas_type=oscope.frequency)
    frequency = str(frequency)+'Hz'
    
    
    #0g = 0v 3g = 3.3v
    #1.1v per g
    #-3g = 0v   3g= 3.3v
    # so 1.65v = 0 g
    
    vmax = oscope.get_measurement(channel=1, meas_type=oscope.max_voltage)
    vmin = oscope.get_measurement(channel=1, meas_type=oscope.min_voltage)
    
    gv_max = (vmax - 1.65)*.818
    gv_min = (vmin - 1.65)*.818
     
    
    
    
    
    
    print time_clock,
    print "Frequency:",
    print frequency,
    print "Vmax[V]:",
    print vmax,
    print "Vmin[V]:",
    print vmin
    print "g+:"+str(gv_max)+" g-: "+str(gv_min)
    
    
    #print time_clock.strip("\n"), j
    #print(time_clock+" "+"Pressure: "+ j)
    

    f.write("{}, {}, {}, \n".format( time_clock, j, battVolts))
    f.write("{}, {}, {}, \n".format( time_clock, j, battVolts))
    error_flag = False

    
        
    
#wda generate instance of serial communication to HiRes         
#e = HiRes(portStr = comPort)
    


    
time_clock = time.strftime("%Y-%m-%d %H:%M:%S", gmtime())    
f.write("{}, \n".format( time_clock))
       
test_active = True
test_cnt = 0

if error_flag == False:
    test_active = True
    



    '''
    wda Start Main Cycle Test
    '''
    while(test_active == True):
        pass
        time_clock = time.strftime("%Y-%m-%d %H:%M:%S", gmtime())
        fetch_data()
        
        time.sleep(1.2)
        
        
        if(test_cnt > 10):
            test_active = False
        
        if(battVolts<3.15):
            test_cnt = test_cnt+1
        else:
            test_cnt = 0
    
    
        if(test_cnt == 5):
            test_cnt = 0
            test_active = False
         
            
print("Test Finished - Check Data Log")
f.write("Test Finished \n")        

f.close()


        


e.ser.close()




