import os
import SAT as SAT
import dimacs_decoder as dimacs
import time as t
import pandas as pd

sudokuSizes = [4, 9]
maxNumber = 5 ## amount of sudokus we want to solve (per size) ## normally 1000

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

    heuristiclist = [['-S1', None], ['-S2','DLCS'], ['-S3', 'DLISN'], ['-S4', 'DLISP'], ['-S5','MOMS']]  

    for heuristic in heuristiclist:
        solved = 0 
        timeList = []   ## lists containing data for every time we run SAT
        lengthList = [] ## we need one list per statistic that we're tracking.
        branchList = [] ## add new lists here if we track new statistics, append in the for loop below.
        unitClauseList = []
        pureClauseList = []
        for sudoku in sudokuList:
            if(solved == maxNumber): ## how many sudoku's do we want to solve in this experiment?
                break
            sudoku = dimacs.dimacs_rules(sudoku)
            startLength = len(sudoku) - ruleLength
            t1 = t.time()
            sol, branches, rem_unit_clause, rem_pure_clause = SAT.backtracking(cnf_formula=sudoku, heuristic=heuristic[1],) ## solve the sudoku,
            time = t.time()-t1
            timeList.append(time) ## keep track of time, wether or not is was solved, and how many numbers we start with
            lengthList.append(startLength) ## add to the lists
            branchList.append(branches)
            unitClauseList.append(rem_unit_clause)
            pureClauseList.append(rem_pure_clause)
            solved += 1
            
        if heuristic[1] == None: heuristic[1] = 'None'
        ## 'Sudoku number': sudokuList[:maxNumber],
        excel = pd.DataFrame({
            'start Length': lengthList,
            'Time': timeList,
            'Branches': branchList,
            'Unit clauses removed': unitClauseList,
            'Pure clauses removed': pureClauseList
        })
        excel.to_csv('statistics_data/'+str(sudokuSize)+'x'+str(sudokuSize)+'/'+str(heuristic[1])+'.csv')
        print(heuristic[1] + str(sudokuSize) +' - file created')