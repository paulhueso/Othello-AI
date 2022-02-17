import random
import neuralNetwork
import board
import copy
import os
import time

class Training:
    def __init__(self, sizeTournament):
        self.nbParticipants = 2**sizeTournament
        self.nbGenerations = 0
        self.currentGeneration = []
        self.currentNbGeneration = 0
        self.board = board.Board()
        self.totalTime = 0
        self.bestOfLastGeneration = None

    def initNeuralNetworks(self, inputLength = 64, layersLength = [16, 16, 16], outputLength = 64):
        self.currentGeneration = []
        for i in range(self.nbParticipants):
            self.currentGeneration.append(neuralNetwork.NeuralNetwork(inputLength, layersLength, outputLength))
        for network in self.currentGeneration:
            network.randomFullPopulate()
    
    def completeGeneration(self, best):
        if(not(os.path.exists("generations"))):
            os.makedirs("generations")
        self.bestOfLastGeneration.save("generations\\" + str(self.currentNbGeneration) + ".txt")
        self.bestOfLastGeneration = best
        avgTimePerGame = self.totalTime / (self.currentNbGeneration * (self.nbParticipants - 1))
        print("The average time per game is " + str(avgTimePerGame) + "s.")
        estimatedTime = avgTimePerGame * (self.nbParticipants - 1) * (self.nbGenerations - self.currentNbGeneration)
        print("The estimated time of arrival is : " + str(int(estimatedTime / 60)) + "m " + str(int(estimatedTime) % 60) +"s. (" + str(self.currentNbGeneration * 100 / self.nbGenerations) + "%)")
        print("End of generation n°" + str(self.currentNbGeneration) + " .")
    
    def regenerateGeneration(self):
        self.currentGeneration = [self.bestOfLastGeneration]
        currentMutationRatio = 0.05
        for i in range(1, self.nbParticipants):
            self.currentGeneration.append(copy.deepcopy(self.bestOfLastGeneration))
            for _ in range(3):
                self.currentGeneration[i].mutate(currentMutationRatio)
                currentMutationRatio += 0.01
    
    def doTournament(self):
        nextRound = [i for i in range(self.nbParticipants)]
        while(len(nextRound) > 1):
            choices = [nextRound[i] for i in range(len(nextRound))]
            currentRound = []
            nextRound = []
            while(len(choices) > 0):
                adversary1 = random.choice(choices)
                choices.remove(adversary1)
                adversary2 = random.choice(choices)
                choices.remove(adversary2)
                currentRound.append((adversary1, adversary2))
            for adversary1, adversary2 in currentRound:
                currentBoard = [[self.board.empty for i in range(8)] for j in range(8)]
                currentBoard[3][3] = self.board.player1
                currentBoard[4][3] = self.board.player2
                currentBoard[3][4] = self.board.player2
                currentBoard[4][4] = self.board.player1
                player1 = self.currentGeneration[adversary1]
                player2 = self.currentGeneration[adversary2]
                played1 = True
                played2 = True
                while(played1 or played2):
                    bestMove = player1.chooseProposition(currentBoard, self.board.player1)
                    if(bestMove != -1):
                        self.board.playProposition(currentBoard, bestMove, self.board.player1)
                        played1 = True
                    else:
                        played1 = False
                    bestMove = player2.chooseProposition(currentBoard, self.board.player2)
                    if(bestMove != -1):
                        self.board.playProposition(currentBoard, bestMove, self.board.player2)
                        played2 = True
                    else:
                        played2 = False
                results = self.board.getScores(currentBoard)
                if(results[0] > results[1]):
                    nextRound.append(adversary1)
                else:
                    nextRound.append(adversary2)
            print("End of the round with " + str(len(currentRound)*2) + " players.")
        return nextRound[0]

    
    def runTraining(self, nbGenerations, fileBest = None):
        self.currentNbGeneration = 0
        self.nbGenerations = nbGenerations
        self.totalTime = 0
        print("Started the training of the AI with " + str(nbGenerations) + " generations, and " + str(self.nbParticipants) + " participants per tournament.")
        if(not(fileBest == None or fileBest == "")):
            self.bestOfLastGeneration = neuralNetwork.NeuralNetwork()
            self.bestOfLastGeneration.load(fileBest)
        else:
            self.bestOfLastGeneration = neuralNetwork.NeuralNetwork(64, [16,16,16], 64)
            self.bestOfLastGeneration.randomFullPopulate()

        while(self.currentNbGeneration < self.nbGenerations):
            self.currentNbGeneration += 1
            self.regenerateGeneration()
            start = time.time()
            bestOfGeneration = self.doTournament()
            end = time.time()
            self.totalTime += end - start
            self.completeGeneration(self.currentGeneration[bestOfGeneration])
        self.bestOfLastGeneration.save()
        print("Ended the training of the AI.")