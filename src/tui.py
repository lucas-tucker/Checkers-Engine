"""
Checkers game Terminal User Interface.

Current Status : Currently need to implement get_move functionality.

Done By : Niko
"""
from typing import Union, Dict


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
                v = input(f"{self.name}> ")

                # Check if input is actually a valid move
                if _______ #condition for valid move :
                    ###
                elif v == "Help":
                    # PRINT VALID MOVES AS TREES #
                else:
                    console.print("[bold red]ERROR:[/bold red] not a valid move, \
                        please try again.")
                    console.print("[i yellow]Hint: enter Help for a list of \
                        valid moves[/i yellow]")

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
    """ 
    Prints the board to the screen.

    In the checkers.py file, there exists a __str__ method, which produces a
    string representation of the board. print_board uses this and then adds
    color and spacing to make the board more comprehensible.

    Args:
        board: The board to print
    Returns: None
    """
    size = board._board_dim  - 1
    s = []
    count = size
    for row in board._board:
        # On each new row we add a number and a divider (ex. 1| )
        if count >= 100:
            s.append(str(count))
        elif count >= 10:
            s.append(" " + str(count))
        else:
            s.append("  " + str(count))
        s.append("│")
        for square in row:
            # For each row we then add all the string rep of the squares (either
            # a piece or a blank)
            s.append(str(square))
        # To end each row we add a new line and decrease our row number
        s.append("\n")
        count += -1

    final_s = ""
    for char in s:
        # For each character of our string representation of the board, we then
        # create a newly formatted representation.
        if char == "□":
            final_s += " ■ "
        elif char == "b":
            final_s += " [blue]●[/blue] "
        elif char == "r":
            final_s += " [red]●[/red] "
        elif char == "B":
            final_s += " [blue]◎[/blue] "
        elif char == "R":
            final_s += " [red]◎[/red] "
        else:
            final_s += char
    # The bulk of the board is now created, we just need to add the bottom count

    alph = "abcdefghijklmnopqrstuvwxyz"
    bottom = []
    for num in range(0, size + 5):
        # First we add a full row of dividers
        if num <= 2:
            # We don't want a divider below the other set of numbers
            bottom.append(" ")
        elif num == 3:
            # We want to connect our dividers
            bottom.append("└")
        else:
            # Finish dividers
            bottom.append("───")
    bottom.append("\n")
    for num in range(0, size + 5):
        # Now we add the numbers to the bottom row
        if num <= 3:
            bottom.append(" ")
        else:
            bottom.append(" " + alph[num - 4] + " ")
    # Finally we combine the two strings and print
    console.print(final_s + ''.join(bottom))
    return None
    

def play_checkers(board: Board, players: Dict[PieceColor, TUIPlayer]) -> None:
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
