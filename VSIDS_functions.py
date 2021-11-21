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