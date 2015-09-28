import math
import os.path
from copy import deepcopy

"""This is where the problem is defined. Initial state, goal state and other information that can be got from the problem"""
class Problem(object):

	

	def __init__(self, initial, size, horizontalChunks, verticalChunks, goal = ""):
		"""This is the constructor for the Problem class. It specifies the initial state, and possibly a goal state, if there is a unique goal.  You can add other arguments if the need arises"""
		self.initial = initial
		self.size = size
		self.horChunks = horizontalChunks
		self.verChunks = verticalChunks

		# Goal holds the solution, once we find it.
		self.goal = goal

		# For a puzzle of size n, initializes blank n x n 2d array
		self.graph = [[0 for x in range(self.size)] for x in range(self.size)] 
		for i in range (0,self.size):
			for j in range (0,self.size):
				self.graph[i][j]  = initial[i*self.size + j]    
		self.initial = ""
		


	def actions(self, state):
		"""Return the actions that can be executed in the given
		state. The result would typically be a list, but if there are
		many actions, consider yielding them one at a time in an
		iterator, rather than building them all at once."""

		# Returns the possible numbers we can use.
		return [(str)(x + 1) for x in range (0,self.size)]

	def result(self, state, action):
		"""Return the state that results from executing the given
		action in the given state. The action must be one of
		self.actions(state)."""

		#Adds new number to the state
		return state + action

	# Creates a new graph with all the numbers from the current state filled in and returns it.
	def makeNewGraph(self, state):
		graphCopy = deepcopy(self.graph)
		stateIndex = 0
		graphIndex = 0
		
		while stateIndex < len(state) and graphIndex < len(self.graph)**2:
			row = math.floor(graphIndex / self.size)
			column = graphIndex % self.size
			if graphCopy[row][column] == " ":
				graphCopy[row][column] = state[stateIndex]
				stateIndex += 1
			graphIndex += 1

		return graphCopy

	# Checks if a state is a valid solution. ignoreSpace can be set as true, to see if the 
	# state is a valid solution so far, even if it's not complete (has spaces left).
	def goal_test(self, state, ignoreSpace = False):
		
		graphCopy = self.makeNewGraph(state)

		# Check to see if any numbers appear twice in a row or column. Also can check if there's any spaces
		numbersRow = []
		numbersColumn = []
		for i in range (0,self.size):
			numbersRow = []
			numbersColumn = []
			for j in range (0,self.size):
				if graphCopy[i][j] == " " and not ignoreSpace:
					return False
				if numbersRow.count(graphCopy[i][j]) > 0 and graphCopy[i][j] != " ":
					return False
				numbersRow.append(graphCopy[i][j])

				if numbersColumn.count(graphCopy[j][i]) > 0 and graphCopy[j][i] != " ":
					return False
				numbersColumn.append(graphCopy[j][i])

		# Check to see if any numbers appear twice in a section. Also checks if there's any spaces
		numbersGrid = []
		for i in range(0,self.size):
			numbersGrid = []
			rowIndex = math.floor(i / self.verChunks) * (int)(self.size/self.verChunks)
			columnIndex = (i % self.horChunks) * (int)(self.size/self.horChunks)
			for j in range(0,(int)(self.size/self.verChunks)):
				for k in range(0,(int)(self.size/self.horChunks)):
					if graphCopy[rowIndex + j][columnIndex + k] == " " and not ignoreSpace:
						return False
					if numbersGrid.count(graphCopy[rowIndex + j][columnIndex + k]) >= 1 and graphCopy[rowIndex + j][columnIndex + k] != " ":
						return False
					numbersGrid.append(graphCopy[rowIndex + j][columnIndex + k])

		
		return True


	def setGoal(self,state):
		self.goal = state

	# Sets the goal, and prints the completed puzzle
	def printSolution(self, solution):
		if (solution == None):
			print ("NO SOLUTION\n")
			return
		self.setGoal(solution.state)
		print(self)

	# Prints the puzzle with the goal. If we haven't found the goal, it prints the original puzzle
	def __str__(self):
		newGraph = self.makeNewGraph(self.goal)
		newString = ""
		for i in range (0,self.size):
			for j in range (0,self.size):
				newString = newString + newGraph[i][j] + " "
				if (j+1)%(int)(self.size/self.horChunks) == 0:
					newString = newString + "| "
			if (i+1)%(int)(self.size/self.verChunks) == 0:
				newString = newString + "\n"
				for k in range (0,self.size + self.horChunks):
					newString = newString + "--"
			newString = newString + "\n"
		return newString




class Node:
	"""A node in a search tree. Contains a pointer to the parent (the node
	that this is a successor of) and to the actual state for this node. Note
	that if a state is arrived at by two paths, then there are two nodes with
	the same state.  Also includes the action that got us to this state"""

	def __init__(self, state, parent=None, action=None):
		"""Create a search tree Node, derived from a parent by an action.
		Update the node parameters based on constructor values"""
		self.state = state
		self.parent = parent
		self.action = action
		self.depth = 0
		# If depth is specified then depth of node will be 1 more than the depth of parent
		if parent:
			self.depth = parent.depth + 1

	def expand(self, problem):
		# List the nodes reachable in one step from this node.
		return [self.child_node(problem, action)
				for action in problem.actions(self.state)]

	def child_node(self, problem, action):
		next = problem.result(self.state, action)
		return Node(next, self, action)


class QueueClass:
	def __init__(self):
		self.data = []
	
	def enqueue(self, node):
		self.data.append(node)

	def dequeue(self):
		return self.data.pop(0)

def breadth_first_search(problem):
	# Start from first node of the problem Tree
	node = Node(problem.initial)

	# Check if problem is already unsolvable
	if (not problem.goal_test(node.state, True)):
		return None

	# Check if problem is already solved
	if problem.goal_test(node.state):
		return node

	# Create a Queue to store all nodes of a particular level. 
	frontier=QueueClass()
	frontier.enqueue(node)

	#Calculate and print total possible guesses for the solution
	problemSize = (problem.size**(problem.size**2 + 1) - 1) / (problem.size - 1)
	print("Max number of nodes: ", problemSize)

	possibilitiesChecked = 0;

	# Loop until all nodes are explored(frontier queue is empty) or Goal_Test criteria are met
	while len(frontier.data) != 0:
		
		# Remove from frontier, for analysis
		node = frontier.dequeue()
		# Loop over all children of the current node
		# Note: We consider the fact that a node can have multiple child nodes here
		for child in node.expand(problem):

			#Keep tracks of how many nodes we've searched
			possibilitiesChecked += 1
			print("\rNodes Checked: %d" % possibilitiesChecked, end = " " )

			# If child node meets Goal_Test criteria, return it
			if problem.goal_test(child.state):
				return child

			# Add every new valid child to the frontier
			if (problem.goal_test(child.state, True)):
				frontier.enqueue(child)
	return None

# Test problems provided from assignment
def testProblems():
	newProblem = Problem('   84 65  8      9     52 1 34 7 5 6 6 251 3 5 9 6 72 1 85     6      4  52 86   ', 9, 3, 3)
	print (newProblem)
	newProblem.setGoal(breadth_first_search(newProblem).state)
	print("\nSOLUTION:\n")
	print (newProblem)

	sixProblem = Problem("15  4 24  564    3     463  2  2  31", 6, 2, 3)
	print (sixProblem)
	solution = breadth_first_search(sixProblem)
	print("\nSOLUTION:\n")
	sixProblem.printSolution(solution)

	sixProblem = Problem("    4 56    3 2654 4 2 34   65156   ", 6, 2, 3)
	print (sixProblem)
	solution = breadth_first_search(sixProblem)
	print("\nSOLUTION:\n")
	sixProblem.printSolution(solution)

# Let user define custom problem
def customProblem():
	userInput = ""
	size = 0

	# Set puzzle size
	# 
	print("Type in 'quit' to return to the main menu at any time\n")
	while not type(userInput) is int:
		userInput = input("What size would you like the puzzle to be?\n>")
		if userInput == "quit":
				return
		try:
			userInput = int(userInput)
			size = userInput
		except ValueError:
			
			print ("\rYour board size must be an integer!")

	# Set the puzzle, checks for validity
	initialProblem = ""
	while initialProblem == "":
		userInput = input("Enter the numbers in the puzzle, from left to right, top to bottom.\nUse spaces for empty squares\n>")
		if userInput.lower() == "quit":
				return
		if len(userInput) != size**2:
			print("Your input does not have the correct number of numbers and spaces!")
			userInput = ""
		else:
			for ch in userInput:
				try:
					ch = int(ch)
					if ch < 1 or ch > size:
						print("Your input includes numbers that are too high or too low!")
						userInput = ""
						break
				except ValueError:
					if ch != " ":
						print("Your input includs an invalid character!")
						userInput = ""
						break
			initialProblem = userInput

	# Calculates the number of grid sections
	horSections = math.floor(math.sqrt(size))
	verSections = int(size/horSections)

	# Sets up and solves the puzzle
	newProblem = Problem(initialProblem, size, horSections, verSections)
	print("PROBLEM:")
	print(newProblem)
	solution = breadth_first_search(newProblem)
	print("\nSOLUTION:\n")
	newProblem.printSolution(solution)

#Let user input problems from text
def textProblem():
	userInput = ""
	puzzleFile = None
	print("\nThe puzzle text file should have one puzzle on each line.\nEach puzzle should have the numbers listed left to right, top to bottom.\nRepresent empty squares using spaces.")
	emptyFile = True

	#get input file
	while True:
		userInput = input("\nFilename: ")
		if os.path.isfile(userInput):
			break
		if userInput.lower() == "quit":
			return
	puzzleFile = open(userInput, "r")
	puzzleNumber = 1

	#Solve each puzzle
	for line in puzzleFile:

		# Set puzzle data
		line = line.rstrip('\n')
		puzzleSize = int(math.sqrt(len(line)))
		horSections = math.floor(math.sqrt(puzzleSize))
		verSections = int(puzzleSize/horSections)

		#check puzzle validity
		for ch in line:
			try:
				ch = int(ch)
				if ch < 1 or ch > puzzleSize:
					print("Your input includes numbers that are too high or too low!")
					userInput = ""
					return
			except ValueError:
				if ch != " ":
					print("Your input includs an invalid character!")
					userInput = ""
					return
		
		#Solve Puzzle
		newProblem = None
		solution = None
		newProblem = Problem(line, puzzleSize, horSections, verSections)
		print("PROBLEM " + str(puzzleNumber) + ":")
		print(newProblem)
		solution = breadth_first_search(newProblem)
		print("\nSOLUTION:\n")
		newProblem.printSolution(solution)
		puzzleNumber += 1


def sudokuSolver():
	userInput = ""
	print("Welcome to Sudoku Solver.")

	# Main Menu
	while userInput != "4" and userInput.lower() != "quit":
		text = """What would you like to do?
(1)Run test puzzles
(2)Enter custom puzzle
(3)Load puzzle from text file
(4)Quit
>"""
		userInput = input(text)
		if userInput == "1":
			testProblems()
		if userInput == "2":
			customProblem()
		if userInput == "3":
			textProblem()

#Automatically run when "python3 sudoku.py" is run in shell
sudokuSolver()


