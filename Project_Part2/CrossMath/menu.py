__author__ = 'Sean Lin'

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

# Gives user choices to choose from.
# QUESTION (string) is the question to ask
# OPTIONS  (string list) is the options to choose from
# quitCommand is what to type to quit
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

# Lets user input a value, stores it in a dictionary.
# QUESTION (string) is the question to ask
# INPUTTYPE(type) is the type the input has to be
# DICTIONARY is the dictionary the response is stored in
# K is the key used
# VALIDITY is a function that checks validity of the input
class InputPrompt(object):

    def __init__(self, question, inputType, dictionary, k, validity = lambda x: True, errorMsg = ""):
        self.question = str(question)
        self.inputType = inputType
        self.dictionary = dictionary
        self.k = k
        self.valid = validity
        self.errorMsg = errorMsg

    def run(self):
        userInput = ""
        typeCorrect = False
        while userInput == "" or not typeCorrect or not self.valid(userInput):
            print(self.question)
            userInput = input(">")
            try:
                temp = self.inputType(userInput)
                if type(temp) is self.inputType:
                    typeCorrect = True
            except:
                typeCorrect = False
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
# FUNCTION is the function to run
# ARGS is the dictionary to use for arguments, use None if there are no arguments
# The function takes the dictionary elements as arguments, in alphabetic order by key.
class FunctionRun(object):

    def __init__(self, function, args):
        self.function = function
        self.args = args

    def setArgs(self, args):
        self.args = args

    def run(self):
        if self.args == None:
            self.function()
            return 0

        listArgs = []
        for e in sorted(self.args.keys()):
            listArgs.append(self.args[e])
        self.function(*listArgs)
        return 0







