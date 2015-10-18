from copy import deepcopy

class menuNode(object):
	def __init__ (self, action, children, returnNode = None):
		self.action = action
		self.children = children
		self.returnNode = returnNode
		#self.parent = parent

	#Execute the node
	def execute(self, parent = None, args = None):
		result = self.action.run()
		if (result == -1):
			if self.returnNode == None:
				return
			self.returnNode.execute()
			return
		if (len(self.children) != 0):
			#print(result)
			self.children[result - 1].execute(self)
			return
		else:
			if self.returnNode == None:
				return
			self.returnNode.execute()
			return

	def setReturnNode(self, node):
		self.returnNode = node

	def setChildren(self, nodes):
		self.children = nodes

# Gives user choices to choose from
class ChoicePrompt(object):

	def __init__(self, question, options, quitCommand = "quit"):
		if (type(question) != str):
			print ("Question must be a string.\n")
			return

		self.question = str(question)
		self.options = options
		self.quitCommand = quitCommand

	def run(self):
		optionCopy = deepcopy(self.options)
		for i in range(0,len(optionCopy)):
			optionCopy[i] = optionCopy[i].lower()
		userInput = 0
		while userInput == 0:
			print (self.question)
			for i in range (0, len(self.options)):
				print ("(" + str(i + 1) + ") " + self.options[i])
			stringInput = input(">")
			try:
				intInput = int(stringInput)
				if intInput > 0 and intInput <= len(self.options):
					userInput = intInput 
				else:
					print("Your input must match one of the options")
			except ValueError:
				if (stringInput.lower() == self.quitCommand):
					userInput  = -1
					break
				try:
					userInput = optionCopy.index(stringInput.lower())
					break
				except ValueError:
					userInput = 0

		return userInput

# Lets user input a value, stores it in a dictionary
class InputPrompt(object):

	def __init__(self, question, inputType, dictionary, k):
		self.question = str(question)
		self.inputType = inputType
		self.dictionary = dictionary
		self.k = k

	def run(self):
		userInput = ""
		while userInput == "":
			print(self.question)
			userInput = input(">")
		self.dictionary[self.k] = self.inputType(userInput)
		return 0

# Displays some text
class TextDisplay(object):

	def __init__(self, display):
		self.display = str(display)

	def run(self):
		print(self.display)
		return 0

# Runs a function, args uses values from an input dictionary
class FunctionRun(object):

	def __init__(self, function, args):
		self.function = function
		self.args = args

	def setArgs(self, args):
		self.args = args

	def run(self):
		self.function(**self.args)
		return 0







