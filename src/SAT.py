import time
import argparse
import dimacs_decoder as decode
import sudoku_printer as sp
from cnf_utils import remove_unit_literals, remove_pure_literals, variable_selection, unit_propagate
from heuristics import DLCS, DLISN, DLISP, MOMS, VSIDSContainer

def backtracking(cnf_formula, partial_assignment=[], heuristic=None,moms_k=None, branches=0, container=None):
    if(container == None and heuristic == 'VSIDS'):
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
    
    (sat, branches) = backtracking(remove_unit_literals(cnf_formula, variable), partial_assignment + [variable], heuristic=heuristic, branches=branches+1, moms_k=moms_k, container=container)
    if not sat:
        (sat, branches) = backtracking(remove_unit_literals(cnf_formula, -variable), partial_assignment + [-variable], heuristic=heuristic, branches=branches+1, moms_k=moms_k, container=container)
    return sat, branches

def main(sudoku_path = '', heuristic = None , printGrid = False, moms_k=None):
    start_time = time.time()
    if (sudoku_path == ''):
        sudoku_path = 'dimacs/sudoku/sudoku-example.txt'
    clauses = decode.dimacs_rules('dimacs/rulesets/sudoku-rules.txt')
    nvars = decode.dimacs_start(sudoku_path)
    startLength = len(nvars)
    clauses.extend(nvars)
    

    (solution, branches) = backtracking(clauses, heuristic=heuristic, moms_k=moms_k)

    satisfied = False
    if solution:
        solution.sort(key=lambda x: abs(x))
        if printGrid == True : sp.grid_printer(solution, 9)
        print('heuristic used: ',heuristic)
        print('s SATISFIABLE')
        satisfied = True
    else:
        print('s UNSATISFIABLE')
    endtime = (time.time() - start_time)
    print("--- %s seconds ---" % (endtime))
    print("--- %s branches ---" % (branches))
    return endtime, satisfied, startLength, branches

# if __name__ == '__main__':
#     # Possible heuristics
#     # DLCS, DLISN, DLISP, MOMS, VSIDS
#     main(heuristic='VSIDS', moms_k=0.3)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="SAT")

    parser.add_argument("-S1", help="Run DPLL with no heuristics.", action="store_true")
    parser.add_argument("-S2", help="Run DPLL with DLCS.", action="store_true")
    parser.add_argument("-S3", help="Run DPLL with DLISN", action="store_true")
    parser.add_argument("-S4", help="Run DPLL with DLISP", action="store_true")
    parser.add_argument("-S5", help="Run DPLL with MOMS", action="store_true")
    parser.add_argument("-S6", help="Run DPLL with VSDIS", action="store_true")

    parser.add_argument("filename", help="Name of the DIMACS file containing sudoku rules and starting positions.")

    arguments, b = parser.parse_known_args()

    try:
        clauses = decode.dimacs_rules(arguments.filename)
    except Exception as e:
        print("Please provide the path of the input file relative to SAT.py")
        exit()

    solution, branches = None, None
    # Vanilla DPLL
    if arguments.S1:
        (solution, branches) = backtracking(clauses)
    # DLCS
    if arguments.S2:
        (solution, branches) = backtracking(clauses, heuristic="DLCS")
    # DLISN
    if arguments.S3:
        (solution, branches) = backtracking(clauses, heuristic="DLISN")
    # DLISP
    if arguments.S4:
        (solution, branches) = backtracking(clauses, heuristic="DLISP")
    # MOMS
    if arguments.S5:
        (solution, branches) = backtracking(clauses, heuristic="MOMS", moms_k=0.7)
    # VSIDS
    if arguments.S6:
        (solution, branches) = backtracking(clauses, heuristic="VSIDS")    

    
