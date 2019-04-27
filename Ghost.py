import random

class Ghost:

    matrix = [[12,11,10,9,8,7,6,5,4,3,2],[13,14,15,16,17,18,19,20,21,22,23],[34,33,32,31,30,29,28,27,26,25,24],[35,36,37,38,39,40,41,42,43,44,45],
          [56,55,54,53,52,51,50,49,48,47,46],[57,58,59,60,61,62,63,64,65,66,67],[78,77,76,75,74,73,72,71,70,69,68],[79,80,81,82,83,84,85,86,87,88,89],
          [100,99,98,97,96,95,94,93,92,91,90],[101,102,103,104,105,106,107,108,109,110,111]]


    def __init__(self, l):
        self.level = l
        self.x = random.randint(0, 9)
        self.y = random.randint(0, 10)

    def getPosition(self):
        return Ghost.matrix[self.x][self.y]

    def movement(self, xPacman, yPacman):
        deltaX = xPacman - self.x
        deltaY = yPacman - self.y
        if deltaX < deltaY:
            if xPacman > self.x:
                self.moveDown()
            else:
                self.moveUp()
        else:
            if yPacman > self.y:
                self.moveRight()
            else:
                self.moveLeft()

    def moveUp(self):
        self.x = max(self.x - 1, 0)

    def moveDown(self):
        self.x = min(self.x + 1, 9)

    def moveRight(self):
        self.y = min(self.y + 1, 10)

    def moveLeft(self):
        self.y = max(self.y - 1, 0)