import random

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
#   ?       = question marked

random.seed(12345)

class game():
    buttons = {}
    boardback = ""
    boardfront = ""
    bombs = ""
    bombcount = ""
    sizex = ""
    sizey = ""

    def __init__(self):
        buttons = {}
        sizex = 0
        sizey = 0

    #perhaps add a reference to the gridlayout, and generate the board here
    # requires a bit more knowledge of layouts
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

        self.boardback = [['X']*self.sizex for i in range(self.sizey)]
        self.boardback = [['U']*self.sizex for i in range(self.sizey)]
        # for y in range(0,self.sizey):
        #     for x in range(0,self.sizex):
        #         print(str(x) + " " + str(y))
        #         self.boardback[y][x] = 'E'
        #         self.boardfront[y][x] = ' '

        bombs = random.sample(range(0,(self.sizex*self.sizey)), self.bombcount)

        for i in bombs:
            bombx = i % self.sizex
            bomby = i % self.sizey
            self.boardback[bomby][bombx] = 'B'
        
    def generatecustomgame(self, height, width, percentbombs):
        self.sizex = width
        self.sizey = height
        print(random.sample(range(1,100), 5))

    def calculatebackend(self):
        for y in range(0,self.sizey):
            for x in range(0,self.sizex):
                if (self.boardback[y][x] == 'B'):
                    continue

                bombcount = 0

                #corners: (0,0)(0,sizex-1)(sizey-1,0)(sizey-1,sizex-1)

                #top left corner
                if (y==0) and (x==0):
                    if (self.boardback[y][x+1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y+1][x] == 'B'):
                        bombcount += 1
                    if (self.boardback[y+1][x+1] == 'B'):
                        bombcount += 1
                    self.boardback[y][x] = bombcount
                    continue

                #top right corner
                if (y==0) and (x==self.sizex-1):
                    if (self.boardback[y][x-1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y+1][x] == 'B'):
                        bombcount += 1
                    if (self.boardback[y+1][x-1] == 'B'):
                        bombcount += 1
                    self.boardback[y][x] = bombcount
                    continue

                #bottom left corner
                if (y==self.sizey-1) and (x==0):
                    if (self.boardback[y-1][x] == 'B'):
                        bombcount += 1
                    if (self.boardback[y-1][x+1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y][x+1] == 'B'):
                        bombcount += 1
                    self.boardback[y][x] = bombcount
                    continue
                    
                #bottom right corner
                if (y==self.sizey-1) and (x==self.sizex-1):
                    if (self.boardback[y-1][x] == 'B'):
                        bombcount += 1
                    if (self.boardback[y-1][x-1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y][x-1] == 'B'):
                        bombcount += 1
                    self.boardback[y][x] = bombcount
                    continue

                #edge cases for borders (corners excluded):
                #all x for y=0
                #all x for y=sizey - 1
                #all y for x=0
                #all y for y = sizex - 1

                #top border
                if (y==0):
                    if (self.boardback[y][x-1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y+1][x-1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y+1][x] == 'B'):
                        bombcount += 1
                    if (self.boardback[y+1][x+1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y][x+1] == 'B'):
                        bombcount += 1
                    self.boardback[y][x] = bombcount
                    continue
                
                #bottom border
                if (y==self.sizey-1):
                    if (self.boardback[y][x-1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y-1][x-1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y-1][x] == 'B'):
                        bombcount += 1
                    if (self.boardback[y-1][x+1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y][x+1] == 'B'):
                        bombcount += 1
                    self.boardback[y][x] = bombcount
                    continue

                #left border
                if (x==0):
                    if (self.boardback[y-1][x] == 'B'):
                        bombcount += 1
                    if (self.boardback[y-1][x+1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y][x+1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y+1][x+1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y+1][x] == 'B'):
                        bombcount += 1
                    self.boardback[y][x] = bombcount
                    continue

                #right border
                if (x==self.sizex-1):
                    if (self.boardback[y-1][x] == 'B'):
                        bombcount += 1
                    if (self.boardback[y-1][x-1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y][x-1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y+1][x-1] == 'B'):
                        bombcount += 1
                    if (self.boardback[y+1][x] == 'B'):
                        bombcount += 1
                    self.boardback[y][x] = bombcount
                    continue

                #non edge case
                if (self.boardback[y-1][x-1] == 'B'):
                    bombcount += 1     
                if (self.boardback[y-1][x] == 'B'):
                    bombcount += 1 
                if (self.boardback[y-1][x+1] == 'B'):
                    bombcount += 1 
                if (self.boardback[y][x-1] == 'B'):
                    bombcount += 1 
                # if (self.boardback[y][x] == 'B'):
                #     bombcount += 1 
                if (self.boardback[y][x+1] == 'B'):
                    bombcount += 1 
                if (self.boardback[y+1][x-1] == 'B'):
                    bombcount += 1 
                if (self.boardback[y+1][x] == 'B'):
                    bombcount += 1 
                if (self.boardback[y+1][x+1] == 'B'):
                    bombcount += 1   
                self.boardback[y][x] = bombcount
                continue
        print(self.boardback)


    def addbutton(self, y, x, button):
        self.buttons[y,x] = button

    def clicked(self, y, x, rightclick):
        print("clicked " + str(y) + ", " + str(x) + str(rightclick))
