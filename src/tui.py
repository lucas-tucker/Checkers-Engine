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

ALP_INT = {a : 1, b : 2, c : 3, d : 4, e : 5, f : 6, g : 7, h : 8,
            i : 9, j : 10, k : 11, l : 12, m : 13, n : 14, o : 15,
            p : 16, q : 17, r : 18, s : 19, t : 20, u : 21, v : 22,
            w : 23, x : 24, y : 25, z : 26}

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
        self.n = n

    def select_piece(self):
        """
        At the start of a players move they must select a piece to then move.

        Returns : list [possible moves for selected piece, piece color]
        """
        if self.bot is not None:
            pass
        else:
            while True:
                v = input(f"{self.name}> ")

                try:
                    col = ALP_INT[v[0]]
                    row = v[1]
                    color = self.board._board[row][col].piece.color
                    pos = self.board._board[row][col]
                    # Check if input is actually a valid move
                    if not pos.has_piece:
                        console.print("[bold red]ERROR:[/bold red] location \
                            does not have piece, please try again")
                        continue
                    moves = self.board.piece_valid_moves((col, row), color)
                    if moves[2].can_execute():
                        return [moves, color]
                    else:
                        console.print("[bold red]ERROR:[/bold red] location \
                            does not have any valid moves, please try again")
                        continue

        
    def do_move(self, moves, color):
        """
        Gets a move from the current player.
        
        If current player is a bot, then update the board state after a delay.
        If current player is human, prompt them for a move.

        Args: 
            moves: possible moves for our selected piece

        Returns: None
        """
        if self.bot is not None:
            pass
        else:
            while moves[2].can_execute:
                poss_cords = []
                for move in moves[2].children:
                    poss_coords.append((move.location.col, move.location.row))
                #poss_coords = [(move[0], move[1]) for move in moves]
                console.print("[bold blue]Possible Continuations: \
                    [/bold blue]" + f"{poss_coords}> ")
                v = input(f"{self.name}> ")
            
                try:
                    col = ALP_INT[v[0]]
                    row = v[1]
                    pos = self.board._board[row][col]
                    valid = False
                    move_index = 0
                    for move in moves[2].children:
                        if col == move.location.col and row == move.location.row:
                            self.board.execute_single_move(move[2])
                            nxt = moves[2].children[move_index]
                            moves = (nxt.location.col, nxt.location.row, nxt)
                            print_board(self.board)
                            valid = True
                            break
                        move_index += 1
                    if not valid:
                        console.print("[bold red]ERROR:[/bold red] Did not \
                            enter a valid move. Please try again.")
                except:
                    console.print("[bold red]ERROR:[/bold red] Please try again.")
                        
                    
            
            """
            # Ask for a move (and re-ask if a valid move is not provided)
            while in_progress:
                v = input(f"{self.name}> ")

                try:
                    col = ALP_INT[v[0]]
                    row = v[1]
                    color = self.board._board[row][col].piece.color
                    pos = self.board._board[row][col]
                    # Check if input is actually a valid move
            
                    moves = self.board.piece_valid_moves((col, row), color)
                    if moves:
                        select = True
                        poss_coords = []
                        for move in moves:
                            #self.board._board[move[1]][move[0]].hl = True
                            poss_coords.append((move[0], move[1]))
                        print_board(self.Board)
                        console.print("[bold blue]Possible Continuations: \
                            [/bold blue]" + f"{poss_coords}> ")
                        last_iter_moves = moves
                        for move in last_iter_moves:

                    elif 

                    else:
                        # This means there are no more valid moves, i.e. we have
                        # reached the end of a move

                        in_progress = False

                        


                    #condition for valid move :
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
    current = players[checkers.PieceColor.BLACK]

    # Keep playing until there is a winner:
    while not board.is_done(current.color):
        # Print the board
        print()
        print_board(board)
        print()

        # Get move from current player
        info = current.select_piece()
        current.do_move(info[0], info[1])


        # Update the player
        if current.color == PieceColor.BLACK:
            current = players[PieceColor.RED]
        elif current.color == PieceColor.RED:
            current = players[PieceColor.BLACK]

    # Escaped loop, game is over, print final board state
    print()
    print_board(board)

    # Find winner and print winner or tie
    if current.color == PieceColor.BLACK:
        current = players[PieceColor.RED]
        console.print(f"[bold magenta]The winner is[/bold magenta] player {current.n}")
    elif current.color == PieceColor.RED:
        current = players[PieceColor.BLACK]
        console.print(f"[bold magenta]The winner is[/bold magenta] player {current.n}")
    else:
        console.print(":pile_of_poo:")