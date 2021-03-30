import glob
import os


RAW_SENSOR_FILE_NAME = r'201215172523.txt'
RAW_SENSOR_FILE_PATH = r'C:/Users/wadre/OneDrive/Desktop/WIT_Sensor/BWT901CL-20201207T194636Z-001/BWT901CL/Standard Software for Windows PC/Data/'


list_of_files = glob.glob('C:/Users/wadre/OneDrive/Desktop/WIT_Sensor/BWT901CL-20201207T194636Z-001/BWT901CL/Standard Software for Windows PC/Data/*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print (latest_file)