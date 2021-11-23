import time
import argparse
import dimacs_decoder as decode
import sudoku_printer as sp
from cnf_utils import remove_unit_literals, remove_pure_literals, unit_propagate
from heuristics import DLCS, DLISN, DLISP, MOMS, VSIDSContainer, variable_selection

def backtracking(cnf_formula, partial_assignment=[], heuristic=None,moms_k=0.5, branches=0, container=None):
    if(container == None):
        container = VSIDSContainer({})
    cnf_formula, pure_assignment = remove_pure_literals(cnf_formula, heuristic=heuristic)
    cnf_formula, unit_assignment = unit_propagate(cnf_formula, heuristic=heuristic, VSIDSContainer=container)
    partial_assignment = partial_assignment + pure_assignment + unit_assignment
    if cnf_formula == -1:
        return [], branches
    if not cnf_formula:
        return partial_assignment, branches

    if heuristic == "MOMS":
        variable = MOMS(cnf_formula, k=moms_k)
    elif heuristic == 'VSIDS':
        variable = container.VSIDS(cnf_formula)
    elif heuristic == 'DLCS':
        variable = DLCS(cnf_formula)
    elif heuristic == 'DLISP':
        variable = DLISP(cnf_formula)
    elif heuristic == 'DLISN':
        variable = DLISN(cnf_formula)
    elif heuristic == None:
        variable = variable_selection(cnf_formula, alpha=True)
    else:
        print("No such heuristic...")
        exit()

    # TODO We need to check how branching is counted
    # Maybe think about branching and recursive depth as different measures
    #???
    branches += 1

    (sat, branches) = backtracking(remove_unit_literals(cnf_formula, variable), partial_assignment + [variable], heuristic=heuristic, branches=branches, moms_k=moms_k, container=container)

    if not sat:
        (sat, branches) = backtracking(remove_unit_literals(cnf_formula, -variable), partial_assignment + [-variable], heuristic=heuristic, branches=branches, moms_k=moms_k, container=container)
    return sat, branches

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="SAT")

    parser.add_argument("-S1", help="Run DPLL with no heuristics.", action="store_true")
    parser.add_argument("-S2", help="Run DPLL with DLCS.", action="store_true")
    parser.add_argument("-S3", help="Run DPLL with DLISN", action="store_true")
    parser.add_argument("-S4", help="Run DPLL with DLISP", action="store_true")
    parser.add_argument("-S5", help="Run DPLL with MOMS", action="store_true")
    parser.add_argument("-S6", help="Run DPLL with VSDIS", action="store_true")

    parser.add_argument("filename", help="Name of the DIMACS file containing sudoku rules and starting positions.")

    parser.add_argument("size", help="Size of the sudoku - 9x9 / 4x4 / etc")
    arguments, b = parser.parse_known_args()

    try:
        clauses = decode.dimacs_rules(arguments.filename)
    except Exception as e:
        print(arguments.filename)
        print("Please provide the path of the input file relative to SAT.py")
        exit()

    t1, t2 = 0, 0
    solution, branches = None, None

    print("==========================================")
    # Vanilla DPLL
    if arguments.S1:
        print("NO HEURISTIC")
        t1 = time.time()
        (solution, branches) = backtracking(clauses)
        t2 = time.time()
    # DLCS
    if arguments.S2:
        print("DLCS")
        t1 = time.time()
        (solution, branches) = backtracking(clauses, heuristic="DLCS")
        t2 = time.time()
    # DLISN
    if arguments.S3:
        print("DLIS with NEGATIVE")
        t1 = time.time()
        (solution, branches) = backtracking(clauses, heuristic="DLISN")
        t2 = time.time()
    # DLISP
    if arguments.S4:
        print("DLIS with POSITIVE")
        t1 = time.time()
        (solution, branches) = backtracking(clauses, heuristic="DLISP")
        t2 = time.time()
    # MOMS
    if arguments.S5:
        print("MOMS")
        t1 = time.time()
        (solution, branches) = backtracking(clauses, heuristic="MOMS", moms_k=0.7)
        t2 = time.time()
    # VSIDS
    if arguments.S6:
        print("VSIDS")
        t1 = time.time()
        (solution, branches) = backtracking(clauses, heuristic="VSIDS")
        t2 = time.time()

    if solution:
        print(f"--- Time elapsed: {t2-t1} ---")
        print(f"--- Number of branches: {branches} ---")
        print("SAT")
        sp.grid_printer(solution, int(arguments.size))
    else:
        print(f"--- Time elapsed: {t2-t1} ---")
        print("UNSAT")
    print("==========================================")

