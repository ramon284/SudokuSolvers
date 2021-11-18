#!/usr/bin/env python

import random
import time
import dimacs_decoder as decode


def remove_unit_literals(cnf_formula, unit):
    removed_units_list = [c for c in cnf_formula if unit not in c]
    new_clauses = []
    for clause in removed_units_list:
        element = [e for e in clause if e != (unit * -1)]
        if len(element) > 0:
            new_clauses.append(element)
    return new_clauses


def remove_pure_literals(cnf_formula):
    counter = get_literals_counter(cnf_formula)
    partial_assignment = []
    pure_literals = [element for element in counter if -1 * element not in counter]
    for pure_literal in pure_literals:
        cnf_formula = remove_unit_literals(cnf_formula, pure_literal)
    partial_assignment += pure_literals

    return cnf_formula, partial_assignment


def unit_propagate(cnf_formula):
    partial_assignment = []
    unit_clauses = [c for c in cnf_formula if len(c) == 1]
    while len(unit_clauses) > 0:
        unit_literal = unit_clauses[0]
        cnf_formula = remove_unit_literals(cnf_formula, unit_literal[0])
        partial_assignment += [unit_literal[0]]
        if cnf_formula == -1:
            return -1, []
        if not cnf_formula:
            return cnf_formula, partial_assignment
        unit_clauses = [c for c in cnf_formula if len(c) == 1]
    return cnf_formula, partial_assignment


def variable_selection(cnf_formula):
    counter = get_literals_counter(cnf_formula)
    return random.choice(list(counter.keys()))


def backtracking(cnf_formula, partial_assignment):
    cnf_formula, pure_assignment = remove_pure_literals(cnf_formula)
    cnf_formula, unit_assignment = unit_propagate(cnf_formula)
    partial_assignment = partial_assignment + pure_assignment + unit_assignment
    if cnf_formula == - 1:
        return []
    if not cnf_formula:
        return partial_assignment

    variable = variable_selection(cnf_formula)
    sat = backtracking(remove_unit_literals(cnf_formula, variable), partial_assignment + [variable])
    if not sat:
        sat = backtracking(remove_unit_literals(cnf_formula, -variable), partial_assignment + [-variable])
    return sat


def get_literals_counter(cnf_formula):
    literals_counter = {}
    for clause in cnf_formula:
        for L in clause:
            if L in literals_counter:
                literals_counter[L] += 1
            else:
                literals_counter[L] = 1
    return literals_counter


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
        if (sol < 0):
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
        solution.sort(key=lambda x: abs(x))
        grid_printer(solution, 9)

        print('s SATISFIABLE')
        print('v ' + ' '.join([str(x) for x in solution]) + ' 0')
    else:
        print('s UNSATISFIABLE')
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
