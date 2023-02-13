"""
from enum import Enum
PiecePlayer = Enum("PiecePlayer", ["P1", "P2"])
"""

class Board:
    """
    Class for representing the checkers board.
    """
    def __init__(self, size, is_computer=False):
        """
        Takes in a size and represents the checkers board.
        """ 
        self.is_computer = is_computer

        board_size = 2*size+2
        self.grid = [[0]*board_size]*board_size
        self.populate()
        self.possible_moves = valid_moves(player1)

    def _populate(self):
        """
        Fills the board grid with Piece objections.
        """
    
    def valid_moves(self, player):
        """
        Returns the set of possible moves for a certain player.
        Calls jump_moves and reg_moves.
        (if jump_moves empty, returns reg_moves. If jump_moves non-empty return.)
        
        Parameters:
            player : int
        
        Returns:
            dictionary
        """

    def jump_moves(self, player):
        """
        Loops through the pieces of the player and returns the moves that
        are jump moves. Recursively calls _jump_recurse to figure out possible 
        multi-jump moves.

        Parameters:
            player : int
        
        Returns:
            dictionary[tuple] -> dictionary
                dictionary[coordinate] -> dictionary
        """
    
    def _jump_recurse(piece)
        """
        recursively finds the possible moves for a piece.

        Parameters:
            piece : tuple

        Returns: 
            dictionary
        """

    def reg_moves(self, player):
        """
        Loops through the pieces of the player and returns the moves that are
        regular moves, i.e. one-square moves.

        Parameters:
            player : int
        
        Returns:
            dictionary
        """

class Piece:
    """
    Class representing individual pieces.
    """
    def __init__(is_king=False, posX, posY, piece_dir):
        """
        Parameters:
            is_King : boolean
            posX : int
            posY : int
            piece_dir : int (either 1 for player 1, -1 for player 2)
        """
        self.is_king = is_king
        self.x = posX
        self.y = posY
        self.color = piece_color