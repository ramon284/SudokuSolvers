import os
import rumy_sat_solver as SAT
import xlsxwriter

directoryName = '1000sudokus'
directory = os.fsencode(directoryName) ## map containing our sudokus
    
sudokuList = [] ## put every filename in a list  
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        sudokuList.append(directoryName+'\\'+filename)

timeList = []
satList = []
lengthList = []
for sudoku in sudokuList:
    time, satisfied, startLength = SAT.main(sudoku) ## solve the sudoku
    timeList.append(time)
    satList.append(satisfied) ## keep track of time, wether or not is was solved, and how many numbers we start with
    lengthList.append(startLength)
    
workbook = xlsxwriter.Workbook('BasicSATResults.xlsx')
worksheet = workbook.add_worksheet('1') ## make an excel file, write the headers
worksheet.write('A1', 'Sudoku number')
worksheet.write('B1', 'startLength')
worksheet.write('C1', 'Time')
worksheet.write('D1', 'Satisfied')

i = 2
for number, time, satisfied, startLen in zip(sudokuList, timeList, satList, lengthList):## write all of our data into the excel file.
    worksheet.write('A'+str(i), number[len(directoryName)+7:-4])  ## [6:-4] removes the first 6 letters ('sudoku') and last 4 ('.txt').
    worksheet.write('B'+str(i), startLen)
    worksheet.write('C'+str(i), time)
    worksheet.write('D'+str(i), satisfied)
    i += 1
    
workbook.close()

