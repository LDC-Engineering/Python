import xlrd
workbook = xlrd.open_workbook('VibData1.xls')
worksheet = workbook.sheet_by_name('Sheet1')
num_rows = worksheet.nrows - 1
curr_row = 0

#creates an array to store all the rows
row_array = []
data1_array = []
column=0

while curr_row < num_rows:
    dataVal = worksheet.cell(curr_row, column)
    data1_array.append(dataVal.value)
    curr_row += 1
 #   row = worksheet.row(curr_row)
  #  row_array += row


print(data1_array)