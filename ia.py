import sys
import Core

class IA:
    """IA implentation for othello"""

    def __init__(self, board, depth):
        minmax(board, depth, true)

    def heuristic(self, playerTurn):
        # Heuristic absolue
        playerScore = score(board, playerTurn) #fonction qui retourne le score du tableau
        opponentScore = score(board, opponentTurn)
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


    # Basic minmax function
    # maximizePlayer dépend du premier joueur qui joue (noir commence puis blanc)
    def minmax(self, currentBoard, depth, maximizePlayer):
        if(depth == 0 or game_over(board)):
            return self.heuristic(board)

        moves = Core.Board.getAllSlotsAvailable(currentBoard, 2)

        if(maximizePlayer):
            bestMove = -sys.maxint - 1
            for(move in moves): #Pour chaque possibilités
                newBoard = #faire le move
                value = self.minmax(newBoard, depth - 1, false)
                bestMove = max(bestMove, value)
        else:
            bestMove = sys.maxint
            for(move in moves):
                newBoard = #faire le move
                value = self.minmax(newBoard, depth - 1, true)
                bestMove = min(bestMove, value)
        return bestMove

    def minmaxAlphaBeta(self, currentBoard, depth, alpha, beta, maximizePlayer):
        if(depth == 0 or game_over(currentBoard)):
            return self.heuristic(currentBoard, 2)

        moves = Core.Board.getAllSlotsAvailable(currentBoard, 2)

        if(maximizePlayer):
            bestMove = -sys.maxint - 1
            for(move in moves): #Pour chaque possibilités
                newBoard = #faire le move
                value = self.minmaxAlphaBeta(newBoard, depth - 1, alpha, beta false)
                bestMove = max(bestMove, value)
                alpha = max(alpha, value)
                if(beta <= alpha):
                    break
        else:
            bestMove = sys.maxint
            for(move in moves):
                newBoard = #faire le move
                value = self.minmaxAlphaBeta(newBoard, depth - 1, alpha, beta, true)
                bestMove = min(bestMove, value)
                beta = min(beta, value)
                if(beta <= alpha):
                    break
        return bestMove

    ##  minimax et negamax sont les même algo mais implémentés différements, ils ont donc les même performances ##

        def negamax(self, currentBoard, depth, player):
            if(depth == 0 or game_over(currentBoard)):
                return self.heuristic(currentBoard, 2)

        moves = Core.Board.getAllSlotsAvailable(currentBoard, 2)

        value = -sys.maxint - 1
        for(move in moves):
            value = max(value, -self.negamax(move, depth - 1, -player))

        return value