import subprocess
import os
import SAT as SAT
import xlsxwriter
import dimacs_decoder as dimacs

directoryName = 'dimacs/1000sudokus/'
directory = os.fsencode(directoryName) ## map containing our sudokus
    
sudokuSize = 9 
rulePath = 'dimacs/rulesets/sudoku-rules.txt'   
ruleSet = dimacs.dimacs_rules(rulePath)    
subprocess.call(['py', 'SAT.py', '-S1', 'input.txt', str(sudokuSize)])    
sudokuList = [] ## put every filename in a list  
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        sudokuList.append(directoryName+'/'+filename)

workbook = xlsxwriter.Workbook('src/statistics_data/SATResults.xlsx')
heuristiclist = [['-S1', 'None'], ['-S2','DLCS'], ['-S3', 'DLISN'], ['-S4', 'DLISP'], ['-S5','MOMS'], ['S6', 'VSIDS']]  
for heuristic in heuristiclist:
    maxNumber = 0 
    timeList = []
    satList = []
    lengthList = []
    branchList = []
    for sudoku in sudokuList:
        if(maxNumber == 200): ## how many sudoku's do we want to solve in this experiment?
            break
        time, satisfied, startLength, branches = SAT.main(sudoku, heuristic, False) ## solve the sudoku
        timeList.append(time)
        satList.append(satisfied) ## keep track of time, wether or not is was solved, and how many numbers we start with
        lengthList.append(startLength)
        branchList.append(branches)
        maxNumber += 1

    if(heuristic == None): ## to prevent errors when creating excel sheets.
        heuristic = 'None'

    worksheet = workbook.add_worksheet(heuristic) ## make an excel file, write the headers
    worksheet.write('A1', 'Sudoku number')
    worksheet.write('B1', 'startLength')
    worksheet.write('C1', 'Time')
    worksheet.write('D1', 'Satisfied')
    worksheet.write('E1', 'branches')

    i = 2
    for number, time, satisfied, startLen, branches in zip(sudokuList, timeList, satList, lengthList, branchList):## write all of our data into the excel file.
        worksheet.write('A'+str(i), number[len(directoryName)+7:-4])  ## [6:-4] removes the first 6 letters ('sudoku') and last 4 ('.txt').
        worksheet.write('B'+str(i), startLen)
        worksheet.write('C'+str(i), time)
        worksheet.write('D'+str(i), satisfied)
        worksheet.write('E'+str(i), branches)
        
        i += 1
    
workbook.close()