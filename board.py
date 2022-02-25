import random

class Board:

    def __init__(self):
        self.player1 = 1
        self.player2 = 2
        self.empty = 0

    def generateStart(self):
        """Generate the board with initial positions
        return the board [8][8]."""
        currentBoard = [[self.empty for i in range(8)] for j in range(8)]
        currentBoard[3][3] = self.player1
        currentBoard[4][3] = self.player2
        currentBoard[3][4] = self.player2
        currentBoard[4][4] = self.player1
        return currentBoard


    def random(self, board, propPlayer1, propPlayer2):
        """Populate the board randomly for test purpose."""
        for x in range(8):
            for y in range(8):
                nb = random.random()
                if(nb < propPlayer1):
                    board[y][x] = self.player1
                elif(nb < propPlayer2):
                    board[y][x] = self.player2
                else:
                    board[x][y] = self.empty

    def displayScores(self, board):
        scores = self.getScores(board)
        score1 = "○: " + str(scores[0]).center(2, " ")
        score2 = "●: " + str(scores[1]).center(2, " ")
        result = (score1 + " -  " + score2).center(32, " ")
        print(result)

    def display(self, board):
        """Display the board."""
        self.displayScores(board)
        text = ""
        for row in board:
            for slot in row:
                if(slot == self.player1):
                    text += "_○_|"
                elif(slot == self.player2):
                    text += "_●_|"
                else:
                    text += "___|"
            text += "\n"
        print(text)

    def displayPossibilities(self, board, colorCheck):
        """Display the board with all the possibilities for the colorCheck player.
        @board : currentBoard
        @colorCheck : player who is playing
        """

        self.displayScores(board)
        slots = self.getAllSlotsAvailable(board, colorCheck)
        text = ""
        for j in range(8):
            for i in range(8):
                slot = board[j][i]
                if((i,j) in slots):
                    text += str.center(str(slots.index((i,j))), 3, "_") + "|"
                elif(slot == self.player1):
                    text += "_○_|"
                elif(slot == self.player2):
                    text += "_●_|"
                else:
                    text += "___|"
            text += "\n"
        print(text)

    def detectAround(self, board, x ,y ,colorCheck):
        directions = []
        for j in range(-1, 2):
            newY = y + j
            if(newY >= 0 and newY <= 7):
                for i in range(-1, 2):
                    newX = x + i
                    if(newX >= 0 and newX <= 7):
                        otherColor = board[newY][newX]
                        if(otherColor != self.empty and colorCheck != otherColor):
                            directions.append((i,j))
        return directions

    def isDirectionValid(self, board, x, y, direction, colorCheck):
        directionX, directionY = direction
        otherColor = board[y + directionY][x + directionX]
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
                newColor = board[newY][newX]
                if(newColor == otherColor):
                    nbOfSlot += 1
                elif (newColor == self.empty):
                    keepContinue = False
                    isValid = False
                else:
                    keepContinue = False
        if(isValid):
            return True

    def isPlayable(self, board, x, y, colorCheck):
        if(x < 0 or x > 7 or y < 0 or y > 7):
            return False
        currentColor = board[y][x]
        if(currentColor != self.empty):
            return False
        directions = self.detectAround(board, x, y, colorCheck)
        for direction in directions:
            if(self.isDirectionValid(board, x, y, direction, colorCheck)):
               return True
        return False

    def getAllSlotsAvailable(self, board, colorCheck):
        """Return all slots that are available to player for current player
        @board : current Board
        @colorCheck : current Player
        return [(x,y), ...]
        """

        slots = []
        for x in range(8):
            for y in range(8):
                if(self.isPlayable(board, x, y, colorCheck)):
                   slots.append((x,y))
        return slots

    def playSlot(self, board, x, y, colorCheck):
        """Return the board after the current player played
        @board : current Board
        @x : position x to play
        @y : position y to play
        @colorCheck : current Player
        """
        if(self.isPlayable(board, x, y, colorCheck)):
            directions = self.detectAround(board, x, y, colorCheck)
            board[y][x] = colorCheck
            for directionX, directionY in directions:
                if(self.isDirectionValid(board, x, y, (directionX,directionY), colorCheck)):
                    nbOfSlots = 1
                    newX = x + directionX * nbOfSlots
                    newY = y + directionY * nbOfSlots
                    newSlot = board[newY][newX]
                    while(newSlot != colorCheck and newSlot != self.empty):
                        board[newY][newX] = colorCheck
                        nbOfSlots += 1
                        newX = x + directionX * nbOfSlots
                        newY = y + directionY * nbOfSlots
                        newSlot = board[newY][newX]
        return board

    def playProposition(self, board, indexToPlay, colorCheck):
        slots = self.getAllSlotsAvailable(board, colorCheck)
        if(indexToPlay < 0 or indexToPlay >= len(slots)):
            return board
        x,y = slots[indexToPlay]
        return self.playSlot(board, x, y, colorCheck)

    def getScores(self, board):
        scores = [0, 0]
        for row in board:
            for slot in row:
                if(slot == self.player1):
                    scores[0] += 1
                elif(slot == self.player2):
                    scores[1] += 1
        return scores

    def isFinished(self, currentBoard):
        movesPlayer1 = self.getAllSlotsAvailable(currentBoard, 1)
        movesPlayer2 = self.getAllSlotsAvailable(currentBoard, 2)
        return (len(movesPlayer1) == 0 and len(movesPlayer2) == 0)

    def winner(self, currentBoard):
        if(not isFinished(currentBoard)):
            return 0

        scores = getScores(currentBoard)

        if(scores[0] > scores[1]):
            return 1
        elif(scores[0] < scores[1]):
            return 2 
        else:
            return -1
