import sys
import board
import copy

class IA:
    """IA implentation for othello"""

    def __init__(self, color, otherColor, depth = 3, strategy = 1):
        self.depth = depth
        self.board = board.Board()
        self.color = color
        self.otherColor = otherColor
        self.strategy = strategy
        self.numberOfMoves = 0

    def score(self, currentBoard, color):
        score = 0
        mixteStrategy = -1
        #Mixte strategy
        if(self.strategy == 4):
            mixteStrategy = 3
            if(self.numberOfMoves < 15):
                mixteStrategy = 2
            elif(self.numberOfMoves > 50):
                mixteStrategy = 1

        #Absolute strategy
        if(self.strategy == 1 or mixteStrategy == 1):
            for j in range(8):
                for i in range(8):
                    slot = currentBoard[j][i]
                    score += (color == slot)
            return score
        
        #Positional strategy
        elif(self.strategy == 2 or mixteStrategy == 2):
            positional = [[500, -150, 30, 10, 10, 10, 30, -150, 500],[-150, -250, 0, 0, 0, 0, -250, -150],[30, 0, 1, 2, 2, 1, 0, 30],[10, 0, 2, 16, 16, 2, 0, 10],[10, 0, 2, 16, 16, 2, 0, 10],[30, 0, 1, 2, 2, 1, 0, 30],[-150, -250, 0, 0, 0, 0, -250, -150],[500, -150, 30, 10, 10, 10, 30, -150, 500]]
            #positional = [[100, -20, 10, 5, 5, 10, -20, 100],[-20, -50, -2, -2, -2, -2, -50, -20],[10, -2, -1, -1, -1, -1, -2, 10],[5, -2, -1, -1, -1, -1, -2, 5],[5, -2, -1, -1, -1, -1, -2, 5],[10, -2, -1, -1, -1, -1, -2, 10],[-20, -50, -2, -2, -2, -2, -50, -20],[100, -20, 10, 5, 5, 10, -20, 100]]
            for j in range(8):
                for i in range(8):
                    slot = currentBoard[j][i]
                    score += (color == slot)*positional[j][i]
            return score
        
        #Mobility strategy
        elif(self.strategy == 3 or mixteStrategy == 3):
            possibleMoves = self.board.getAllSlotsAvailable(currentBoard, color)
            return len(possibleMoves)


    def heuristic(self, currentBoard, color):
        playerScore = self.score(currentBoard, self.color)
        opponentScore = self.score(currentBoard, self.otherColor)
        return playerScore - opponentScore

    def startMinMax(self, board, numberOfMoves):
        self.numberOfMoves = numberOfMoves
        newBoard = copy.deepcopy(board)
        bestMove = self.minmax(newBoard, self.depth, True)
        print("The AI played the choice n°" + str(bestMove[0]) + " with a score of " + str(bestMove[1]) + ".")
        return bestMove

    # Basic minmax function
    def minmax(self, currentBoard, depth, maximizePlayer):
        if(depth == 0):
            return (-1, self.heuristic(currentBoard, int(maximizePlayer)*self.color + int(not(maximizePlayer))*self.otherColor))

        if(maximizePlayer):
            moves = self.board.getAllSlotsAvailable(currentBoard, self.color)
            if(len(moves) == 0):
                return (-1, self.heuristic(currentBoard, self.color))
            bestMove = (-1, -10000000)
            for i in range(len(moves)):
                newBoard = self.board.playProposition(copy.deepcopy(currentBoard),i,self.color)
                value = self.minmax(newBoard, depth - 1, False)
                if(bestMove[1] < value[1]):
                    bestMove = (i, value[1])
        else:
            moves = self.board.getAllSlotsAvailable(currentBoard, self.otherColor)
            if(len(moves) == 0):
                return (-1, self.heuristic(currentBoard, self.otherColor))
            bestMove = (-1, 10000000)
            for i in range(len(moves)):
                newBoard = self.board.playProposition(copy.deepcopy(currentBoard),i,self.otherColor)
                value = self.minmax(newBoard, depth - 1, True)
                if(bestMove[1] > value[1]):
                    bestMove = (i, value[1])
        return bestMove

    def startMinMaxAlphaBeta(self, board, numberOfMoves):
        self.numberOfMoves = numberOfMoves
        newBoard = copy.deepcopy(board)
        bestMove = self.minmaxAlphaBeta(newBoard, self.depth, -10000000, 10000000, True)
        print("The AI played the choice n°" + str(bestMove[0]) + " with a score of " + str(bestMove[1]) + ".")
        return bestMove
    
    def minmaxAlphaBeta(self, currentBoard, depth, alpha, beta, maximizePlayer):
        if(depth == 0):
            return (-1, self.heuristic(currentBoard, self.color))
        
        if(maximizePlayer):
            moves = self.board.getAllSlotsAvailable(currentBoard, self.color)
            if(len(moves) == 0):
                return (-1, self.heuristic(currentBoard, self.color))
            bestMove = (-1, -10000000)
            for i in range(len(moves)):
                newBoard = self.board.playProposition(copy.deepcopy(currentBoard), i, self.color)
                value = self.minmaxAlphaBeta(newBoard, depth - 1, alpha, beta, False)
                if(bestMove[1] < value[1]):
                    bestMove = (i, value[1])
                alpha = max(alpha, bestMove[1])
                if(beta <= alpha):
                    break
        else:
            moves = self.board.getAllSlotsAvailable(currentBoard, self.otherColor)
            if(len(moves) == 0):
                return (-1, self.heuristic(currentBoard, self.otherColor))
            bestMove = (-1, 10000000)
            for i in range(len(moves)):
                newBoard = self.board.playProposition(copy.deepcopy(currentBoard),i,self.otherColor)
                value = self.minmaxAlphaBeta(newBoard, depth - 1, alpha, beta, True)
                if(bestMove[1] > value[1]):
                    bestMove = (i, value[1])
                beta = min(beta, bestMove[1])
                if(beta <= alpha):
                    break
        return bestMove

    ##  minimax et negamax sont les même algo mais implémentés différements, ils ont donc les même performances ##

        def negamax(self, currentBoard, depth, player):
            if(depth == 0 or game_over(currentBoard)):
                return self.heuristic(currentBoard, self.color)

        moves = Core.Board.getAllSlotsAvailable(currentBoard, self.color)

        value = -sys.maxint - 1
        for move in moves:
            value = max(value, -self.negamax(move, depth - 1, -player))

        return value
