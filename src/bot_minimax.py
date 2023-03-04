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

class Move_Tree:
    """
    Trees for individual move-index pairs that represent all potential game
    continuations.
    """
    def __init__(self, mv, ind, opp_trees, board_state):
        self.move = mv
        self.index = ind
        self.opp_trees = opp_trees
        self.board_state = board_state

class Bot:
    """
    Minimax bot
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

    def mini_max(self, depth):
        """
        Given a depth level, this method assesses all possible moves up to the
        depth and returns the move-index pair which minimizes over worst-case
        outcomes. 
        """
        # Get possible moves for this color
        possible_mvs = self.non_empties(self._checkers.valid_moves(self._color))
        # Use get_trees to get list of trees corresponding to possible moves
        tree_list = self.get_trees(possible_mvs, self._color, depth, self._checkers)
        worst = -math.inf
        best_mv = None
        for tree in tree_list:
            worst_outcome = self.get_worst(tree, self._color)
            # Find tree with least worst possible outcome
            if worst_outcome >= worst:
                best_mv = [tree.move, tree.index]
        return best_mv
   
    def get_worst(self, tree, color):
        """
        Given a Move_Tree object and a color, this method determines the worst
        possible outcome (given by an integer score) from this tree
        """
        worst = math.inf
        # Base case is that tree has no children, so we assess state here
        if not(tree.opp_trees):
            return self.assess_state(tree.board_state, color)
        for subtree in tree.opp_trees:
            # Recursive call to get closer to the base case of tree leaves 
            cur_worst = self.get_worst(subtree, color)
            if cur_worst < worst:
                worst = cur_worst
        return worst

    def assess_state(self, board, color):
        """
        Given a board and a color, this method returns an assessment (int) of 
        the board from the standpoint of king and piece counts. 
        """
        opp_color = self.opposite_color(color)
        # Note that valid_moves returns Moves objects for each piece
        opp_mvs = board.valid_moves(opp_color)
        mvs = board.valid_moves(color)
        king_dif = 2 * (self.king_tally(mvs) - self.king_tally(opp_mvs))
        pieces_dif = len(mvs) - len(opp_mvs)
        return king_dif + pieces_dif

    def king_tally(self, mvs):
        """
        Given a list of move objects, this method returns the total number which
        correspond to king pieces.
        """
        tally = 0
        for mv in mvs:
            if mv.location.piece.is_king:
                tally += 1
        return tally

    def get_trees(self, mvs, color, depth, board):
        """
        Given a list of possible moves, a color, depth, and board, this method
        returns a tree list (one tree per move-index pair of the mvs list)
        corresponding to potential game continuations.
        """
        opp_color = self.opposite_color(color)
        tree_list = []
        for mv in mvs:
            for ind, child in enumerate(mv.children):
                new_state = self.simulate_move(board, mv, ind)
                if depth == 0:
                    tree_list.append(Move_Tree(mv, ind, [], new_state))
                else:
                    # Get all opponent's potential moves in this new state
                    opp_mvs = self.non_empties(new_state.valid_moves(opp_color))
                    # Recursive call to make tree list for this move/ind's tree
                    opp_trees = self.get_trees(opp_mvs, opp_color, depth - 1, new_state)
                    tree_list.append(Move_Tree(mv, ind, opp_trees, new_state))
        return tree_list
    
    def simulate_move(self, board, mv, ind):
        """
        Given a board, move and index, this method returns a new board state
        (a Checkers object) corresponding to if that move-index were to be 
        played.
        """
        new_state = copy.deepcopy(board)
        mv_copy = copy.deepcopy(mv)
        ind_copy = copy.deepcopy(ind)
        new_state.execute_single_move(mv_copy, ind_copy)
        return new_state
    
    def opposite_color(self, color):
        if color == PieceColor.RED:
            return PieceColor.BLACK
        return PieceColor.RED

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
    
# Testing Code Below
bot_wins = 0
rand_wins = 0

for i in range(10):
    game = Checkers(3)
    black = PieceColor.BLACK
    red = PieceColor.RED
    comp1 = Bot(game, red)
    prev = black
    while (not game.is_done(red)) and (not game.is_done(black)):
        print(game)
        if prev == black:
            move, index = comp1.mini_max(depth=3)
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
