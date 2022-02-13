import time
import random
# TODO: créer une fonction qui récupère toutes les positions des jetons d'un joueur (peut être implémenter un tableau qui est modifié selon les positions des jetons)

class Board:
    """Core game for Othello"""
    
    def __init__(self):
        self.player1 = 1
        self.player2 = 2
        self.empty = 0
        self.turn = 0
        self.player = 1
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

    def displayScores(self):
        scores = self.getScores()
        score1 = "○: " + str(scores[0]).center(2, " ")
        score2 = "●: " + str(scores[1]).center(2, " ")
        result = (score1 + "  -  " + score2).center(32, " ")
        print(result)

    def display(self):
        self.displayScores()
        text = ""
        for row in self.board:
            for slot in row:
                if(slot == self.player1):
                    text += "_○_|"
                elif(slot == self.player2):
                    text += "_●_|"
                else:
                    text += "___|"
            text += "\n"
        print(text)

    def displayPossibilities(self, colorCheck):
        self.displayScores()
        slots = self.getAllSlotsAvailable(colorCheck)
        text = ""
        for j in range(8):
            for i in range(8):
                slot = self.board[j][i]
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

    def isDirectionValid(self, x, y, direction, colorCheck):
        directionX, directionY = direction
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
            
    def isPlayable(self, x, y, colorCheck):
        if(x < 0 or x > 7 or y < 0 or y > 7):
            return False
        currentColor = self.board[y][x]
        if(currentColor != self.empty):
            return False
        directions = self.detectAround(x,y,colorCheck)
        for direction in directions:
            if(self.isDirectionValid(x,y,direction,colorCheck)):
               return True
        return False

    def getAllSlotsAvailable(self, colorCheck):
        slots = []
        for x in range(8):
            for y in range(8):
                if(self.isPlayable(x, y, colorCheck)):
                   slots.append((x,y))
        return slots

    def playSlot(self, x, y, colorCheck):
        if(self.isPlayable(x,y,colorCheck)):
            directions = self.detectAround(x,y,colorCheck)
            self.board[y][x] = colorCheck
            for directionX, directionY in directions:
                if(self.isDirectionValid(x, y, (directionX,directionY), colorCheck)):
                    nbOfSlots = 1
                    newX = x + directionX * nbOfSlots
                    newY = y + directionY * nbOfSlots
                    newSlot = self.board[newY][newX]
                    while(newSlot != colorCheck and newSlot != self.empty):
                        self.board[newY][newX] = colorCheck
                        nbOfSlots += 1
                        newX = x + directionX * nbOfSlots
                        newY = y + directionY * nbOfSlots
                        newSlot = self.board[newY][newX]
            return True
        return False

    def playProposition(self, indexToPlay, colorCheck):
        slots = self.getAllSlotsAvailable(colorCheck)
        if(indexToPlay < 0 or indexToPlay >= len(slots)):
            return False
        x,y = slots[indexToPlay]
        return self.playSlot(x,y,colorCheck)

    def getScores(self):
        scores = [0, 0]
        for row in self.board:
            for slot in row:
                if(slot == self.player1):
                    scores[0] += 1
                elif(slot == self.player2):
                    scores[1] += 1
        return scores

def inputInArray(array, question = "Please, choose.", error = "Votre entrée n'est pas valide."):
    x = ""
    if(len(array) == 0):
        return x
    arrayType = type(array[0])
    while(not(x in array)):
        print(question)
        x = input()
        if(arrayType == type(0)):
            try:
                x = int(x, 10)
            except(ValueError):
                print("Please write a NUMBER !")
        if(not(x in array)):
            print(error)
    return x

def choosePlayer(numPlayer):
    human = ["y", "Y", "Yes", "Oui", "oui", "o"]
    ia = ["n", "N", "No", "Non", "Non"]
    random = ["r", "R", "random", "Random", "rand", "Rand"]
    p = inputInArray(human + ia + random, "Is the player" + str(numPlayer) + " a human ?")
    if(p in human):
        p = 0
    elif(p in ia):
        p = 1
    else:
        p = 2
    return p

def choosePlayers(othello):
    p1 = (othello.player1, choosePlayer(1))
    p2 = (othello.player2, choosePlayer(2))
    return [p1, p2]

def doTurn(othello, player, times):
    color, nbType = player
    print("It's the turn to player " + str(color) + " !")
    othello.displayPossibilities(color)
    slots = othello.getAllSlotsAvailable(color)
    if(len(slots) == 0):
        return False
    # TODO : Put a switch
    if(nbType == 0): # human        
        choices = [i for i in range(len(slots))]
        start = time.time()
        choice = inputInArray(choices, "Choose a number between 0 and " + str(len(slots) - 1) + ".", "the number isn't between 0 and " + str(len(slots) - 1) + " !")
        end = time.time()
        times[color - 1] += end - start
        x,y = slots[choice]
        othello.playSlot(x,y,color)
    elif(nbType == 1): # IA
        print("IA NOT IMPLEMENTED YET !")
        start = time.time()
        end = time.time()
        times[color - 1] += end - start
    elif(nbType == 2):
        start = time.time()
        slot = random.choice(slots)
        x,y = slot
        othello.playSlot(x,y,color)
        end = time.time()
        times[color - 1] += end - start
    return True

        
def runOthello():
    othello = Board()
    players = choosePlayers(othello)
    played1 = True
    played2 = True
    turns = 0
    times = [0,0]
    while(played1 and played2):
        turns += 1
        played1 = doTurn(othello, players[0], times)
        if(not(played1)):
            print("The player1 can't play !")
        played2 = doTurn(othello, players[1], times)
        if(not(played2)):
            print("The player2 can't play !")
    scores = othello.getScores()
    if(scores[0] > scores[1]):
        print("The player" + str(othello.player1) + " wins the game with a score of " + str(scores[0]) + " !")
    else:
        print("The player" + str(othello.player2) + " wins the game with a score of " + str(scores[1]) + " !")
    print("The average time for player1 is : " + str(times[0] / turns) + " s !")
    print("The average time for player2 is : " + str(times[1] / turns) + " s !")
    

runOthello()       

# Calcul of time execution

##othello.random(0.3,0.5)
##start = time.time()
##for i in range(1000):
##    othello.getAllSlotsAvailable(2)
##end = time.time()
##othello.displayPossibilities(2)
##print("--- %s seconds ---" % (end - start))
