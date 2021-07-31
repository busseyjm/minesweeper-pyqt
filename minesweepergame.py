import random
import math

#coord system for this game:
#using the basis of a 2d array
#(y, x) and growing right and down
# eg:
# (0,0)(0,1)(0,2)
# (1,0)(1,1)(1,2)
# (2,0)(2,1)(2,2)

#difficulties:
#   easy    8x8,    10 mines
#   medium  16x16   40 mines
#   expert  30x16   99 mines

# board symbols:
# BACK:
#   X       = uninitialized
#   B       = bomb
#   0-8     = bomb count
# FRONT:
#   U       = unclicked
#   E       = empty and clicked
#   1-8     = bomb count and clicked
#   F       = flagged
#   B       = bomb
#   C       = clicked bomb
#   W       = wrongly flagged bomb

random.seed(12345)

class game():
    #front and back arrays, front is what the user sees
    boardback = dict()
    boardfront = dict()
    changes = dict()

    #coordinates of every bomb, in tuples
    bombs = []

    #how many bombs there are
    bombcount = 0

    #size of the game
    sizex = 0
    sizey = 0

    #def __init__(self):

    def generategame(self, difficulty):
        if (difficulty == "EASY"):
            self.bombcount = 10
            self.sizex = 8
            self.sizey = 8

        elif (difficulty == "MEDIUM"):
            self.bombcount = 40
            self.sizex = 16
            self.sizey = 16

        elif (difficulty == "EXPERT"):
            self.bombcount = 99
            self.sizex = 30
            self.sizey = 16

        for y in range(0,self.sizey):
            for x in range(0,self.sizex):
                self.boardback[y,x] = 'X'
                self.boardfront[y,x] = 'U'

        # generate a sequence of unique numbers that are within the max square count
        bombs = random.sample(range(0,(self.sizex*self.sizey)), self.bombcount)

        # translate the numbers into coordinates within the grid
        for i in bombs:
            bombx = i % self.sizex
            i = math.floor(i/self.sizex)
            bomby = i % self.sizey
            self.boardback[bomby,bombx] = 'B'
            self.bombs.append((bomby,bombx))
        
        self.calculatebackend()

    def generatecustomgame(self, height, width, percentbombs):
        #TODO
        self.sizex = width
        self.sizey = height
        print(random.sample(range(1,100), 5))

    # function to maintain a running list of changes, so that the frontend may update just those cells
    def setfront(self,y,x,value):
        self.boardfront[y,x] = value
        self.changes[y,x] = value


    def calculatebackend(self):
        for y in range(0,self.sizey):
            for x in range(0,self.sizex):
                if (self.boardback[y,x] == 'B'):
                    continue

                bombcount = 0

                if (((y-1,x-1) in self.boardback) and self.boardback[y-1,x-1] == 'B'):
                    bombcount += 1     
                if (((y-1,x) in self.boardback) and self.boardback[y-1,x] == 'B'):
                    bombcount += 1 
                if (((y-1,x+1) in self.boardback) and self.boardback[y-1,x+1] == 'B'):
                    bombcount += 1 
                if (((y,x-1) in self.boardback) and self.boardback[y,x-1] == 'B'):
                    bombcount += 1 
                # if (((y,x) in self.boardback) and  self.boardback[y,x] == 'B'):
                #     bombcount += 1 
                if (((y,x+1) in self.boardback) and self.boardback[y,x+1] == 'B'):
                    bombcount += 1 
                if (((y+1,x-1) in self.boardback) and self.boardback[y+1,x-1] == 'B'):
                    bombcount += 1 
                if (((y+1,x) in self.boardback) and self.boardback[y+1,x] == 'B'):
                    bombcount += 1 
                if (((y+1,x+1) in self.boardback) and self.boardback[y+1,x+1] == 'B'):
                    bombcount += 1   
                self.boardback[y,x] = bombcount
                continue

    # recursive reveal function, called when clicking on a square that is not a bomb
    # will reveal all 0s adjacent to the clicked square, and all numbered squares
    #   adjacent to any 0 squares
    def reveal(self,y,x):
        #recursion base case, stop when it reaches a revealed square
        if (self.boardfront[y,x] != 'U'):
            return
        #any square adjacent to a zero is either a 0 or a number
        # show the number, recurse on the 0s
        if (self.boardfront[y,x] == 'U'):
            if (self.boardback[y,x] == 0):
                self.setfront(y,x,'E')
                if ((y-1,x-1) in self.boardback):
                    self.reveal(y-1,x-1)
                if ((y-1,x) in self.boardback):
                    self.reveal(y-1,x)
                if ((y-1,x+1) in self.boardback):
                    self.reveal(y-1,x+1)
                if ((y,x-1) in self.boardback):
                    self.reveal(y,x-1)
                # if ((y,x) in self.boardback):
                #     self.reveal(y,x)
                if ((y,x+1) in self.boardback):
                    self.reveal(y,x+1)
                if ((y+1,x-1) in self.boardback):
                    self.reveal(y+1,x-1)
                if ((y+1,x) in self.boardback):
                    self.reveal(y+1,x)
                if ((y+1,x+1) in self.boardback):
                    self.reveal(y+1,x+1)
            if (self.boardback[y,x] in range(1,9)):
                self.setfront(y,x,self.boardback[y,x])
        
    def clicked(self, y, x, rightclick):
        print("clicked " + str(y) + ", " + str(x) + " " + str(rightclick))
        print(self.boardback[y,x])

        if (self.boardfront[y,x] == 'E'):
            return

        if (rightclick):
            #flag and unflag the rightclicked square
            if (self.boardfront[y,x] == 'F'):
                self.setfront(y,x,'U')
                
            else:
                self.setfront(y,x,'F')
            return

        #unclicked buttons
        if (self.boardfront[y,x] == 'U'):
            if (self.boardback[y,x] == 0):
                self.reveal(y,x)
                self.debugprint()
                return

            if (self.boardback[y,x] in range(0,9)):
                self.setfront(y,x,self.boardback[y,x])
                return

            if (self.boardback[y,x] == 'B'):
                # TODO: lose game code here (clicked bomb, replace all unflagged unclicked bombs with bombs)
                # until then just put a clicked bomb
                self.setfront(y,x,'C')
                return

        #clicked buttons (quick clearing by clicking numbers w/ flagged spaces adjacent)
        # TODO    
        

    def getboardback(self):
        return self.boardback

    def getboardfront(self):
        return self.boardfront

    def getchanges(self):
        returnval = self.changes
        self.changes = dict()
        print(returnval)
        return returnval

    def debugprint(self):
        print("Boardback:")
        for y in range(0,self.sizey):
            print("[", end="")
            for x in range(0,self.sizex):
                if (x!=self.sizex-1):
                    print(self.boardback[y,x], end=", ")
                else:
                    print(self.boardback[y,x], end="")
            print("]")

        print("Boardfront:")
        for y in range(0,self.sizey):
            print("[", end="")
            for x in range(0,self.sizex):
                if (x!=self.sizex-1):
                    print(self.boardfront[y,x], end=", ")
                else:
                    print(self.boardfront[y,x], end="")
            print("]")
