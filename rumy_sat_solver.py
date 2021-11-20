import random
import time
import dimacs_decoder as decode
import sudoku_printer as sp


# def remove_unit_literals(cnf_formula, unit): ## legacy code baby
#     removed_units_list = [c for c in cnf_formula if unit not in c]
#     new_clauses = []
#     for clause in removed_units_list:
#         element = [e for e in clause if e != (unit * -1)]
#         if len(element) > 0:
#             new_clauses.append(element)
#     return new_clauses

def remove_unit_literals(cnf_formula, unit):
    new_clauses = []
    for cnf in cnf_formula:
        if unit in cnf:
            continue
        if (unit * -1) in cnf:
            cls = [x for x in cnf if (x != (unit * -1))]
            if (len(cls) == 0): 
                return -1
            new_clauses.append(cls)
        else:
            new_clauses.append(cnf)
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
    if cnf_formula == -1:
        return []
    if not cnf_formula:
        return partial_assignment

    variable = variable_selection(cnf_formula)
    sat = backtracking(remove_unit_literals(cnf_formula, variable), partial_assignment + [variable])
    if not sat:
        sat = backtracking(remove_unit_literals(cnf_formula, -variable), partial_assignment + [-variable])
    return sat


def get_literals_counter(cnf_formula): ## counts how often every literal is in the formula
    literals_counter = {}
    for clause in cnf_formula:
        for L in clause:
            if L in literals_counter:
                literals_counter[L] += 1
            else:
                literals_counter[L] = 1
    return literals_counter

def main(sudoku_path = ''):
    start_time = time.time()
    if (sudoku_path == ''):
        sudoku_path = 'sudoku-example.txt'
    clauses = decode.dimacs_rules("sudoku-rules.txt")
    nvars = decode.dimacs_start(sudoku_path)
    startLength = len(nvars)
    clauses.extend(nvars)
    solution = backtracking(clauses, [])
    satisfied = False

    if solution:
        solution.sort(key=lambda x: abs(x))
        sp.grid_printer(solution, 9)
        print('s SATISFIABLE')
        satisfied = True
        #print('v ' + ' '.join([str(x) for x in solution]) + ' 0')
    else:
        print('s UNSATISFIABLE')
    endtime = (time.time() - start_time)
    print("--- %s seconds ---" % (endtime))
    return endtime, satisfied, startLength


if __name__ == '__main__':
    main()
