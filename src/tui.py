"""
Checkers game Terminal User Interface.

Current Status : Reading code from checkers.py to understand where to begin

Done By : Niko
"""
from checkers import Board, Square, Piece, Moves
from rich.console import Console

console = Console()

def board_printing():
    b = Board(3)
    