"""
Class for Checkers: this is the Checkers game logic file.

Current Status : comments, docstring

Author: Daniel Chen
"""

"""
Example calls:

    1) Creating a board::

        checkers = Checkers(3)

    2) Getting the valid moves list of Red:

        move_list = checkers.valid_moves(PieceColor.RED)
    
    3) executing a single move:

        checkers.execute_single_move(move_list[3], 1)
    
    4) drawing the game:

        checkers.draw_game()

    5) resigning the game for Red:

        checkers.resign_game(PieceColor.RED)
"""


from enum import Enum
from typing import Optional, List, Union
import random

PieceColor = Enum("PieceColor", ["RED", "BLACK"])

opposite_color = {}
opposite_color[PieceColor.RED] = PieceColor.BLACK
opposite_color[PieceColor.BLACK] = PieceColor.RED

class Checkers:
    #PRIVATE ATTRIBUTES

    #the board itself
    _game_board: object

    #dimensions of the board
    _board_dim: int

    #size of the game - how many rows of pieces
    _size: int

    #winner (if any) of the game
    _winner: Optional[PieceColor]

    #whether or not the game has been resigned or drawn
    _resigned: bool

    #PUBLIC ATTRIBUTES

    #how many moves since last piece was taken
    consecutive_non_jump_moves: int

    def __init__(self, size):
        """
        Initializes the game board. At first, there is no winner, no
        consecutive non jump moves, no one has resigned, and the board
        state is as it is at the start of the game.
        """
        self._size = size
        self._board_dim = 2*size+2
        self._game_board = Board(self._board_dim, self._board_dim)
        self._winner = None
        self.consecutive_non_jump_moves = 0
        self._resigned = False
        self._populate()

    def __str__(self):
        """
        Returns a string representation of the game, which
        is just a string representation of the board.

        Args: None
        Returns: str
        """
        return str(self._game_board)


    def get_board(self):
        """
        Returns the board.

        Args: None
        Returns: Board
        """
        return self._game_board

    def valid_moves(self, piece_color):
        """
        Returns the set of possible moves for a certain player.
        Calls jump_moves and reg_moves.

        Args:
            piece_color : Enum(PieceColor)
        
        Returns:
            list[Move]
        """
        jump_move_list, can_jump = self.jump_moves(piece_color)
        if can_jump:
            # print("we should jump")
            return jump_move_list
        else: #no valid jump moves
            reg_move_list = self.reg_moves(piece_color)
            return reg_move_list

    def piece_valid_moves(self, coord, piece_color):
        """
        When given a tuple of board coordinates, returns a list of tuples with
        the coordinate to move to and the move itself.

        Args:
            coord (int, int): Board Coordinates
            piece_color: Enum piece color

        Returns:
            list[(int, int, Move), ...] : List of tuples containing the new
            coordinate and the possible moves from that coordinate. Returns an
            empty list is no moves are possible from entered coordinate.
        """
        possible_moves = []
        poss_results = []
        all_moves = self.valid_moves(piece_color)
        for move in all_moves:
            if move.location.row == coord[1] and move.location.col == coord[0]:
                # Do something with move.children
                return (coord[1], coord[0], move)
                possible_moves += move.children
        for move in possible_moves:
            poss_results.append((move.location.col, move.location.row, move))
        return poss_results


    def jump_moves(self, piece_color):
        """
        Returns the jumping-moves of a particular color, and whether
        any of them are jumping moves.

        Args:
            piece_color : Enum(PieceColor)
        
        Returns:
            list[Move], bool

            NOT FIXED
        """
        move_list = []
        can_jump = False
        for row in self.get_board().board:
            for square in row:
                if square.has_color(piece_color):
                    move, can_jump_this_move = self._jump_moves_piece(square)
                    move_list.append(move)
                    can_jump = can_jump or can_jump_this_move
        
        return move_list, can_jump

    def _jump_moves_piece(self, square):
        """
        Private method

        Args:
            square : Square (start of the move tree)

        Returns:
            Move, bool

        """
        jump_moves = Moves(square, set())
        self._jump_recurse(square, square.piece.color, jump_moves, square.piece, square)
        can_jump = False
        if jump_moves.can_execute():
            can_jump = True
        return jump_moves, can_jump



    
    def _jump_recurse(self, square, piece_color, move, first_piece, first_square):
        """
        Private method

        Args: 
            square : Square (square currently on)
            piece_color : Enum(PieceColor) (to remember which color we can jump over)
            move : Move (we build off this tree)
            first_piece : Piece (actually not sure why we need this)
            first_square : Square (we could revisit this square, so we need to treat as if it's empty)

        Returns:
            None

        """
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
                                    #print(move)
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
        for row in self.get_board().board:
            for square in row:
                if square.has_color(piece_color):
                    move_list.append(self._reg_moves_piece(square))
        
        return move_list


    def _reg_moves_piece(self, square):
        """
        Args:
            square : Square (square we want to check the possible moves of)

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
        """ 
        Executes a move given a move tree, randomly deciding which
        of the children to follow.
        Turns a piece into a king if it is at the end of the board.

        Args:
            move : Move (tree of moves)
        
        Returns: None
        """

        if move.can_execute():
            cur_move = move
            while bool(cur_move.children):
                index = random.randint(0, len(cur_move.children)-1)
                moving_piece = cur_move.location.piece
                cur_move.location.piece = None
                cur_move.children[index].location.piece = moving_piece
                cur_move = cur_move.children[index]
            if cur_move.dead_squares:
                for dead_square in cur_move.dead_squares:
                    dead_square.piece = None
                    self.consecutive_non_jump_moves = 0
            else:
                self.consecutive_non_jump_moves += 1
                    #print("killed: " + "[" + str(dead_square.row) + "," + str(dead_square.col) + "]")
            
            #check if we are kinging
            if cur_move.location.row == 0:
                if moving_piece.color.value == PieceColor.RED.value:
                    moving_piece.is_king = True
            if cur_move.location.row == self._board_dim -1:
                if moving_piece.color.value == PieceColor.BLACK.value:
                    moving_piece.is_king = True
        else:
            pass
    
    def make_random_move(self, piece_color):
        """
        Makes a random valid move given a piece's color.

        Args:
            piece_color : Enum(PieceColor)
        
        Returns:
            None
        """
        move_list = self.valid_moves(piece_color)
        random.shuffle(move_list)
        if len(move_list) == 0:
            return None
            #print("WIN")
            #exit()
        i = 0
        while not move_list[i].can_execute():
            i += 1
        #for move in move_list:
            #print(move)
        self.execute_move(move_list[i])

    def execute_single_move(self, move, child):
        """
        Executes a single move given a move and a child index specifying
        which of the children-moves the method will execute.

        Args:
            move: Move
            child: int

        Returns:
            None
        """
        moving_piece = move.location.piece
        move.children[child].location.piece = moving_piece
        move.location.piece = None
        if move.children[child].dead_squares:
            for dead_square in move.children[child].dead_squares:
                dead_square.piece = None
                self.consecutive_non_jump_moves = 0
                #print("killed: " + "[" + str(dead_square.row) + "," + str(dead_square.col) + "]")
        else:
            self.consecutive_non_jump_moves += 1
        
        if move.children[child].location.row == 0:
            if moving_piece.color.value == PieceColor.RED.value:
                moving_piece.is_king = True
        if move.children[child].location.row == self._board_dim -1:
            if moving_piece.color.value == PieceColor.BLACK.value:
                moving_piece.is_king = True
    
    def execute_single_move_rand(self, move, child):
        """
        Executes a single move given a move and a child index specifying
        which of the children-moves the method will execute. Then
        randomly finishes the move from there.

        Args:
            move: Move
            child: int

        Returns:
            None
        """
        moving_piece = move.location.piece
        move.children[child].location.piece = moving_piece
        move.location.piece = None
        if move.children[child].dead_squares:
            for dead_square in move.children[child].dead_squares:
                dead_square.piece = None
                self.consecutive_non_jump_moves = 0
                #print("killed: " + "[" + str(dead_square.row) + "," + str(dead_square.col) + "]")
        else:
            self.consecutive_non_jump_moves += 1
        if move.children[child].can_execute():
            self.execute_move(move.children[child])
        
        if move.children[child].location.row == 0:
            if moving_piece.color.value == PieceColor.RED.value:
                moving_piece.is_king = True
        if move.children[child].location.row == self._board_dim -1:
            if moving_piece.color.value == PieceColor.BLACK.value:
                moving_piece.is_king = True

    def is_done(self, piece_color):
        """
        Returns if the game is done, i.e. someone has won.
        
        Returns:
            bool (True if piece_color has no valid moves left or 
                move count exceded, False otherwise)
        """
        if self._resigned:
            #game ends bc one player resigned or agreed to draw
            return True
        elif self.consecutive_non_jump_moves >= 80:
            #draw by 40-move rule
            return True

        #we must check if there is a valid move of the piece_color player
        move_list = self.valid_moves(piece_color)
        for move in move_list:
            if move.can_execute():
                return False
        #no executeable moves for piece_color
        self._winner = opposite_color[piece_color]
        return True
    
    def resign_game(self, piece_color):
        """
        The player of piece_color resigns the game. The other
        player is the winner.

        Args:
            piece_color: Enum(PieceColor)

        Returns:
            None
        """
        self._resigned = True
        self._winner = opposite_color[piece_color]

    def draw_game(self):
        """
        The players draw the game. There is no winner.

        Args: None
        Returns: None
        """
        self._resigned = True
        self._winner = None

    def get_winner(self):
        """
        Returns self._winner.

        Args: None
        Returns: self._winner.
        """
        return self._winner

    def _populate(self):
        """ 
        Populates the board with squares containing pieces and pieces.
        Additionally, it resets the board to a starting state if called.
        
        Args: None
        Returns: None
        """
        #1st loop - populate board
        for i in range(self._board_dim): #row
            for j in range(self._board_dim): #col
                if (i+j) % 2 == 1:
                    if i < self._size:
                        self.get_board().board[i][j].piece = Piece(PieceColor.BLACK)
                    elif i > self._size+1:
                        self.get_board().board[i][j].piece = Piece(PieceColor.RED)
                    else:
                        self.get_board().board[i][j].piece = None
                    
        #2nd loop - connections
        dirs = {"NW" : (-1, -1),          "NE" : (-1, +1),

                "SW" : (+1, -1),          "SE" : (+1, +1)}
 
        for row in self.get_board().board:
            for square in row:
                if (square.row + square.col) % 2 == 1:
                    for dir in dirs:
                        dr, dc = dirs[dir]
                        cur_row = square.row
                        cur_col = square.col
                        target_row = cur_row+dr
                        target_col = cur_col+dc
                        if 0 <= target_row < self._board_dim and 0 <= target_col < self._board_dim:
                            square.neighbors[dir] = self.get_board().board[target_row][target_col]
    

class Board:
    """
    Class for representing a board for an abritrary game.
    """
    board: List[List[Optional[PieceColor]]]
    #_board_dim: int
    #_size: int
    #_winner: Optional[PieceColor]
    _board_width: int
    _board_height: int

    def __init__(self, width, height):
        """
        Constructor

        Args:
            size (int) : no. of rows of pieces

        Returns: None
        """
        #self._size = size
        #self._board_dim = 2*size+2
        self._board_width = width
        self._board_height = height
        self.board = [[None]*self._board_width for _ in range(self._board_height)]
        self._populate()

    def _populate(self):
        """
        Populates the board with square objects. 

        Args: None

        Returns: None
        """
        for i in range(self._board_height): #row
            for j in range(self._board_width): #col
                self.board[i][j] = Square(i,j, None)
            

    def __str__(self) -> str:
        """
        Represents the board as a string.

        Returns:
            str
        """
        s = ""
        for row in self.board:
            for square in row:
                s += str(square)
            s += "\n"
        return s
    
        


class Square:
    """
    Class for the squares on the board.
    """
    def __init__(self, row, col, piece, highlighted=False) -> None:
        """
        Constructor
        
        Args:
            row (int) : row value of the square
            col (int) : column value of the square
            piece (Piece) : if there is a piece on the board
            highlighted (bool) : True if this is a possible move
        """
        self.piece = piece
        self.row = row
        self.col = col
        self.neighbors = {'NW' : None, 'NE' : None, 'SE' : None, 'SW' : None}
        self.hl = highlighted

    def __str__(self) -> str:
        """ Returns a string representation of what is on the square."""
        if self.hl:
            return "hl"
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
            piece_color : Enum(PieceColor)
            is_King : boolean
        """
        self.is_king = is_king
        self.color = piece_color

    def move_directions(self):
        """ Returns a list of the possible directions a piece could move."""
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
        """ Returns string representation, DFS-like. """
        s = "[" + str(self.location.row) + "," + str(self.location.col)+ "]"
        for move in self.children:
            s += str(move)
        return s
    
    def can_execute(self):
        return bool(self.children) #shortcut to say  
"""
Example code to run a simulation random game

board_size = 3
c = Checkers(board_size)
BLACK = c.get_board().board[0][1].piece.color
RED = c.get_board().board[2*board_size+1][0].piece.color

for i in range(100):
    print("RED MOVE")
    c.make_random_move(RED)
    print(c)
    input("Press Enter to continue...")

    print("BLACK MOVE")
    c.make_random_move(BLACK)
    print(c)
    input("Press Enter to continue...")
"""