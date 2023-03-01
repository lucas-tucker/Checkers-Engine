"""
Bots for Connect-M

(and command for running simulations with bots)
"""
import random
import copy
import math
from typing import Union

from checkers import Checkers, Board, Piece, Moves, Square, PieceColor

#
# BOTS
#
# exit() method in make_random_move class not defined


class Bot:
    """
    Simple Bot that abides by the following strategy:
    - If jumping moves are available, first choose one which kings a piece.
    Otherwise, choose one which jumps toward the center of the board. Then,
    choose one of the longest jumps. If all the same length, then choose at random.

    - If no jumping moves are available, first choose that which kings a piece.
    Then, move a piece toward the center. Otherwise, move a piece not on squares
    1 and 3 (for white) and not on 30 and 32 (for black), otherwise choose
    random move.

    https://hobbylark.com/board-games/Checkers-Strategy-Tactics-How-To-Win
    """

    _checkers: Checkers
    _color: PieceColor

    def __init__(self, checkers: Checkers, color: PieceColor):
        """ Constructor

        Args:
            checkers: Checkers object the bot will use as guide
            color: Bot's color
        """
        self._checkers = checkers
        self._color = color

    def suggest_move(self, need_score=False) -> list[tuple[Moves, int], int]:
        """
        Suggests a move according to the standards above.

        Returns: (move, index) --> (Move, int)
        """
        score = None
        possible_mvs = self.non_empties(self._checkers.valid_moves(self._color))
        kinging_mvs = self.kinging_moves(possible_mvs)
        move_found = False
        can_jump = self._checkers.jump_moves(self._color)[1]

        if kinging_mvs:
            print("found king")
            move = self.choose_rand(kinging_mvs)
            move_found = True

        if not move_found:
            center_mvs = self.center_moves(possible_mvs)
            if center_mvs:
                print("found center_move")
                move = self.choose_rand(center_mvs)
                move_found = True
        
        if (not move_found) and can_jump:
            long_jump_mvs = self.longest_jump(possible_mvs)
            print("found long_jump")
            move = self.choose_rand(long_jump_mvs)
            move_found = True

        if not(move_found):
            print(self.to_dict(possible_mvs))
            move = self.choose_rand(self.to_dict(possible_mvs))
        
        return [move, score]
    
    def beta_depth_smartbot(self, depth):
        possible_mvs = self.non_empties(self._checkers.valid_moves(self._color))
        high_score = -math.inf
        cur_best = None
        for mv in possible_mvs:
            for ind in range(len(mv.children)):
                cur_score = self.smartbot_score(mv, ind, depth)
                if cur_score > high_score:
                    cur_best = (mv, ind)
        return cur_best

    def smartbot_score(self, mv, ind, depth):
        sub_game = copy.deepcopy(self._checkers)
        sub_game.execute_single_move(mv, ind)
        score = 0
        i = depth
        first_bot = Bot(sub_game, self._color)
        # NEED TO IMPLEMENT OPPOSITE COLOR
        second_bot = Bot(sub_game, self.opposite_color(self._color))
        while i > 0:
            next_move = sub_game.suggest_move()
            score += next_move[1]

        return 

    def non_empties(self, mvs):
        """
        Given a list of Moves objects, each corresponding to a piece of the
        bot's color, this method returns a new list of those Moves objects with
        nonempty children (all valid moves). 

        Returns: list[Moves]
        """
        non_empty_lst = []
        for mv in mvs:
            if mv.children:
                non_empty_lst.append(mv)
        return non_empty_lst
        
    def to_dict(self, mvs_lst):
        """
        Given a list of Moves objects, this method returns a dictionary which 
        maps each Moves object to its children. 

        Returns: dict{Moves : list[int]}
        """
        mv_dict = {}
        for mv in mvs_lst:
            mv_dict[mv] = list(range(len(mv.children)))
        return mv_dict

    def longest_jump(self, possible_mvs):
        """
        Given a list of possible squares (moves), returns a dictionary of moves
        associated with a sublist of their respective children such that 
        each move-child pair leads to a jump-sequence with an equal number of 
        total jumps. 

        Returns: Dict(Move: [int])
        """
        curr_max = 0 
        jump_dict = {}
        for mv in possible_mvs:
            # Get subtree height and corresponding indices for each Moves obj.
            mv_height, indices = self.jump_length(mv)
            # Replace dictionary with current Move if exceeds previous max jumps
            if mv_height > curr_max:
                curr_max = mv_height
                jump_dict = {mv: indices}
            # Add to dictionary if current Move matches previous max jumps
            if mv_height == curr_max:
                jump_dict[mv] = indices
        return jump_dict

    def choose_rand(self, move_dict):
        """ 
        Given a dictionary which maps Moves to lists of child indices, this
        method returns a random Move-index tuple corresponding to one move on
        the board. 

        Args:
            move_dict: dict{Moves: list[int]}
        
        Returns:
            (Moves, int)
        """
        rand_mv = random.choice(list(move_dict.items()))[0]
        rand_child = random.choice(move_dict[rand_mv])
        return (rand_mv, rand_child)
    
    def jump_length(self, mv):
        """ 
        Given a Moves object, this method returns a tuple consisting of the 
        maximum length of a jump-sequence based on the Moves tree as the first
        element, and a list of the indicies which correspond to sequences of
        this length as the second element.

        Args:
            mv: Moves
        
        Returns:
            (int, list[int])
        """
        max = 0
        jump_lst = []
        for ind, child in enumerate(mv.children):
            # Find longest move subtree
            child_height = self.num_jumps(child)
            # Replace index list with ind if subtree height greater than max
            if child_height > max:
                max = child_height
                jump_lst = [ind]
            # Add index if subtree height matches the maximum
            if child_height == max:
                jump_lst.append(ind)
        return (max, jump_lst)
            
    def num_jumps(self, mv):
        """ 
        Given a Moves tree, this method returns the height of the tree,
        corresponding to the longest sequence of jumps off of the move mv.

        Args:
            mv: Moves
        
        Returns:
            int
        """
        mv_lst = [0]
        for child in mv.children:
            mv_lst.append(1 + self.num_jumps(child))
        return max(mv_lst)
        
    def center_moves(self, move_lst) -> dict:
        """ 
        Given a list of Moves objects, returns a dictionary which maps Moves
        to their subindices which correspond to a center move.

        Args:
            move_lst: list[Moves]
        
        Returns:
            dict{Moves: list[int]}
        """
        center_dict = {}
        for mv in move_lst:
            for child_ind in range(len(mv.children)):
                self.update_center_dict(mv, child_ind, center_dict)
        return center_dict

    def update_center_dict(self, mv, child_ind, center_dict):
        """ 
        Given a move, its child sub-index, and a dictionary which maps move
        objects to lists of child subindices, this method adds to the dictionary
        the move-index pair which corresponds to a center move. This method 
        does not return anything.

        Args:
            mv : Moves
            ind : int
            center_dict : dict{Moves : list[int]}
        """
        curr_x = mv.location.col
        potential_x = mv.children[child_ind].location.col
        if self.is_toward_center(curr_x, potential_x):
            if mv in center_dict:
                center_dict.append(child_ind)
            else:
                center_dict[mv] = [child_ind]

    def kinging_moves(self, move_lst) -> dict:
        """ 
        Given a list of Moves objects, returns a dictionary which maps Moves
        to their subindices which correspond to a kinging move.

        Args:
            move_lst: list[Moves]
        
        Returns:
            dict{Moves: list[int]}
        """
        king_dict = {}
        for mv in move_lst:
            if not(mv.location.piece.is_king):
                for ind, child in enumerate(mv.children):
                    self.update_king_dict(mv, ind, child, king_dict)
        return king_dict

    def update_king_dict(self, mv, ind, child, king_dict):
        """ 
        Given a move, its child sub-index, and a dictionary which maps move
        objects to lists of child subindices, this method adds the move and its
        appropriate subindex which corresponds to a king move. This method does
        not return anything.

        Args:
            mv : Moves
            ind : int
            king_dict : dict{Moves : list[int]}
        """
        add_mv = False
        if child.location.row == 0:
            if self._color.value == PieceColor.RED.value:
                add_mv = True
        if child.location.row == self._checkers._board_dim - 1:
            if self._color.value == PieceColor.BLACK.value:
                add_mv = True
        if add_mv:
            if mv in king_dict:
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
        if float(x_1) < (self._checkers._size / 2) - 0.5 and x_1 < x_2:
                return True
        if float(x_1) > (self._checkers._size / 2) - 0.5 and x_1 > x_2:
                return True
        return False
    
#BELOW IS TESTING CODE    
""" game = Checkers(4)
black = PieceColor.BLACK
red = PieceColor.RED
comp1 = Bot(game, PieceColor.RED)
comp2 = Bot(game, PieceColor.BLACK)
prev = red

while (not game.is_done(red)) and (not game.is_done(black)):
    print(game)
    if prev != red:
        move, index = comp1.suggest_move()[0]
        game.execute_single_move(move, index)
        prev = red
    else:
        move, index = comp2.suggest_move()[0]
        game.execute_single_move(move, index)
        prev = black """
