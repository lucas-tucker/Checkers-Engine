"""
Checkers game Terminal User Interface.

File Note: Due to the fact that some terminal interfaces are gray and black,
    instead of using black and red piece colors, I show the pieces as blue and
    red.

Current Status : Awaiting bot development to then implement into TUI.

Done By : Niko
"""
from typing import Union, Dict
import time

from checkers import Board, Square, Piece, Moves, PieceColor
from rich.console import Console
from enum import Enum

# Initialize console (for typesetting) and useful global variables.
console = Console()
alph = "abcdefghijklmnopqrstuvwxyz"
count = 0
# ALP_INT will take in a character in the alphabet, and return an integer
ALP_INT = {}
for char in alph:
    ALP_INT[char] = count
    count += 1
# INT_ALP will take in an integer (0-25) and return the cooresponding letter
INT_ALP = {}
for numb in range(0,26):
    INT_ALP[numb] = alph[numb]

class ExitError(Exception):
    """
    Custom ExitError class made for exiting piece selection or move selection.
    """
    pass

def select_piece(board, color):
    """
    At the start of a players move they must select a piece to then move.

    Returns : list [possible moves for selected piece, piece color]
    """
    if False: #self.bot is not None:
        pass
    else:
        num_input_error = 0
        while True:
            if num_input_error >= 5:
                # If a player gives a wrong input 5 times, we give them a way
                # to exit from the game.
                console.print("[bold yellow]Hint:[/bold yellow] If stuck," 
                    " typing [magenta]<exit>[/magenta] will exit you from the game.")
            col = ""
            if color.name == "BLACK":
                col = "Blue"
            else:
                col = "Red"
            v = input(f"{col}'s Turn> ")
            try:
                if v == "exit":
                    # If player types exit, raise an error to end the game.
                    raise ExitError
                out = v.split('|')
                col = ALP_INT[out[0]]
                row = int(out[1])
                pos = board._board[row][col]
                if color != board._board[row][col].piece.color:
                    # If we reach here input was wrong color.
                    console.print("[bold red]ERROR:[/bold red] Piece is not "
                        "the correct color. Please try again.")
                    num_input_error += 1
                if not pos.has_piece:
                    # If we reach here, input is not a piece.
                    console.print("[bold red]ERROR:[/bold red] location"
                        "does not have piece, please try again")
                    num_input_error += 1
                    continue
                moves = board.piece_valid_moves((col, row), color)
                if moves[2].can_execute():
                    # If we reach here a valid move was inputted.
                    return [moves, color]
                else:
                    # If we reach here, the input has no valid moves.
                    console.print("[bold red]ERROR:[/bold red] Location "
                        "does not have any valid moves, please try again")
                    if num_input_error >= 2:
                        console.print("[bold i yellow]Hint: Check for jump "
                            "moves! [/bold i yellow]")
                    num_input_error += 1
                    continue
            except:
                if v == "exit":
                    raise ExitError
                # If we reach here, there was some error with the input.
                console.print("[bold red]ERROR:[/bold red] Please try again.")
                num_input_error += 1
    
def do_move(moves, color, board):
    """
    Gets a move from the current player.
    
    If current player is a bot, then update the board state after a delay.
    If current player is human, prompt them for a move.

    Args: 
        moves: possible moves for our selected piece

    Returns: None
    """
    if False: # bot is not None:
        pass
    else:
        while moves[2].can_execute():
            # The move is not finished until the move class instance (moves[2])
            # has no more children. can_execute is a method which checks this.

            # First we show the player their possible moves for the selected
            # piece, or if they are halfway through a jump move, their possible
            # continuations.
            poss = [(INT_ALP[m.location.col], m.location.row) for m in moves[2].children]
            console.print("[bold blue]Possible Continuations: \
                [/bold blue]" + "[bold white]" +f"{poss}[/bold white] ")

            # Next we get the player's input, and check if they tried to exit.
            col = ""
            if color.name == "BLACK":
                col = "Blue"
            else:
                col = "Red"
            v = input(f"{col}'s Turn> ")            

            try:
                if v == "exit":
                    # If input was "exit", raise ExitError
                    raise ExitError

                out = v.split('|')
                col = ALP_INT[out[0]]
                row = int(out[1])
                #pos = board._board[row][col]
                valid = False
                move_index = 0

                for move in moves[2].children:
                    if col == move.location.col and row == move.location.row:
                        # If the input has a valid row and column, execute move.
                        board.execute_single_move(moves[2], move_index)

                        # Now we change moves to the subtree.
                        nxt = moves[2].children[move_index]

                        moves = (nxt.location.col, nxt.location.row, nxt)
                        print_board(board)
                        valid = True
                        continue
                    move_index += 1
                if not valid:
                    console.print("[bold red]ERROR:[/bold red] Did not "
                        "enter a valid move. Please try again.")
            except:
                if v == "exit":
                    # If input was "exit", raise ExitError
                    raise ExitError
                # If we reach here, there was some error with the input.
                console.print("[bold red]ERROR:[/bold red] Please try again.")
                num_imput_error += 1

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
    count = 0
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
        count += 1

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
            bottom.append(" [bold cyan]" + alph[num - 4] + "[/bold cyan] ")
    # Finally we combine the two strings and print
    console.print(final_s + ''.join(bottom))
    console.print("Input format: [bold yellow]<x-coord>[/bold yellow] " 
        "[bold red]|[/bold red] [bold yellow]<y-coord>[/bold yellow]")
    return None
    
def start_message(color, game_over=False):
    """
    Produces a start message saying which color goes first.

    Args:
        PieceColor: Starting Color
    Returns:
        console.print: Text output for who starts
    """
    col_str = ""
    if color.value == PieceColor.BLACK.value:
        if game_over:
            msg_str = "The winner is [bold blue]Blue![/bold blue]"
            top = "┌───────────────────┐\n"
            rw2 = "│                   │\n"
            rw3 = "│                   │\n"
            rw4 = f"│{msg_str}│\n"
            rw5 = "│                   │\n"
            rw6 = "│                   │\n"
            btm = "└───────────────────┘\n"
        else:
            col_str = "[bold blue]Blue[/bold blue]"
            top = "┌─────────────────┐\n"
            rw2 = "│                 │\n"
            rw3 = "│                 │\n"
            rw4 = f"│   {col_str} Starts   │\n"
            rw5 = "│                 │\n"
            rw6 = "│                 │\n"
            btm = "└─────────────────┘\n"
    else:
        if game_over:
            msg_str = "The winner is [bold red]Red![/bold red]"
            top = "┌──────────────────┐\n"
            rw2 = "│                  │\n"
            rw3 = "│                  │\n"
            rw4 = f"│{msg_str}│\n"
            rw5 = "│                  │\n"
            rw6 = "│                  │\n"
            btm = "└──────────────────┘\n"
        else:    
            col_str = "[bold red]Red[/bold red]"
            top = "┌────────────────┐\n"
            rw2 = "│                │\n"
            rw3 = "│                │\n"
            rw4 = f"│   {col_str} Starts   │\n"
            rw5 = "│                │\n"
            rw6 = "│                │\n"
            btm = "└────────────────┘\n"
    
    console.print(top + rw2 + rw3 + rw4 + rw5 + rw6 + btm)
    

def play_checkers(board: Board, player1_is_bot=False, player2_is_bot=False) -> None:
    """ Plays a game of Connect Four on the terminal
    Args:
        board: The board to play on
        players: A dictionary mapping piece colors to
            TUIPlayer objects.
    Returns: None
    """
    # Save the starting board state to restart at the end of game.
    start_board = Board(board._size)

    # The starting player is BLACK
    current = PieceColor.BLACK
    start_message(current)
    time.sleep(1)

    # Keep playing until there is a winner:
    while not board.is_done(current):
        # Print the board
        print()
        print_board(board)
        print()

        # Get move from current player
        info = select_piece(board, current)
        do_move(info[0], info[1], board)


        # Update the player
        if current.value == PieceColor.BLACK.value:
            current = PieceColor.RED
        elif current.value == PieceColor.RED.value:
            current = PieceColor.BLACK

    # Escaped loop, game is over, print final board state
    print("hi")
    print_board(board)

    # Find winner and print winner or tie
    print()
    print()

    if current == PieceColor.BLACK:
        start_message(PieceColor.RED, game_over=True)
    elif current == PieceColor.RED:
        start_message(PieceColor.BLACK, game_over=True)
    else:
        console.print(":pile_of_poo:")
    
    # Reset board
    print()
    print()
    console.print("[bold i yellow]Remember to reset the board![/bold i yellow]")


console = Console()
b = Board(3)
play_checkers(b)