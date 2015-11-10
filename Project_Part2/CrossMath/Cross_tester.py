__author__ = 'Sean'

import testRead
import AC3_Cross
import MAC_Cross
import menu
import DFS_Cross

lineDict = dict()
def setLineRead(line):
    testRead.lineRead = line

def runAC3():
    const = []
    vars = dict()
    AC3_Cross.setupAC3(const, vars)
    AC3_Cross.AC3(const, vars, None)

def runMAC():
    op, vars, ans, groupR = testRead.readCrossMath()
    solver = MAC_Cross.MacCrypt(op, vars, ans, groupR)
    solution = solver.solve()
    print("\nFinal Solution")
    for k in sorted(solution.keys()):
        print(k, " = ", solution[k].domain[0])

def runDFS():
    op, var, ans, groupR = testRead.readCrossMath()
    solver = DFS_Cross.DFSCross(op, var, ans, groupR)
    solution = solver.solve()
    print("\nFinal Solution")
    for k in sorted(solution.keys()):
        print(k, " = ", solution[k])

# Setup menu items
mainChoice = menu.ChoicePrompt("Do you want to run AC3 or MAC?", ["AC3", "MAC", "DFS"])
chooseTest = menu.InputPrompt("Which puzzle, numbers 0 - 4, do you want to run?", int, lineDict, "line",
                              lambda x: int(x) >= 0 and int(x) <= 4)
setLine = menu.FunctionRun(setLineRead, lineDict)
runAC3Test = menu.FunctionRun(runAC3, None)
runMACTest = menu.FunctionRun(runMAC, None)
runDFSTest = menu.FunctionRun(runDFS, None)

# Setup menu tree
runAC3Node = menu.menuNode(runAC3Test, [])
runMACNode = menu.menuNode(runMACTest, [])
runDFSNode = menu.menuNode(runDFSTest, [])

setAC3TestNode = menu.menuNode(setLine, [runAC3Node])
setMACTestNode = menu.menuNode(setLine, [runMACNode])
setDFSTestNode = menu.menuNode(setLine, [runDFSNode])

choseAC3Node = menu.menuNode(chooseTest, [setAC3TestNode])
choseMACNode = menu.menuNode(chooseTest, [setMACTestNode])
choseDFSNode = menu.menuNode(chooseTest, [setDFSTestNode])

mainChoiceNode = menu.menuNode(mainChoice, [choseAC3Node, choseMACNode, choseDFSNode])

choseAC3Node.setReturnNode(mainChoiceNode)
choseMACNode.setReturnNode(mainChoiceNode)
choseDFSNode.setReturnNode(mainChoiceNode)

setAC3TestNode.setReturnNode(choseAC3Node)
setMACTestNode.setReturnNode(choseMACNode)
setDFSTestNode.setReturnNode(choseDFSNode)

runAC3Node.setReturnNode(mainChoiceNode)
runMACNode.setReturnNode(mainChoiceNode)
runDFSNode.setReturnNode(mainChoiceNode)

mainChoiceNode.execute()