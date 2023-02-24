"""
Checkers game Terminal User Interface.

Current Status : Currently need to implement get_move functionality.

Done By : Niko
"""
from typing import Union, Dict

from checkers import Board, Square, Piece, Moves, PieceColor
from rich.console import Console
from enum import Enum

#PieceColor = Enum("PieceColor", ["RED", "BLACK"])
console = Console()

ALP_INT = {'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3, 'e' : 4, 'f' : 5, 'g' : 6, 'h' : 7,
            'i' : 8, 'j' : 9, 'k' : 10, 'l' : 11, 'm' : 12, 'n' : 13, 'o' : 14,
            'p' : 15, 'q' : 16, 'r' : 17, 's' : 18, 't' : 19, 'u' : 20, 'v' : 21,
            'w' : 22, 'x' : 23, 'y' : 24, 'z' : 25}

name: str
board: Board
color: PieceColor

def select_piece(board, color):
    """
    At the start of a players move they must select a piece to then move.

    Returns : list [possible moves for selected piece, piece color]
    """
    if False: #self.bot is not None:
        pass
    else:
        while True:
            v = input(f"{color.value}'s Turn> ")
            out = v.split('|')
            try:
                col = ALP_INT[out[0]]
                row = int(out[1])
                if color != board._board[row][col].piece.color:
                    console.print("[bold red]ERROR:[/bold red] Piece is not \
                        the correct color. Please try again.")
                pos = board._board[row][col]
                # Check if input is actually a valid move
                if not pos.has_piece:
                    console.print("[bold red]ERROR:[/bold red] location \
                        does not have piece, please try again")
                    continue
                moves = board.piece_valid_moves((col, row), color)
                if moves[2].can_execute():
                    return [moves, color]
                else:
                    console.print("[bold red]ERROR:[/bold red] location \
                        does not have any valid moves, please try again")
                    continue
            except:
                console.print("[bold red]ERROR:[/bold red] Please try again.")
    
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
            poss_coords = []
            for move in moves[2].children:
                poss_coords.append((move.location.col, move.location.row))
            #poss_coords = [(move[0], move[1]) for move in moves]
            console.print("[bold blue]Possible Continuations: \
            [/bold blue]" + f"{poss_coords}> ")
            v = input(f"{color.value}'s Turn> ")
            out = v.split('|')

            col = ALP_INT[out[0]]
            row = int(out[1])
            pos = board._board[row][col]
            valid = False
            move_index = 0
            for move in moves[2].children:
                print(move.location.col, move.location.row)
                if col == move.location.col and row == move.location.row:
                    nxt = moves[2].children[move_index]
                    board.execute_single_move(moves[2], move_index)
                    moves = (nxt.location.col, nxt.location.row, nxt)
                    print_board(board)
                    valid = True
                    continue
                move_index += 1
            if not valid:
                console.print("[bold red]ERROR:[/bold red] Did not \
                    enter a valid move. Please try again.")

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
    console.print("Input format: [bold yellow]<x-coord>[/bold yellow] \
        [bold red]|[/bold red] [bold yellow]<y-coord>[/bold yellow]")
    return None
    

def play_checkers(board: Board, player1_is_bot=False, player2_is_bot=False) -> None:
    """ Plays a game of Connect Four on the terminal
    Args:
        board: The board to play on
        players: A dictionary mapping piece colors to
            TUIPlayer objects.
    Returns: None
    """
    # The starting player is BLACK
    current = PieceColor.BLACK

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
    if current == PieceColor.BLACK:
        console.print("[bold]The winner is[/bold] [bold red]red![/bold red]")
    elif current == PieceColor.RED:
        console.print("[bold]The winner is[/bold] [bold blue]blue![/bold blue]")
    else:
        console.print(":pile_of_poo:")