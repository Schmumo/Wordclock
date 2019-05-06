import random
from threading import Timer

class Ghost:

    matrix = [[12,11,10,9,8,7,6,5,4,3,2],[13,14,15,16,17,18,19,20,21,22,23],[34,33,32,31,30,29,28,27,26,25,24],[35,36,37,38,39,40,41,42,43,44,45],
          [56,55,54,53,52,51,50,49,48,47,46],[57,58,59,60,61,62,63,64,65,66,67],[78,77,76,75,74,73,72,71,70,69,68],[79,80,81,82,83,84,85,86,87,88,89],
          [100,99,98,97,96,95,94,93,92,91,90],[101,102,103,104,105,106,107,108,109,110,111]]

    allGhosts = []
    prisons = [0,1,112,113]
    finishFlag = False
    powerFlag = False


    def __init__(self, l, i):
        self.level = l
        self.identifier = i
        self.prisoned = False
        self.x = random.randint(0, 9)
        self.y = random.randint(0, 10)

    def newPosition(self):
        self.x = random.randint(0, 9)
        self.y = random.randint(0, 10)

    def getPosition(self):
        if self.prisoned == False:
            return Ghost.matrix[self.x][self.y]
        else:
            return Ghost.prisons[self.identifier]

    def getOtherPositions(self):
        otherPositions = []
        for i in range(len(Ghost.allGhosts)):
            if Ghost.allGhosts[i].identifier != self.identifier:
                otherPositions.append(Ghost.allGhosts[i].getPosition())
        return otherPositions

    def getAllPositions(self):
        allPositions = []
        for i in range(len(Ghost.allGhosts)):
            allPositions.append(Ghost.allGhosts[i].getPosition())
        return allPositions

    def getPrisoned(self):
        self.prisoned = True
        Timer(3, self.prisonOver).start()

    def prisonOver(self):
        self.prisoned = False

    def movement(self, xPacman, yPacman):
        if self.prisoned == False and self.getPosition() != Ghost.prisons[self.identifier]:
            if random.randint(1,2*self.level) == self.level:
            #if random.randint(1,1) == 1:
            #if random.randint(1,1) == 2:
                self.moveRandom()
                return
            deltaX = xPacman - self.x
            deltaY = yPacman - self.y
            if abs(deltaX) >= abs(deltaY):
                if xPacman > self.x and Ghost.powerFlag == False:
                    self.moveDown()
                else:
                    self.moveUp()
            else:
                if yPacman > self.y and Ghost.powerFlag == False:
                    self.moveRight()
                else:
                    self.moveLeft()
        elif self.prisoned == False:
            if self.identifier == 0:
                self.x = 0
                self.y = 0
            elif self.identifier == 1:
                self.x = 0
                self.y = 10
            elif self.identifier == 2:
                self.x = 9
                self.y = 10
            elif self.identifier == 3:
                self.x = 9
                self.y = 0

    def moveRandom(self):
        i = random.randint(1,4)
        if i == 1: self.moveUp()
        elif i == 2: self.moveDown()
        elif i == 3: self.moveRight()
        elif i == 4: self.moveLeft()

    def moveUp(self):
        if self.x == 0 or Ghost.matrix[self.x - 1][self.y] in self.getOtherPositions():
            self.moveRandom()
            return
        self.x = max(self.x - 1, 0)

    def moveDown(self):
        if self.x == 9 or Ghost.matrix[self.x + 1][self.y] in self.getOtherPositions():
            self.moveRandom()
            return
        self.x = min(self.x + 1, 9)

    def moveRight(self):
        if self.y == 10 or Ghost.matrix[self.x][self.y + 1] in self.getOtherPositions():
            self.moveRandom()
            return
        self.y = min(self.y + 1, 10)

    def moveLeft(self):
        if self.y == 0 or Ghost.matrix[self.x][self.y - 1] in self.getOtherPositions():
            self.moveRandom()
            return
        self.y = max(self.y - 1, 0)
