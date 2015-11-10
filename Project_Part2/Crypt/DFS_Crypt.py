__author__ = 'Sean'
from testRead import *
import time
import copy
class DFSCrypt:

    def __init__(self, op, words, letters):
        self.op = op
        self.words = words
        self.letters = letters
        self.cons = []
        self.vars = dict()
        self.nodesExplored = 0

    # Sets up data to be used
    def solve(self):
        for l in self.letters:
            self.vars[l] = -1

        domain = [x for x in range(0,10)]

        t = time.time()
        sol =  self.DFS(0, domain)
        t = time.time() - t
        print("Time Taken: ", t)
        print("Nodes explored: ", self.nodesExplored)
        return sol

    def DFS(self, varIndex, dom):
        self.nodesExplored += 1

        # Check each value for this variable
        for i in dom:
            #print("Depth: ", varIndex, i)

            # Return whether we have valid solution
            self.vars[self.letters[varIndex]] = i
            if varIndex == len(self.letters) - 1:
                solved = self.isSolution()
                if solved:
                    return copy.deepcopy(self.vars)
                else:
                    return None

            # Check the next variable
            newDom = copy.copy(dom)
            newDom.remove(i)
            result = self.DFS(varIndex + 1, newDom)
            if result != None:
                return result

        self.vars[self.letters[varIndex]] = -1
        return None

    # Checks if we have a valid solution
    def isSolution(self):
        upperSum = 0
        lowerSum = 0
        # Sum up upper words
        for i in range(len(self.words)-1):
            # Words can't start with 0
            if self.vars[self.words[i][0]] == 0:
                return False
            for j in range(len(self.words[i])):
                upperSum += self.vars[self.words[i][len(self.words[i]) - j - 1]] * (10**j)

        # Sum up answer word
        i = len(self.words) - 1
        for j in range(len(self.words[i])):
                lowerSum += self.vars[self.words[i][len(self.words[i]) - j - 1]] * (10**j)

        #print(upperSum, lowerSum)

        # Return if solution is valid
        if (upperSum == lowerSum):
            return True
        return False
"""
op, words, letters = readCrypt()
solver = DFSCrypt(op, words, letters)
solution = solver.solve()
print(solution)
"""
