__author__ = 'Sean'
from SlidingPuzzle import SlidingPuzzle
from  AStar import AStar
import menu
import math

#####
#  Set test puzzles
size = 3
puzzle8_5 = SlidingPuzzle(size,  [[1,2,3],[4,8,0],[7,6,5]])
puzzle8_11 = SlidingPuzzle(size, [[5,1,2],[6,3,0],[4,7,8]])
puzzle8_16 = SlidingPuzzle(size, [[3,5,6],[1,4,8],[0,7,2]])
puzzle8_21 = SlidingPuzzle(size, [[3,0,2],[6,5,1],[4,7,8]])
puzzle8_25 = SlidingPuzzle(size, [[8,7,4],[3,2,0],[6,5,1]])
puzzle8_30 = SlidingPuzzle(size, [[8,7,6],[5,4,3],[2,1,0]])
puzzle8_goal = SlidingPuzzle(size)
puzzle8_goal.setAsGoal()

size = 4
puzzle15_32 = SlidingPuzzle(size, [[15,2,3,4],[5,6,7,8],[9,10,11,12],[13,1,14,0]])
puzzle15_goal = SlidingPuzzle(size)
puzzle15_goal.setAsGoal()

# Run a sample puzzle
def runFastTests():
    print(puzzle8_21)
    solve_puzzle8_21_1 = AStar(puzzle8_21, puzzle8_goal, 0)
    solve_puzzle8_21_2 = AStar(puzzle8_21, puzzle8_goal, 1)
    solve_puzzle8_21_3 = AStar(puzzle8_21, puzzle8_goal, 0, True)
    solve_puzzle8_21_4 = AStar(puzzle8_21, puzzle8_goal, 1, True)

    print("\nSAMPLE PUZZLE STRAIGHT LINE")
    solution = solve_puzzle8_21_1.search()
    print("Moves Taken:    " + str(len(solution.moves)) + " moves")
    solution.printSolution()

    print("\nSAMPLE PUZZLE MANHATTAN")
    solution = solve_puzzle8_21_2.search()
    print("Moves Taken:    " + str(len(solution.moves)) + " moves")
    solution.printSolution()

    print("\nSAMPLE PUZZLE STRAIGHT LINE WITH LINEAR CONFLICT")
    solution = solve_puzzle8_21_3.search()
    print("Moves Taken:    " + str(len(solution.moves)) + " moves")
    solution.printSolution()

    print("\nSAMPLE PUZZLE MANHATTAN WITH LINEAR CONFLICT")
    solution = solve_puzzle8_21_4.search()
    print("Moves Taken:    " + str(len(solution.moves)) + " moves")
    solution.printSolution()

# Runs a custom puzzle
def runCustomPuzzle(puzzle, size):
    if type(puzzle) == int:
        temp = size
        size = puzzle
        puzzle = temp

    # Make puzzle
    realSize = int(math.sqrt(size+1))
    puzList = list(puzzle)
    if size+1 != len(puzList):
        print("\nPUZZLE SIZE AND NUMBER OF TILES INPUT DO NOT MATCH\n")
        return
    puzArray = [[int(puzList[j*realSize + i]) for i in range(realSize)] for j in range(realSize)]

    customPuzzle = SlidingPuzzle(realSize, puzArray)
    customGoal = SlidingPuzzle(realSize)
    customGoal.setAsGoal()

    solver_1 = AStar(customPuzzle, customGoal, 0)
    solver_2 = AStar(customPuzzle, customGoal, 1)
    solver_3 = AStar(customPuzzle, customGoal, 0, True)
    solver_4 = AStar(customPuzzle, customGoal, 1, True)

    # Solve puzzle
    print("\nCUSTOM PUZZLE STRAIGHT LINE")
    solution = solver_1.search()
    print("Moves Taken:    " + str(len(solution.moves)) + " moves")

    print("\nCUSTOM PUZZLE MANHATTAN")
    solution = solver_2.search()
    print("Moves Taken:    " + str(len(solution.moves)) + " moves")

    print("\nCUSTOM PUZZLE STRAIGHT LINE WITH LINEAR CONFLICT")
    solution = solver_3.search()
    print("Moves Taken:    " + str(len(solution.moves)) + " moves")

    print("\nCUSTOM PUZZLE MANHATTAN WITH LINEAR CONFLICT")
    solution = solver_4.search()
    print("Moves Taken:    " + str(len(solution.moves)) + " moves")
#
#####

#####
# Make menus
customData = {}

# Make menu Items
m_intro = menu.TextDisplay("Hello, Welcome to Sliding Puzzle Solver. Type 'quit' at any prompt to quit.")
m_choice1 = menu.ChoicePrompt("\nWhat would you like to do?", ["Run test puzzles", "Run custom puzzle"])
m_choice2 = menu.ChoicePrompt("This will only run a sample 8-puzzle, running all puzzles would take hours.",
                              ["Run sample puzzle", "Return to menu"])
m_func1 = menu.FunctionRun(runFastTests, {})
m_input1 = menu.InputPrompt("What size of puzzle? (8 or 15?)", int, customData, "size")
m_input2 = menu.InputPrompt("Enter the puzzle values from left to right, top to bottom. "
                            + "The blank space is zero. For example, a finished 8-puzzle "
                            + "would be '123456780'.", str, customData, "puzzle")
m_func2 = menu.FunctionRun(runCustomPuzzle, customData)

# Make menu graph/tree
n_func2 = menu.menuNode(m_func2, [])
n_input2 = menu.menuNode(m_input2, [n_func2])
n_input1 = menu.menuNode(m_input1, [n_input2])
n_func1 = menu.menuNode(m_func1, [])
n_choice2 = menu.menuNode(m_choice2,[n_func1,n_func1])
n_choice1 = menu.menuNode(m_choice1, [n_choice2, n_input1])
n_title = menu.menuNode(m_intro, [n_choice1])

n_choice2.setReturnNode(n_choice1)
n_choice2.setChildren([n_func1, n_choice1])
n_func1.setReturnNode(n_choice1)
n_func2.setReturnNode(n_choice1)
#
#####

# Run program
n_title.execute()


"""
size = 4
goalPuzzle = SlidingPuzzle(size)
goalPuzzle.setAsGoal()
initPuzzle = SlidingPuzzle(size, [[15,2,3,4],[5,6,7,8],[9,10,11,12],[13,1,14,0]])
print("Solving...")
print(initPuzzle)
solverAStarStraightLine = AStar(initPuzzle, goalPuzzle, 0)
solverAStarManhattan = AStar(initPuzzle, goalPuzzle, 1)
solverAStarLineConflict = AStar(initPuzzle, goalPuzzle, 0, True)
solverAStarManhattanConflict = AStar(initPuzzle, goalPuzzle, 1, True)

solverBBFS = BBFS(initPuzzle, goalPuzzle)

print("STRAIGHT LINE")
solutionStraightLine = solverAStarStraightLine.search()
print("Moves Taken:    " + str(len(solutionStraightLine.moves)) + " moves")
solutionStraightLine.printSolution()

print("\nMANHATTAN")
solutionManhattan = solverAStarManhattan.search()
print("Moves taken:    " + str(len(solutionManhattan.moves)) + " moves")
solutionManhattan.printSolution()

print("\nSTRAIGHT LINE LINEAR CONFLICT")
solutionLineConflict = solverAStarLineConflict.search()
print("Moves taken:    " + str(len(solutionLineConflict.moves)) + " moves")
solutionLineConflict.printSolution()

print("\nMANHATTAN LINEAR CONFLICT")
solutionManhattanConflict = solverAStarManhattanConflict.search()
print("Moves taken:    " + str(len(solutionManhattanConflict.moves)) + " moves")
solutionManhattanConflict.printSolution()

print("\nBIDIRECTION BFS")
solutionBBFS = solverBBFS.search()
print("Moves taken:    " + str(len(solutionBBFS.moves)) + " moves")
solutionBBFS.printSolution()
"""