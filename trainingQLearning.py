import board
import neuralNetwork as nn
import random
import core

class QLearning:
    """Implementation of Qlearning algorithm for Othello"""

    def __init__(self, color, opponentColor, learningRate = 0.1, gamma = 1):
        self.board = board.Board()
        self.color = color
        self.learningRate = learningRate
        self.gamma = gamma
        self.opponentColor = opponentColor
        self.bestOfLastGeneration = None
        self.scores = [0,0]

        
    """def initNeuralNetworks(self, inputLength = 64, layersLength = [16, 16, 16], outputLength = 64):
        Initialize the Qself.currentGeneration = []
        for i in range(self.nbParticipants):
            self.currentGeneration.append(neuralNetwork.NeuralNetwork(inputLength, layersLength, outputLength))
        for network in self.currentGeneration:
            network.randomFullPopulate()
    """

    def chooseMove(self, currentBoard, neuralNetwork, eps):
        """Choose an action by epsilon greedy method
        @currentBoard : current state of the board    
        @neuralNetwork : output of the neural network
        @eps : probability of exploitation
        return a move to play and the reward associated
        """
        legalMoves = self.board.getAllSlotsAvailable(currentBoard, self.color)
        if random.uniform(0,1) < eps:
            return random.choice(legalMoves) #Choisir l'action aléatoirement
        else:
            #Sélectionner plus grande probabilité dans l'output du nn
            bestMove = (-1, -1000000)
            for move in range(len(legalMoves)):
                x,y = legalMoves[move]
                valueMove = neuralNetwork[y * 8 + x]
                if(valueMove > bestMove[1]):
                    bestMove = (move, valueMove)
            return bestMove[0]

    def playMove(self, board, x, y):
        newBoard = self.board.playSlot(board, at[0], at[1], self.color)
        reward = 0
        if self.board.winner(board) == self.color:
            reward = 1
            self.scores[0] += 1
        elif self.board.winner(board) == self.opponentColor:
            reward = -1
            self.scores[1] += 1

        return newBoard, reward


    def training(self, doTurn, nbOfGames = 500):

        game = core.Core()

        playerType = 2#choosePlayerType()

        neuralNetwork = nn.NeuralNetwork(64, [16,16,16], 64)
        neuralNetwork.randomFullPopulate()

        for _ in range (nbOfGames):

            boardt0 = self.board.generateStart() #Reset the board

            while not self.board.isFinished(boardt0):

                at0 = self.chooseMove(boardt0, neuralNetwork.choosePlay(boardt0, self.color), 0.1) #10% chance of exploration
                at0x, at0y = at0[0], at0[1]

                boardt1, reward = self.playMove(boardt0, at0x, at0y) 
                
                boardt2 = doTurn(newBoard, self.opponentColor, [0,0])

                #Update Neural Network
                at1 = self.chooseMove(boardt2, neuralNetwork.choosePlay(boardt2, self.color), 0.0) #Exploitation
                at1x, at1y = at1[0], at1[1]
                
                #Mettre à jour tous les noeuds si on gagne ?
                neuralNetwork[at0x + at0y * 8] += self.learningRate * (reward + self.gamma * neuralNetwork[at1x + at1y * 8] - neuralNetwork[at0x + at0y * 8])

                boardt0 = boardt2

            print(self.scores)