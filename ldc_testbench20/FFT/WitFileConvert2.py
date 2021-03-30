import csv

txt_file = "mytxt.txt"
csv_file = "mycsv.csv"

# use 'with' if the program isn't going to immediately terminate
# so you don't leave files open
# the 'b' is necessary on Windows
# it prevents \x1a, Ctrl-z, from ending the stream prematurely
# and also stops Python converting to / from different line terminators
# On other platforms, it has no effect

rawdata_X_array = []
rawdata_Y_array = []
rawdata_Z_array = []

with open(txt_file, newline='') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        if(row[0]=='0x50'):
            rawdata_X_array.append(row[2])
            rawdata_Y_array.append(row[3])
            rawdata_Z_array.append(row[4])

print(rawdata_X_array)
'''
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(reader)        
col 2 x
col 3 y
col 4 z

reader = csv.reader(open(txt_file, 'r', newline=''), delimiter = '\t')

for row in reader:
    if(row[0] == '0x50'):
        x = row[2]
        print(row[2])

print("hello = {}".format(x))


in_txt = csv.reader(open(txt_file, 'r', newline=''), delimiter = '\t')
print(in_txt)
print(in_txt.line_num())
out_csv = csv.writer(open(csv_file, 'w', newline=''))

out_csv.writerows(in_txt)
'''