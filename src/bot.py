"""
Bots for Connect-M

(and command for running simulations with bots)
"""
import random
import copy
from typing import Union

import click
from design import Board, Piece, Moves, Square, PieceColor

#
# BOTS
#

class Bot:
    """
    Simple Bot that abides by the following strategy:
    - If jumping moves are available, first choose that which kings a piece.
    Otherwise, choose that which jumps toward the center of the board. Then,
    choose the longest jump. If all the same length, then choose at random.

    - If no jumping moves are available, first choose that which kings a piece.
    Then, move a piece toward the center. Otherwise, move a piece not on squares
    1 and 3 (for white) and not on 30 and 32 (for black), otherwise choose
    random move.

    https://hobbylark.com/board-games/Checkers-Strategy-Tactics-How-To-Win
    """

    _board: Board
    _color: str
    _opponent_color: str

    def __init__(self, board: Board, color: str,
                 opponent_color: str, player: int):
        """ Constructor

        Args:
            board: Board the bot will play on
            color: Bot's color
            opponent_color: Opponent's color
        """
        self._board = board
        self._color = color
        self._opponent_color = opponent_color

    def suggest_move(self) -> int:
        """
        Suggests a move according to the standards above.

        Returns: (move, index) --> (Move, int)
        """
        possible_mvs = Board.valid_moves(self._color)
        kinging_mvs = self.kinging_moves(possible_mvs)
        move_found = False

        if kinging_mvs:
            move = self.choose_rand(kinging_mvs)
            move_found = True

        else:
            long_jump_mvs = self.longest_jump(possible_mvs)
            if long_jump_mvs:
                if len(long_jump_mvs) > 1:
                    move = self.choose_rand(long_jump_mvs)
                    move_found = True

            if not(move_found):
                move = self.choose_rand(possible_mvs)
        
        return move
    
    def longest_jump(self, possible_mvs):
        """
        Given a list of possible squares (moves), returns a dictionary of moves
        associated with a sublist of their respective children such that 
        each move-child pair leads to a jump-sequence with an equal number of 
        total jumps. 

        Returns: Dict(Move: [int])
        """
        #Initialize max to 1 so that we only get jump moves
        max = 1 
        jump_dict = {}
        for mv in possible_mvs:
            mv_height, indices = self.jump_length(mv)
            if mv_height > max:
                max = mv_height
                jump_dict = {mv: indices}
            if mv_height == max:
                jump_dict[mv] = indices
        return jump_dict

    def choose_rand(self, move_dict):
            rand_mv = random.choice(list(move_dict.items()))
            rand_child = random.choice(move_dict[rand_mv])
            return (rand_mv, rand_child)
    
    def jump_length(self, mv):
        max = 0
        jump_lst = []
        for ind, child in enumerate(mv.children):
            child_height = self.num_jumps(child)
            if child_height > max:
                max = child_height
                jump_lst = [ind]
            if child_height == max:
                jump_lst.append(ind)
        return (max, jump_lst)
            
    def num_jumps(self, mv):
        mv_lst = [0]
        for child in mv.children:
            mv_lst.append(1 + self.jump_length(child))
        return max(mv_lst)
        
    def center_moves(self, move_lst) -> dict:
        center_dict = {}
        for mv in move_lst:
            for child_ind in range(len(mv.children)):
                self.update_center_dict(mv, child_ind, center_dict)
        return center_dict

    def update_center_dict(self, mv, child_ind, center_dict):
        curr_x = mv.location.col
        potential_x = mv.children[child_ind].location.col
        if self.is_toward_center(curr_x, potential_x):
            if center_dict[mv]:
                center_dict.append(child_ind)
            else:
                center_dict[mv] = [child_ind]

    def kinging_moves(self, move_lst):
        king_dict = {}
        for mv in move_lst:
            for ind, child in enumerate(mv.children):
                if not(child.location.piece.is_king):
                    self.update_king_dict(mv, ind, king_dict)
        return king_dict

    def update_king_dict(self, mv, ind, king_dict):
        add_mv = False
        if mv.children[ind].location.row == 0:
            if self._color.value == PieceColor.RED.value:
                add_mv = True
        if mv.children[ind].location.row == self._board._board_dim - 1:
            if self._color.value == PieceColor.BLACK.value:
                add_mv = True
        if add_mv:
            if king_dict[mv]:
                king_dict[mv].append(ind)
            else:
                king_dict[mv] = [ind]
                                
    def is_toward_center(self, x_1, x_2) -> bool:
        """ 
        Given two x positions of pieces, tells whether moving from x_1 to x_2
        is a move toward the center. 

        Args:
            x_1 : int
            x_2 : int
        
        Returns:
            bool
        """
        if float(x_1) < (self._board.size / 2) - 0.5 and x_1 < x_2:
                return True
        if float(x_1) > (self._board.size / 2) - 0.5 and x_1 > x_2:
                return True
        return False
    
    


