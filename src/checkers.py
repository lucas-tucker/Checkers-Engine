from enum import Enum
from typing import Optional, List, Union

PieceColor = Enum("PieceColor", ["RED", "BLACK"])

class Board:
    _board: List[List[Optional[PieceColor]]]
    _board_dim: int
    _size: int
    _winner: Optional[PieceColor]

    def __init__(self, size):
        self._size = size
        self._board_dim = 2*size+2
        self._board = [[None]*self._board_dim for _ in range(self._board_dim)]
        self._winner = None
        self._populate()
        
    def _populate(self):
        #1st loop - populate board
        for i in range(self._board_dim): #row
            for j in range(self._board_dim): #col
                self._board[i][j] = Square(i,j, None)
                if (i+j) % 2 == 1:
                    if i < self._size:
                        self._board[i][j].piece = Piece(PieceColor.BLACK)
                
                    if i > self._size+1:
                        self._board[i][j].piece = Piece(PieceColor.RED)
        #2nd loop - connections
        dirs = {"NW" : (-1, -1),          "NE" : (-1, +1),

                "SW" : (+1, -1),          "SE" : (+1, +1)}
        
        for row in self._board:
            for square in row:
                if square.has_piece():
                    for dir in dirs:
                        dr, dc = dirs[dir]
                        cur_row = square.row
                        cur_col = square.col
                        target_row = cur_row+dr
                        target_col = cur_col+dc
                        if 0 <= target_row < self._board_dim and 0 <= target_col < self._board_dim:
                            square.neighbors[dir] = self._board[target_row][target_col]
                            #self._board[target_row][target_col].neighbors[opposite[dir]] = square

    def __str__(self) -> str:
        s = ""
        for row in self._board:
            for square in row:
                s += str(square)
            s += "\n"
        return s

class Square:
    def __init__(self, row, col, piece) -> None:
        self.piece = piece
        self.row = row
        self.col = col
        self.neighbors = {'NW' : None, 'NE' : None, 'SE' : None, 'SW' : None}

    def __str__(self) -> str:
        if self.piece == None:
            return "□"
        return self.piece.color.name[0]
    
    def has_piece(self):
        return self.piece is not None



class Piece:
    """
    Class representing individual pieces.
    """
    is_king: bool
    def __init__(self, piece_color, is_king=False):
        """
        Parameters:
            is_King : boolean
            posX : int
            posY : int
            piece_dir : int (either 1 for player 1, -1 for player 2)
        """
        self.is_king = is_king
        self.color = piece_color