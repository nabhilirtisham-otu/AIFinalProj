'''
This file handles board representation, ensures move validity, and
checks if the game is over (win/loss/draw).
'''

class Game:
    
    #constructor
    def __init__(self):
        self.board = self.initialize_board()
      
    #reset to empty 3x3 board
    def initialize_board(self):
        board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        return board
    
    #return all empty positions on the board (list)
    def get_available_moves(self, board):
        available_moves = []
        for i in range(3):
            for j in range(3):
                if (board[i][j] == ""):
                    move_tuple = (i, j)
                    available_moves.append(move_tuple)
        return available_moves
    
    #update the board after a move
    def apply_move(self, board, move, player):
        new_board = [row[:] for row in board]
        new_board[move[0]][move[1]] = player
        return new_board
    
    #check if a player has won (rows, columns, and diagonals)
    def is_winner(self, board, player):
        for i in range(3):
            if (board[i][0] == player and board[i][1] == player and board[i][2] == player):
                return True
        for j in range(3):
            if (board[0][j] == player and board[1][j] == player and board[2][j] == player):
                return True
        if (board[0][0] == player and board[1][1] == player and board[2][2] == player):
            return True
        if (board[0][2] == player and board[1][1] == player and board[2][0] == player):
            return True
        return False
    
    #check if the players have drawn
    def is_draw(self, board):
        return len(self.get_available_moves(board)) == 0 and \
            not self.is_winner(board, "X") and \
            not self.is_winner(board, "O")
            
    
    #end game if win/draw (return True)
    def is_terminal(self, board):
        return (
            self.is_winner(board, "X") or
            self.is_winner(board, "O") or
            self.is_draw(board)
        )
    
    #+1/-1/0 for each leaf
    def evaluate_terminal(self, board, ai_player, human_player):
        if self.is_winner(board, ai_player):
            return 1
        elif self.is_winner(board, human_player):
            return -1
        else:
            return 0