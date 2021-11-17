#!/usr/bin/env python
'''
	SAT solver based on DPLL
	Course in Advanced Programming in Artificial Intelligence - UdL
'''

import random
import time
import dimacs_decoder as decode


def bcp(formula, unit):
    modified = []
    for clause in formula:
        if unit in clause:
            continue
        if unit * -1 in clause:
            c = [x for x in clause if x != unit * -1]
            if len(c) == 0:
                return -1
            modified.append(c)
        else:
            modified.append(clause)
    return modified


def get_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter


def pure_literal(formula):
    counter = get_counter(formula)
    assignment = []
    pures = []  # [ x for x,y in counter.items() if -x not in counter ]
    for literal, times in counter.items():
        if -1* literal not in counter:
            pures.append(literal)
    for pure in pures:
        print('hoi bcp')
        formula = bcp(formula, pure)
    assignment += pures
    
    return formula, assignment


def unit_propagation(formula):
    assignment = []
    unit_clauses = [c for c in formula if len(c) == 1]
    while len(unit_clauses) > 0:
        unit = unit_clauses[0]
        formula = bcp(formula, unit[0])
        assignment += [unit[0]]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, assignment
        unit_clauses = [c for c in formula if len(c) == 1]
    return formula, assignment


def get_tautologies(formula):
    """Returns the tautologic clauses (i.e. [p ^ -p]) from the cnf"""
    ## Something is wrong with this function but I'm having a hard time figuring it out.
    tautologies = []
    for clause in formula:  # Loop through clauses and their terms
        tautologies += [clause for negation in clause if negation * -1 ]  # check for negations of current term
    return tautologies


def remove_clauses_from_cnf(formula, clauses):
    ## The way we handle data inside of this function is reliant on the tautology function, requires some debugging.
    for clause in clauses:
        #formula.remove(clause) ## this kinda depends on how the tautology function works, can't test yet.
        for line in formula:
            if(clause in line):
                formula.remove(line)
    return formula


def variable_selection(formula):
    counter = get_counter(formula)
    return random.choice(list(counter.keys()))


def backtracking(formula, assignment):
    #tautologies = get_tautologies(formula)
    #remove_clauses_from_cnf(formula, tautologies)
    formula, pure_assignment = pure_literal(formula)
    formula, unit_assignment = unit_propagation(formula)
    assignment = assignment + pure_assignment + unit_assignment
    if formula == - 1:
        return []
    if not formula:
        return assignment

    variable = variable_selection(formula)
    solution = backtracking(bcp(formula, variable), assignment + [variable])
    if not solution:
        solution = backtracking(bcp(formula, -variable), assignment + [-variable])
    return solution


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
        if(sol < 0):
            continue
        row, col = str(sol)[0], str(sol)[1]
        grid[int(row) - 1][int(col) - 1] = str(sol)[2]
    return grid


def main():
    start_time = time.time()
    clauses = decode.dimacs_rules("sudoku-rules.txt")
    nvars = decode.dimacs_start('sudoku-example.txt')
    clauses.extend(nvars)
    solution = backtracking(clauses, [])

    if solution:
        print(len(solution))
        # for x in range(1, len(nvars) + 1):
        #     if x not in solution and -x not in solution:
        #         print(x)
        #         solution += x ## not sure what this does?
        #         pass
        solution.sort(key=lambda x: abs(x))
        grid_printer(solution, 9)

        print('s SATISFIABLE')
        print('v ' + ' '.join([str(x) for x in solution]) + ' 0')
    else:
        print('s UNSATISFIABLE')
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
