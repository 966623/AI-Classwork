# AUTHOR: Amy C Larson
#
# MODIFICATION HISTORY:
#   11.02.2014  Version 0.0: Board implementation. Single Gold piece. Basic movement.
#   11.07.2014  Version 1.0: Multiple gold pieces. Gold consumption. Score keeping. Text Box. "Game Over"
#   11.08.2014  Version 1.1: Distance and vector calculations among object pieces
#   11.11.2014  Version 2.0:
#                   Created a single move look-ahead using a "happyFuture" board piece that does not display
#                   Created an evaluation function for happy and poison
#                   Added portals to the walls so pieces can wrap around to other side of board
#                   Added a matrix to represent board (only used for portals)

import random
from random import *

from math import *
from functools import *

import graphics
from graphics import *

class gamePiece( object ):
    # typePiece = { "happy", "poison", "gold", "obstacle" }
    # graphicsObject = the graphics object instance of either Image or Rectangle
    # gridPos = x,y graphics Point in the grid coordinates range 1 to gridSize
    # pieceID = identification number that is the index of the gamePieces list
    # active = true or false, indicating whether it is active on the board (gold becomes inactive when consumed)
    def __init__( self, graphicsObject, typePiece, gridPos, pieceID ):
        self.obj = graphicsObject
        self.type = typePiece
        self.pos = gridPos
        self.id = pieceID
        self.active = True

        @property
        def obj(self): return self.__obj

        @property
        def type(self): return self.__type

        @property
        def pos(self): return self.__pos

        @property
        def id(self): return self.__id

        @property
        def active(self): return self.__active
        
        @pos.setter
        def pos( self, newpos ): self.__pos = newpos

        @active.setter
        def active( self, state ): self.__active = state


##################  PRIMARY CLASS to Manage Pieces on the Board ###################
#
class board():
    def __init__(self, w=1000, h=800, g=20, ob=4, gc=10, b=10):
        # window dimensions, NxN grid size, number of obstacles, gold count, border cushion between window and board 
        self.width = w
        self.height = h
        self.gridSize = g
        self.border = b

        self.grids = [ [0 for x in range(self.gridSize+1)] for y in range(self.gridSize+1) ]
        
        #determine how many x (hspace) and y (vspace) units are in each grid square
        self.hspace = self.width/self.gridSize
        self.vspace = self.height/self.gridSize

        #determine location of portals. Chose to put 2 evenly distributed on each side of the board
        # indexing is awkward since python is 0-based and my grid is 1-based. Might fix that one day
        gp = int(self.gridSize/4)
        portalPos = [ gp-1, gp, gp+1, gp*3-1, gp*3, gp*3+1 ]
        self.portals = []
        for xy in portalPos:
            self.portals.extend( (Point(xy,1),  Point(xy,self.gridSize), Point(1,xy), Point(self.gridSize,xy)) )
        for p in self.portals:
           self.grids[p.getX()][p.getY()] = "portal"
        
         # create instance of graphics window and set coordinates so that lower-left of board is at {0,0}
        self.boardWin = GraphWin("Happy-Poison",self.width+2*self.border,self.height+2*self.border)
        self.boardWin.setCoords(-self.border,-self.border,self.width+self.border,self.height+self.border)

        # text box in lower left corner of graphics window
        self.statusText = Text( Point(500,-self.border+20), "Setting Up Game" )
        self.statusText.draw(self.boardWin)
        
        # maintain a list of board elements to display on board (e.g. happy, poison, gold)
        self.gamePieces = []      
        self.gamePieceCount = 0

        self.obsCount = ob
        self.obstacles = []

        self.goldCount = gc
        self.golds = []

    def getWindow( self ): return self.boardWin

    def getPosition( self, pieceID) : return self.gamePieces[pieceID].pos

    # this setPosition sets grid position only in data structure. does not redraw object.
    def setPosition( self, pieceID, newpos) : self.gamePieces[pieceID].pos = newpos

    def changeMsg( self, txt ):
        self.statusText.setText(txt)

    # convert grid coordinates in range {1..gridSize} to screen coordinates in range { 0..width/height }
    def convert( self, g ):
        return Point( self.hspace*(g.getX() - 0.5), self.vspace*(g.getY()-0.5) )

    # happy often gets stuck around portals. not sure if that's the eval function or something buggy with this
    def pieceAtPos( self, gPos ):
        # given a grid position, return the type of the object at that position (or "none")
        gx = gPos.getX() 
        gy = gPos.getY() 
        
        # check for walls and portals
        if ( gx == 0 ):
            if self.grids[1][gy] == "portal":
                return self.pieceAtPos( Point(self.gridSize,gy) )
            else:
                return "wall"
        if ( gy == 0 ):
            if self.grids[gx][1] == "portal":
                return self.pieceAtPos( Point(gx,self.gridSize))
            else:
                return "wall"
        if ( gx > self.gridSize) or ( gy > self.gridSize ):
            gx = gx%self.gridSize
            gy = gy%self.gridSize
            if self.grids[gx][gy]== "portal":
                return self.pieceAtPos( Point(gx,gy))
            else:
                return "wall"

        # check for other game pieces
        for gp in self.gamePieces:
            if ( gp.pos.getX() == gx) and ( gp.pos.getY() == gy) and gp.active==True:
                return gp.type
        return "none"

   # get random grid location for placing an object
    def getRandom( self ):
        while (1) :
            px = randrange(2,self.gridSize)
            py = randrange(2,self.gridSize)
            if ( "none" == self.pieceAtPos( Point( px, py ) ) ):
                return Point( px, py )

    # ---------- Fixed Board Elements
    def drawPerimeter(self):
        self.perimeter = Rectangle(Point(0,0),Point(self.width,self.height))
        self.perimeter.draw(self.boardWin)
    
    def drawHlines(self):
        #draw horizontal lines
        Ys = [  0 + self.vspace*i for i in range(1,self.gridSize) ]
        hLines = [ Line(Point(0,y),Point(self.width,y)) for y in Ys ]
        for l in hLines:
            l.setFill("PeachPuff")
            l.draw(self.boardWin)

    def drawVlines(self):
        #draw vertical lines
        Xs = [  0 + self.hspace*i for i in range(1,self.gridSize) ] 
        vLines = [ Line(Point(x,0),Point(x,self.height)) for x in Xs ]
        for l in vLines:
            l.setFill("PeachPuff")
            l.draw(self.boardWin)

    # awkward due to mismatched indexing (grid used 1-based)
    def drawPortals(self):
        pLines = []
        for p in self.portals:
            startX = p.getX()-1
            endX = p.getX()
            startY = p.getY()-1
            endY = p.getY()
            if p.getX() == self.gridSize:
                startX = p.getX()
            if p.getX() == 1:
                endX = endX-1
            if p.getY() == self.gridSize:
                startY = p.getY()
            if p.getY() == 1:
                endY = endY-1
            pLines.append( Line( Point( startX*self.hspace, startY*self.vspace ),
                                 Point( endX*self.hspace, endY*self.vspace) ))
        for l in pLines:
            l.setFill("white")
            l.draw(self.boardWin)

    def draw(self):
        self.drawPerimeter()
        self.drawHlines()
        self.drawVlines()
        self.drawPortals()

    # --------- Obstacles and Gold

    def createObstacles( self ):
        # create obstacles, saving the grid location of each
        for i in range(self.obsCount):
            gP = self.getRandom()
            self.obstacles.append( self.registerGamePiece( "obstacle", gP ) )
            
    def createGolds( self ):
        # create golds, saving the grid location of each
        for i in range(self.goldCount):
            gP = self.getRandom()
            self.golds.append( self.registerGamePiece( "gold",gP,"C:\\Users\\Amy\\Documents\\__4511\\CODE\\gold_xs.gif" ))

    def drawObstacles(self):
        for ob in self.obstacles:
            self.gamePieces[ob].obj.draw(self.boardWin)
            
    def drawGolds(self):
        for au in self.golds:
            self.gamePieces[au].obj.draw(self.boardWin)

    def removeGold( self, pieceID ):
        gx = self.gamePieces[pieceID].pos.getX()
        gy = self.gamePieces[pieceID].pos.getY()
        for au in self.golds:
            goldPiece = self.gamePieces[au]
            if gx == goldPiece.pos.getX() and gy == goldPiece.pos.getY() :
                goldPiece.active = False
                goldPiece.obj.undraw()
                

# ----- Information Gathering
    # calculate the abolute manhattan distance from piece1 to piece2. These pieces can be any object registered and in gamePieces
    def distance( self, piece1, piece2 ):
        pos1 = self.gamePieces[piece1].pos
        pos2 = self.gamePieces[piece2].pos
        return abs(pos1.getX()-pos2.getX()) + abs(pos1.getY()-pos2.getY())

    def vector( self, piece1, piece2 ):
        pos1 = self.gamePieces[piece1].pos
        pos2 = self.gamePieces[piece2].pos
        return [ pos2.getX()-pos1.getX(), pos2.getY()-pos1.getY() ]

    # generate a vector of absolute manhattan distances to all visible gold pieces
    def distancesToGolds( self, piece1 ):
        distances = []
        pos = self.gamePieces[piece1].pos
        for g in self.golds:
            au = self.gamePieces[g]
            if ( au.active == True ):
                distances.append( abs(au.pos.getX()-pos.getX()) + abs(au.pos.getY()-pos.getY() ) )
        return distances

    def vectorsToGolds( self, piece1 ):
        vectors = []
        pos = self.gamePieces[piece1].pos
        for g in self.golds:
            au = self.gamePieces[g]
            if ( au.active == True ):
                vectors.append( [ au.pos.getX()-pos.getX() , au.pos.getY()-pos.getY() ] )
        return vectors

# ---- Controlling Game pieces

   # add an object to the board and let the board be responsible for moving and displaying
    def registerGamePiece( self, pieceType, gPos, fname="none" ):
        if pieceType in [ "happy", "poison", "gold" ]:
            pos = self.convert( gPos )
            obj = Image( pos, fname )
            self.gamePieces.append( gamePiece( obj, pieceType, gPos, self.gamePieceCount ) )
            self.gamePieceCount = self.gamePieceCount+1
            return self.gamePieceCount-1
        elif ( "obstacle" == pieceType ):
            x = (gPos.getX()-1)*self.hspace
            y = (gPos.getY()-1)*self.vspace
            obj = Rectangle( Point(x,y), Point( x+self.hspace, y+self.vspace ) )
            obj.setFill("DarkRed")
            self.gamePieces.append( gamePiece( obj, pieceType, gPos, self.gamePieceCount ))
            self.gamePieceCount = self.gamePieceCount+1
            return self.gamePieceCount-1
        elif ( "happyFuture" == pieceType ):
            # this piece is not visible. used for look-ahead. might want to do the same for poison
            pos = self.convert( gPos )
            obj = pieceType
            self.gamePieces.append( gamePiece( obj, pieceType, gPos, self.gamePieceCount ) )
            self.gamePieces[self.gamePieceCount].active = False
            self.gamePieceCount = self.gamePieceCount+1
            return self.gamePieceCount-1
        else:
            print("object type unknown in registerObject()")

    # dpos is a potential change in x,y for pieceID. return the object type that is at this potential position
    # pieceAtPos adjusts for positions that pass through portals
    def checkMove( self, pieceID, dpos ):
        gPiece = self.gamePieces[pieceID]
        gx = gPiece.pos.getX() + dpos.getX()
        gy = gPiece.pos.getY() + dpos.getY()
        return self.pieceAtPos( Point( gx, gy ) )

    # move pieceID by dpos (in grid coords) on the board (NOTE: This assumes it is a legal move. Might want to checkMove before this)
    def movePieceRelative( self, pieceID, dpos ):
        gPiece = self.gamePieces[pieceID]
        gx = gPiece.pos.getX() + dpos.getX()
        if ( gx == 0 ):
            gx = self.gridSize
        if ( gx > self.gridSize ):
            gx = 1
        gy = gPiece.pos.getY() + dpos.getY()
        if ( gy == 0 ):
            gy = self.gridSize
        if ( gy > self.gridSize ):
            gy = 1
        # use movePieceAbsolute because this can deal with moving through portals
        return self.movePieceAbsolute( pieceID, Point(gx,gy ))


    # move pieceID to newpos (in grid coords) on board (NOTE: This assumes it is a legal move. Might want to checkMove before this)
    def movePieceAbsolute( self, pieceID, newpos ):
        bxy = self.convert( newpos )
        gPiece = self.gamePieces[pieceID]
        if gPiece.active == True:
            xy = gPiece.obj.getAnchor()
            dx = bxy.getX()-xy.getX()
            dy = bxy.getY()-xy.getY()
            gPiece.obj.move( dx, dy )
        gPiece.pos = newpos
        return gPiece.pos

    def drawObjects( self ):
        for gp in self.gamePieces:
            if gp.active==True: gp.obj.draw( self.boardWin )
            
    def drawObject( self, gpID ):
        self.gamePieces[gpID].obj.draw( self.boardWin)
        
    def gameOver( self ):
        msgObj = Text( Point( self.width/2, self.height/2), "Game Over")
        msgObj.setSize( 32 )
        msgObj.setTextColor( "red" )
        msgObj.draw(self.boardWin)
        for i in range(10):
            # put in empty loops because sleep crashed python
            for j in range(10000000): x=1
            msgObj.setTextColor( "white" )
            for j in range(10000000) : x=1
            msgObj.setTextColor("red")
        self.boardWin.close()
                                    
def test():

    #establish window and board
    happyBoard = board( 1000, 800, 20, 15, 15, 50 )    # ( width, height, NxN grid size, obstacle count, gold count, border )
    happyBoard.draw()

    # add obstacles and gold to board
    happyBoard.createObstacles()
    happyBoard.createGolds()
    
    # add happy
    # NOTE: the pathname needs to be changed for these files to reflect your location
    happy = happyBoard.registerGamePiece( "happy", happyBoard.getRandom() , "C:\\Users\\Amy\\Documents\\__4511\\CODE\\happy_xs.gif" )
    happyFuture = happyBoard.registerGamePiece( "happyFuture", happyBoard.getPosition(happy),"none")
    
    # add poisons
    poison1 = happyBoard.registerGamePiece( "poison", happyBoard.getRandom() ,"C:\\Users\\Amy\\Documents\\__4511\\CODE\\poison_xs.gif")   
    poison2 = happyBoard.registerGamePiece( "poison", happyBoard.getRandom() ,"C:\\Users\\Amy\\Documents\\__4511\\CODE\\poison_xs.gif")

    happyBoard.drawObjects()

    happyBoard.changeMsg("press key to move pieces")

    # delta change for each of the directional movements
    NSEW = [ Point(0,1), Point(1,0), Point(0,-1), Point(-1,0) ]
    happyPoints = 0
    gameOver = False
    
    status =  str( happyBoard.distancesToGolds(happy) )
    status = status + "     Poison1: " + str( happyBoard.distance( happy, poison1 )) + "   Poison2: " + str( happyBoard.distance( happy, poison2 ))
    
    status =  str( happyBoard.vectorsToGolds(happy) )
    status = status + "     Poison1: " + str( happyBoard.vector( happy, poison1 )) + "   Poison2: " + str( happyBoard.vector( happy, poison2 ))
    
    happyBoard.changeMsg( status )

    while ( not gameOver ):
        
        #sit in this empty loop until user presses a key
        while (not happyBoard.getWindow().checkKey()):
            x=1


        # can be used for random movement on board
        '''# move happy
        d = randrange( 0, 4 )
        occupiedBy = happyBoard.checkMove( happy, NSEW[d] )
        if occupiedBy == "none":
            happyBoard.movePiece( happy, NSEW[d] )
        elif occupiedBy == "gold":
            happyBoard.movePiece( happy, NSEW[d] )
            happyPoints = happyPoints+1
            happyBoard.changeMsg("Score: "+str(happyPoints))
            happyBoard.removeGold( happy )'''

        # move happy
        maxValue = "none"
        move = -1
        values = []
        for d in NSEW:
            occupiedBy = happyBoard.checkMove( happy, d )
            if occupiedBy in ["gold"]:
                move = d
                maxValue = "gold"
                break;
            elif occupiedBy in ["none"]:
                # move virtual piece in direction d
                happyBoard.movePieceRelative( happyFuture, d )
                # gather stats about board
                goldDistances = happyBoard.distancesToGolds( happyFuture )
                poison1Distance = happyBoard.distance( happyFuture, poison1 )
                poison2Distance = happyBoard.distance( happyFuture, poison2 )
                goldDistances = sorted(goldDistances)

                # Experimenting with evaluation functions ...
                scale = [ i for i in range(len(goldDistances),0,-1) ]
                maxdist = 20
                value = 0
                #valueview = []
                # only care about 3 closest golds. f(gold) = (20-gold)*weight, where weight scales with distance
                scale = [10, 5, 2]
                for i in range(min(3,len(goldDistances))):
                    #valueview.append( (maxdist-goldDistances[i])*scale[i])
                    value = value + (maxdist-goldDistances[i])*scale[i]
                    #value = value + distVectorG[i]*scale[i]
                #print(valueview, value, d)
                value = value + 10*min(poison1Distance,poison2Distance) + 5*max(poison1Distance,poison2Distance)
                values.append(value)

                # move virtual happyFuture back to happy position
                happyBoard.setPosition( happyFuture, happyBoard.getPosition(happy) )
                if move == -1:
                    move = d
                    maxValue = value
                elif value > maxValue:
                    move = d
                    maxValue = value
            #else occupiedBy in ["poison","obstacle","wall"]:
        #print(values)

        # if not moving, then probably something not working right, but this way it won't crash
        if ( not -1 == move ):
            happyBoard.movePieceRelative( happy, move )
            happyBoard.movePieceAbsolute( happyFuture, happyBoard.getPosition(happy) )
            if maxValue == "gold":
                happyPoints = happyPoints+1
                happyBoard.changeMsg("Score: "+str(happyPoints))
                happyBoard.removeGold( happy )

        # move poisons. this is hand calculating moves. needs to get fixed to work with portals. virtual poisonFuture probably good idea
        distH = happyBoard.vector( poison1, happy )
        minValue = "none"
        move = -1
        for d in NSEW:
            occupiedBy = happyBoard.checkMove( poison1, d )
            if occupiedBy in ["none","gold"]:
                value = sqrt(pow(distH[0]-d.getX(),2)+pow(distH[1]-d.getY(),2))
                if minValue == "none":
                    minValue = value
                    move = d
                elif value < minValue:
                    minValue = value
                    move = d
            if occupiedBy == "happy":
                happyBoard.movePieceRelative( poison1, d )
                happyBoard.gameOver()
                gameOver = True
                break;
        if not move == -1:
            happyBoard.movePieceRelative( poison1, move )
            
            
        distH = happyBoard.vector( poison2, happy )
        minValue = "none"
        move = -1
        for d in NSEW:
            occupiedBy = happyBoard.checkMove( poison2, d )
            if occupiedBy in ["none","gold"]:
                value = sqrt(pow(distH[0]-d.getX(),2)+pow(distH[1]-d.getY(),2))
                if minValue == "none":
                    minValue = value
                    move = d
                elif value < minValue:
                    minValue = value
                    move = d
            if occupiedBy == "happy":
                happyBoard.movePieceRelative( poison2, d )
                happyBoard.gameOver()
                gameOver = True
                break;
        if not move == -1:
           happyBoard.movePieceRelative( poison2, move )

        status =  str( happyBoard.distancesToGolds(happy) )
        status = status + "     Poison1: " + str( happyBoard.distance( happy, poison1 )) + "   Poison2: " + str( happyBoard.distance( happy, poison2 ))
        happyBoard.changeMsg( status )

if __name__ == "__main__":
    test()
