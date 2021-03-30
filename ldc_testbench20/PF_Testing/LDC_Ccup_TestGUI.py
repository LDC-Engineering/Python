# -*- coding: utf-8 -*-
"""
Created on Wed Apr 09 11:17:13 2014

@author: adrewd 2021
"""

DEBUG_NOSCOPE   = False
DEBUG_TIMETEST  = False

DATA_OFFSET     = 8

COL_DF_LINE     = 0
COL_DEV_LEVEL   = 1
COL_FREQ        = 2
COL_PRES_MAX    = 3
COL_PRES_MIN    = 4
COL_PRES_ABS    = 5


from ldc_pf_ui3 import Ui_MainWindow
import time
from time import gmtime

import xlwt
import os


#from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore
import sys

from ds1054z import DS1054Z



class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        #super(Main, self).__init__()
        super().__init__(parent)
        self.app_version = '1.0'
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_gui()
        self.init_bindings()



        ###INIT VARS############
        self.test_enabled = False
        self.testlevel_instance = {'Freq': None, 'Pmax': None, 'Pmin': None, 'Pabs':None}

        self.frequency = 0
        self.pressure_min = 0
        self.pressure_max = 0
        self.pressure_abs = 0
        self.datafile_line = 0

        self.time_now = 0
        self.time_last = 0


        #self.time_clock = time.strftime("%Y-%m-%d %H:%M:%S", gmtime())
        #self.oscope = DS1054Z('10.10.10.232')
        if(DEBUG_NOSCOPE == False):
            self.init_scope()
            self.timer_workerA = QtCore.QTimer(self)
            self.timer_workerA.timeout.connect(self.watchdog_thread)
            self.timer_workerA.start(2000)
        self.b_network_status = True


        self.timer_workerB = QtCore.QTimer(self)
        self.timer_workerB.timeout.connect(self.worker_thread)
        self.timer_workerB.start(200)





    def watchdog_thread(self):
        if(self.check_network_connection() == True):
            self.ui.label_networkstatus.setText("Connection Ok:)")

        else:
            self.ui.label_networkstatus.setText("Connection Lost:(")
            self.test_enabled = False


    def worker_thread(self):
        if(DEBUG_TIMETEST == False):
            if(self.b_network_status == True):
                self.fetch_scope_data()
        else:
            self.time_now = time.clock()
            print(self.oscope.idn)
            print(self.time_now - self.time_last)
            self.time_last = self.time_now





    def init_gui(self):
        self.ui.frame_Testing.setEnabled(False)
        self.ui.frame_TestSetup.setEnabled(True)
        self.ui.lcdNumber_avgfreq.display(0.0)
        self.ui.lcdNumber_maxpres.display(0.0)
        self.ui.lcdNumber_minpres.display(0.0)
        self.ui.lcdNumber_abspres.display(0.0)

    def init_bindings(self):
        self.ui.pb_enabletest.clicked.connect(self.onclick_enabletest)
        self.ui.pb_logfreq.clicked.connect(self.onclick_logfreq)
        self.ui.pb_logpres.clicked.connect(self.onclick_logpres)
        self.ui.pb_logandinc.clicked.connect(self.onclick_logandinc)

    def onclick_logfreq(self):
        if(self.test_enabled == True):
            self.test_level = self.ui.spinBox_testlevel.value()
            self.log_data(log_freq=True)
            ##write frequency to datalog


    def onclick_logpres(self):
        if(self.test_enabled == True):
            self.test_level = self.ui.spinBox_testlevel.value()
            self.log_data(log_freq=False, log_pmax=True, log_pmin=True, log_pabs=True)

    def onclick_logandinc(self):
        if(self.test_enabled == True):
            self.test_level = self.ui.spinBox_testlevel.value()
            self.log_data(log_freq=True,log_pmax=True,log_pmin=True,log_pabs=True)
            self.test_level +=1
            self.ui.spinBox_testlevel.setValue(self.test_level)


    def onclick_spin_testlevel(self):
        if(self.test_enabled == True):
            self.reset_testlevel_instance()
            self.datafile_line += 1









    def onclick_enabletest(self):
        if(self.test_enabled == True): #test in progress
            self.finish_test_instance()
            self.test_enabled = False

        else:
            tempstr = self.ui.lineEdit_deviceid.text()
            if (tempstr == "Enter Device Name"):
                print("Please Enter Device ID")
                self.ui.label_appStatus.setText("Must Enter Valid Device ID - Try to keep short and meaningful- ex: Onda2proto0411A")
                self.ui.pb_enabletest.setChecked(False)
            elif (tempstr.__contains__(" ")):
                print("Device ID must NOT contain spaces")
                self.ui.label_appStatus.setText("Must Enter Valid Device ID - Must NOT Contain Spaces")
                self.ui.pb_enabletest.setChecked(False)

            elif self.b_network_status == False:
                print("Network Connection Issues")
                self.ui.label_appStatus.setText("Please verify Oscope is setup and connected to LAN")
                self.ui.pb_enabletest.setChecked(False)

            else:
                self.test_enabled = True
                self.init_testing()

                #self.ui.pb_enabletest.setChecked(True)

    def init_testing(self):
        self.ui.pb_enabletest.setText("DISABLE TEST + SAVE")
        self.ui.label_appStatus.setText("Data File Created- Begin to Gather P/F Data")
        self.ui.frame_TestSetup.setEnabled(False)
        self.ui.frame_Testing.setEnabled(True)
        self.ui.label_teststatus.setText("Testing Enabled")
        self.ui.label_teststatus.setEnabled(True)

        self.ui.spinBox_testlevel.setValue(1)

        self.init_datafile()

        #self.fetch_scope_data()
        #print(self.check_network_connection())

    def finish_test_instance(self):

        self.ui.pb_enabletest.setText("ENABLE TESTING")
        self.ui.label_appStatus.setText("Enter information for Test Device")
        self.ui.frame_TestSetup.setEnabled(True)
        self.ui.frame_Testing.setEnabled(False)
        self.ui.label_teststatus.setText("Testing Disabled")

        self.time_clock = time.strftime("%Y-%m-%d", gmtime())
        self.datafile.save(self.datafile_name)
        self.ui.textBrowser.append("Datafile Saved")
        self.ui.textBrowser.append(self.datafile_rel)
        print("\n")
        print("Data File Saved ")
        print(self.datafile_name)
        #Open logfile in same folder directory- search for files of same name- if exists, test_code. Then search again until no returns

    def get_datafile_name(self):
        rootdir = os.path.dirname(__file__)

        file_name = os.path.join(rootdir, "data/testf3.xls")


        self.time_clock = time.strftime("%Y-%m-%d", gmtime())

        self.datafile_date = self.time_clock
        self.dut_id = self.ui.lineEdit_deviceid.text()


        self.datafile_rel   = "data/"+self.dut_id+"_PFtesting_"+self.datafile_date+"_"+str(self.test_code)+".xls"
        self.datafile_name  = os.path.join(rootdir, self.datafile_rel)


    def init_datafile(self):
        self.test_code = 1
        self.get_datafile_name()
        print(self.datafile_name)

        #Open logfile in same folder directory- search for files of same name- if exists, test_code. Then search again until no returns
        self.datafile_line = 0

        file_name_unique = False

        while(file_name_unique == False):
            try:
                self.get_datafile_name()
                f = open(self.datafile_name, "r")
                # Do something with the file
            except IOError:  # meaning file Does NOT exists
                print("File Does Not Exist - Creating New")
                file_name_unique = True
            else:  ##file Does exist - increment code
                print("File Does Exist - incrementing code")
                f.close()
                self.test_code += 1
                self.get_datafile_name()
            time.sleep(.2)


        self.datafile = xlwt.Workbook()



        self.report_sheet = self.datafile.add_sheet("pf data")

        temp = self.report_sheet.col(0)
        temp.width = 5000

        temp2 = self.report_sheet.col(1)
        temp2.width = 5000


        for i in range(2,7):
            temp = self.report_sheet.col(i)
            temp.width = 4000









        self.report_sheet.write(0, 0, "LDC Air Stimulation Pressure/Frequency Test Data")
        self.report_sheet.write(1,0, "Date:")
        self.report_sheet.write(1,1, self.datafile_date)

        tempstr = self.ui.lineEdit_ldcrep.text()
        if(tempstr == "Who Performed Testing"):
            tempstr = "No Rep Entered"
        self.report_sheet.write(2, 0, "LDC Rep:")
        self.report_sheet.write(2,1, tempstr)

        self.report_sheet.write(3, 0, "Sensor/s:")
        self.report_sheet.write(3, 1, self.ui.lineEdit_sensorID.text())

        self.report_sheet.write(4, 0, "Seal Interface:")
        tmp="Unknown Seal Interface"
        if(self.ui.radioButton_testmeth_fixture.isChecked()):
            tmp = "Fixtured DUT"
        if(self.ui.radioButton_testmeth_handpuck.isChecked()):
            tmp = "Handheld Puck"
        self.report_sheet.write(4, 1, tmp )

        self.report_sheet.write(5,0, "Device (DUT):")
        self.report_sheet.write(5, 1, self.ui.lineEdit_deviceid.text())

        self.report_sheet.write(6,0, "Device Info:")
        tempstr = self.ui.lineEdit_deviceid_2.text()
        if(tempstr == "Enter Important Device Info"):
            tempstr = "No Info Entered"
        self.report_sheet.write(6, 1, tempstr)

        self.report_sheet.write(7, 0, "Datafile Line#")
        self.report_sheet.write(7, 1, "Test Device Level#")
        self.report_sheet.write(7, 2, "Frequency [Hz]")
        self.report_sheet.write(7, 3, "Pressure Max [psi]")
        self.report_sheet.write(7, 4, "Pressure Min [psi]")
        self.report_sheet.write(7, 5, "Pressure Abs [psi]")



#
        #        for x in range(1, 11):
#            for y in range(1, 11):
#                sheet.write(x - 1, y - 1, x * y)







    def init_scope(self):
        self.oscope = DS1054Z('10.10.10.232')
        print(self.oscope.idn)
        #self.ui.label_appStatus.setText(self.scope.idn)

    def fetch_scope_data(self):
        if(DEBUG_NOSCOPE == False):
            self.frequency = self.oscope.get_channel_measurement(1, item='frequency', type='AVER')
            if(not isinstance(self.frequency, float)):
                self.frequency = 0.0

            volts_max_avg = self.oscope.get_channel_measurement(1, item='vmax', type='AVER')
            #print("Volts Max"+str(volts_max_avg))
            if(not isinstance(volts_max_avg, float)):
                volts_max_avg = 0.0

            volts_min_avg = self.oscope.get_channel_measurement(1, item='vmin', type='AVER')
            #print("Volts Min"+str(volts_min_avg))
            if(not isinstance(volts_min_avg, float)):
                volts_min_avg = 0.0
        else:
            self.frequency = 1.0
            volts_max_avg = 1.0
            volts_min_avg = 1.0

        #print("Volts Max2" + str(volts_max_avg))
        #print("Volts Min2" + str(volts_min_avg))

        self.pressure_max = (volts_max_avg - 3.0) / 0.1379
        #print("Press Max"+str(self.pressure_max))
        self.pressure_min = (volts_min_avg - 3.0) / 0.1379
        #print("Press Min"+str(self.pressure_min))


        if(self.pressure_min < 0):
            volts_abs = volts_max_avg +(-volts_min_avg)
            self.pressure_abs = self.pressure_max + (-self.pressure_min)
        else:
            volts_abs = volts_max_avg + (volts_min_avg)
            self.pressure_abs = self.pressure_max + (self.pressure_min)

        #\\print("Press Abs" + str(self.pressure_abs))

        self.pressure_abs = round(self.pressure_abs, 3)
        self.pressure_min = round(self.pressure_min, 3)
        self.pressure_max = round(self.pressure_max, 3)
        self.frequency = round(self.frequency,3)


        self.ui.lcdNumber_avgfreq.display(self.frequency)
        self.ui.lcdNumber_maxpres.display(self.pressure_max)
        self.ui.lcdNumber_minpres.display(self.pressure_min)
        self.ui.lcdNumber_abspres.display(self.pressure_abs)
        #self.log_data(freq=self.frequency, minpressure=self.pressure_min, maxpressure=self.pressure_max, abspressure=self.pressure_abs)

    def check_network_connection(self):
        scope_id = self.oscope.idn
        if(scope_id.__contains__('RIGOL')):
            self.b_network_status = True
            return True

        else:
            self.b_network_status = False
            return False

    def reset_testlevel_instance(self):
        self.testlevel_instance['Freq'] = None
        self.testlevel_instance['Pmax'] = None
        self.testlevel_instance['Pmin'] = None
        self.testlevel_instance['Pabs'] = None

    #def log_data(self, testlevel = None, freq = None, minpressure = None, maxpressure = None, abspressure = None):

    def log_data(self, log_freq = False, log_pmax = False, log_pmin = False, log_pabs = False):
        #self.test_level = self.ui.spinBox_testlevel.value()
        ##test level might be tested more than once- if so, keep testlevel the same- and datafile_line++
        ##datafile_line is generally 1-10, though could be larger if multiple tests on the same test_level
        if(log_freq == True):
            if(self.testlevel_instance['Freq'] == None):
                self.testlevel_instance['Freq'] = self.frequency
                self.report_sheet.write((DATA_OFFSET+self.datafile_line), COL_FREQ, self.frequency)
                #log freq in correct cell on line datafile_line

        if(log_pmax == True):
            if(self.testlevel_instance['Pmax'] == None):
                self.testlevel_instance['Pmax'] = self.pressure_max
                self.report_sheet.write((DATA_OFFSET + self.datafile_line), COL_PRES_MAX, self.pressure_max)
                # log into correct cell on line datafile_line

        if(log_pmin == True):
            if(self.testlevel_instance['Pmin'] == None):
                self.testlevel_instance['Pmin'] = self.pressure_min
                self.report_sheet.write((DATA_OFFSET + self.datafile_line), COL_PRES_MIN, self.pressure_min)
                #log into correct cell on line datafile_line

        if(log_pabs == True):
            if(self.testlevel_instance['Pabs'] == None):
                self.testlevel_instance['Pabs'] = self.pressure_abs
                self.report_sheet.write((DATA_OFFSET + self.datafile_line), COL_PRES_ABS, self.pressure_abs)
                # log into correct cell on line datafile_line


        print("Datafile Line#: "+str(self.datafile_line)+" TestLevel:"+str(self.test_level)+ str(self.pressure_max)+" "+ str(self.pressure_min)+" "+ str(self.pressure_abs))
        self.ui.textBrowser.append("Line#:"+str(self.datafile_line)+" Device Setting#:"+str(self.test_level)+"  f[Hz]:"+str(self.frequency)+"   Pmin[psi]:"+str(self.pressure_max)+"   Pmax[psi]:"+ str(self.pressure_min)+"   Pabs[psi]:"+ str(self.pressure_abs))

        if(self.testlevel_instance['Freq']!=None and self.testlevel_instance['Pmin']!=None and self.testlevel_instance['Pmax']!=None and self.testlevel_instance['Pabs']!=None):
            self.report_sheet.write((DATA_OFFSET + self.datafile_line), COL_DF_LINE, self.datafile_line)
            self.report_sheet.write((DATA_OFFSET + self.datafile_line), COL_DEV_LEVEL, self.test_level)
            self.datafile_line += 1
            self.reset_testlevel_instance()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Main()
    form.show()
    sys.exit(app.exec_())




