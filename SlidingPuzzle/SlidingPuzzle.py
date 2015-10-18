__author__ = 'Sean'
import math
from random import *

# This is a node in the Astar graph, stores the puzzle, and actions possible for the puzzle
class SlidingPuzzle:
    def __init__(self, size, puzzle = [], moves = [], initData = []):
        self.size = size
        self.fn = 0
        self.data = puzzle
        self.moves = moves

        if puzzle == []:
            self.randomize()

        if initData == []:
            self.initData = self.data
        else:
            self.initData = initData

        # Set Empty Square
        for i in range(self.size):
            for j in range(self.size):
                if self.data[j][i] == 0:
                    self.emptySquare = [i,j]
                    return
        # Set up goal state

    # Sets the puzzle to the solution state
    def setAsGoal(self):
        self.data = [[j*self.size + (i+1) for i in range(self.size)] for j in range(self.size)] # [Row][Column]
        self.data[self.size - 1][self.size - 1] = 0
        self.emptySquare = [self.size - 1, self.size - 1]

    # Generates a random puzzle
    def randomize(self, weight = 100):
        self.setAsGoal()
        for i in range(weight):

            # Get to random squares
            p1 = p2 = 0
            while p1 == p2:
                p1 = randint(0,self.size**2-2)
                p2 = randint(0,self.size**2-2)

                x1 = p1%self.size
                y1 = math.floor(p1/self.size)
                x2 = p2%self.size
                y2 = math.floor(p2/self.size)

            # Swap their values
            tempInt = self.data[y1][x1]
            self.data[y1][x1] = self.data[y2][x2]
            self.data[y2][x2] = tempInt
        return

    # Creates an array with the neighbors of this node
    def expand(self):
        movesArray = []

        for i in range(4):
            spaceCheck = self.emptySquare[i%2] + int((-1.5+i)/abs(-1.5+i))
            if  spaceCheck >= 0 and spaceCheck <= self.size-1:
                newArray = self.puzzleCopy(self.data)

                if i == 0:
                    offsetX = -1
                    offsetY = 0
                elif i == 1:
                    offsetX = 0
                    offsetY = -1
                elif i == 2:
                    offsetX = 1
                    offsetY = 0
                else:
                    offsetX = 0
                    offsetY = 1

                # Slides a tile by swapping values
                slidingValue = newArray[self.emptySquare[1] + offsetY][self.emptySquare[0] + offsetX]
                newArray[self.emptySquare[1]][self.emptySquare[0]] = slidingValue
                newArray[self.emptySquare[1] + offsetY][self.emptySquare[0] + offsetX] = 0

                newMoves = []
                for m in self.moves:
                    newMoves.append(m)
                newMoves.append(i + 1)
                movesArray.append(SlidingPuzzle(self.size, newArray, newMoves, self.initData))
        """
        if self.emptySquare[0]-1 >= 0:
            newArray = self.puzzleCopy(self.data)
            newArray[self.emptySquare[1]][self.emptySquare[0]] = newArray[self.emptySquare[1]][self.emptySquare[0]-1]
            newArray[self.emptySquare[1]][self.emptySquare[0]-1] = 0
            newMoves = []
            for m in self.moves:
                newMoves.append(m)
            newMoves.append(1)
            movesArray.append(SlidingPuzzle(self.size, newArray, newMoves, self.initData))
        if self.emptySquare[1]-1 >= 0:
            newArray = self.puzzleCopy(self.data)
            newArray[self.emptySquare[1]][self.emptySquare[0]] = newArray[self.emptySquare[1]-1][self.emptySquare[0]]
            newArray[self.emptySquare[1]-1][self.emptySquare[0]] = 0
            newMoves = []
            for m in self.moves:
                newMoves.append(m)
            newMoves.append(2)
            movesArray.append(SlidingPuzzle(self.size, newArray, newMoves, self.initData))
        if self.emptySquare[0]+1 <= self.size-1:
            newArray = self.puzzleCopy(self.data)
            newArray[self.emptySquare[1]][self.emptySquare[0]] = newArray[self.emptySquare[1]][self.emptySquare[0]+1]
            newArray[self.emptySquare[1]][self.emptySquare[0]+1] = 0
            newMoves = []
            for m in self.moves:
                newMoves.append(m)
            newMoves.append(3)
            movesArray.append(SlidingPuzzle(self.size, newArray, newMoves, self.initData))
        if self.emptySquare[1]+1 <= self.size-1:
            newArray = self.puzzleCopy(self.data)
            newArray[self.emptySquare[1]][self.emptySquare[0]] = newArray[self.emptySquare[1]+1][self.emptySquare[0]]
            newArray[self.emptySquare[1]+1][self.emptySquare[0]] = 0
            newMoves = []
            for m in self.moves:
                newMoves.append(m)
            newMoves.append(4)
            movesArray.append(SlidingPuzzle(self.size, newArray, newMoves, self.initData))
        """
        return movesArray

    # Copies a puzzle's data
    def puzzleCopy(self, puz2):
        puz1 = [[puz2[j][i] for i in range(self.size)] for j in range(self.size)]
        return puz1

    # Prints the solution, can simply print the moves, or show a graphical representation of all the moves
    def printSolution(self, complex = False):
        if not complex:
            print(str(self.moves))
            return
        output = "Step: " + str(len(self.moves)) + str(self)
        dataCopy = self.puzzleCopy(self.data)
        for i in range(len(self.moves)-1):
            move = self.moves[len(self.moves)-i-1]
            if move == 1:
                self.data[self.emptySquare[1]][self.emptySquare[0]] = self.data[self.emptySquare[1]][self.emptySquare[0]+1]
                self.data[self.emptySquare[1]][self.emptySquare[0]+1] = 0
                self.emptySquare[0] += 1
            elif move == 2:
                self.data[self.emptySquare[1]][self.emptySquare[0]] = self.data[self.emptySquare[1]+1][self.emptySquare[0]]
                self.data[self.emptySquare[1]+1][self.emptySquare[0]] = 0
                self.emptySquare[1] += 1
            elif move == 3:
                self.data[self.emptySquare[1]][self.emptySquare[0]] = self.data[self.emptySquare[1]][self.emptySquare[0]-1]
                self.data[self.emptySquare[1]][self.emptySquare[0]-1] = 0
                self.emptySquare[0] -= 1
            elif move == 4:
                self.data[self.emptySquare[1]][self.emptySquare[0]] = self.data[self.emptySquare[1]-1][self.emptySquare[0]]
                self.data[self.emptySquare[1]-1][self.emptySquare[0]] = 0
                self.emptySquare[1] -= 1
            output = "Step: " + str(len(self.moves)-i-1) + str(self) + "\n" + output
        self.data = dataCopy
        print(output)

    # Prints the current puzzle data
    def __str__(self):
        puzzle = self.data
        output = "\n"
        for i in range(self.size):
            for j in range(self.size):
                output += str(puzzle[i][j])
                for k in range(len(str(self.size**2)) - math.floor(puzzle[i][j]/10) - 1):
                    output += " "
                output += "|"
            output += "\n"
            for l in range((len(str(self.size**2))+1)*self.size):
                output += "-"
            output += "\n"
        return output

"""
p = SlidingPuzzle(3)
print(p)
a = p.expand()
p2 = SlidingPuzzle(3,a[0])
print(p2)
a = p2.expand()
p3 = SlidingPuzzle(3,a[0])
print(p3)
a = p3.expand()
p4 = SlidingPuzzle(3,a[0])
print(p4)
"""