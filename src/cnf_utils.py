import operator
import random


def min_clauses(cnf_formula):  # @Wafaa
    min_clauses = []
    size = -1
    for clause in cnf_formula:
        clause_size = get_clause_size(clause)
        # Either the current clause is smaller
        if size == -1 or clause_size < size:
            min_clauses = [clause]
            size = clause_size
        # Or it is of minimum size as well
        elif clause_size == size:
            min_clauses.append(clause)
    return min_clauses


def get_clause_size(clause):  # @Wafaa
    counter = 0
    for literal in clause:
        counter = counter + 1
    return counter


def unit_propagate(cnf_formula, VSIDSContainer, heuristic):
    partial_assignment = []
    unit_clauses = [c for c in cnf_formula if len(c) == 1]
    removed_unit_clauses_counter = len(cnf_formula)
    while len(unit_clauses) > 0:
        unit_literal = unit_clauses[0]
        if heuristic == 'VSIDS':
            cnf_formula = VSIDSContainer.remove_unit_literals_VSIDS(cnf_formula, unit_literal[0])
        else:
            cnf_formula = remove_unit_literals(cnf_formula, unit_literal[0])
        partial_assignment += [unit_literal[0]]
        if cnf_formula == -1:
            return -1, [], 0
        if not cnf_formula:
            return cnf_formula, partial_assignment, removed_unit_clauses_counter
        unit_clauses = [c for c in cnf_formula if len(c) == 1]
    removed_unit_clauses_counter -= len(cnf_formula)
    return cnf_formula, partial_assignment, removed_unit_clauses_counter


def remove_pure_literals(cnf_formula, heuristic=None):
    counter = get_literals_counter(cnf_formula)
    partial_assignment = []
    pure_literals = [element for element in counter if -1 * element not in counter]
    for pure_literal in pure_literals:
        cnf_formula = remove_unit_literals(cnf_formula, pure_literal)
    partial_assignment += pure_literals
    return cnf_formula, partial_assignment


def get_most_occurent_literal(formula):  # @Wafaa
    counter = get_literals_counter(formula)
    return min(counter.items(), key=operator.itemgetter(1))[0]


def get_literals_counter(cnf_formula):  # counts how often every literal is in the formula
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
        return sorted(list(counter.keys()))[0]
    return random.choice(list(counter.keys()))


def remove_unit_literals(cnf_formula, unit):  # take all clauses + one literal
    new_clauses = []
    for cnf in cnf_formula:
        if unit in cnf:
            continue
        if (unit * -1) in cnf:
            cls = [x for x in cnf if (x != (unit * -1))]
            if len(cls) == 0:
                return -1
            new_clauses.append(cls)
        else:
            new_clauses.append(cnf)
    return new_clauses
