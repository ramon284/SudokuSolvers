from cnf_utils import  variable_selection, get_literals_counter, minClauses

global scoreCounter
scoreCounter = {}

def add_score(literals): ## adds score to unsolvable literal (has to be T and F at the same time)
    literals = list({abs(x) for x in literals}) ## make negative values positive, remove duplicates.
    for lit in literals:
        lit = abs(lit)
        scoreCounter[lit]=scoreCounter.get(lit,0)+1
        
def reduce_score(reduction = 0.95): ## reduce the score of a variable every scoring iteration
    for score in scoreCounter:
        if(scoreCounter[score] != 0):
            scoreCounter[score] = round(scoreCounter[score]*reduction, 3)

def return_highest_score():
    if(not scoreCounter):
        return -1
    reduce_score()
    highest = max(scoreCounter, key=scoreCounter.get)
    scoreCounter[highest] -= 0.05
    return highest

def VSIDS(cnf_formula): # @Ramon
    variable = return_highest_score() ## get highest scoring variable
    if(variable == -1): 
        variable = variable_selection(cnf_formula) ## if no scores are in the scoreboard, pick a random variable
    if(variable in scoreCounter):
        scoreCounter[variable] -= 0.2 ##reduce score of chosen variable a bit more than the other variables.
        if scoreCounter[variable] <= 0: del scoreCounter[variable]
    return variable

def DLCS(cnf_formula): # @Ned
    counter = get_literals_counter(cnf_formula)

    largest_CP_CN = -1
    choice = None
    polarity = None

    for L in list(counter.keys()):
        CP = counter[abs(L)]
        CN = counter[-abs(L)]

        if CP + CN > largest_CP_CN:
            choice = abs(L)
            largest_CP_CN = CP + CN
            polarity = CP > CN
    if choice and polarity:
        return choice
    elif choice:
        return -choice

def DLISP(cnf_formula): # @Ned
    counter = get_literals_counter(cnf_formula)

    largest_CP = -1
    choice = None
    polarity = None

    for L in list(counter.keys()):
        if abs(L) in counter:
            CP = counter[abs(L)]
        else:
            CP = 0
        
        if CP > largest_CP:
            choice = abs(L)
            largest_CP = CP
            polarity = CP > counter[-abs(L)]
    if choice and polarity:
        return choice
    elif choice:
        return -choice

def DLISN(cnf_formula): # @Ned
    counter = get_literals_counter(cnf_formula)

    largest_CN = -1
    choice = None
    polarity = None

    for L in list(counter.keys()):
        if -abs(L) in counter:
            CN = counter[-abs(L)]
        else:
            CN = 0
        if CN > largest_CN:
            choice = abs(L)
            largest_CN = CN
            polarity = CN > counter[abs(L)]
    if choice and polarity:
        return choice
    elif choice:
        return -choice

def maximize_function(min_clauses, k=0.5): # @Ned
    best_literal = None
    Fmax = -1

    literals = get_literals_counter(min_clauses)
    
    for literal in list(literals.keys()):
        Fx = literals[abs(literal)] if abs(literal) in literals else 0
        Fxp = literals[-abs(literal)] if -abs(literal) in literals else 0

        F = (Fx + Fxp) * (2**k) + Fx * Fxp

        if F > Fmax:
            best_literal = literal
            Fmax = F

    return best_literal

def MOMS(cnf_formula): # @Wafaa
    minc = minClauses(cnf_formula)
    return maximize_function(minc)