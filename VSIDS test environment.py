import random
import time
import dimacs_decoder as decode
import sudoku_printer as sp

## this function removes True clauses by checking for a certain literal

def boolean_constraint_propagation(cnf_formula, unit, scoreCounter): ## take all clauses + one literal
    new_clauses = []
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
                add_score(scoreCounter, vsids_set)
                print('score added in bcp')
                return -1
            new_clauses.append(cls) ## otherwise, remove the False literal and keep the others.
        else:
            new_clauses.append(cnf) ## if clause not in literal, just keep the clause.
    return new_clauses

def add_score(scoreCounter, literals): ## adds score to unsolvable literal (has to be T and F at the same time)
    for lit in literals:
        scoreCounter[lit]=scoreCounter.get(lit,0)+1
        #scoreCounter[lit] += 1
    
def reduce_score(scoreCounter, reduction = 0.95): ## reduce the score of a variable every scoring iteration
    for score in scoreCounter:
        if(scoreCounter[score] != 0):
            scoreCounter[score] = round(scoreCounter[score]*reduction, 3)

def return_highest_score(scoreCounter, cnf_formula):
    if(not scoreCounter):
        print('random select')
        return variable_selection(cnf_formula)
    reduce_score(scoreCounter)
    highest = max(scoreCounter, key=scoreCounter.get)
    scoreCounter[highest] -= 0.05
    return highest
    
    
def remove_pure_literals(cnf_formula, scoreCounter): 
    counter = get_literals_counter(cnf_formula)
    partial_assignment = []
    pure_literals = [element for element in counter if -1 * element not in counter]
    for pure_literal in pure_literals:
        cnf_formula = boolean_constraint_propagation(cnf_formula, pure_literal, scoreCounter)
    partial_assignment += pure_literals

    return cnf_formula, partial_assignment


def unit_propagate(cnf_formula, scoreCounter):
    partial_assignment = []
    unit_clauses = [c for c in cnf_formula if len(c) == 1]
    while len(unit_clauses) > 0:
        unit_literal = unit_clauses[0]
        cnf_formula = boolean_constraint_propagation(cnf_formula, unit_literal[0], scoreCounter)
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


def backtracking(cnf_formula, partial_assignment, scoreCounter = {}):
    cnf_formula, pure_assignment = remove_pure_literals(cnf_formula, scoreCounter)
    cnf_formula, unit_assignment = unit_propagate(cnf_formula, scoreCounter)
    partial_assignment = partial_assignment + pure_assignment + unit_assignment
    if cnf_formula == -1:
        return []
    if not cnf_formula:
        return partial_assignment

    #variable = variable_selection(cnf_formula) ## picks random
    variable = return_highest_score(scoreCounter, cnf_formula) ## uses scoreCounting from VSIDS
    print('score:', scoreCounter)
    print('variable:', variable)
    sat = backtracking(boolean_constraint_propagation(cnf_formula, variable, scoreCounter), partial_assignment + [variable], scoreCounter)
    if not sat:
        sat = backtracking(boolean_constraint_propagation(cnf_formula, -variable, scoreCounter), partial_assignment + [-variable], scoreCounter)
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
