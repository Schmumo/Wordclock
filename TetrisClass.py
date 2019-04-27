# -*- coding: utf-8 -*-
from neopixel import *

###Farben für die Blöcke, GRB###

#Originalfarben, volle Power
#COLOR_Q = Color(200,255,0) #Gelb
#COLOR_J = Color(50,0,255) #Blau
#COLOR_L = Color(50,255,0) #Orange
#COLOR_Z = Color(0,255,0) #Rot
#COLOR_S = Color(255,0,0) #Grün
#COLOR_T = Color(0,75,255) #Lila
#COLOR_I = Color(255,0,255) #Cyan

#Rot-Gelb in Abstufungen
COLOR_Q = Color(0,255,0)
COLOR_J = Color(10,255,0)
COLOR_L = Color(20,255,0)
COLOR_Z = Color(40,255,0) 
COLOR_S = Color(95,255,0) 
COLOR_T = Color(130,255,0)
COLOR_I = Color(160,255,0)

#Rot, Orange und Gelb
#COLOR_Q = Color(0,255,0)
#COLOR_J = Color(0,255,0)
#COLOR_L = Color(50,255,0)
#COLOR_Z = Color(50,255,0) 
#COLOR_S = Color(50,255,0) 
#COLOR_T = Color(160,255,0)
#COLOR_I = Color(160,255,0)

class Tetris:

    allFields = []
    allColors = []
    removedRows = []
    score = 0
    matrix = [[12,11,10,9,8,7,6,5,4,3,2],[13,14,15,16,17,18,19,20,21,22,23],[34,33,32,31,30,29,28,27,26,25,24],[35,36,37,38,39,40,41,42,43,44,45],
          [56,55,54,53,52,51,50,49,48,47,46],[57,58,59,60,61,62,63,64,65,66,67],[78,77,76,75,74,73,72,71,70,69,68],[79,80,81,82,83,84,85,86,87,88,89],
          [100,99,98,97,96,95,94,93,92,91,90],[101,102,103,104,105,106,107,108,109,110,111]]

    
    def __init__(self):
        self.platzhalter = 0

    def moveDown(self):
        for i in range (len(self.y)):
            self.x[i] = self.x[i] + 1
        return self.isMovable()

    def moveRight(self):
        for i in range (len(self.y)):                
            if ((self.y[i] == 10) or (Tetris.matrix[self.x[i]][self.y[i]+1] in Tetris.allFields)):
                return True
        for i in range (len(self.y)):                
            self.y[i] = self.y[i] + 1
        return self.isMovable()

    def moveLeft(self):
        for i in range (len(self.y)):                
            if ((self.y[i] == 0) or (Tetris.matrix[self.x[i]][self.y[i]-1] in Tetris.allFields)):
                return True
        for i in range (len(self.y)):                
            self.y[i] = self.y[i] - 1
        return self.isMovable()

    def getAllFields(self):
        return Tetris.allFields

    def getAllColors(self):
        return Tetris.allColors

    def delete(self):
        Tetris.allFields = []
        Tetris.allColors = []
        Tetris.score = 0

    def addToField(self):
        for i in range (len(self.y)):                 
           Tetris.allFields.append(Tetris.matrix[self.x[i]][self.y[i]])
           Tetris.allColors.append(self.getColor())

    def getBlock(self):
        currentBlock = []
        for i in range (len(self.y)):                 
           currentBlock.append(Tetris.matrix[self.x[i]][self.y[i]])
        return currentBlock

    def isMovable(self):
        for i in range (len(self.y)):
            if ((self.x[i] == 9) or (Tetris.matrix[self.x[i]+1][self.y[i]] in Tetris.allFields)):
                return False
        return True

    def checkAndRemoveFullRows(self):
        bonus = 0
        Tetris.removedRows = []
        removedAnything = False
        for i in range (len(Tetris.matrix)):
            if set(Tetris.matrix[i]).issubset(Tetris.allFields):
                removedAnything = True
                Tetris.removedRows.append(i)
                Tetris.score = Tetris.score + 1 + bonus
                bonus = bonus + 1
                for j in range (len(Tetris.matrix[i])):
                    index = Tetris.allFields.index(Tetris.matrix[i][j])
                    del Tetris.allFields[index]
                    del Tetris.allColors[index]
        return removedAnything

    def fillEmptyRows(self):
        for i in range (len(Tetris.removedRows)):
            for j in range(Tetris.removedRows[i]-1, -1, -1):
                for k in range (len(Tetris.matrix[j])):   
                    if Tetris.matrix[j][k] in Tetris.allFields:
                        index = Tetris.allFields.index(Tetris.matrix[j][k])
                        color = Tetris.allColors.pop(index)
                        del Tetris.allFields[index]
                        Tetris.allFields.append(Tetris.matrix[j+1][k])
                        Tetris.allColors.append(color)
        Tetris.removedRows = []
            

    def isLost(self):
        for i in range (len(self.y)):
            if (Tetris.matrix[self.x[i]][self.y[i]] in Tetris.allFields):
                return True
        return False

    def getScore(self):
        return Tetris.score


class QBlock(Tetris):
    def __init__(self):
        self.x = [0, 0, 1, 1]
        self.y = [4, 5, 4, 5]

    def rotateLeft(self):
        return True

    def rotateRight(self):
        return True

    def getColor(self):
        return COLOR_Q

class JBlock(Tetris):  
    def __init__(self):
        self.x = [0, 1, 1, 1]
        self.y = [4, 4, 5, 6]
        self.rotationsR = 0
        self.rotationsL = 0

    def rotateLeft(self):
        rotationLCopy = self.rotationsL
        rotationRCopy = self.rotationsR
        if self.rotationsL == 0:
            #Verschiebung
            newX = [self.x[0]+2, self.x[1]+1, self.x[2], self.x[3]-1]
            newY = [self.y[0], self.y[1]+1, self.y[2], self.y[3]-1]
            self.rotationsL = 1
            self.rotationsR = 3
        elif self.rotationsL == 1:
            #Verschiebung
            newX = [self.x[0], self.x[1]-1, self.x[2], self.x[3]+1]
            newY = [self.y[0]+2, self.y[1]+1, self.y[2], self.y[3]-1]
            self.rotationsL = 2
            self.rotationsR = 2
        elif self.rotationsL == 2:
            #Verschiebung
            newX = [self.x[0]-2, self.x[1]-1, self.x[2], self.x[3]+1]
            newY = [self.y[0], self.y[1]-1, self.y[2], self.y[3]+1]
            self.rotationsL = 3
            self.rotationsR = 1
        elif self.rotationsL == 3:
            #Verschiebung
            newX = [self.x[0], self.x[1]+1, self.x[2], self.x[3]-1]
            newY = [self.y[0]-2, self.y[1]-1, self.y[2], self.y[3]+1]
            self.rotationsL = 0
            self.rotationsR = 0
        #Wenn Rotation nicht möglich, Methode verlassen
        for i in range (len(self.y)):
            if ((newX[i] >= 10) or (newX[i] <= -1) or (newY[i] >= 11) or (newY[i] <= -1) or
                (Tetris.matrix[newX[i]][newY[i]] in Tetris.allFields)):
                self.rotationsL = rotationLCopy
                self.rotationsR = rotationRCopy
                return True
        #Wenn möglich: neues Array setzen
        self.x = newX
        self.y = newY
        return self.isMovable()

    def rotateRight(self):
        rotationRCopy = self.rotationsR
        rotationLCopy = self.rotationsL
        if self.rotationsR == 0:
            #Verschiebung
            newX = [self.x[0], self.x[1]-1, self.x[2], self.x[3]+1]
            newY = [self.y[0]+2, self.y[1]+1, self.y[2], self.y[3]-1]
            self.rotationsR = 1
            self.rotationsL = 3
        elif self.rotationsR == 1:
            #Verschiebung
            newX = [self.x[0]+2, self.x[1]+1, self.x[2], self.x[3]-1]
            newY = [self.y[0], self.y[1]+1, self.y[2], self.y[3]-1]
            self.rotationsR = 2
            self.rotationsL = 2
        elif self.rotationsR == 2:
            #Verschiebung
            newX = [self.x[0], self.x[1]+1, self.x[2], self.x[3]-1]
            newY = [self.y[0]-2, self.y[1]-1, self.y[2], self.y[3]+1]
            self.rotationsR = 3
            self.rotationsL = 1
        elif self.rotationsR == 3:
            #Verschiebung
            newX = [self.x[0]-2, self.x[1]-1, self.x[2], self.x[3]+1]
            newY = [self.y[0], self.y[1]-1, self.y[2], self.y[3]+1]
            self.rotationsR = 0
            self.rotationsL = 0
        #Wenn Rotation nicht möglich, Methode verlassen
        for i in range (len(self.y)):
            if ((newX[i] >= 10) or (newX[i] <= -1) or (newY[i] >= 11) or (newY[i] <= -1) or
                (Tetris.matrix[newX[i]][newY[i]] in Tetris.allFields)):
                self.rotationsR = rotationRCopy
                self.rotationsL = rotationLCopy
                return True
        #Wenn möglich: neues Array setzen
        self.x = newX
        self.y = newY
        return self.isMovable()

    def getColor(self):
        return COLOR_J

class LBlock(Tetris):  
    def __init__(self):
        self.x = [1, 1, 0, 1]
        self.y = [4, 5, 6, 6]
        self.rotationsL = 0
        self.rotationsR = 0

    def rotateLeft(self):
        rotationLCopy = self.rotationsL
        rotationRCopy = self.rotationsR
        if self.rotationsL == 0:
            #Verschiebung
            newX = [self.x[0]+1, self.x[1], self.x[2], self.x[3]-1]
            newY = [self.y[0]+1, self.y[1], self.y[2]-2, self.y[3]-1]
            self.rotationsL = 1
            self.rotationsR = 3
        elif self.rotationsL == 1:
            #Verschiebung
            newX = [self.x[0]-1, self.x[1], self.x[2]+2, self.x[3]+1]
            newY = [self.y[0]+1, self.y[1], self.y[2], self.y[3]-1]
            self.rotationsL = 2
            self.rotationsR = 2
        elif self.rotationsL == 2:
            #Verschiebung
            newX = [self.x[0]-1, self.x[1], self.x[2], self.x[3]+1]
            newY = [self.y[0]-1, self.y[1], self.y[2]+2, self.y[3]+1]
            self.rotationsL = 3
            self.rotationsR = 1
        elif self.rotationsL == 3:
            #Verschiebung
            newX = [self.x[0]+1, self.x[1], self.x[2]-2, self.x[3]-1]
            newY = [self.y[0]-1, self.y[1], self.y[2], self.y[3]+1]
            self.rotationsL = 0
            self.rotationsR = 0
        #Wenn Rotation nicht möglich, Methode verlassen
        for i in range (len(self.y)):
            if ((newX[i] >= 10) or (newX[i] <= -1) or (newY[i] >= 11) or (newY[i] <= -1) or
                (Tetris.matrix[newX[i]][newY[i]] in Tetris.allFields)):
                self.rotationsL = rotationLCopy
                self.rotationsR = rotationRCopy
                return True
        #Wenn möglich: neues Array setzen
        self.x = newX
        self.y = newY
        return self.isMovable()

    def rotateRight(self):
        rotationRCopy = self.rotationsR
        rotationLCopy = self.rotationsL
        if self.rotationsR == 0:
            #Verschiebung
            newX = [self.x[0]-1, self.x[1], self.x[2]+2, self.x[3]+1]
            newY = [self.y[0]+1, self.y[1], self.y[2], self.y[3]-1]
            self.rotationsR = 1
            self.rotationsL = 3
        elif self.rotationsR == 1:
            #Verschiebung
            newX = [self.x[0]+1, self.x[1], self.x[2], self.x[3]-1]
            newY = [self.y[0]+1, self.y[1], self.y[2]-2, self.y[3]-1]
            self.rotationsR = 2
            self.rotationsL = 2
        elif self.rotationsR == 2:
            #Verschiebung
            newX = [self.x[0]+1, self.x[1], self.x[2]-2, self.x[3]-1]
            newY = [self.y[0]-1, self.y[1], self.y[2], self.y[3]+1]
            self.rotationsR = 3
            self.rotationsL = 1
        elif self.rotationsR == 3:
            #Verschiebung
            newX = [self.x[0]-1, self.x[1], self.x[2], self.x[3]+1]
            newY = [self.y[0]-1, self.y[1], self.y[2]+2, self.y[3]+1]
            self.rotationsR = 0
            self.rotationsL = 0
        #Wenn Rotation nicht möglich, Methode verlassen
        for i in range (len(self.y)):
            if ((newX[i] >= 10) or (newX[i] <= -1) or (newY[i] >= 11) or (newY[i] <= -1) or
                (Tetris.matrix[newX[i]][newY[i]] in Tetris.allFields)):
                self.rotationsR = rotationRCopy
                self.rotationsL = rotationLCopy
                return True
        #Wenn möglich: neues Array setzen
        self.x = newX
        self.y = newY
        return self.isMovable()

    def getColor(self):
        return COLOR_L

    
class ZBlock(Tetris): 
    def __init__(self):
        self.x = [0, 0, 1, 1]
        self.y = [4, 5, 5, 6]
        self.rotations = 0

    def rotateLeft(self):
        return self.rotateRight()

    def rotateRight(self):
        rotationCopy = self.rotations
        if self.rotations == 0:
            #Verschiebung
            newX = [self.x[0]-1, self.x[1], self.x[2]-1, self.x[3]]
            newY = [self.y[0]+1, self.y[1], self.y[2]-1, self.y[3]-2]
            self.rotations = 1
        elif self.rotations == 1:
            #Verschiebung
            newX = [self.x[0]+1, self.x[1], self.x[2]+1, self.x[3]]
            newY = [self.y[0]-1, self.y[1], self.y[2]+1, self.y[3]+2]
            self.rotations = 0
        #Wenn Rotation nicht möglich, Methode verlassen
        for i in range (len(self.y)):
            if ((newX[i] >= 10) or (newX[i] <= -1) or (newY[i] >= 11) or (newY[i] <= -1) or
                (Tetris.matrix[newX[i]][newY[i]] in Tetris.allFields)):
                self.rotations = rotationCopy
                return True
        #Wenn möglich: neues Array setzen
        self.x = newX
        self.y = newY
        return self.isMovable()

    def getColor(self):
        return COLOR_Z

class SBlock(Tetris): 
    def __init__(self):
        self.x = [1, 0, 1, 0]
        self.y = [4, 5, 5, 6]
        self.rotations = 0

    def rotateLeft(self):
        return self.rotateRight()

    def rotateRight(self):
        rotationCopy = self.rotations
        if self.rotations == 0:
            #Verschiebung
            newX = [self.x[0]-2, self.x[1], self.x[2]-1, self.x[3]+1]
            newY = [self.y[0], self.y[1], self.y[2]-1, self.y[3]-1]
            self.rotations = 1
        elif self.rotations == 1:
            #Verschiebung
            newX = [self.x[0]+2, self.x[1], self.x[2]+1, self.x[3]-1]
            newY = [self.y[0], self.y[1], self.y[2]+1, self.y[3]+1]
            self.rotations = 0
        #Wenn Rotation nicht möglich, Methode verlassen
        for i in range (len(self.y)):
            if ((newX[i] >= 10) or (newX[i] <= -1) or (newY[i] >= 11) or (newY[i] <= -1) or
                (Tetris.matrix[newX[i]][newY[i]] in Tetris.allFields)):
                self.rotations = rotationCopy
                return True
        #Wenn möglich: neues Array setzen
        self.x = newX
        self.y = newY
        return self.isMovable()
		
    def getColor(self):
        return COLOR_S
    
class TBlock(Tetris):   
    def __init__(self):
        self.x = [1, 0, 1, 1]
        self.y = [4, 5, 5, 6]
        self.rotationsR = 0
        self.rotationsL = 0

    def rotateRight(self):
        rotationRCopy = self.rotationsR
        rotationLCopy = self.rotationsL
        if self.rotationsR == 0:
            #Verschiebung
            newX = [self.x[0]-1, self.x[1]+1, self.x[2], self.x[3]+1]
            newY = [self.y[0]+1, self.y[1]+1, self.y[2], self.y[3]-1]
            self.rotationsR = 1
            self.rotationsL = 3
        elif self.rotationsR == 1:
            #Verschiebung
            newX = [self.x[0]+1, self.x[1]+1, self.x[2], self.x[3]-1]
            newY = [self.y[0]+1, self.y[1]-1, self.y[2], self.y[3]-1]
            self.rotationsR = 2
            self.rotationsL = 2
        elif self.rotationsR == 2:
            #Verschiebung
            newX = [self.x[0]+1, self.x[1]-1, self.x[2], self.x[3]-1]
            newY = [self.y[0]-1, self.y[1]-1, self.y[2], self.y[3]+1]
            self.rotationsR = 3
            self.rotationsL = 1
        elif self.rotationsR == 3:
            #Verschiebung
            newX = [self.x[0]-1, self.x[1]-1, self.x[2], self.x[3]+1]
            newY = [self.y[0]-1, self.y[1]+1, self.y[2], self.y[3]+1]
            self.rotationsR = 0
            self.rotationsL = 0
        #Wenn Rotation nicht möglich, Methode verlassen
        for i in range (len(self.y)):
            if ((newX[i] >= 10) or (newX[i] <= -1) or (newY[i] >= 11) or (newY[i] <= -1) or
                (Tetris.matrix[newX[i]][newY[i]] in Tetris.allFields)):
                self.rotationsR = rotationRCopy
                self.rotationsL = rotationLCopy
                return True
        #Wenn möglich: neues Array setzen
        self.x = newX
        self.y = newY
        return self.isMovable()

    def rotateLeft(self):
        rotationLCopy = self.rotationsL
        rotationRCopy = self.rotationsR
        if self.rotationsL == 0:
            #Verschiebung
            newX = [self.x[0]+1, self.x[1]+1, self.x[2], self.x[3]-1]
            newY = [self.y[0]+1, self.y[1]-1, self.y[2], self.y[3]-1]
            self.rotationsL = 1
            self.rotationsR = 3
        elif self.rotationsL == 1:
            #Verschiebung
            newX = [self.x[0]-1, self.x[1]+1, self.x[2], self.x[3]+1]
            newY = [self.y[0]+1, self.y[1]+1, self.y[2], self.y[3]-1]
            self.rotationsL = 2
            self.rotationsR = 2
        elif self.rotationsL == 2:
            #Verschiebung
            newX = [self.x[0]-1, self.x[1]-1, self.x[2], self.x[3]+1]
            newY = [self.y[0]-1, self.y[1]+1, self.y[2], self.y[3]+1]
            self.rotationsL = 3
            self.rotationsR = 1
        elif self.rotationsL == 3:
            #Verschiebung
            newX = [self.x[0]+1, self.x[1]-1, self.x[2], self.x[3]-1]
            newY = [self.y[0]-1, self.y[1]-1, self.y[2], self.y[3]+1]
            self.rotationsL = 0
            self.rotationsR = 0
        #Wenn Rotation nicht möglich, Methode verlassen
        for i in range (len(self.y)):
            if ((newX[i] >= 10) or (newX[i] <= -1) or (newY[i] >= 11) or (newY[i] <= -1) or
                (Tetris.matrix[newX[i]][newY[i]] in Tetris.allFields)):
                self.rotationsL = rotationLCopy
                self.rotationsR = rotationRCopy
                return True
        #Wenn möglich: neues Array setzen
        self.x = newX
        self.y = newY
        return self.isMovable()
    
    def getColor(self):
        return COLOR_T

class IBlock(Tetris):   
    def __init__(self):
        self.x = [0, 0, 0, 0]
        self.y = [3, 4, 5, 6]
        self.rotations = 0

    def rotateLeft(self):
        return self.rotateRight()

    def rotateRight(self):
        rotationCopy = self.rotations
        if self.rotations == 0:
            #Verschiebung
            newX = [self.x[0], self.x[1]+1, self.x[2]+2, self.x[3]+3]
            newY = [self.y[0]+1, self.y[1], self.y[2]-1, self.y[3]-2]
            self.rotations = 1
        elif self.rotations == 1:
            #Verschiebung
            newX = [self.x[0], self.x[1]-1, self.x[2]-2, self.x[3]-3]
            newY = [self.y[0]-1, self.y[1], self.y[2]+1, self.y[3]+2]
            self.rotations = 0
        #Wenn Rotation nicht möglich, Methode verlassen
        for i in range (len(self.y)):
            if ((newX[i] >= 10) or (newX[i] <= -1) or (newY[i] >= 11) or (newY[i] <= -1) or
                (Tetris.matrix[newX[i]][newY[i]] in Tetris.allFields)):
                self.rotations = rotationCopy
                return True
        #Wenn möglich: neues Array setzen
        self.x = newX
        self.y = newY
        return self.isMovable()
    
    def getColor(self):
        return COLOR_I


