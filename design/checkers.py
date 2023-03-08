
from enum import Enum
from typing import Optional, List
PieceColor = Enum("PieceColor", ["RED", "BLACK"])


class Checkers:
    """
    Class for representing all the checkers game logic. Uses the Board,
    Square, Move, and Piece classes.
    """
    _game_board: object
    _board_dim: int
    _size: int
    _winner: Optional[PieceColor]
    consecutive_non_jump_moves: int
    _resigned: bool

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

    def get_board(self):
        """
        Returns the board.

        Args: None
        Returns: Board
        """

    def valid_moves(self, piece_color):
        """
        Returns the set of possible moves for a certain player.
        Calls jump_moves and reg_moves.

        Args:
            piece_color : Enum(PieceColor)
        
        Returns:
            list[Move]
        """

    def jump_moves(self, piece_color):
        """
        Returns the jumping-moves of a particular color, and whether
        any of them are jumping moves.

        Args:
            piece_color : Enum(PieceColor)
        
        Returns:
            list[Move], bool
        """

    def _jump_moves_piece(self, square):
        """
        Private method

        Args:
            square : Square (start of the move tree)

        Returns:
            Move, bool

        """

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

    def reg_moves(self, piece_color):
        """
        Finds all the regular moves of a certain piece_color.

        Parameters:
            piece_color : Enum PieceColor
        
        Returns:
            list[Moves]
        """

    def _reg_moves_piece(self, square):
        """
        Args:
            square : Square (square we want to check the possible moves of)

        Returns:
            Moves
        """

    def execute_move(self, move):
        """ 
        Executes a move given a move tree, randomly deciding which
        of the children to follow.
        Turns a piece into a king if it is at the end of the board.

        Args:
            move : Move (tree of moves)
        
        Returns: None
        """

    def make_random_move(self, piece_color):
        """
        Makes a random valid move given a piece's color.

        Args:
            piece_color : Enum(PieceColor)
        
        Returns:
            None
        """

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

    def is_done(self, piece_color):
        """
        Returns if the game is done, i.e. someone has won.
        
        Returns:
            bool (True if piece_color has no valid moves left or 
                move count exceded, False otherwise)
        """

    def resign_game(self, piece_color):
        """
        The player of piece_color resigns the game. The other
        player is the winner.

        Args:
            piece_color: Enum(PieceColor)

        Returns:
            None
        """

    def draw_game(self):
        """
        The players draw the game. There is no winner.

        Args: None
        Returns: None
        """

    def _populate(self):
        """ 
        Populates the board with squares containing pieces and pieces.
        Additionally, it resets the board to a starting state if called.
        
        Args: None
        Returns: None
        """

class Board:
    """
    Class for representing a board for an abritrary game.
    """
    board: List[List[Optional[PieceColor]]]
    _board_width: int
    _board_height: int

    def __init__(self, width, height):
        """
        Constructor. Initializes the board as a list of lists, then
        calls _populate() to populate the board with squares.

        Args:
            size (int) : no. of rows of pieces
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

class Square:
    """
    Class for the squares on the board.
    We use this as a graph structure.
    """
    def __init__(self, row, col, piece, highlighted=False) -> None:
        """
        Constructor. Initializes a square, which does not connect to any 
        neighbors, and exists at a location with a piece on it.
        
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
        """ 
        Returns a string representation of what is on the square.
        Returns different things depending on if there is no piece, 
        a red piece, a black piece, or a king piece, or some combination.

        Args: None

        Returns: str
        """

    def has_piece(self):
        """ 
        Checks if piece exists on the square. 
        Returns true the square has a piece.
        
        Args: None
        
        Returns: bool
        """
    
    def is_empty(self):
        """ 
        Returns true if there is no piece. 
        
        Args: None

        Returns: bool 
        """
    
    def has_color(self, piece_color):
        """ 
        Checks if the piece is of the color we want. 
        
        Args: piece_color (what piece color we want to look for)
        
        Returns: bool (True if the piece's color and piece_color agrees.)
        """


class Piece:
    """
    Class representing individual pieces. Has some data unique to checkers,
    such as piece_color being red/black, and is_king being whether the
    piece is a kinged piece or not.
    """
    is_king: bool

    def __init__(self, piece_color, is_king=False):
        """
        Initializes the piece.

        Parameters:
            piece_color : Enum(PieceColor)
            is_king : boolean
        """
        self.is_king = is_king
        self.color = piece_color

    def move_directions(self):
        """ 
        Returns a list of the possible directions a piece could move.
        If it is a king, it is all four. If it is red, and not king, we can 
        move "up" the board. If it is black, and not king, we can move 
        "down" the board.
        
        Args: None
        
        Returns: list[str]
        """


class Moves:
    """
    Class representing possible moves a piece could take using a tree
    structure.
    """
    def __init__(self, square, dead) -> None:
        """
        Initializes the move tree. We want a square that is the head of the move
        tree, and has no children, and the move jumps over no pieces, so 
        there are no dead squares.

        Args:
            square : Square (current location)
            dead : set[Square] (list of dead squares)
            """
        self.location = square
        self.dead_squares = dead
        self.children = [] #set of moves
    
    def add_move(self, square, new_dead):
        """
        Adds a move to the move tree.

        Args:
            square : Square (current location)
            new_dead = Square (just jumped over)
        """
    
    def __str__(self):
        """ 
        Returns string representation of the movetree, DFS-like. 

        Args: None

        Returns: str
        """
    
    def can_execute(self):
        """
        Since we wish to have a move tree for every piece, we also want to know
        whether or not a move is executable. Returns true if it has children,
        false if not.
        """

