import time
import random
import board
import ia
# TODO: créer une fonction qui récupère toutes les positions des jetons d'un joueur (peut être implémenter un tableau qui est modifié selon les positions des jetons)

class Core:
    """Core game for Othello"""
    
    def __init__(self):
        self.turn = 0
        self.player = 1
        self.board = board.Board()
        self.currentBoard = [[self.board.empty for i in range(8)] for j in range(8)]
        self.currentBoard[3][3] = self.board.player1
        self.currentBoard[4][3] = self.board.player2
        self.currentBoard[3][4] = self.board.player2
        self.currentBoard[4][4] = self.board.player1
        self.numberOfMoves = 0

    def inputInArray(self, array, question = "Please, choose.", error = "Votre entrée n'est pas valide."):
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

    def choosePlayer(self, numPlayer):
        human = ["h", "H", "human", "Human"]
        ia = ["i","I","ia","IA","AI","ai","a"]
        random = ["r", "R", "random", "Random", "rand", "Rand"]
        p = self.inputInArray(human + ia + random, "Is the player" + str(numPlayer) + " Human, an AI or Random ?")
        if(p in human):
            p = 0
        elif(p in ia):
            p = 1
        else:
            p = 2
        return p

    def choosePlayers(self):
        p1 = (self.board.player1, self.choosePlayer(1))
        if(p1[1] == 1):
            depth = input("\nAI depth: ")
            strategy = input("\nStrategy: \n1) Absolute\n2) Positional\n3) Mobility\n4) Mixte (Recommended)\nChoice: ")
            self.ia1 = ia.IA(self.board.player1, self.board.player2, int(depth), int(strategy))
        p2 = (self.board.player2, self.choosePlayer(2))
        if(p2[1] == 1):
            depth = input("AI depth: ")
            strategy = input("\nStrategy: \n1) Absolute\n2) Positional\n3) Mobility\n4) Mixte (Recommended)\nChoice: ")
            self.ia2 = ia.IA(self.board.player2, self.board.player1, int(depth), int(strategy))
        return [p1, p2]

    def doTurn(self, player, times):
        color, nbType = player
        print("Player " + str(color) + ": ")
        self.board.displayPossibilities(self.currentBoard, color)
        slots = self.board.getAllSlotsAvailable(self.currentBoard, color)
        if(len(slots) == 0):
            return False
        # TODO : Put a switch
        if(nbType == 0): # human        
            choices = [i for i in range(len(slots))]
            start = time.time()
            choice = self.inputInArray(choices, "Choose a number between 0 and " + str(len(slots) - 1) + ".", "the number isn't between 0 and " + str(len(slots) - 1) + " !")
            end = time.time()
            times[color - 1] += end - start
            x,y = slots[choice]
            self.board.playSlot(self.currentBoard, x, y, color)
        elif(nbType == 1): # IA
            if(color == self.board.player1):
                start = time.time()
                bestMove = self.ia1.startMinMaxAlphaBeta(self.currentBoard, self.numberOfMoves)
                end = time.time()
                times[0] += end - start
            else:
                start = time.time()
                bestMove = self.ia2.startMinMaxAlphaBeta(self.currentBoard, self.numberOfMoves)
                end = time.time()
                times[1] += end - start
            self.board.playProposition(self.currentBoard, bestMove[0], color)
        elif(nbType == 2): # random
            start = time.time()
            slot = random.choice(slots)
            x,y = slot
            self.board.playSlot(self.currentBoard, x, y, color)
            end = time.time()
            times[color - 1] += end - start
        self.numberOfMoves += 1
        return True

    def saveScores(self, result1, result2):
        lines = []
        print("Saving scores...", end=" ")
        try:
            with open("scores.txt", "r") as f:
                lines = f.readlines()
        except(FileNotFoundError):
            print("The file 'scores.txt' couldn't be found !")
        with open("scores.txt","w") as f:
            found = False
            for score in lines:
                type1,type2,score1,score2 = score.split(" ")
                type1,type2,score1,score2 = int(type1),int(type2),int(score1),int(score2)
                if(type1 == result1[0] and type2 == result2[0]):
                    score1 += result1[1]
                    score2 += result2[1]
                    found = True
                f.write(str(type1) + " " + str(type2) + " " + str(score1) + " " + str(score2) + "\n")
            if(not(found)):
                f.write(str(result1[0]) + " " + str(result2[0]) + " " + str(result1[1]) + " " + str(result2[1]) + "\n")
        print("Done !")
            
    def runOthello(self):
        players = self.choosePlayers()
        played1 = True
        played2 = True
        turns = 0
        times = [0,0]
        while(played1 or played2):
            turns += 1
            played1 = self.doTurn(players[0], times)
            if(not(played1)):
                print("Player1 can't play !")
            played2 = self.doTurn(players[1], times)
            if(not(played2)):
                print("Player2 can't play !")
        scores = self.board.getScores(self.currentBoard)
        if(scores[0] > scores[1]):
            print("Player" + str(self.board.player1) + " wins the game with a score of " + str(scores[0]) + " !")
            self.saveScores((players[0][1], 1),(players[1][1], 0))
        else:
            print("The player" + str(self.board.player2) + " wins the game with a score of " + str(scores[1]) + " !")
            self.saveScores((players[0][1], 0),(players[1][1], 1))
        print("The average time for player1 is : " + str(times[0] / turns) + " s !")
        print("The average time for player2 is : " + str(times[1] / turns) + " s !")


core = Core()
core.runOthello()

# Calcul of time execution

##othello.random(0.3,0.5)
##start = time.time()
##for i in range(1000):
##    othello.getAllSlotsAvailable(2)
##end = time.time()
##othello.displayPossibilities(2)
##print("--- %s seconds ---" % (end - start))
