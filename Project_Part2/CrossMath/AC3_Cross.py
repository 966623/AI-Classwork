__author__ = 'Sean'
from random import randrange
# Sean Lin
# Cross Math

import time
import sys
import functools
import queue
from functools import reduce
from testRead import *
# The primary problem set-up consists of "variables" and "constraints":
#   "variables" are a dictionary of constraint variables (of type ConstraintVar), example variables['A1']
#   "constraints" are a set of binary constraints (of type BinaryConstraint)

# First, Node Consistency is achieved by passing each UnaryConstraint of each variable to nodeConsistent().
# Arc Consistency is achieved by passing "constraints" to Revise().
# AC3 is not fully implemented, Revise() needs to be repeatedly called until all domains are reduced to a single value

class ConstraintVar:
    # instantiation example: ConstraintVar( [1,2,3],'A1' )
    # MISSING filling in neighbors to make it easy to determine what to add to queue when revise() modifies domain
    def __init__( self, d, n ):
        self.domain = [ v for v in d ]
        self.name = n
        self.neighbors = []

class UnaryConstraint:
    # v1 is of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiation example: UnaryConstraint( variables['A1'], lambda x: x <= 2 )
    def __init__( self, v, fn ):
        self.var = v
        self.func = fn

class BinaryConstraint:
    # v1 and v2 should be of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiate example: BinaryConstraint( A1, A2, lambda x,y: x != y )
    def __init__(self, v1, v2, fn):
        self.var1 = v1
        self.var2 = v2
        self.func = fn

class TernaryConstraint:
    # v1, v2 and v3 should be of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiate example: BinaryConstraint( A1, A2, A3 lambda x,y,z: x != y != z )
    def __init__(self, v1, v2, v3, fn):
        self.var1 = v1
        self.var2 = v2
        self.var3 = v3
        self.func = fn

def allDiff( constraints, v ):
    # generate a list of constraints that implement the allDiff constraint for all variable combinations in v
    # constraints is a preconstructed list. v is a list of ConstraintVar instances.
    # call example: allDiff( constraints, [A1,A2,A3] ) will generate BinaryConstraint instances for [[A1,A2],[A2,A1],[A1,A3] ...
    fn = lambda x,y: x != y
    for i in range( len( v ) ):
        for j in range( len( v ) ):
            if ( i != j ) :
                constraints.append( BinaryConstraint( v[ i ], v[ j ], fn ) )


# setup up cross math constraints
def setUpCross(variables, constraints, op, var, ans, groupR):
    vList = []
    vList = vList + var[0] + var[1] + var[2]
    #print(vList)

    domain = [i for i in range(1,10)]

    for v in vList:
        variables[v] = ConstraintVar(domain, v)

    allCons = []
    for k in variables.keys():
        allCons.append( variables[k] )

    # Constrain all spaces to different digits
    allDiff( constraints, allCons )

    # Constrain each set of spaces using the given equation
    for i in range(len(op)):
        #print(groupR[i])
        if groupR[i]:
            constraints.append(TernaryConstraint(variables[var[i][0]],variables[var[i][1]],variables[var[i][2]],
                                                 lambda x,y,z,op1 = ops[op[i][0]], op2 = ops[op[i][1]], a = int(ans[i]):
                                                 op1(x,op2(y,z)) == a))

            constraints.append(TernaryConstraint(variables[var[i][1]],variables[var[i][0]],variables[var[i][2]],
                                                 lambda x,y,z,op1 = ops[op[i][0]], op2 = ops[op[i][1]],a = int(ans[i]):
                                                 op1(y,op2(x,z)) == a))

            constraints.append(TernaryConstraint(variables[var[i][2]],variables[var[i][1]],variables[var[i][0]],
                                                 lambda x,y,z,op1 = ops[op[i][0]], op2 = ops[op[i][1]], a = int(ans[i]):
                                                 op1(z,op2(y,x)) == a))

        else:
            constraints.append(TernaryConstraint(variables[var[i][0]],variables[var[i][1]],variables[var[i][2]],
                                                 lambda x,y,z,op1 = ops[op[i][0]], op2 = ops[op[i][1]],a = int(ans[i]):
                                                 op2(op1(x,y),z) == a))

            constraints.append(TernaryConstraint(variables[var[i][1]],variables[var[i][0]],variables[var[i][2]],
                                                 lambda x,y,z,op1 = ops[op[i][0]], op2 = ops[op[i][1]],a = int(ans[i]):
                                                 op2(op1(y,x),z) == a))

            constraints.append(TernaryConstraint(variables[var[i][2]],variables[var[i][1]],variables[var[i][0]],
                                                 lambda x,y,z,op1 = ops[op[i][0]], op2 = ops[op[i][1]],a = int(ans[i]):
                                                 op2(op1(z,y),x) == a))

def Revise( cv , variables):
    revised = False
    domain_list = []
    if ( type( cv ) == TernaryConstraint ):

        if not ( cv.var2 in cv.var1.neighbors ):
            cv.var1.neighbors.append( cv.var2 )
        if not ( cv.var3 in cv.var1.neighbors ):
            cv.var1.neighbors.append( cv.var3 )
        if not ( cv.var1 in cv.var2.neighbors ):
            cv.var1.neighbors.append( cv.var1 )
        if not ( cv.var3 in cv.var2.neighbors ):
            cv.var1.neighbors.append( cv.var3 )
        if not ( cv.var1 in cv.var3.neighbors ):
            cv.var1.neighbors.append( cv.var1 )
        if not ( cv.var2 in cv.var3.neighbors ):
            cv.var1.neighbors.append( cv.var2 )

        dom1 = list( variables[cv.var1.name].domain )
        dom2 = list( variables[cv.var2.name].domain )
        dom3 = list( variables[cv.var3.name].domain )
        # for each value in the domain of variable 1
        for x in dom1:
            check = 0
            # for each value in the domain of variable 2
            for y in dom2:
                # for each value in the domain of variable 3
                for z in dom3:
                # if nothing in domain of variable2 satisfies the constraint when variable1==x, remove x
                    if ( cv.func( x, y, z ) == False ):
                        check += 1
                    if ( check == len( dom2 ) * len( dom3 ) ):
                        variables[cv.var1.name].domain.remove( x )
                        revised = True

    elif ( type( cv ) == BinaryConstraint ):
        if not ( cv.var2 in cv.var1.neighbors ):
            cv.var1.neighbors.append( cv.var2 )
        if not ( cv.var1 in cv.var2.neighbors ):
            cv.var1.neighbors.append( cv.var1 )

        dom1 = list( variables[cv.var1.name].domain)
        dom2 = list( variables[cv.var2.name].domain)
        # for each value in the domain of variable 1
        for x in dom1:
            check = 0
            # for each value in the domain of variable 2
            for y in dom2:
            # if nothing in domain of variable2 satisfies the constraint when variable1==x, remove x

                if ( cv.func( x, y ) == False):
                    check += 1
                if ( check == len( dom2 ) ):

                    variables[cv.var1.name].domain.remove( x )
                    revised = True

    elif ( type( cv ) == UnaryConstraint ):
        dom = list( variables[cv.var.name].domain)
        # for each value in the domain of variable
        for x in dom:
            if ( cv.func( x ) == False ):
                variables[cv.var.name].domain.remove( x )
                revised = True

    return revised

def nodeConsistent( uc ):
    domain = list(uc.var.domain)
    for x in domain:
        if ( False == uc.func(x) ):
            uc.var.domain.remove(x)

def printDomains( vars, n=3 ):
    count = 0
    for k in sorted(vars.keys()):
        print( k,'{',vars[k].domain,'}, ',end="" )
        count = count+1
        if ( 0 == count % n ):
            print(' ')

# Sets up variables and constraints, runs ac3 once
def setupAC3(constraints, variables):
    # create a dictionary of ConstraintVars keyed by names in VarNames.
    op, var, ans, groupR = readCrossMath()

    t = time.time()
    setUpCross(variables, constraints, op, var, ans, groupR)
    print("Initial Domains")
    printDomains( variables )

    #transferConstraint( cons, constraints, variables )
    que = queue.LifoQueue()

    # Initialize the queue by putting all the constraint variables in the queue
    for c in constraints:
        que.put(c)

    while not( que.empty() ):
        constr = que.get()
        if Revise( constr, variables ):
            que.put(constr)

    t = time.time() - t
    print("\nDomains after AC3")
    printDomains( variables )
    print("\n")
    print("AC3 Time Taken: ", t)

# Runs ac3 on the variables and constraints again. only ques neighbors of var if var isn't None
def AC3(constraints, variables, var = None):
    #transferConstraint( cons, constraints, variables )
    que = queue.LifoQueue()

    # Initialize the queue by putting all the constraint variables in the queue

    if var != None:
        for c in constraints:
            if type(c) == TernaryConstraint:
                if c.var2.name == var.name or c.var3.name == var.name:
                    que.put(c)
            elif type(c) == BinaryConstraint:
                if c.var2.name == var.name:
                    que.put(c)

    else:
        for c in constraints:
            que.put(c)


    while not( que.empty() ):
        constr = que.get()
        if Revise( constr, variables ):
            que.put(constr)

    #print("\nFinal Domains")
    #printDomains( variables )
    #dString = "."*randrange(1,6)
    #print(dString)
    #print("\rSolving" + dString, end ="")

    for k in list(variables.keys()):
        if len(variables[k].domain) == 0:
            return -1
        elif len(variables[k].domain) > 1:
            return 0
    return 1
"""
const = []
vars = dict()
setupAC3(const, vars)
AC3(const, vars, None)
"""



