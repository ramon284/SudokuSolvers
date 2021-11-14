import Dimacs_decoder as dim
import time

def negate(number): ## actually has strings as in- and output.
    if (int(number) < 0):
        return str(abs(int(number)))
    return ('-'+number)

def grid_printer(grid, sudokuSize): ## prints our sudoku game nicely.
    i = 0
    for row in grid:
        if(i % 3 == 0):
            print('-'*sudokuSize*3)
        print('|',row[0],row[1],row[2],'|',row[3],row[4],row[5],'|',
              row[6],row[7],row[8],'|')
        i += 1
    print('-'*sudokuSize*3)
    
def into_grid(solution, sudokuSize):
    grid = [[0 for x in range(sudokuSize)] for y in range(sudokuSize)]
    for sol in solution:
        print(sol)
        row, col = sol[0], sol[1]
        grid[int(row)-1][int(col)-1] = sol[2]
    return grid

def SAT(solution, rules):
    clauseBool = True
    for clause in rules: # check all clauses
        literalBool = False 
        for literal in clause: 
            if(literalBool == True):
                break
            if (literal[0] == '-'): ## these are the "not x or not y" clauses
                if(literal in solution):
                    clauseBool = True
                    break
                else:
                    clauseBool = False
            if (literal[0] != '-'): ## these are the big clauses, checking for positives
                if (literal in solution):
                    clauseBool = True
                    break
                clauseBool = False
                
        if (clauseBool == False): ## clause is false, try new solution.
            print('failed because of clause: ', clause)
            return False
    return True

def createSolution(start, sudokuSize):
    start_time = time.time()
    x = 0
    addedElements = []
    discarded = []
    while(True):
        for row in range(1, sudokuSize + 1):
            for column in range(1, sudokuSize + 1):
                for i in range(1, sudokuSize + 1):
                    new = str(row)+str(column)+str(i)
                    if(new in start):
                        continue ## ignore if duplicate.
                    temp = start[:]
                    temp.append(new)
                    if(SAT(temp, rules) == True):
                        ## this means the location isn't illegal
                        pass ## but it could still be wrong.
                    else:
                        ## 
                        pass
          
        if(len(start) == 81):
            print(time.time() - start_time)
            return start

startName = 'sudoku-example.txt'
sudokuSize = 9
start = dim.dimacs_start(startName) ## setting up rules and start locations
rules = dim.dimacs_rules('sudoku-rules.txt')

allNumbers = ['-'+str(i) for i in range(111,1000)] ## create every possible number, start as False
allNumbers = [x for x in allNumbers if not ('0' in x)]

for element in start: ## turn the False start numbers into True (regular numbers)
    if ('-'+element in allNumbers):
        idx = (allNumbers.index('-'+element))
        allNumbers[idx] = negate(allNumbers[idx])
print(allNumbers)




