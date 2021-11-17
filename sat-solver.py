import time

import dimacs_decoder as dim


def negate(number):  # actually has strings as in- and output.
    if int(number) < 0:
        return str(abs(int(number)))
    return '-' + number


def grid_printer(solution, sudoku_size):  # prints our sudoku game nicely.
    grid = into_grid(solution, sudoku_size)
    i = 0
    for row in grid:
        if i % 3 == 0:
            print('-' * sudoku_size * 3)
        print('|', row[0], row[1], row[2], '|', row[3], row[4], row[5], '|',
              row[6], row[7], row[8], '|')
        i += 1
    print('-' * sudoku_size * 3)


def into_grid(solution, sudoku_size):
    grid = [[0 for x in range(sudoku_size)] for y in range(sudoku_size)]
    for sol in solution:
        print(sol)
        row, col = sol[0], sol[1]
        grid[int(row) - 1][int(col) - 1] = sol[2]
    return grid


def dpll_ramon(solution, sudoku_rules):
    clause_bool = True
    for clause in sudoku_rules:  # check all clauses
        for literal in clause:  # works for both positive and negative literals
            if literal[0] == '-':  # these are the "not x or not y" clauses
                if not (literal[1:] in solution):
                    clause_bool = True
                    break  # if one of the numbers is not found, return true
                else:
                    clause_bool = False  # if all are found, it will be false.

            if len(solution) == 81:
                if literal[0] != '-':  # these are the big clauses, checking for positives
                    if literal in solution:  # problem:always returns false for sudoku's that aren't 100% filled in yet.
                        clause_bool = True
                        break
                    else:
                        clause_bool = False
        if not clause_bool:  # clause is false
            # print('failed because of clause: ', clause)
            return False
    return True


def create_solution(start, sudoku_size):
    start_time = time.time()
    discarded = []
    added = []
    solution = start[:]
    attempt = True
    for row in range(1, 10):
        for column in range(1, 10):
            temp = True
            row_column = str(row) + str(column)  # creates for example '15' for row 1 column 5
            for sol in solution:
                if sol[:2] == row_column:  # checks if this location is already filled
                    temp = False
                    break
            if not temp:  # if it is, move to the next location (next column)
                continue
            for i in range(1, 10):
                new = row_column + str(i)
                solution.append(new)
                if dpll_ramon(solution, rules):
                    create_solution(solution, sudoku_size)
                    if len(solution) == 81:
                        print("--- %s seconds ---" % (time.time() - start_time))
                        return solution
                    solution.pop()

                else:
                    solution.pop()


startName = 'sudoku-example.txt'
sudokuSize = 9
start = dim.dimacs_start(startName)  # setting up rules and start locations
rules = dim.dimacs_rules('sudoku-rules.txt')

x = create_solution(start, rules)
print(x)

# print(allNumbers)
# print(SAT(allNumbers, rules))


# allNumbers = ['-'+str(i) for i in range(111,1000)] ## create every possible number, start as False
# allNumbers = [x for x in allNumbers if not ('0' in x)] ## filter some numbers
# for element in start: ## turn the False start numbers into True (regular numbers)
#     if ('-'+element in allNumbers):
#         idx = (allNumbers.index('-'+element))
#         allNumbers[idx] = negate(allNumbers[idx])
