import time
import random

class Board:
    """Core game for Othello"""
    
    def __init__(self):
        self.player1 = 1
        self.player2 = 2
        self.empty = 0
        self.board = [[self.empty for i in range(8)] for j in range(8)]
        self.board[3][3] = self.player1
        self.board[4][3] = self.player2
        self.board[3][4] = self.player2
        self.board[4][4] = self.player1
        self.board[4][4] = self.player1

    def random(self, propPlayer1, propPlayer2):
        for x in range(8):
            for y in range(8):
                nb = random.random()
                if(nb < propPlayer1):
                    self.board[y][x] = self.player1
                elif(nb < propPlayer2):
                    self.board[y][x] = self.player2
                else:
                    self.board[x][y] = self.empty

    def display(self):
        text = ""
        for row in self.board:
            for slot in row:
                if(slot == self.player1):
                    text += "○|"
                elif(slot == self.player2):
                    text += "●|"
                else:
                    text += "_|"
            text += "\n"
        print(text)

    def displayPossibilities(self, colorCheck):
        slots = self.getAllSlotsAvailable(colorCheck)
        text = ""
        for j in range(8):
            for i in range(8):
                slot = self.board[j][i]
                if((i,j) in slots):
                    text += str(slots.index((i,j))) + "|"
                elif(slot == self.player1):
                    text += "○|"
                elif(slot == self.player2):
                    text += "●|"
                else:
                    text += "_|"
            text += "\n"
        print(text)

    def detectAround(self, x ,y ,colorCheck):
        directions = []
        for j in range(-1, 2):
            newY = y + j
            if(newY >= 0 and newY <= 7):
                for i in range(-1, 2):
                    newX = x + i
                    if(newX >= 0 and newX <= 7):
                        otherColor = self.board[newY][newX]
                        if(otherColor != self.empty and colorCheck != otherColor):
                            directions.append((i,j))
        return directions
               
    def isPlayable(self, x, y, colorCheck):
        if(x < 0 or x > 7 or y < 0 or y > 7):
            return False
        currentColor = self.board[y][x]
        if(currentColor != self.empty):
            return False
        directions = self.detectAround(x,y,colorCheck)
        for directionX, directionY in directions:
            otherColor = self.board[y + directionY][x + directionX]
            nbOfSlot = 2
            isValid = True
            keepContinue = True
            while(keepContinue):
                newX = x + directionX * nbOfSlot
                newY = y + directionY * nbOfSlot
                if(newY < 0 or newY > 7 or newX < 0 or newX > 7):
                    keepContinue = False
                    isValid = False
                else:
                    newColor = self.board[newY][newX]
                    if(newColor == otherColor):
                        nbOfSlot += 1
                    elif (newColor == self.empty):
                        keepContinue = False
                        isValid = False
                    else:
                        keepContinue = False
            if(isValid):
                return True
        return False

    def getAllSlotsAvailable(self, colorCheck):
        slots = []
        for x in range(8):
            for y in range(8):
                if(self.isPlayable(x, y, colorCheck)):
                   slots.append((x,y))
        return slots

othello = Board()

# Calcul of time execution

##othello.random(0.3,0.5)
##start = time.time()
##for i in range(1000):
##    othello.getAllSlotsAvailable(2)
##end = time.time()
##othello.displayPossibilities(2)
##print("--- %s seconds ---" % (end - start))
