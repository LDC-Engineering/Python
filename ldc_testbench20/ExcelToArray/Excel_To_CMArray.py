import numpy as np
import pylab as pl
import random
import xlrd
import sys
import xlwt
import time
from datetime import datetime

RawDataFile = "Spreadsheet_Data"



embedded_file = 'C:/Users/wadre/OneDrive/Documents/CM_LDC_UI_Arrays.txt'

array_file = open(embedded_file, "w")
#array_file = open("Array_File.txt", "w")

workbook = xlrd.open_workbook(RawDataFile+'.xls')
worksheet = workbook.sheet_by_name('optionB')
num_rows = worksheet.nrows
num_cols = worksheet.ncols
curr_row = 0


#creates an array to store all the rows
row_array = []
data1_array = []
column=0

array_file.write("unsigned int array_generated")
array_file.write("["+str(num_rows)+"]"+"["+str(num_cols)+"] = ")
array_file.write("{")
array_file.write("\n")
while curr_row < (num_rows):
    dataVal_1 = (worksheet.cell(curr_row, column+4))
    dataVal_2 = (worksheet.cell(curr_row, column+3))

    dataVal_1 = str(int(dataVal_1.value))
    dataVal_2 = str(int(dataVal_2.value))


    array_file.write("{"+dataVal_1+","+dataVal_2+"}")
    if(curr_row < (num_rows-1)):
        array_file.write(",")
    array_file.write("\n")
    curr_row += 1

array_file.write("};")



array_file.close()

print("Conversion Done")