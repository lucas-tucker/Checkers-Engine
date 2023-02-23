from enum import Enum
from typing import Optional, List, Union
import random

PieceColor = Enum("PieceColor", ["RED", "BLACK"])

opposite_color = {}
opposite_color[PieceColor.RED] = PieceColor.BLACK
opposite_color[PieceColor.BLACK] = PieceColor.RED

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
                if (square.row + square.col) % 2 == 1:
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
        jump_move_list, can_jump = self.jump_moves(piece_color)
        if can_jump:
            print("we should jump")
            return jump_move_list
        else: #no valid jump moves
            reg_move_list = self.reg_moves(piece_color)
            return reg_move_list

    def jump_moves(self, piece_color):
        move_list = []
        can_jump = False
        for row in self._board:
            for square in row:
                if square.has_color(piece_color):
                    move, can_jump_this_move = self._jump_moves_piece(square)
                    move_list.append(move)
                    can_jump = can_jump or can_jump_this_move
        
        return move_list, can_jump

    def _jump_moves_piece(self, square):
        jump_moves = Moves(square, set())
        self._jump_recurse(square, square.piece.color, jump_moves, square.piece, square)
        can_jump = False
        if jump_moves.can_execute():
            can_jump = True
        return jump_moves, can_jump



    
    def _jump_recurse(self, square, piece_color, move, first_piece, first_square):
        opposite: Optional[PieceColor]
        if piece_color.value == PieceColor.RED.value:
            opposite = PieceColor.BLACK
        else:
            opposite = PieceColor.RED

        for dir in first_piece.move_directions():
            if square.neighbors[dir] is not None: #neighbor exists
                if square.neighbors[dir].has_piece(): #neighbor has piece
                    if square.neighbors[dir].piece.color.value == opposite.value: #neighbor piece is opposite color
                        if square.neighbors[dir] not in move.dead_squares:
                            #we haven't visited this square
                            if square.neighbors[dir].neighbors[dir] is not None: #two neighbors down exists
                                if square.neighbors[dir].neighbors[dir].is_empty() or square.neighbors[dir].neighbors[dir] == first_square: #two neighbors down is empty
                                    #if our targeted jump square is empty or is the original square
                                    #we only need to keep track of the 1st square - if we jump to
                                    #a square we've visited in the past that isn't the 1st square
                                    #it must already be empty
                                    #parity ensures that if we kill a piece
                                    #we cannot return to it
                                    last_index = len(move.children)
                                    move.add_move(square.neighbors[dir].neighbors[dir], square.neighbors[dir])
                                    print(move)
                                    self._jump_recurse(square.neighbors[dir].neighbors[dir], piece_color, move.children[last_index], first_piece, first_square)



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
                    move_list.append(self._reg_moves_piece(square))
        
        return move_list


    def _reg_moves_piece(self, square):
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
                    moves.add_move(square.neighbors[dir], None)
        
        return moves
    
    def execute_move(self, move):
        #test method - just execute the first move of the tree - will
        #update later to have true-random
        if move.can_execute():
            cur_move = move
            while bool(cur_move.children):
                moving_piece = cur_move.location.piece
                cur_move.location.piece = None
                cur_move.children[0].location.piece = moving_piece
                '''
                for dead_square in cur_move.dead_squares:
                    dead_square.piece = None
                    print("killed: " + "[" + str(dead_square.row) + "," + str(dead_square.col) + "]")
                '''
                cur_move = cur_move.children[0]
            if cur_move.dead_squares:
                for dead_square in cur_move.dead_squares:
                    dead_square.piece = None
                    print("killed: " + "[" + str(dead_square.row) + "," + str(dead_square.col) + "]")
            
            #check if we are kinking
            if cur_move.location.row == 0:
                if moving_piece.color.value == PieceColor.RED.value:
                    moving_piece.is_king = True
            if cur_move.location.row == self._board_dim -1:
                if moving_piece.color.value == PieceColor.BLACK.value:
                    moving_piece.is_king = True
        else:
            pass
    
    def make_random_move(self, piece_color):
        move_list = self.valid_moves(piece_color)
        random.shuffle(move_list)
        i = 0
        while not move_list[i].can_execute():
            i += 1
        for move in move_list:
            print(move)
        self.execute_move(move_list[i])


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
        if self.piece.is_king:
            return self.piece.color.name[0]
        return self.piece.color.name[0].lower()
    
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
            self.children.append(Moves(square, self.dead_squares.copy()))
        else:
            new_dead_set = self.dead_squares.copy()
            new_dead_set.add(new_dead)
            self.children.append(Moves(square, new_dead_set))
    
    def __str__(self):
        s = "[" + str(self.location.row) + "," + str(self.location.col)+ "]"
        for move in self.children:
            s += str(move)
        return s
    
    def can_execute(self):
        return bool(self.children) #shortcut to say  
"""
multi jump test

b = Board(3)
print(b)
m = b._reg_moves_piece(b._board[2][1])
b.execute_move(m)
print(b)
m2 = b._reg_moves_piece(b._board[3][2])
b.execute_move(m2)
print(b)
b._board[1][2].piece = None
print(b)

#k = b.valid_moves(PieceColor.RED)

m3, a = b._jump_moves_piece(b._board[5][2])
print(m3)
b.execute_move(m3)
print(b)

b._board[0][1].piece = None
print(b)

m4 = b._reg_moves_piece(b._board[1][2])
b.execute_move(m4)
print(b)

m5 = b._reg_moves_piece(b._board[0][1])
b.execute_move(m5)
print(b)
"""

"""
multi-king jump test

b = Board(2)
print(b)
print(b._board[2][5].neighbors)
b._board[3][2].piece = Piece(PieceColor.BLACK)
b._board[3][4].piece = Piece(PieceColor.BLACK)
b._board[0][3].piece = None
b._board[4][3].piece.is_king = True
move, l = b._jump_moves_piece(b._board[4][3])
print(b)
print(l)
print(move)
b.execute_move(move)
print(b)
print(b._board[2][5].neighbors)
"""

b = Board(3)
print("START")
print(b)
BLACK = b._board[0][1].piece.color
RED = b._board[7][0].piece.color

for i in range(15):
    print("RED MOVE")
    b.make_random_move(RED)
    print(b)
    input("Press Enter to continue...")

    print("BLACK MOVE")
    b.make_random_move(BLACK)
    print(b)
    input("Press Enter to continue...")