
class Board:
    """Core game for Othello"""
    
    def __init__(self):
        self.player1 = 1
        self.player2 = 2
        self.empty = 0
        self.board = [[self.empty for i in range(8)] for j in range(8)]
        self.board[3][3] = self.player1
        self.board[4][3] = self.player2
        self.board[3][4] = self.player2
        self.board[4][4] = self.player1

    def display(self):
        for row in self.board:
            for text in row:
                print(text, end=" | ")
            print()

    def getPossibleMoves(self):
        
        

othello = Board()
