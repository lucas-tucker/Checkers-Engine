"""
Checkers game Terminal User Interface.

Current Status : Currently need to implement get_move functionality.

Done By : Niko
"""
from checkers import Board, Square, Piece, Moves
from rich.console import Console
from enum import Enum

PieceColor = Enum("PieceColor", ["RED", "BLACK"])
console = Console()

name: str
board: Board
color: PieceColor

class TUIPlayer:
    """
    terminal goes crazy
    """
    def __init__(self, n: int, player_type: str, board: Board, color: PieceColor):
        """
        Constructor

        Args:
            n: The player's number (1 or 2)
            player_type: "human" or "bot"
            board: The checkers board
        """
        if player_type == "human":
            self.name = f"Player {n}"
            self.bot = None
        else:
            #implement bot
            pass
        self.board = board
        self.color = color
    
    def get_move(self):
        """
        Gets a move from the current player.
        
        If current player is a bot, then update the board state after a delay.
        If current player is human, prompt them for a move.

        Returns: None
        """
        pass
        """
        if self.bot is not None:
                    time.sleep(self.bot_delay)
                    column = self.bot.suggest_move()
                    # Print prompt with column already filled in
                    print(Style.BRIGHT + f"{self.name}> " + Style.RESET_ALL + str(column+1))
                    return column
                else:
                    # Ask for a move (and re-ask if a valid move is not provided)
                    while True:
                        v = input(Style.BRIGHT + f"{self.name}> " + Style.RESET_ALL)
                        if len(v) == 1 and v[0] in "1234567":
                            try:
                                col = int(v) - 1
                                if self.board.can_drop(col):
                                    return col
                            except ValueError:
                                continue
                        if self.board.valid_moves(self.color)
        """
def print_board(board: Board) -> None:
    """ Prints the board to the screen
    Args:
        board: The board to print
    Returns: None
    """
    s = []
    for row in board:
        for square in row:
            s.append(str(square))
        s.append("\n")
    final_s = ""
    for char in s:
        if char == "□":
            final_s += " [bold]□[/bold] "
        elif char == "b":
            final_s += " [blue]o[/blue] "
        elif char == "r":
            final_s += " [red]o[/red] "
        elif char == "B":
            final_s += " [blue]O[/blue] "
        elif char == "R":
            final_s += " [red]O[/red] "
        else:
            final_s += char
    console.print(final_s)
    return None
    

def play_checkers(board: BoardType, players: Dict[PieceColor, TUIPlayer]) -> None:
    """ Plays a game of Connect Four on the terminal
    Args:
        board: The board to play on
        players: A dictionary mapping piece colors to
            TUIPlayer objects.
    Returns: None
    """
    # The starting player is BLACK
    current = players[PieceColor.BLACK]

    # Keep playing until there is a winner:
    while not board.is_done():
        # Print the board
        print()
        print_board(board)
        print()

        # Get move from current player
        move = current.get_move()

        # Drop the piece
        board.execute_move(move)

        # Update the player
        if current.color == PieceColor.BLACK:
            current = players[PieceColor.RED]
        elif current.color == PieceColor.RED:
            current = players[PieceColor.BLACK]

    # Escaped loop, game is over, print final board state
    print()
    print_board(board)

    # Find winner and print winner or tie
    winner = board.get_winner()
    if winner is not None:
        print(f"The winner is {players[winner].name}!")
    else:
        print("It's a tie!")
