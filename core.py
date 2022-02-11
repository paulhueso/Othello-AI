
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

    def detectAround(self, x ,y ,colorCheck):
        directions = []
        for j in range(-1, 2):
           for i in range(-1, 2):
                newX = x + i
                newY = y + j
                if(newX < 0
                otherColor = self.board[y + j][x + i]
                if(otherColor != self.empty and colorCheck != otherColor):
                    directions.append((i,j))
        return directions
               
    def isPlayable(self, x, y):
        if(x < 0 or x > 7 or y < 0 or y > 7):
            return False
        

othello = Board()
