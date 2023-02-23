from enum import Enum
from typing import Optional, List, Union

PieceColor = Enum("PieceColor", ["RED", "BLACK"])

class Board:
    _board: List[List[Optional[PieceColor]]]
    _board_dim: int
    _size: int
    _winner: Optional[PieceColor]

    def __init__(self, size):
        """
        Constructor

        Args:
            size (int) : no. of rows of pieces
        """
        self._size = size
        self._board_dim = 2*size+2
        self._board = [[None]*self._board_dim for _ in range(self._board_dim)]
        self._winner = None
        self._populate()
        
    def _populate(self):
        """ Populates the board with squares containing pieces and pieces."""
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
        """
        Represents the board as a string.

        Returns:
            str
        """
        s = ""
        for row in self._board:
            for square in row:
                s += str(square)
            s += "\n"
        return s
    
    def valid_moves(self, piece_color):
        pass

    def jump_moves(self, piece_color):
        pass

    def reg_moves(self, piece_color):
        """
        Finds all the regular moves of a certain piece_color.

        Parameters:
            piece_color : Enum PieceColor
        
        Returns:
            list[Moves]
        """
        move_list = []
        for row in self._board:
            for square in row:
                if square.has_color(piece_color):
                    move_list.append(self.reg_moves_piece(square))
        
        return move_list


    def reg_moves_piece(self, square):
        """
        Returns:
            Moves
        """
        moves = Moves(square, set())
        for dir in square.piece.move_directions():
            '''
            if not square.neighbors[dir].has_piece:
                print(dir)
                moves.add_move(square.neighbors[dir], None)
            '''
            if square.neighbors[dir] is not None: #check to see if adjacent exists
                if square.neighbors[dir].is_empty(): #if the neighboring square is empty
                    print("a")
                    moves.add_move(square.neighbors[dir], None)
        
        return moves


class Square:
    """
    Class for the squares on the board.
    """
    def __init__(self, row, col, piece) -> None:
        """
        Constructor
        
        Args:
            row (int) : row value of the square
            col (int) : column value of the square
            piece (Piece) : if there is a piece on the board
        """
        self.piece = piece
        self.row = row
        self.col = col
        self.neighbors = {'NW' : None, 'NE' : None, 'SE' : None, 'SW' : None}

    def __str__(self) -> str:
        """ Returns a string representation of what is on the square."""
        if self.piece == None:
            return "□"
        return self.piece.color.name[0]
    
    def has_piece(self):
        """ Checks if piece exists on the square."""
        return self.piece is not None
    
    def is_empty(self):
        """ Returns true if there is no piece. """
        return self.piece is None
    
    def has_color(self, piece_color):
        """ Checks if the piece is of the color we want. """
        if self.has_piece():
            return piece_color == self.piece.color
        return False


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

    def move_directions(self):
        if self.is_king:
            return ["NW", "NE", "SE", "SW"]
        if self.color.value == PieceColor.BLACK.value:
            return ["SE", "SW"]
        return ["NW", "NE"] #self.color is RED


class Moves:
    def __init__(self, square, dead) -> None:
        """
        Args:
            square : Square (current location)
            dead : set[Square] (list of dead squares)
            """
        self.location = square
        self.dead_squares = dead
        self.children = [] #set of moves
    
    def add_move(self, square, new_dead):
        """
        Args:
            square : Square (current location)
            new_dead = Square (just jumped over)
        """
        if new_dead is None:
            self.children.append(Moves(square, self.dead_squares))
        else:
            self.children.append(Moves(square, self.dead_squares.add(new_dead)))
    
    def __str__(self):
        s = "[" + str(self.location.row) + "," + str(self.location.col)+ "]"
        for move in self.children:
            s += str(move)
        return s