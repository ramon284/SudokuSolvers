def dimacs_rules(file): ## creates a list containing clauses of rules
    sudoku_rules = [line.strip() for line in open(file, 'r')]
    rules = []
    for line in sudoku_rules:
        clause = []
        if ((line[0].isdigit()) or (line[0] == "-")): ## ignor header lines
            line = [int(i) for i in line.split()]  
            if (line[-1] == 0):
                line.pop() ## remove the 0 from the lines, do we need the "if"?
            for element in line:
                if (str(element)[0] == '-'):
                    clause.append((0, abs(element)))
                else:
                    clause.append((1, element))                
            rules.append((clause))
    return rules
  
def dimacs_start(file): ## parse the starting points into a list
    locations = [line.strip() for line in open(file, 'r')]
    locationList = []   
    for position in locations:
        locationList.append(int(position[:3]))
    return locationList

def dimacs_encode(solution, name): ## turns solution list into dimacs format.
    solutionName = "sudoku-solution"+name+".txt"
    with open(solutionName, 'w') as f:
        for element in solution:
            f.write(str(element) + " 0\n")
        
rulesFile = "sudoku-rules.txt"
startFile = "sudoku-example.txt"
rules = dimacs_rules(rulesFile)
startLocations = dimacs_start(startFile)
dimacs_encode(startLocations,'1')
        

            
            
        


        
        
            
        
        