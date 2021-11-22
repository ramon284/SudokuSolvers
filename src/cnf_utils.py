import random
import operator

def minClauses(cnf_formula): # @Wafaa
    minClauses = []
    size = -1
    for clause in cnf_formula:
        clauseSize = get_clause_size(clause)
        # Either the current clause is smaller
        if size == -1 or clauseSize < size:
            minClauses = [clause]
            size = clauseSize
        # Or it is of minimum size as well
        elif clauseSize == size:
            minClauses.append(clause)
    return minClauses

def get_clause_size(clause): # @Wafaa
    counter = 0
    for literal in clause:
        counter = counter + 1
    return counter

def unit_propagate(cnf_formula, heuristic=None):
    partial_assignment = []
    unit_clauses = [c for c in cnf_formula if len(c) == 1]
    while len(unit_clauses) > 0:
        unit_literal = unit_clauses[0]
        cnf_formula = remove_unit_literals(cnf_formula, unit_literal[0], heuristic=heuristic)
        partial_assignment += [unit_literal[0]]
        if cnf_formula == -1:
            return -1, []
        if not cnf_formula:
            return cnf_formula, partial_assignment
        unit_clauses = [c for c in cnf_formula if len(c) == 1]
    return cnf_formula, partial_assignment

def remove_pure_literals(cnf_formula, heuristic=None): 
    counter = get_literals_counter(cnf_formula)
    partial_assignment = []
    pure_literals = [element for element in counter if -1 * element not in counter]
    for pure_literal in pure_literals:
        cnf_formula = remove_unit_literals(cnf_formula, pure_literal, heuristic=heuristic)
    partial_assignment += pure_literals
    return cnf_formula, partial_assignment

def get_most_occurent_literal(formula): # @Wafaa
    counter = get_literals_counter(formula)
    return min(counter.items(), key=operator.itemgetter(1))[0]

def get_literals_counter(cnf_formula): ## counts how often every literal is in the formula
    literals_counter = {}
    for clause in cnf_formula:
        for L in clause:
            if L in literals_counter:
                literals_counter[L] += 1
            else:
                literals_counter[L] = 1
    return literals_counter

def variable_selection(cnf_formula, alpha=False):
    counter = get_literals_counter(cnf_formula)
    if alpha:
        return list(counter.keys())[0]
    return random.choice(list(counter.keys()))

def remove_unit_literals(cnf_formula, unit, heuristic=None): ## take all clauses + one literal
    new_clauses = []
    if(heuristic != 'VSIDS'):
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
                    add_score(vsids_set)
                    return -1
                new_clauses.append(cls) ## otherwise, remove the False literal and keep the others.
            else:
                new_clauses.append(cnf) ## if clause not in literal, just keep the clause.
        return new_clauses