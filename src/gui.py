"""
Checkers game GUI

Author: Althea Li
"""

import pygame
from pygame.locals import *
import click
import sys

from checkers import Board, Square, Piece, Moves, PieceColor

from enum import Enum

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

try:
    os.environ["DISPLAY"]
except: 
    os.environ["SDL_VIDEODRIVER"] = 'windib'
os.environ['SDL_AUDIODRIVER'] = 'dsp'
os.environ["SDL_VIDEO_CENTERED"] = '1'

pygame.init()

Board_width = 3 # or range from 6 to 20
Empty_Grid = "Empty_Grid"
Grid_pixelsize = 100
Black = (0, 0, 0)
Red = ( 255, 0, 0)
Light_Brown = ( 200, 157, 124)
Dark_Brown = ( 105, 53, 36)
Dark_Gray = (100, 100, 100)
Gray = (180, 180, 180)
White = (255,255,255)
Background = Gray

WIDTH = 600
HEIGHT = 600
"""
def draw_board(surface: pygame.surface.Surface, board):
    Draws the state of the board in the window
    
    Args:
        surface: Pygame surface to draw the board on
        board: The board to draw

    Returns: None
    
    grid = board._board
    board_dim = board._board_dim

    rh = HEIGHT / (board_dim + 1)
    cw = WIDTH / (board_dim+1)
    for row in range(board_dim):
        for col in range(board_dim):
            rect = (col * cw, row * rh, cw, rh)
            if (row + col)%2 == 0:
                pygame.draw.rect(surface, color=White, rect=rect, width=2)
            else:
                pygame.draw.rect(surface, color=Black, rect=rect, width=2)
"""

def play_checkers(board):
    """
    Plays a game of checkers on a Pygame window

    Args:
        board: The board to play on

    Returns: None

    """
    current = PieceColor.BLACK


    pygame.display.set_caption("Checkers")


    pygame.display.set_mode([600,600])

    pygame.display.list_modes()
    clock = pygame.time.Clock()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        #draw_board(surface, board)
        pygame.display.update()
        clock.tick(24)

b = Board(3)
play_checkers(b)
