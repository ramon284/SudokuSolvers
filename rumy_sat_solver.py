from os import X_OK
import random
import time
import dimacs_decoder as decode
import sudoku_printer as sp
import VSIDS_functions as vsids
from copy import deepcopy


def remove_unit_literals(cnf_formula, unit): ## take all clauses + one literal
    new_clauses = []
    if(heuristic == None):
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
    
    elif(heuristic == 'VSIDS'):
        vsids_list = [] ##vsids keeps track of all clauses containing our literal, both T and F
        for cnf in cnf_formula: ## for every clause in formula
            if unit in cnf:     ## if literal in clause, clause = True so remove it
                vsids_list.append(cnf)
                continue
            if (unit * -1) in cnf: ## if negation of our literal is found, make list of all other literals in clause
                vsids_list.append(cnf)
                cls = [x for x in cnf if (x != (unit * -1))]
                if (len(cls) == 0): ## no other literals? Than clause = False, thus return -1  
                    vsids_flatten = [item for sublist in vsids_list for item in sublist]
                    vsids_set = set(vsids_flatten)
                    vsids_set.remove(unit)
                    vsids.add_score(vsids_set)
                    return -1
                new_clauses.append(cls) ## otherwise, remove the False literal and keep the others.
            else:
                new_clauses.append(cnf) ## if clause not in literal, just keep the clause.
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


def variable_selection(cnf_formula, alpha=False):
    counter = get_literals_counter(cnf_formula)
    if alpha:
        return list(counter.keys())[0]
    return random.choice(list(counter.keys()))

def MOMS(): # @Wafaa
    pass
def VSIDS(cnf_formula): # @Ramon
    variable = vsids.return_highest_score() ## get highest scoring variable
    if(variable == -1): 
        variable = variable_selection(cnf_formula) ## if no scores are in the scoreboard, pick a random variable
    if(variable in vsids.scoreCounter):
        vsids.scoreCounter[variable] -= 0.2 ##reduce score of chosen variable a bit more than the other variables.
        if vsids.scoreCounter[variable] <= 0: del vsids.scoreCounter[variable]
    return variable
def DLCS(): # @Ned
    pass
def DLIS(): # @Ned
    pass

def backtracking(cnf_formula, partial_assignment, heuristic=None, branches=0):
    cnf_formula, pure_assignment = remove_pure_literals(cnf_formula)
    cnf_formula, unit_assignment = unit_propagate(cnf_formula)
    partial_assignment = partial_assignment + pure_assignment + unit_assignment
    if cnf_formula == -1:
        return [], branches
    if not cnf_formula:
        return partial_assignment, branches

    if heuristic == "MOMS":
        variable = MOMS()
    elif heuristic == 'VSIDS':
        variable = VSIDS(cnf_formula)
    elif heuristic == 'DLCS':
        variable = DLCS()
    elif heuristic == 'DLIS':
        variable = DLIS()
    else:
        variable = variable_selection(cnf_formula, alpha=True)
    
    (sat, branches) = backtracking(remove_unit_literals(cnf_formula, variable), partial_assignment + [variable], heuristic=heuristic, branches=branches+1)
    if not sat:
        (sat, branches) = backtracking(remove_unit_literals(cnf_formula, -variable), partial_assignment + [-variable], heuristic=heuristic, branches=branches+1)
    return sat, branches


def get_literals_counter(cnf_formula): ## counts how often every literal is in the formula
    literals_counter = {}
    for clause in cnf_formula:
        for L in clause:
            if L in literals_counter:
                literals_counter[L] += 1
            else:
                literals_counter[L] = 1
    return literals_counter

def main(sudoku_path = '', heur = None):
    global heuristic
    heuristic = heur
    start_time = time.time()
    if (sudoku_path == ''):
        sudoku_path = 'sudoku-example.txt'
    clauses = decode.dimacs_rules("sudoku-rules.txt")
    nvars = decode.dimacs_start(sudoku_path)
    startLength = len(nvars)
    clauses.extend(nvars)
    (solution, branches) = backtracking(clauses, [], heuristic)
    satisfied = False

    if solution:
        solution.sort(key=lambda x: abs(x))
        sp.grid_printer(solution, 9)
        print('s SATISFIABLE')
        satisfied = True
    else:
        print('s UNSATISFIABLE')
    endtime = (time.time() - start_time)
    print("--- %s seconds ---" % (endtime))
    print("--- %s branches ---" % (branches))
    return endtime, satisfied, startLength


if __name__ == '__main__':
    main('')
