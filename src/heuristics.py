from cnf_utils import  variable_selection, get_literals_counter, minClauses

class VSIDSContainer:
    def __init__(self, score_counter):
        self.score_counter = score_counter

    def remove_unit_literals_VSIDS(self, cnf_formula, unit):
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
                    self.add_score(vsids_set)
                    return -1
                new_clauses.append(cls) ## otherwise, remove the False literal and keep the others.
            else:
                new_clauses.append(cnf) ## if clause not in literal, just keep the clause.
        return new_clauses

    def add_score(self, literals): ## adds score to unsolvable literal (has to be T and F at the same time)
        literals = list({abs(x) for x in literals}) ## make negative values positive, remove duplicates.
        for lit in literals:
            lit = abs(lit)
            self.score_counter[lit]=self.score_counter.get(lit,0)+1
        
    def reduce_score(self, reduction = 0.95): ## reduce the score of a variable every scoring iteration
        for score in self.score_counter:
            if(self.score_counter[score] != 0):
                self.score_counter[score] = round(self.score_counter[score]*reduction, 3)

    def return_highest_score(self):
        if(not self.score_counter):
            return -1
        self.reduce_score()
        highest = max(self.score_counter, key=self.score_counter.get)
        self.score_counter[highest] -= 0.02
        return highest

    def VSIDS(self, cnf_formula): # @Ramon
        variable = self.return_highest_score() ## get highest scoring variable
        if(variable == -1): 
            variable = variable_selection(cnf_formula) ## if no scores are in the scoreboard, pick a random variable
        if(variable in self.score_counter):
            if self.score_counter[variable] <= 0: del self.score_counter[variable]
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

def MOMS(cnf_formula, k=0.5): # @Wafaa
    minc = minClauses(cnf_formula)
    return maximize_function(minc, k=k)