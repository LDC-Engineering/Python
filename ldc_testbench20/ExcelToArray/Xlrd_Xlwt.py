import xlrd
import xlwt
import xlutils
import os


##first

relpath = "/data/"
title1 = "protoA"
data = "01_10_11"
code = 1
file_name = ''



fileDir = os.path.dirname(os.path.realpath('__file__'))
print (fileDir)



c
print(file_name)


#file_name = 'test.xls'


def get_filename():
    global file_name
    file_name = title1+data+"_"+str(code)+".xls"

f = open(file_name, 'w')

f.close()

while(True):
    pass
#get_filename()

try:
    f = open(file_name, "r")
    # Do something with the file
except IOError: #meaning file Does NOT exists
    print("File Does Not Exist - Creating New")
else: ##file Does exist
    print("File Does Exist - incrementing code")
    f.close()
    code+=2
    get_filename()


datafile = xlwt.Workbook()

sheet = datafile.add_sheet("pf data")

for x in range(1,11):
    for y in range(1,11):
        sheet.write(x-1,y-1,x*y)



datafile.save(file_name)

