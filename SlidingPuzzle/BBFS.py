__author__ = 'Sean'
import math
import time

class BBFS:

    def __init__(self, start, goal):
        self.startNode = start
        self.currentNode = start
        self.goalNode = goal
        self.frontierStart = [start]
        self.exploredStart = []
        self.frontierGoal = [goal]
        self.exploredGoal = []

    # Expand a node to find its parents
    def expand(self, node, frontier, explored):
        explored.append(node)
        frontier.remove(node)
        for n in node.expand():
            add = True
            for e in explored:
                if n.data == e.data:
                    add = False
            for f in frontier:
                if n.data == f.data:
                    add = False
            if add:
                frontier.append(n)
        return

    def findSolution(self):
        for n in self.frontierGoal:
            for m in self.frontierStart:
                if n.data == m.data:
                    return True, m, n
        return False, None, None

    # Do the search
    def search(self):
        startTime = time.time()
        while not self.findSolution()[0]:
            for n in self.frontierStart:
                self.expand(n, self.frontierStart, self.exploredStart)
            for n in self.frontierGoal:
                self.expand(n, self.frontierGoal, self.exploredGoal)

            if len(self.frontierGoal) == 0 and len(self.frontierStart) == 0:
                return None

        endTime = time.time()

        solutionStart = self.findSolution()[1]
        moves1 = solutionStart.moves
        moves2 = self.findSolution()[2].moves
        moves2.reverse()
        for m in moves2:
            if m == 1:
                m = 3
            elif m == 3:
                m = 1
            elif m == 2:
                m = 4
            elif m == 4:
                m = 2
            moves1.append(m)
        solutionStart.moves = moves1
        print("Nodes Explored: " + str(len(self.exploredGoal) + len(self.exploredStart)))
        print("Time taken:     " + str(endTime-startTime))
        return self.findSolution()[1]
