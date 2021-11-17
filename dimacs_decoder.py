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
                    clause.append(element)
                else:
                    clause.append(element)
            rules.append(clause)
    return rules


def dimacs_start(file):  # parse the starting points into a list
    locations = [line.strip() for line in open(file, 'r')]
    location_list = []
    for position in locations:
        location_list.append((position[:3]))
    return location_list


def dimacs_encode(solution, name):  # turns solution list into dimacs format.
    solution_name = "sudoku-solution" + name + ".txt"
    with open(solution_name, 'w') as f:
        for element in solution:
            f.write(str(element) + " 0\n")

# start = dimacs_start('sudoku-example.txt')
# rules = dimacs_rules("D:\Projects\SudokuSolvers\sudoku-rules.txt")
# print(rules)
