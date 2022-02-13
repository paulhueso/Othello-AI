import sys
import board
import copy

class IA:
    """IA implentation for othello"""

    def __init__(self, color, otherColor, depth = 3):
        self.depth = depth
        self.board = board.Board()
        self.color = color
        self.otherColor = otherColor

    def score(self, currentBoard, color):
        #positional = [[500, -150, 30, 10, 10, 10, 30, -150, 500],[-150, -250, 0, 0, 0, 0, -250, -150],[30, 0, 1, 2, 2, 1, 0, 30],[10, 0, 2, 16, 16, 2, 0, 10],[10, 0, 2, 16, 16, 2, 0, 10],[30, 0, 1, 2, 2, 1, 0, 30],[-150, -250, 0, 0, 0, 0, -250, -150],[500, -150, 30, 10, 10, 10, 30, -150, 500]]
        positional = [[100, -20, 10, 5, 5, 10, -20, 100],[-20, -50, -2, -2, -2, -2, -50, -20],[10, -2, -1, -1, -1, -1, -2, 10],[5, -2, -1, -1, -1, -1, -2, 5],[5, -2, -1, -1, -1, -1, -2, 5],[10, -2, -1, -1, -1, -1, -2, 10],[-20, -50, -2, -2, -2, -2, -50, -20],[100, -20, 10, 5, 5, 10, -20, 100]]
        score = 0
        for j in range(8):
            for i in range(8):
                slot = currentBoard[j][i]
                score += (color == slot)*positional[j][i]
        return score

    def heuristic(self, currentBoard, color):
        # Heuristic absolue
        if(color == self.color):
            playerScore = self.score(currentBoard, self.color)
            opponentScore = self.score(currentBoard, self.otherColor)
        else:
            playerScore = self.score(currentBoard, self.otherColor)
            opponentScore = self.score(currentBoard, self.color)
        return playerScore - opponentScore
        # Heuristic positionnel
        """positional1 = 
        [
            [500, -150, 30, 10, 10, 10, 30, -150, 500]
            [-150, -250, 0, 0, 0, 0, -250, -150]
            [30, 0, 1, 2, 2, 1, 0, 30]
            [10, 0, 2, 16, 16, 2, 0, 10]
            [10, 0, 2, 16, 16, 2, 0, 10]
            [30, 0, 1, 2, 2, 1, 0, 30]
            [-150, -250, 0, 0, 0, 0, -250, -150]
            [500, -150, 30, 10, 10, 10, 30, -150, 500]
        ]

        positional2 =
        [
            [100, -20, 10, 5, 5, 10, -20, 100]
            [-20, -50, -2, -2, -2, -2, -50, -20]
            [10, -2, -1, -1, -1, -1, -2, 10]
            [5, -2, -1, -1, -1, -1, -2, 5]
            [5, -2, -1, -1, -1, -1, -2, 5]
            [10, -2, -1, -1, -1, -1, -2, 10]
            [-20, -50, -2, -2, -2, -2, -50, -20]
            [100, -20, 10, 5, 5, 10, -20, 100]
        ]"""

    def startMinMax(self, board):
        newBoard = copy.deepcopy(board)
        return self.minmax(newBoard, self.depth, True)

    # Basic minmax function
    # maximizePlayer dépend du premier joueur qui joue (noir commence puis blanc)
    def minmax(self, currentBoard, depth, maximizePlayer):
        if(depth == 0):
            return (-1, self.heuristic(currentBoard, int(maximizePlayer)*self.color + int(not(maximizePlayer))*self.otherColor))

        if(maximizePlayer):
            moves = self.board.getAllSlotsAvailable(currentBoard, self.color)
            if(len(moves) == 0):
                return (-1, self.heuristic(currentBoard, self.color))
            bestMove = (-1, -10000000)
            for i in range(len(moves)):  #Pour chaque possibilités
                newBoard = copy.deepcopy(self.board.playProposition(currentBoard,i,self.color))
                value = self.minmax(newBoard, depth - 1, False)
                bestMove = (i, max(bestMove[1], value[1]))
        else:
            moves = self.board.getAllSlotsAvailable(currentBoard, self.otherColor)
            if(len(moves) == 0):
                return (-1, self.heuristic(currentBoard, self.otherColor))
            bestMove = (-1, 10000000)
            for i in range(len(moves)):
                newBoard = copy.deepcopy(self.board.playProposition(currentBoard,i,self.otherColor))
                value = self.minmax(newBoard, depth - 1, True)
                bestMove = (i, min(bestMove[1], value[1]))
        return bestMove

    def minmaxAlphaBeta(self, currentBoard, depth, alpha, beta, maximizePlayer):
        if(depth == 0):
            return self.heuristic(currentBoard, self.color)

        moves = Core.Board.getAllSlotsAvailable(currentBoard, self.color)

        if(maximizePlayer):
            bestMove = -sys.maxint - 1
            for move in moves: #Pour chaque possibilités
                newBoard = self.board.playProposition(currentBoard,x,y,self.color)
                value = self.minmaxAlphaBeta(newBoard, depth - 1, alpha, beta, False)
                bestMove = max(bestMove, value)
                alpha = max(alpha, value)
                if(beta <= alpha):
                    break
        else:
            bestMove = sys.maxint
            for move in moves:
                newBoard = self.board.playProposition(currentBoard,x,y,self.otherColor)
                value = self.minmaxAlphaBeta(newBoard, depth - 1, alpha, beta, True)
                bestMove = min(bestMove, value)
                beta = min(beta, value)
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
