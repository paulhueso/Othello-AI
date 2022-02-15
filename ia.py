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

    def heuristic(self, currentBoard):
        mixteStrategy = -1

        #Mixte strategy
        if(self.strategy == 4):
            mixteStrategy = self.heuristic_mixte(currentBoard)

        if(self.strategy == 1 or mixteStrategy == 1):
            return self.heuristic_absolute(currentBoard)
        elif(self.strategy == 2 or mixteStrategy == 2):
            return self.heuristic_positional(currentBoard)
        elif(self.strategy == 3 or mixteStrategy == 3):
            return self.heuristic_mobility(currentBoard)

    def heuristic_mixte(self, currentBoard):
        if(self.numberOfMoves < 20):
            return 2
        elif(self.numberOfMoves > 45):
            return 1
        else:
            return 3

    def heuristic_absolute(self, currentBoard):
        score = 0
        opponentScore = 0
        for j in range(8):
            for i in range(8):
                slot = currentBoard[j][i]
                score += (self.color == slot)
                opponentScore += (self.otherColor == slot)
        return score - opponentScore

    def heuristic_positional(self, currentBoard):
        score = 0
        opponentScore = 0
        positional = [[500, -150, 30, 10, 10, 10, 30, -150, 500],[-150, -250, 0, 0, 0, 0, -250, -150],[30, 0, 1, 2, 2, 1, 0, 30],[10, 0, 2, 16, 16, 2, 0, 10],[10, 0, 2, 16, 16, 2, 0, 10],[30, 0, 1, 2, 2, 1, 0, 30],[-150, -250, 0, 0, 0, 0, -250, -150],[500, -150, 30, 10, 10, 10, 30, -150, 500]]
        #positional = [[100, -20, 10, 5, 5, 10, -20, 100],[-20, -50, -2, -2, -2, -2, -50, -20],[10, -2, -1, -1, -1, -1, -2, 10],[5, -2, -1, -1, -1, -1, -2, 5],[5, -2, -1, -1, -1, -1, -2, 5],[10, -2, -1, -1, -1, -1, -2, 10],[-20, -50, -2, -2, -2, -2, -50, -20],[100, -20, 10, 5, 5, 10, -20, 100]]
        for j in range(8):
            for i in range(8):
                slot = currentBoard[j][i]
                score += (self.color == slot)*positional[j][i]
                opponentScore += (self.otherColor == slot)*positional[j][i]
        return score - opponentScore
            
    #Mobility strategy Van Eck, N. J., & van Wezel, M. (2008). Application of reinforcement learning to the game of Othello. Computers & Operations Research, 35(6), 1999–2017. 
    def heuristic_mobility(self, currentBoard):
        nbCorners = 0
        nbOpponentCorners = 0
        possibleMoves = len(self.board.getAllSlotsAvailable(currentBoard, self.color))
        possibleOpponentMoves = len(self.board.getAllSlotsAvailable(currentBoard, self.otherColor))

        for i in range(0,8,7):
            for j in range(0,8,7):
                nbCorners += (self.color == currentBoard[i][j])
                nbOpponentCorners += (self.otherColor == currentBoard[i][j])

        if(possibleMoves + possibleOpponentMoves == 0): 
            return 10*(nbCorners - nbOpponentCorners)
        return 10*(nbCorners - nbOpponentCorners) + (possibleMoves - possibleOpponentMoves) / (possibleMoves + possibleOpponentMoves)

    def startMinMax(self, board, numberOfMoves):
        self.numberOfMoves = numberOfMoves
        newBoard = copy.deepcopy(board)
        bestMove = self.minmax(newBoard, self.depth, True)
        print("The AI played the choice n°" + str(bestMove[0]) + " with a score of " + str(bestMove[1]) + ".")
        return bestMove

    # Basic minmax function
    def minmax(self, currentBoard, depth, maximizePlayer):
        if(depth == 0):
            return (-1, self.heuristic(currentBoard))

        if(maximizePlayer):
            moves = self.board.getAllSlotsAvailable(currentBoard, self.color)
            if(len(moves) == 0):
                return (-1, self.heuristic(currentBoard))
            bestMove = (-1, -10000000)
            for i in range(len(moves)):
                newBoard = self.board.playProposition(copy.deepcopy(currentBoard),i,self.color)
                value = self.minmax(newBoard, depth - 1, False)
                if(bestMove[1] < value[1]):
                    bestMove = (i, value[1])
        else:
            moves = self.board.getAllSlotsAvailable(currentBoard, self.otherColor)
            if(len(moves) == 0):
                return (-1, self.heuristic(currentBoard))
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
            return (-1, self.heuristic(currentBoard))
        
        if(maximizePlayer):
            moves = self.board.getAllSlotsAvailable(currentBoard, self.color)
            if(len(moves) == 0):
                return (-1, self.heuristic(currentBoard))
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
                return (-1, self.heuristic(currentBoard))
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
                return self.heuristic(currentBoard)

        moves = Core.Board.getAllSlotsAvailable(currentBoard, self.color)

        value = -sys.maxint - 1
        for move in moves:
            value = max(value, -self.negamax(move, depth - 1, -player))

        return value
