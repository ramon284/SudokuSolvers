import os
import SAT as SAT
import dimacs_decoder as dimacs
import time as t

sudokuSizes = [4, 9]
<<<<<<< Updated upstream
maxNumber = 10 ## amount of sudokus we want to solve (per size)
=======
maxNumber = 1000 ## amount of sudokus we want to solve (per size)
>>>>>>> Stashed changes

for sudokuSize in sudokuSizes:
    directoryName = ''
    if(sudokuSize == 9):
        directoryName = 'dimacs/1000sudokusWithRules/'
        ruleLength = 11988
    elif(sudokuSize == 4):
        directoryName = 'dimacs/4x4sudokusWithRules/'
        ruleLength = 448
    directory = os.fsencode(directoryName) ## map containing our sudokus
            
    sudokuList = [] ## put every filename in a list  
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            sudokuList.append(directoryName+'/'+filename)


    workbook = xlsxwriter.Workbook('statistics_data/SATResults' +str(sudokuSize)+'.xls')
    heuristiclist = [['-S1', None], ['-S2','DLCS'], ['-S3', 'DLISN'], ['-S4', 'DLISP'], ['-S5','MOMS'], ['S6', 'VSIDS']]  




    for heuristic in heuristiclist:
        solved = 0 
        ########################################################
        timeList = []   ## lists containing data for every time we run SAT
        lengthList = [] ## we need one list per statistic that we're tracking.
        branchList = [] ## add new lists here if we track new statistics, append in the for loop below.
        ########################################################
        for sudoku in sudokuList:
            if(solved == maxNumber): ## how many sudoku's do we want to solve in this experiment?
                break
            sudoku = dimacs.dimacs_rules(sudoku)
            startLength = len(sudoku) - ruleLength
            t1 = t.time()
            sol, branches = SAT.backtracking(cnf_formula=sudoku, heuristic=heuristic[1],) ## solve the sudoku,
            time = t.time()-t1
            timeList.append(time) ## keep track of time, wether or not is was solved, and how many numbers we start with
            lengthList.append(startLength) ## add to the lists
            branchList.append(branches)
            solved += 1
            print('sudoku completed :)')
            
        if heuristic[1] == None: heuristic[1] = 'None'
        worksheet = workbook.add_worksheet(heuristic[1]) ## make an excel file, write the headers
        worksheet.write('A1', 'Sudoku number')
        worksheet.write('B1', 'startLength')
        worksheet.write('C1', 'Time')
        worksheet.write('D1', 'branches')
        ############################################################
        ##worksheet.write('E1', '')
        ##worksheet.write('F1', '') 
        ##worksheet.write('G1', '') ## Can add extra data here
        ##worksheet.write('H1', '')
        ##worksheet.write('I1', '')
        ############################################################

        i = 2
        for number, time, startLen, branches in zip(sudokuList, timeList, lengthList, branchList):## write all of our data into the excel file.
            worksheet.write('A'+str(i), number[len(directoryName)+7:-4])  ## [6:-4] removes the first 6 letters ('sudoku') and last 4 ('.txt').
            worksheet.write('B'+str(i), startLen)
            worksheet.write('C'+str(i), time)
            worksheet.write('D'+str(i), branches)
            ##########################################################
            ##worksheet.write('E'+str(i), xxx)
            ##worksheet.write('F'+str(i), xxx)
            ##worksheet.write('G'+str(i), xxx)
            ##worksheet.write('H'+str(i), xxx)
            ##worksheet.write('I'+str(i), xxx)
            ##########################################################
            i += 1
    
    workbook.close()