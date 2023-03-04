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
# Notes:
# - exit() method in make_random_move class not defined
# - running into error in line 274 of checkers.py code where
# moving_piece is apparently a NoneType object

class Bot:
    """
    Bot that chooses the move with the most points:
  
    - King move is +6 points, Long Jump move is +3 points, Jump move is +1
    point, and Center Move (which avoids moving pieces at the ends of the
    board) is +1. Random move is +0. 

    subgame_suggest abides by the following strategy:
    - For all possible moves, play a mini-game (using basic bots) up to depth
    and associate with it a score. Then, choose the move with the highest score.

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
        self._size = self._checkers._size


    def basic_suggest(self) -> list[tuple[Moves, int], int]:
        """
        Suggests a move according to the standards above.

        Returns: (move, index) --> (Move, int)
        """
        # possible_mvs retrieves all possible moves for this bot's color
        possible_mvs = self.non_empties(self._checkers.valid_moves(self._color))
        high_score = -math.inf
        best_moves = {}
        # Loop through possible_mvs and find highest scoring move
        for mv in possible_mvs:
            for ind in range(len(mv.children)):
                # Call helper method get_score
                cur_score = self.get_score(self._color, mv, ind, self, possible_mvs)
                if cur_score > high_score:
                    best_moves = {mv : [ind]}
                    high_score = cur_score
                if cur_score == high_score:
                    if mv in best_moves:
                        best_moves[mv].append(ind)
                    else:
                        best_moves[mv] = [ind]
        best = self.choose_rand(best_moves)
        # Return the move in addition to the score
        return best + [high_score]
        
    def subgame_suggest(self, depth):
        """
        For each possible valid moves, this method finds the move which leads
        to the highest score if two basic bots (using basic_suggest) were
        to play out another depth-many moves after playing that one.

        Returns: (move, index) --> (Move, int)
        """
        possible_mvs = self.non_empties(self._checkers.valid_moves(self._color))
        high_score = -math.inf
        cur_best = None
        for mv in possible_mvs:
            for ind in range(len(mv.children)):
                cur_score = self.subgame_score(mv, ind, depth, possible_mvs)
                if cur_score > high_score:
                    high_score = cur_score
                    cur_best = (mv, ind)
        return cur_best
    
    def get_score(self, color, mv, ind, bot, possible_mvs):
        """
        Given a color, move, a corresponding index, and a bot, this method
        gets the score 

        Returns: (move, index) --> (Move, int)
        """
        kinging_mvs = bot.kinging_moves(possible_mvs)
        long_jump_mvs = bot.longest_jump(possible_mvs)
        center_mvs = bot.center_moves(possible_mvs)

        # Add to score to incorporate all information
        score = 0
        row = mv.location.row
        can_jump = bot._checkers.jump_moves(color)[1]
        if can_jump:
            score += 1
            if mv in long_jump_mvs and ind in long_jump_mvs[mv]:
                print(f"found long jump move {mv}")
                score += 3
        if mv in kinging_mvs and ind in kinging_mvs[mv]:
            print(f"found king move {mv}")
            score += 5
        if mv in center_mvs and ind in center_mvs[mv]:
            print(f"found center move {mv}")
            score += 1
        if (row == 0 or row == self._checkers._board_dim - 1):
            score -= 4
        return score
    
    def opposite_color(self, color):
        if color == PieceColor.RED:
            return PieceColor.BLACK
        return PieceColor.RED

    def subgame_score(self, mv, ind, depth, possible_mvs):
        """
        Given a move, a corresponding index, and a depth number, this method
        plays a game between two basic bots (using basic_suggest) depth-many
        moves ahead, adding to the score the first_bot's moves and subtracting
        the opposite colored bot's moves.

        Returns: (move, index) --> (Move, int)
        """
        # PROBLEM: deepcopy seems to not create a deep copy of the board state
        sub_game = copy.deepcopy(self._checkers)
        first_bot = Bot(sub_game, self._color)
        score = self.get_score(self._color, mv, ind, first_bot, possible_mvs)

        print("SUBGAME 1")
        print(self._checkers)
        sub_game.execute_single_move(mv, ind)
        print("SUBGAME 2")
        print(self._checkers)

        opp = self.opposite_color(self._color)
        second_bot = Bot(sub_game, opp)
        color = opp
        i = depth
        # play i many moves ahead using basic_suggest
        while i > 0:
            if color == opp:     
                mv, ind, scr = second_bot.basic_suggest()
                score = score - scr
                sub_game.execute_single_move(mv, ind)
                if sub_game.is_done(self.opposite_color(color)):
                    score = score - 100
                    break
                color = self._color
            else:   
                mv, ind, scr = first_bot.basic_suggest()
                score = score + scr
                sub_game.execute_single_move(mv, ind)
                if sub_game.is_done(self.opposite_color(color)):
                    score = score + 100
                    break
                color = opp
            i = i - 1
        return score

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
        # set max to 1 so we only get multi-jumps
        curr_max = 1
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
        return [rand_mv, rand_child]
    
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
        # Avoid moving pieces on the ends of the board
        curr_x = mv.location.col
        potential_x = mv.children[child_ind].location.col
        if self.is_toward_center(curr_x, potential_x):
            if mv in center_dict:
                center_dict[mv].append(child_ind)
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
        is_red = self._color.value == PieceColor.RED.value
        # Check to see if piece is at the end of the board
        if child.location.row == 0 and is_red:
                add_mv = True
        if child.location.row == self._checkers._board_dim - 1 and not(is_red):
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
        if float(x_1) < (self._checkers._board_dim / 2) - 0.5 and x_1 < x_2:
                return True
        if float(x_1) > (self._checkers._board_dim / 2) - 0.5 and x_1 > x_2:
                return True
        return False
    
# Testing Code Below
bot_wins = 0
rand_wins = 0

for i in range(1):
    game = Checkers(3)
    black = PieceColor.BLACK
    red = PieceColor.RED
    comp1 = Bot(game, red)
    prev = black
    j = 2
    while (not game.is_done(red)) and (not game.is_done(black)) and j>0:
        print(game)
        j -= 1
        print("THE COPY BEFORE EXECUTION: ")
        cpy = copy.deepcopy(game)
        print(cpy)
        move, index, scr = comp1.basic_suggest()
        cpy.execute_single_move(move, index)
        print("THE COPY AFTER EXECUTION: ")
        print(cpy)
        break
        if prev == black:
            move, index, scr = comp1.basic_suggest()
            game.execute_single_move(move, index)
            prev = red
        else:
            possible_mvs = comp1.non_empties(comp1._checkers.valid_moves(black))
            move, index = comp1.choose_rand(comp1.to_dict(possible_mvs))
            game.execute_single_move(move, index)
            prev = black
    if game.is_done(red):
        rand_wins += 1
    else:
        bot_wins += 1
    print(f"bot won {bot_wins} games, random won {rand_wins} games")





"""  def simple_suggest(self) -> list[tuple[Moves, int], int]:
        #Best scoring seems to be 5, 3, 1
        possible_mvs = self.non_empties(self._checkers.valid_moves(self._color))
        kinging_mvs = self.kinging_moves(possible_mvs)
        move_found = False
        can_jump = self._checkers.jump_moves(self._color)[1]

        if kinging_mvs:
            move = self.choose_rand(kinging_mvs)
            move_found = True
        
        if (not move_found) and can_jump:
            long_jump_mvs = self.longest_jump(possible_mvs)
            move = self.choose_rand(long_jump_mvs)
            move_found = True

        if not move_found:
            center_mvs = self.center_moves(possible_mvs)
            if center_mvs:
                move = self.choose_rand(center_mvs)
                move_found = True

        if not(move_found):
            move = self.choose_rand(self.to_dict(possible_mvs))
        return move
"""