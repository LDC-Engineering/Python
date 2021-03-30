import serial  # import Serial Library
import numpy  # Import numpy
import matplotlib.pyplot as plt  # import matplotlib library
from drawnow import *
#import random_gen
import random

f = 0.0

f = 5 * (random.random())
print (f)

script_active = True












def GetSerialPort():
    theNum = input("Enter the Serial Port Number >>")
    if theNum.isdigit():
        return theNum
    else:
        return False

def initDataSources():
    '''create objects etcs for each data source- serial, i2c etc'''
    pass

def get_data():
    '''return two floats for both axis'''
    pass

def handle_close(evt):
    global script_active

    print('Closed Figure!')
    plt.close()
    script_active = False



tempF = []
pressure = []
#serialData = serial.Serial('com11', 115200)  # Creating our serial object named serialData
plt.ion()  # Tell matplotlib you want interactive mode to plot live data
cnt = 0
plt.connect('close_event', handle_close)


print("please enter first x-variable>>")
print("please enter y-min")
print(GetSerialPort())


def makeFig():  # Create a function that makes our desired plot
   # if(plt.)
    plt.ylim(0, 5)  # Set y min and max values
    plt.title('My Live Streaming Sensor Data')  # Plot the title
    plt.grid(True)  # Turn the grid on
    plt.ylabel('Temp F')  # Set ylabels
    plt.plot(tempF, 'ro-', label='Degrees F')  # plot the temperature
    plt.legend(loc='upper left')  # plot the legend
    plt2 = plt.twinx()  # Create a second y axis
    plt.ylim(0, 5)  # Set limits of second y axis- adjust to readings you are getting
    plt2.plot(pressure, 'b^-', label='Pressure (Pa)')  # plot pressure data
    plt2.set_ylabel('Pressrue (Pa)')  # label second y axis
    plt2.ticklabel_format(useOffset=False)  # Force matplotlib to NOT autoscale y axis
    plt2.legend(loc='upper right')  # plot the legend


while True:  # While loop that loops forever
    # while (serialData.inWaiting() == 0):  # Wait here until there is data
    #     pass  # do nothing
    # arduinoString = serialData.readline()  # read the line of text from the serial port
    # dataArray = arduinoString.split(',')  # Split it into an array called dataArray
    # temp = float(dataArray[0])  # Convert first element to floating number and put in temp
    # P = float(dataArray[1])  # Convert second element to floating number and put in P
    if(script_active == True):
        temp = 5*random.random()
        P = 4*random.random()
        tempF.append(temp)  # Build our tempF array by appending temp readings
        pressure.append(P)  # Building our pressure array by appending P readings
        drawnow(makeFig)  # Call drawnow to update our live graph
        plt.pause(.000001)  # Pause Briefly. Important to keep drawnow from crashing
        cnt = cnt + 1
        if (cnt > 50):  # If you have 50 or more points, delete the first one from the array
            tempF.pop(0)  # This allows us to just see the last 50 data points
            pressure.pop(0)
