import sys
import Core

class IA:
    """IA implentation for othello"""

    def __init__(self, board, depth):
        minmax(board, depth, true)

    def heuristic(self, playerTurn):
        playerScore = score(board, playerTurn) #fonction qui retourne le score du tableau
        opponentScore = score(board, opponentTurn)
        return playerScore - opponentScore

    # Basic minmax function
    # maximizePlayer dépend du premier joueur qui joue (noir commence puis blanc)
    def minmax(self, currentBoard, depth, maximizePlayer):
        if(depth == 0 or game_over(board)):
            return self.heuristic(board)

        moves = Core.Board.getAllSlotsAvailable(currentBoard, 2)

        if(maximizePlayer):
            maxValue = -sys.maxint - 1
            for(move in moves): #Pour chaque possibilités
                newBoard = #faire le move
                value = self.minmax(newBoard, depth - 1, false)
                maxValue = max(maxValue, value)
        else:
            maxValue = sys.maxint
            for(move in moves):
                newBoard = #faire le move
                value = self.minmax(newBoard, depth - 1, true)
                maxValue = min(maxValue, value)
        return maxValue