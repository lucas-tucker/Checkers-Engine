"""
Checkers game GUI

Author: Althea Li
"""

import pygame
from pygame.locals import *
import click
import sys

from checkers import Board, Square, Piece, Moves, PieceColor, Checkers

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

crown = pygame.transform.scale(pygame.image.load('crown.png'),(44, 25))

def draw_board(surface: pygame.surface.Surface, game, move=None):
    """
    Draws the state of the board in the window
    
    Args:
        surface: Pygame surface to draw the board on
        board: The board to draw

    Returns: None
    """
    
    grid = game.get_board().board
    board_dim = game._board_dim

    rh = HEIGHT / (board_dim)
    cw = WIDTH / (board_dim)
    for row in range(board_dim):
        for col in range(board_dim):
            rect = (col * cw, row * rh, cw, rh)
            if (row + col)%2 == 0:
                pygame.draw.rect(surface, color=White, rect=rect, width=0)
            else:
                pygame.draw.rect(surface, color=Black, rect=rect, width=0)

    for i, row in enumerate(grid):
        for j, square in enumerate(row):
            if square.is_empty():
                continue
            is_king = square.piece.is_king
            color = square.piece.color
            circle_color = None
            king_color = None
            if color == PieceColor.BLACK:
                circle_color = (52, 110, 235)
                if is_king:
                    king_color = (107, 141, 191)
            elif color == PieceColor.RED:
                circle_color = (255, 0, 0)
                if is_king:
                    king_color = (217, 113, 151)

            center = (j * cw + cw // 2, i * rh + rh // 2)
            radius = rh // 2 - (rh//10)
            pygame.draw.circle(surface, color=circle_color,
                               center=center, radius=radius)
            if is_king:
                king_radius = radius - (rh//6)
                pygame.draw.circle(surface, color=king_color, center=center, radius=king_radius)
                surface.blit(crown, center[0], center[1])

    border_size = int(rh // 12)
    if move is not None:
        r = move.location.row
        c = move.location.col
        rect = (c * cw, r * rh, cw, rh)
        pygame.draw.rect(surface, color=Dark_Gray, rect=rect, width=border_size)
        for move in move.children:
            row = move.location.row
            col = move.location.col
            rect = (col * cw, row * rh, cw, rh)
            pygame.draw.rect(surface, color=(148, 214, 81), rect=rect, width=border_size)

def play_checkers(game):
    """
    Plays a game of checkers on a Pygame window

    Args:
        board: The board to play on

    Returns: None

    """
    current = PieceColor.BLACK
    current_move = None

    opposite_color = {}
    opposite_color[PieceColor.RED] = PieceColor.BLACK
    opposite_color[PieceColor.BLACK] = PieceColor.RED

    pygame.init()
    pygame.display.set_caption("Checkers")
    surface = pygame.display.set_mode([WIDTH, HEIGHT])
    clock = pygame.time.Clock()

    pygame.key.set_repeat(1,10)

    draw_board(surface, game)

    board_dim = game._board_dim
    square_size = HEIGHT // (board_dim)

    locked_in = False

    is_done= game.is_done(current)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos_x, pos_y = pygame.mouse.get_pos() #row is y, col is x
                select_row = pos_y//square_size
                select_col = pos_x//square_size
                square = game.get_board().board[select_row][select_col]
                """
                print("pos_x: " + str(pos_x))
                print("pos_y: " + str(pos_y))
                print("row: " + str(select_row))
                print("col: " + str(select_col))
                """
                if current_move is not None:
                    move_dict = {}
                    for i, move in enumerate(current_move.children):
                        future_move_row = move.location.row
                        future_move_col = move.location.col
                        move_dict[(future_move_row, future_move_col)] = i
                    index = None
                    try:
                        index = move_dict[(select_row, select_col)]
                        game.execute_single_move(current_move, index)
                        locked_in = True
                        if current_move.children[index].can_execute():
                            current_move = current_move.children[index]
                        else:
                            current = opposite_color[current]
                            current_move = None
                            locked_in = False
                    except:
                        pass
                    
                if square.has_piece() and not locked_in:
                    if square.piece.color == current:
                        piece_valid_move = game.piece_valid_moves((select_col, select_row), current)
                        current_move = piece_valid_move[2]
            if event.type == pygame.KEYDOWN and locked_in == False:
                if 'r' == event.unicode:
                    game.make_random_move(current)
                    current = opposite_color[current]
                    current_move = None

        draw_board(surface, game, current_move)
        pygame.display.update()
        clock.tick(24)
        is_done = game.is_done(current)
        if is_done:
            winner = opposite_color[current].name
            print(winner)
            
            font = pygame.font.Font('freesansbold.ttf', 32)
            if winner == PieceColor.BLACK:
                winstr='Black'
            else:
                winstr='Red'

            text = font.render(winstr +'wins!', True, Black, Red)
            textRect = text.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT // 2)
            surface.blit(text, textRect)

"""
board_size = 1
c = Checkers(board_size)
c.get_board().board[0][1].piece.is_king = True
c.get_board().board[2*board_size+1][0].piece.is_king = True
play_checkers(c)
"""

@click.command(name = "checkers-gui")
@click.option('--size', default = 3)
def cmd(size):
    board_size = size
    c = Checkers(board_size)
    play_checkers(c)

if __name__ == '__main__':
    cmd()