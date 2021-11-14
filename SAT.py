import Dimacs_decoder as dim
import time


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

startName = 'sudoku-example.txt'
sudokuSize = 9
start = dim.dimacs_start(startName)
rules = dim.dimacs_rules('sudoku-rules.txt')

def SAT(solution, rules):
    clauseBool = True
    for clause in rules:
        literalBool = False
        for literal in clause: 
            if(literalBool == True):
                break
            if (literal[0] == 1):
                for sol in solution:
                    if(sol == literal[1]):
                        literalBool = True
                        break
            if (literal[0] == 0):
                if not (literal[1] in solution):
                    clauseBool = True
                    break
                else:
                    clauseBool = False
        if (clauseBool == False): ## clause is false, try new solution.
            #print('failed because of clause: ', clause)
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

#print(SAT(start, rules))
solution = createSolution(start, sudokuSize)
print('importanto:      ',len(solution))
tempgrid = into_grid(solution, sudokuSize)
grid_printer(tempgrid, sudokuSize)



