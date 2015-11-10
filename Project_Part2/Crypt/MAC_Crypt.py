__author__ = 'Sean'
from testRead import *
import random
import time
import copy
import AC3_Crypt
class MacCrypt:
    # Initialize data
    def __init__(self, op, words, letters):
        self.op = op
        self.words = words
        self.letters = letters
        self.cons = []
        self.vars = dict()
        self.nodesExplored = 0

    # Sets up and starts the solver
    def solve(self):
        # Check if solvable
        if len(self.letters) > 10:
            print("Unsolvable, too many letters.")
            return 0

        t = time.time()
        # Setup the variables and constraints, runs AC3 once.
        AC3_Crypt.setupAC3(self.cons, self.vars)

        keys = list(self.vars.keys())
        #keys = sorted(self.vars.keys(), key = lambda x: len(self.vars[x].domain))
        #for k in keys:
            #print(k, len(self.vars[k].domain))
        final = self.backtrace(self.cons, self.vars, keys, 0)

        t = time.time()-t
        print("MAC Time Taken: ", t)
        print("MAC Nodes Explored: ", self.nodesExplored)
        return final

    # Searches over each variable, trying to guess the variables's value
    def backtrace(self, constraints, variables, keys, keyIndex, currentVar = None):
        self.nodesExplored += 1
        # Check if solution is found, or there is no solution
        varCopy = copy.deepcopy(variables)
        state = AC3_Crypt.AC3(constraints, varCopy, currentVar)

        if state == -1:
            return None
        if state == 1:
            if self.testSumSolution(varCopy):
                return varCopy
            else:
                return None

        keyVal = keys[keyIndex]
        #print(keyVal)
        domain = copy.deepcopy(varCopy[keyVal].domain)

        # Try each possible value for the variable
        for d in list(domain):
            varCopy[keyVal].domain = [d]

            # Guesses next variable
            state = self.backtrace(constraints, varCopy, keys, keyIndex + 1, varCopy[keyVal])

            if state != None:
                return state

        return None

    # Checks if a solution is valid
    def testSumSolution(self, variables):
        # Calculate and add up variable values
        sum = 0
        for i in range(len(self.words) - 1):
            word = self.words[i]
            if variables[word[0]].domain[0]== 0:
                return False
            wordLen = len(word)
            for j in range(wordLen):
                sum += (10**j) * variables[word[wordLen - j - 1]].domain[0]

        # Calculate and add up solution value
        solution = 0
        word = self.words[len(self.words) - 1]
        if variables[word[0]].domain[0]== 0:
            return False
        wordLen = len(word)
        for j in range(wordLen):
            solution += (10**j) * variables[word[wordLen - j - 1]].domain[0]

        # Return whether solution true or false
        if (solution == sum):
            return True
        else:
            return False
"""
op, words, letters = readCrypt()
solver = MacCrypt(op, words, letters)
solution = solver.solve()
print("\nFinal Solution")
for k in sorted(solution.keys()):
    print(k, ", ", solution[k].domain)

"""