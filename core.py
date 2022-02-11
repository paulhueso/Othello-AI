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

    def display(self):
        for row in self.board:
            for text in row:
                print(text, end=" | ")
            print()

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
