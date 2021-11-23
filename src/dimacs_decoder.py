def dimacs_rules(file):  # creates a list containing clauses of rules
    sudoku_rules = [line.strip() for line in open(file, 'r')]
    rules = []
    for line in sudoku_rules:
        clause = []
        if (line[0].isdigit()) or (line[0] == "-"):  # ignore header lines
            line = [x for x in line.split()]
            if line[-1] == '0':
                line.pop()  # remove the 0 from the lines, do we need the "if"?
            for element in line:
                if element[0] == '-':
                    clause.append(int(element)) ## integers
                    #clause.append(element) ## strings
                else:
                    clause.append(int(element))
                    #clause.append(element)
            rules.append(clause)
    return rules


def dimacs_start(file):  # parse the starting points into a list
    locations = [line.strip() for line in open(file, 'r')]
    location_list = []
    for position in locations:
        location_list.append([(int(position[:3]))]) ## int
        #location_list.append((position[:3])) ## str
    return location_list


def dimacs_encode(solution, name):  # turns solution list into dimacs format.
    if(name[-4:] != '.txt'):
        name = name+'.txt'
    with open(name, 'w') as f:
        for element in solution:
            element = str.strip(str(element), '[]')
            f.write(element.replace(',','') + " 0\n")
            
def sudoku_file_into_dimacs_file(filePath, rules):
    with open (filePath) as f: ## takes a .txt file with 81 characters representing the start of a sudoku board
        i = 0                  ## and turns it into a dimacs format, for testing purposes.
        for line in f:
            dimacs = rules[:]
            for row in range(1,10):
                for column in range(1,10):
                    if(line[0] != '.'):
                        dimacs.append(str(row)+str(column)+line[0])
                    line = line[1:]
            dimacs_encode(dimacs, 'dimacs/1000sudokusWithRules/sudoku'+str(i))
            i += 1

rules = dimacs_rules('dimacs/rulesets/sudoku-rules.txt')

sudoku_file_into_dimacs_file('test_problems/1000sudokus.txt', rules)   

# start = dimacs_start('sudoku-example.txt')
# rules = dimacs_rules("D:\Projects\SudokuSolvers\sudoku-rules.txt")
# print(rules)
