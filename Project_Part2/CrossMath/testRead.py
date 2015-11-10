import re
import operator

# Thanks StackOverflow: http://stackoverflow.com/questions/1740726/python-turn-string-into-operator
ops = {'+': operator.add,
       '-': operator.sub,
       '*': operator.mul,
       '/': operator.truediv,
       '==': operator.eq,
       '!=': operator.ne,
       '<': operator.lt,
       '<=': operator.le,
       '>': operator.gt,
       '>=': operator.ge,
       'abs': operator.abs,
       '^': operator.pow
       }

def readCrossMath():

    # I was assuming operators applied in order as listed on puzzle, but
    # probably supposed to follow op precedence. If so, this isn't quite right.

    # read in the file with constraints for KenKen puzzles (1 line per puzzle)
    lines = open('testCrossMath.txt').readlines()
    testLine = 0 # test this line in file
    l = lines[testLine]
    #remove white space
    l=re.sub('[ ]','',l)
    print('l ',l)

    # split into the different constraints
    cs=re.split(',',l)
    print('cs ',cs)

    op = []
    vars = []
    ans = []
    fns = []
    groupR = []
    # for each constraint, extract vars and create lambda
    for c in cs:
        # extract what the equation equates to
        answer = re.findall('=\d+',c)
        answer = re.sub('=','',answer[0])
        c = re.sub('=\d+','',c)

        groupRight = False
        # check for parantheses for precedence
        if re.search('\)',c):
            if ( re.search('\)',c).start() == len(c)-2 ):
                groupRight = True
            c = re.sub('\(','',c)
            c = re.sub('\)','',c)

 
        # extract the 2 operators and the 3 vars, create the function
        op2 = re.findall('\W',c)
        var3 = re.findall('\w+\d+',c)


        print('c ',c)
        if groupRight:
            fn = lambda x,y,z : ops[op2[0]](x,ops[op2[1]](y,z)) == eval(answer)
        else:
            fn = lambda x,y,z : ops[op2[1]](ops[op2[0]](x,y),z) == eval(answer)
        op2 = op2[:2]

        op.append(op2)
        vars.append(var3)
        ans.append(answer)
        fns.append(fn)
        groupR.append(groupRight)
        # test the results with a print
        print('op var answer fn(16,16,4)',op2,' ',var3,' ',answer,' ',fn(16,16,4))
    return op, vars, ans, groupR


if __name__ == "__main__":
    #readKenKen()
    #readCrypt()
    #readFutoshiki()
    readCrossMath()
    
