__author__ = 'Sean'
import math
import time

class AStar:

    def __init__(self, start, goal, hNumber = 0, linearConflict = False):
        self.startNode = start
        self.currentNode = start
        self.goalNode = goal
        self.frontier = [start]
        self.explored = []
        self.hNumber = hNumber
        self.linearConflict = linearConflict

    # Expand a node to find its parents
    def expand(self, node):
        # Choose node to explore
        self.explored.append(node)
        del self.frontier[0]

        # Expand node, adding neighbors to frontier, if it's not already in explored or frontier sets
        for n in node.expand():
            add = True
            for e in self.explored:
                if n.data == e.data:
                    if len(n.moves) < len(e.moves):
                        e.moves = n.moves
                    add = False
            for f in self.frontier:
                if n.data == f.data:
                    if len(n.moves) < len(f.moves):
                        f.moves = n.moves
                    add = False

            # The frontier is an ordered queue, this inserts new nodes into the frontier in sorted order.
            if add:
                n.f = self.heuristic(n) + self.currentCost(n)

                addedToFrontier = False
                startIndex = 0
                endIndex = len(self.frontier)-1

                if endIndex == -1:
                    self.frontier.append(n)
                elif n.f > self.frontier[endIndex].f:
                    self.frontier.append(n)
                    addedToFrontier = True
                elif n.f < self.frontier[0].f:
                    self.frontier.insert(0,n)
                    addedToFrontier = True
                else:

                    while abs(startIndex-endIndex) != 1:
                        halfIndex = int((endIndex + startIndex)/2)
                        if n.f == self.frontier[halfIndex].f:
                            self.frontier.insert(halfIndex, n)
                            addedToFrontier = True
                            break
                        elif n.f < self.frontier[halfIndex].f:
                            endIndex = halfIndex
                        else:
                            startIndex = halfIndex

                if not addedToFrontier:
                    self.frontier.insert(endIndex,n)

        return

    # h(n)
    def heuristic(self, input, printInfo = False):
        h = 0
        # Code for heuristic here
        if self.hNumber == 0:
            # Straight Line, adds distance to goal for each tile
            for i in range(input.size):
                for j in range(input.size):
                    v = input.data[j][i]
                    if v != 0:
                        x = (v-1)%input.size
                        y = math.floor((v-1)/input.size)
                        h += math.sqrt((x-i)**2 + (y-j)**2)

        elif self.hNumber == 1:
            # Manhattan, adds distance to goal for each tile
            for i in range(input.size):
                for j in range(input.size):
                    v = input.data[j][i]
                    if v != 0:
                        x = (v-1)%input.size
                        y = math.floor((v-1)/input.size)
                        h += abs(x-i)+abs(y-j)

        # Linear Conflict, adds to h(n) for every two tiles that are guaranteed to collide
        if self.linearConflict:
            for j in range(input.size):
                for i in range(input.size - 1):
                    v = input.data[j][i]
                    if v <= (j+1)*input.size and v > j*input.size:
                        for k in range(input.size-i-1):
                            w = input.data[j][i+k]
                            if v > w and w != 0 and w <= (j+1)*input.size and w > j*input.size:
                                h += 2
                                #print(str(v), str(w))
            for i in range(input.size):
                for j in range(input.size - 1):
                    v = input.data[j][i]
                    if (v-i-1)%3 == 0:
                        for k in range(input.size-j-1):
                            w = input.data[j+k][i]
                            if v > w and w != 0 and (w-i-1)&3 == 0:
                                h += 2
                                #print(str(v), str(w))
        if printInfo:
            print(str(h))
        return h

    #g(n)
    def currentCost(self, input):
        # This is the number of steps taken to reach this node
        g = 0
        g += len(input.moves)
        return g

    # Do the search
    def search(self):

        # Sets up search
        startTime = time.time()
        bestNode = self.startNode
        self.heuristic(bestNode, True)
        maxFrontier = 0
        maxDepth = 0
        # Executes search, until solution is found, or we know there is no solution
        while bestNode.data != self.goalNode.data:

            self.expand(bestNode)
            frontierLen = len(self.frontier)
            if frontierLen == 0:
                return None
            elif frontierLen > maxFrontier:
                maxFrontier = frontierLen
            bestNode = self.frontier[0]
            depth = len(bestNode.moves)
            if depth > maxDepth:
                maxDepth = depth


        print("Nodes explored: " + str(len(self.explored)))
        print("Max frontier size: " + str(maxFrontier))
        print("Max depth explored: " + str(maxDepth))
        endTime = time.time()
        timeElapsed = endTime - startTime
        print("Time taken:     " + str(timeElapsed))
        return bestNode

"""
s = Node(0)
g = Node(100)
a = AStar(s,g)
print(str(a.search().data))
"""