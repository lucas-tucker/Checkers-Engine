"""
Bots for Checkers

(and command for running simulations with bots)

Author: Lucas Tucker
"""
import random
import copy
import math
from typing import Union
import click

from checkers import Checkers, Board, Piece, Moves, Square, PieceColor

# Current Win Rates:
# Depth 1: 75%
# Depth 2: 95%
# Depth 3+: 99+%

"""
Strategy source: https://www.ultraboardgames.com/checkers/tips.php
Strategy source suggests to crown kings and try to have more pieces than 
opponent. Therefore, min_max box optimizes for piece count and king count
(with 2x weight for piece count). 

Source consulted for minimax logic implementation:
https://www.youtube.com/watch?v=STjW3eH0Cik&t=1591s
"""

class Move_Tree:
    """
    Trees for individual move-index pairs that represent all potential game
    continuations, with opp_trees as the subsequent move trees for the 
    opponent. 
    """
    def __init__(self, mv, ind, opp_trees, board_state):
        """
        Constructor with:
        mv (Moves); ind (int); opp_trees (list[Move_Tree]);
        board_state (Checkers)
        """
        self.move = mv
        self.index = ind
        self.opp_trees = opp_trees
        self.board_state = board_state

class SmartBot:
    """
    Minimax bot
    """
    _checkers: Checkers
    _color: PieceColor

    def __init__(self, checkers, color, opponent_color, depth):
        """ 
        Constructor that consumes checkers (Checkers object bot will use),
        color (PieceColor attribute of bot), opponent_color (PieceColor attr. of
        opponent player), and depth (depth of bot). 

        Input:
            checkers: Checkers
            color: PieceColor attribute
            opponent_color: PieceColor attribute
            depth: int
        """
        self._checkers = checkers
        self._color = color
        self._depth = depth
        self._oppcolor = opponent_color

    def suggest_move(self):
        """
        This method assesses all possible moves up to the depth and returns the
        move-index pair with the optimal min max outcome. 

        Input: depth (int)
        Output: list[Moves, int]
        """
        # Get possible moves for this color
        depth = self._depth
        possible_mvs = self.non_empties(self._checkers.valid_moves(self._color))
        # Use get_trees to get list of trees corresponding to possible moves
        tree_list = self.get_trees(possible_mvs, self._color, depth, self._checkers)
        best = -math.inf
        best_mv = None
        for tree in tree_list:
            cur = self.get_minmax(tree, opp=True)
            # Find tree with best minmax value
            if cur >= best:
                best = cur
                best_mv = [tree.move, tree.index]
        return best_mv
   
    def get_minmax(self, tree, opp):
        """
        Given a Move_Tree object and a color, this method determines maxmin 
        value (given by an integer score) from this tree

        Input: tree (Move_Tree), opp (bool)
        Output: min_max (int)
        """
       # Base case is that tree has no children, so we assess state here
        if not(tree.opp_trees):
            return self.assess_state(tree.board_state)
        if not(opp):
            min_max = -math.inf
            for subtree in tree.opp_trees:
                # Recursive call now for opponent's move
                score = self.get_minmax(subtree, opp=True)
                if score > min_max:
                    min_max = score
        else:
            min_max = math.inf
            for subtree in tree.opp_trees:
                # Recursive call for bot's move
                score = self.get_minmax(subtree, opp=False)
                if score < min_max:
                    min_max = score
        return min_max

    def assess_state(self, board):
        """
        Given a board and a color, this method returns an assessment (int) of 
        the board from the standpoint of king and piece counts. 

        Input: board (Checkers)
        Output: int
        """
        opp_color = self._oppcolor
        # valid_moves returns Moves objects for each piece of the given color
        opp_mvs = board.valid_moves(opp_color)
        mvs = board.valid_moves(self._color)
        king_dif = self.king_tally(mvs) - self.king_tally(opp_mvs)
        pieces_dif = 2 * (len(mvs) - len(opp_mvs))
        return king_dif + pieces_dif

    def king_tally(self, mvs):
        """
        Given a list of move objects, this method returns the total number which
        correspond to king pieces.

        Input: mvs (list[Moves])
        Output: int
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
        
        Input: mvs (list[Moves]), color (PieceColor.color), depth (int),
        board (Checkers)

        Output: list[Move_Tree]
        """
        opp_color = self.opposite_color(color)
        tree_list = []
        for mv in mvs:
            for ind, child in enumerate(mv.children):
                new_state = self.simulate_move(board, mv, ind, color)
                if depth == 0:
                    tree_list.append(Move_Tree(mv, ind, [], new_state))
                else:
                    # Get all opponent's potential moves in this new state
                    opp_mvs = self.non_empties(new_state.valid_moves(opp_color))
                    # Recursive call to make tree list for this move/ind's tree
                    opp_trees = self.get_trees(opp_mvs, opp_color, depth - 1, new_state)
                    tree_list.append(Move_Tree(mv, ind, opp_trees, new_state))
        return tree_list
    
    def simulate_move(self, board, mv, ind, color):
        """
        Given a board, move and index, this method returns a new board state
        (a Checkers object) corresponding to if that move-index were to be 
        played.

        Input: board (Checkers); mv (Moves); ind (int); color (PieceColor attr.)
        Output: new_state (Checkers)
        """
        new_state = copy.deepcopy(board)
        # Note that the Moves object inserted into execute_single_move_rand 
        # needs to be a Moves object that belongs to the copied board
        mv_copy = self.copy_move_select(mv, new_state, color)
        new_state.execute_single_move_rand(mv_copy, ind)
        return new_state

    def copy_move_select(self, mv, copied_state, color):
        """
        Given a copied board, a Moves object, and a color, this method returns
        the equivalent Moves object in the copied board. 

        Input: mv (Moves); copied_state (Checkers); color (PieceColor attribute)
        Output: cp (Moves)
        """
        row = mv.location.row
        col = mv.location.col
        copy_mvs = self.non_empties(copied_state.valid_moves(color))
        for cp in copy_mvs:
            # Find equivalent Moves object
            if cp.location.row == row and cp.location.col == col:
                return cp
    
    def opposite_color(self, color):
        """
        Given a PieceColor Enum object, this method returns that of the opposite
        color. 

        Input: color (PieceColor attribute)
        Output: PieceColor attribute
        """
        if color == PieceColor.RED:
            return PieceColor.BLACK
        return PieceColor.RED

    def non_empties(self, mvs):
        """
        Given a list of Moves objects, each corresponding to a piece of the
        bot's color, this method returns a new list of those Moves objects with
        nonempty children (to yield playable moves). 

        Returns: list[Moves]
        """
        non_empty_lst = []
        for mv in mvs:
            if mv.children:
                non_empty_lst.append(mv)
        return non_empty_lst

class RandomBot:
    """
    Random bot class -- this bot makes only random moves.  
    """
    def __init__(self, checkers, color):
        """ 
        Constructor

        Input:
            checkers: Checkers
            color: PieceColor attribute
        """
        self._checkers = checkers
        self._color = color

    def suggest_move(self):
        """ 
        Given a dictionary which maps Moves to lists of child indices, this
        method returns a random Move-index list corresponding to one move on
        the board. 

        Input:
            move_dict: dict{Moves: list[int]}
        
        Returns:
            list[Moves, int]
        """
        game = self._checkers
        possible_mvs = self.non_empties(game.valid_moves(self._color))
        return self.find_rand(self.to_dict(possible_mvs))

    def find_rand(self, move_dict):
        """ 
        Given a dictionary which maps Moves to lists of child indices, this
        method returns a random Move-index tuple corresponding to one move on
        the board. 

        Input:
            move_dict: dict{Moves: list[int]}
        
        Returns:
            (Moves, int)
        """
        rand_mv = random.choice(list(move_dict.items()))[0]
        rand_child = random.choice(move_dict[rand_mv])
        return [rand_mv, rand_child]
    
    def non_empties(self, mvs):
        """
        Given a list of Moves objects, each corresponding to a piece of the
        bot's color, this method returns a new list of those Moves objects with
        nonempty children (all valid moves). 

        Input: mvs (list[Moves])
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

class BotPlayer:
    """
    Simple class to store information about a bot player in a simulation.
    """
    name: str
    bot: Union[RandomBot, SmartBot]
    color: PieceColor
    wins: int

    def __init__(self, name: str, board: Checkers, color: PieceColor,
                 opponent_color: PieceColor, depth):
        """ Constructor
        Input:
            name: Name of the bot
            board: Board to play on
            color: Bot's color
            opponent_color: Opponent's color
        """
        self.name = name

        if self.name == "random":
            self.bot = RandomBot(board, color)
        elif self.name == "smart":
            self.bot = SmartBot(board, color, opponent_color, depth)
        self.color = color
        self.wins = 0


def simulate(game: Checkers, n: int, bots, dim: int) -> None:
    """ 
    Simulates n games between the Bots specified by bots, played on a board of
    dimension (2 * dim) + 2 x (2 * dim) + 2. Number of wins are updated in the
    BotPlayer objects within bots.  

    Input:
        board: The board on which to play
        n: The number of games to play
        bots: Dictionary mapping piece colors to Player objects (the bots that 
        will play one another)
        dim: Board is of dimensions (2*(dim) + 2) x (2*(dim) + 2)
    Returns: None
    """
    for i in range(n):
        game = Checkers(dim)
        bots[PieceColor.RED].bot._checkers = game
        bots[PieceColor.BLACK].bot._checkers = game
        # When reset function implemented code here is more efficient
        # game.reset() 
        current = bots[PieceColor.RED]
        while (not game.is_done(PieceColor.RED)) and (not game.is_done(PieceColor.BLACK)):
            # Get corresponding bot's move to play
            move, index = current.bot.suggest_move()
            game.execute_single_move_rand(move, index)

            # Alternate turns by switching bots
            if current.color == PieceColor.BLACK:
                current = bots[PieceColor.RED]
            elif current.color == PieceColor.RED:
                current = bots[PieceColor.BLACK]
        
        # Get the winner from the Checkers object
        winner = game._winner
        if winner is not None:
            bots[winner].wins += 1


@click.command(name="Checkers Bot")
@click.option('-n', '--num-games', type=click.INT, default=100)
@click.option('--player1',
              type=click.Choice(['random', 'smart'], case_sensitive=False),
              default="random")
@click.option('--player2',
              type=click.Choice(['random', 'smart'], case_sensitive=False),
              default="random")
@click.option('--depth1', type=click.INT, default=3)
@click.option('--depth2', type=click.INT, default=3)
@click.option('--board_size', type=click.INT, default=3)

def cmd(num_games, player1, player2, depth1, depth2, board_size):
    # Remove this code if TUI/GUI work
    print("")
    print("Hello. In this mode only bots can be played against one another.")
    print("Note that you will be prompted for the depths of both bots,")
    print("and this number is disregarded in the case of a random bot.")
    print("")
    num_games = int(input("Enter the number of games you want the bots to play (integer): "))
    player1 = input("Enter 'random' or 'smart' for player 1: ")
    depth1 = int(input("Enter player 1 depth (integer): "))
    player2 = input("Enter 'random' or 'smart' for player 2: ")
    depth2 = int(input("Enter player 2 depth (integer): "))
    board_size = int(input("Enter integer n for board size (2n + 2)x(2n + 2): "))
    print("")
    print("Playing games... (depth 3+ can take a bit)")
    print("")

    board = Checkers(board_size)
    bot1 = BotPlayer(player1, board, PieceColor.RED, PieceColor.BLACK, depth1)
    bot2 = BotPlayer(player2, board, PieceColor.BLACK, PieceColor.RED, depth2)

    bots = {PieceColor.RED: bot1, PieceColor.BLACK: bot2}

    simulate(board, num_games, bots, board_size)

    bot1_wins = bots[PieceColor.RED].wins
    bot2_wins = bots[PieceColor.BLACK].wins
    ties = num_games - (bot1_wins + bot2_wins)

    print(f"Bot 1 ({player1}) wins: {100 * bot1_wins / num_games:.2f}%")
    print(f"Bot 2 ({player2}) wins: {100 * bot2_wins / num_games:.2f}%")
    print(f"Ties: {100 * ties / num_games:.2f}%")


if __name__ == "__main__":
    cmd()



