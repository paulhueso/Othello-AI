from concurrent.futures.thread import _threads_queues
from copy import deepcopy
from logging import StringTemplateStyle
import os
import board
import training
import ia
import neuralNetwork
import time
import random
import multiprocessing
import matplotlib.pyplot as plt
import matplotlib.figure as figure

class Core:
    """Core game for Othello"""
    
    def __init__(self):
        self.turn = 0
        self.player = 1
        self.board = board.Board()
        self.numberOfMoves = 0
        self.currentBoard = self.board.generateStart()
    
    def inputInArray(self, array, question = "Please, choose.", error = "Your input isn't valid."):
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
        neural = ["n", "N", "Neural", "NEURAL"]
        p = self.inputInArray(human + ia + random + neural, "Is the player" + str(numPlayer) + " Human, an AI, a Neural Network or Random ?")
        if(p in human):
            p = 0
        elif(p in ia):
            p = 1
        elif(p in random):
            p = 2
        else:
            p = 3
        return p

    def choosePlayers(self):
        p1 = (self.board.player1, self.choosePlayer(1))
        if(p1[1] == 1):
            depth = input("\nAI depth: ")
            strategy = input("\nStrategy: \n1) Absolute\n2) Positional\n3) Mobility\n4) Mixte (Recommended)\nChoice: ")
            timeOfThinking = float(input("Maximum time before the AI gives his move (in seconde) :"))
            self.ia1 = ia.IA(self.board.player1, self.board.player2, int(depth), int(strategy), timeOfThinking)
        elif(p1[1] == 3):
            self.neural1 = neuralNetwork.NeuralNetwork()
            fileName = input("Which AI would you like to load ?")
            self.neural1.load(fileName)
        p2 = (self.board.player2, self.choosePlayer(2))
        if(p2[1] == 1):
            depth = input("AI depth: ")
            strategy = input("\nStrategy: \n1) Absolute\n2) Positional\n3) Mobility\n4) Mixte (Recommended)\nChoice: ")
            timeOfThinking = float(input("Maximum time before the AI gives his move (in seconde) :"))
            self.ia2 = ia.IA(self.board.player2, self.board.player1, int(depth), int(strategy), timeOfThinking)
        elif(p2[1] == 3):
            self.neural2 = neuralNetwork.NeuralNetwork()
            fileName = input("Which AI would you like to load ?")
            self.neural2.load(fileName)
        return [p1, p2]

    def doTurn(self, currentBoard, player, times, display = True):
        color, nbType = player
        if(display):
            print("Player " + str(color) + ": ")
            self.board.displayPossibilities(currentBoard, color)
        slots = self.board.getAllSlotsAvailable(currentBoard, color)
        if(len(slots) == 0):
            return False
        if(nbType == 0): # human        
            choices = [i for i in range(len(slots))]
            start = time.time()
            choice = self.inputInArray(choices, "Choose a number between 0 and " + str(len(slots) - 1) + ".", "the number isn't between 0 and " + str(len(slots) - 1) + " !")
            end = time.time()
            times[color - 1] += end - start
            x,y = slots[choice]
            self.board.playSlot(currentBoard, x, y, color)
        elif(nbType == 1): # IA
            if(color == self.board.player1):
                start = time.time()
                bestMove = self.ia1.startMinMaxAlphaBeta(currentBoard, self.numberOfMoves, display)
                end = time.time()
                times[0] += end - start
            else:
                start = time.time()
                bestMove = self.ia2.startMinMaxAlphaBeta(currentBoard, self.numberOfMoves, display)
                end = time.time()
                times[1] += end - start
            self.board.playProposition(currentBoard, bestMove[0], color)
        elif(nbType == 2): # random
            start = time.time()
            slot = random.choice(slots)
            x,y = slot
            self.board.playSlot(currentBoard, x, y, color)
            end = time.time()
            times[color - 1] += end - start
        elif(nbType == 3): # neural network
            if(color == self.board.player1):
                start = time.time()
                bestMove = self.neural1.chooseProposition(currentBoard, color)
                end = time.time()
                times[0] += end - start
            else:
                start = time.time()
                bestMove = self.neural2.chooseProposition(currentBoard, color)
                end = time.time()
                times[1] += end - start
            self.board.playProposition(currentBoard, bestMove, color)
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
        self.currentBoard = self.board.generateStart()
        players = self.choosePlayers()
        played1 = True
        played2 = True
        turns = 0
        times = [0,0]
        while(played1 or played2):
            turns += 1
            played1 = self.doTurn(self.currentBoard, players[0], times)
            if(not(played1)):
                print("Player1 can't play !")
            played2 = self.doTurn(self.currentBoard, players[1], times)
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
        if(players[0][1] == 1):
            print("Number of nodes generated for P1 :", self.ia1.totalNumberNode)
        if(players[1][1] == 1):
            print("Number of nodes generated for P2 :", self.ia2.totalNumberNode)
    
    def testGame(self, queueGames, queueResults, queueTimes, players):
        while(not(queueGames.empty())):
            queueGames.get()
            currentBoard = self.board.generateStart()
            played1 = True
            played2 = True
            turns = 0
            times= [0,0]
            while(played1 or played2):
                turns += 1
                played1 = self.doTurn(currentBoard, players[0], times, False)
                played2 = self.doTurn(currentBoard, players[1], times, False)
            scores = self.board.getScores(currentBoard)
            if(scores[0] > scores[1]):
                queueResults.put(0)
            else:
                queueResults.put(1)
            queueTimes.put(times)
    
    def runTest(self):
        totalScores = [0,0]
        players = self.choosePlayers()
        nbGames = int(input("How many games to play ?\n"))
        queueGames = multiprocessing.Queue()
        queueTimes = multiprocessing.Queue()
        queueResults = multiprocessing.Queue()
        totGames = 0
        times = [0,0]
        for i in range(nbGames):
            queueGames.put(i)
        process = []
        nbProcess = min(8, int(nbGames))
        for _ in range(nbProcess):
            newProcess = multiprocessing.Process(target = self.testGame, args = (queueGames, queueResults, queueTimes, players))
            process.append(newProcess)
            newProcess.start()
        isRunning = True
        while(isRunning):
            currentRunning = False
            for p in process:
                currentRunning = currentRunning or p.is_alive()
            isRunning = currentRunning
            if(not(queueResults.empty())):
                result = queueResults.get()
                totalScores[result] += 1
                totGames += 1
            if(not(queueTimes.empty())):
                time = queueTimes.get()
                times[0] += time[0]
                times[1] += time[1]
                if(totGames > 0):
                    sETA = (times[0] + times[1]) * (nbGames - totGames) / (totGames * nbProcess)
                    print("The estimated time of arrival is : " + str(int(sETA / 60)) + "m " + str(int(sETA) % 60) + "s.")
        for p in process:    
            p.join()
        print("Temps moyen par partie J1 : " + str(times[0] / nbGames) + " s.")
        print("Temps moyen par partie J2 : " + str(times[1] / nbGames) + " s.")
        print("Final result is : " + str(totalScores[0]) + "-" + str(totalScores[1]) + " (" + str(totalScores[0] * 100 / nbGames) + "% - " + str(totalScores[1] * 100 / nbGames) + "%).")

    def runGame(self, typeP1 : int, typeP2 : int, depthP1 : int, depthP2 : int, strategyP1 : int, strategyP2 : int):
        currentBoard = self.board.generateStart()
        self.numberOfMoves = 0
        played1 = True
        played2 = True
        turns = 0
        timesMove1 = []
        timesMove2 = []
        players = [[self.board.player1, typeP1], [self.board.player2, typeP2]]
        if(typeP1 == 1):
            self.ia1 = ia.IA(self.board.player1, self.board.player2, depthP1, strategyP1)
        if(typeP2 == 1):
            self.ia2 = ia.IA(self.board.player2, self.board.player1, depthP2, strategyP2)
        while(played1 or played2):
            turns += 1
            times= [0,0]
            played1 = self.doTurn(currentBoard, players[0], times, False)
            if(played1):
                timesMove1.append(times[0])
            else:
                timesMove1.append(-1)
            times= [0,0]
            played2 = self.doTurn(currentBoard, players[1], times, False)
            if(played2):
                timesMove2.append(times[1])
            else:
                timesMove2.append(-1)
        scores = self.board.getScores(currentBoard)
        result = -1
        if(scores[0] > scores[1]):
            result = 1
        else:
            result = 2
        timeGame = 0
        for time in timesMove1:
            if(time > 0):
                timeGame += time
        for time in timesMove2:
            if(time > 0):
                timeGame += time
        return [result, strategyP1, strategyP2, depthP1, depthP2, timeGame, timesMove1, timesMove2]

    def runGamesProcessus(self, queueNextGame : multiprocessing.Queue, queueResultGame : multiprocessing.Queue) -> None:
        end = False
        while(not(end)):
            if(not(queueNextGame.empty())):
                end, typeP1, typeP2, depthP1, depthP2, strategyP1, strategyP2  = queueNextGame.get()
                if(not(end)):
                    print("Starting game : " + str(strategyP1) + " - " + str(strategyP2) + "    " + str(depthP1) + " - " + str(depthP2))
                    value = self.runGame(typeP1, typeP2, depthP1, depthP2, strategyP1, strategyP2)
                    queueResultGame.put(value)
                    print("End game : " + str(strategyP1) + " - " + str(strategyP2))

    def runTestAll(self):
        maxDepth = max(2,int(input("Max depth to compute : ")))
        queueNextGame = multiprocessing.Queue()
        queueResultGame = multiprocessing.Queue()
        processus = []
        for _ in range(8):
            newProcess = multiprocessing.Process(target=self.runGamesProcessus, args=(queueNextGame, queueResultGame))
            newProcess.start()
            processus.append(newProcess)
        nbGames = 0
        for depthP1 in range(2,maxDepth+1):
            for depthP2 in range(2,maxDepth+1):
                for strategyP1 in range(1,5):
                    for strategyP2 in range(1,5):
                        queueNextGame.put([False, 1, 1, depthP1, depthP2, strategyP1, strategyP2])
                        nbGames += 1
        nbFinishedGame = 0
        results = []
        while (nbFinishedGame < nbGames):
            if(not(queueResultGame.empty())):
                results.append(queueResultGame.get())
                nbFinishedGame += 1
        print("Quitting proccess... ", end="")
        for _ in range(8):
            queueNextGame.put([True, -1, -1, -1, -1, -1, -1])
        for process in processus:
            process.join()
        print("DONE !")
        with open("results.txt", "w") as f:
            for result, typeP1, typeP2, depthP1, depthP2, timeGame, timesMove1, timesMove2 in results:
                f.write(str(result) + ";")
                f.write(str(typeP1) + ";")
                f.write(str(typeP2) + ";")
                f.write(str(depthP1) + ";")
                f.write(str(depthP2) + ";")
                f.write(str(timeGame) + ";")
                f.write(str(timesMove1) + ";")
                f.write(str(timesMove2) + ";")
                f.write("\n")
    
    def runOutputValuesForTestAllAI(self):
        lines = []
        with open("results.txt", "r") as f:
            lines = f.readlines()
        namesAI = ["Absolute","Positional","Mobility","Mixte"]
        plt.rcParams['figure.figsize'] = [12, 7]
        for line in lines:
            allValues = line.split(";")
            result = int(allValues[0])
            typeP1 = int(allValues[1])
            typeP1 = namesAI[typeP1 - 1]
            typeP2 = int(allValues[2])
            typeP2 = namesAI[typeP2 - 1]
            depthP1 = int(allValues[3])
            depthP2 = int(allValues[4])
            timeGame = float(allValues[5])
            timesMove1 = allValues[6].split(", ")
            timesMove1[0] = timesMove1[0].removeprefix("[")
            timesMove1[-1] = timesMove1[-1].removesuffix("]")
            timesMove1 = [float(val) for val in timesMove1]
            totalTime1 = sum(timesMove1)
            timesMove2 = allValues[7].split(", ")
            timesMove2[0] = timesMove2[0].removeprefix("[")
            timesMove2[-1] = timesMove2[-1].removesuffix("]")
            timesMove2 = [float(val) for val in timesMove2]
            totalTime2 = sum(timesMove2)
            playedMoves1 = []
            nbMove = 1
            for timeM1 in timesMove1:
                if(timeM1 != -1):
                    playedMoves1.append(nbMove)
                    nbMove += 2
                else:
                    nbMove += 2
            timesMove1 = list(filter(lambda a: a != -1, timesMove1))
            playedMoves2 = []
            nbMove = 2
            for timeM1 in timesMove2:
                if(timeM1 != -1):
                    playedMoves2.append(nbMove)
                    nbMove += 2
                else:
                    nbMove += 2
            timesMove2 = list(filter(lambda a: a != -1, timesMove2))
            plt.plot(playedMoves1, timesMove1)
            plt.plot(playedMoves2, timesMove2)
            plt.ylabel("Time for each move in s")
            plt.xlabel("The number of the move")
            plt.legend(["P1 : " + typeP1 + " of depth " + str(depthP1), "P2 : " + typeP2 + " of depth " + str(depthP2)])
            plt.figtext(0.7,0.6,"The winner is P" + str(result))
            plt.figtext(0.7,0.58,"The total time is " + str(timeGame)[:6] + " s")
            plt.figtext(0.7,0.56,"The total time of P1 is " + str(totalTime1)[:6] + " s")
            plt.figtext(0.7,0.54,"The total time of P2 is " + str(totalTime2)[:6] + " s")
            path = "plots"
            if(not(os.path.exists(path))):
                os.makedirs(path)
            path += os.path.sep + typeP1 + str(depthP1) + "_" + typeP2 + str(depthP2) + ".png"
            plt.savefig(path)
            plt.close()

        

    def runMenu(self):
        run = True
        while(run):
            fight = ["f", "F", "fight", "FIGHT", "1"]
            train = ["t","T", "train", "TRAIN", "2"]
            test = ["test", "TEST", "3"]
            testAll = ["all", "ALL", "4"]
            outputAll = ["o", "O", "OUT", "out", "5"]
            quit = ["q","Q", "quit", "QUIT", "6"]
            print("""What do you want to do ?
            1) FIGHT !
            2) Train AI
            3) Test AI
            4) Test all AI
            5) Generates plots for the results of test all AI.
            6) Quit""")
            choice = self.inputInArray(fight + train + test + testAll + quit + outputAll)
            if(choice in fight):
                self.runOthello()
            elif(choice in train):
                tournamentSize = int(input("Choose the size of the tournament (recommended = 6) :\n"))
                nbGenerations = int(input("Choose the number of generation (~ 1 min per generation for 6 in size of tournament) :\n"))
                trainingAI = training.Training(tournamentSize)
                bestFileName = input("Enter the name of the current best AI (press enter if there is not) :\n")
                trainingAI.runTraining(nbGenerations, bestFileName)
            elif(choice in test):
                self.runTest()
            elif(choice in testAll):
                self.runTestAll()
            elif(choice in outputAll):
                self.runOutputValuesForTestAllAI()
            else:
                run = False

if __name__ == '__main__':
    core = Core()
    core.runMenu()