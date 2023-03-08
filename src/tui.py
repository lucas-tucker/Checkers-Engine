"""
Checkers game Terminal User Interface.

File Note: Due to the fact that some terminal interfaces are gray and black,
    instead of using black and red piece colors, I show the pieces as blue and
    red.

File Use: calling <python3 tui.py> in terminal will load the file, and then
    prompt the user for game setup questions. Recommended use is simply to
    retype this command to replay.

Done By : Niko Matheos
"""
import time
from rich.console import Console
from checkers import Checkers, PieceColor
from bot_minimax import SmartBot, RandomBot

# Initialize console (for typesetting) and useful global variables.
console = Console()
ALPH = "abcdefghijklmnopqrstuvwxyz"
# ALP_INT will take in a character in the alphabet, and return an integer
# INT_ALP will take in an integer (0-25) and return the cooresponding letter
ALP_INT = {}
INT_ALP = {}
for numb in range(0,26):
    INT_ALP[numb] = ALPH[numb]
    ALP_INT[ALPH[numb]] = numb

class ExitError(Exception):
    """
    Custom ExitError class made for exiting piece selection or move selection.
    """

def select_piece(game, color, opp_type):
    """
    At the start of a human players move they must select a piece to then move.
    This function gets an input from the player and then ensures that the input
    is valid. Also checks for draw offers and resignations.

    Args:
        game : Checkers game instance
        color : current player's color
        opp_type : Opponent type (used for draw offer)

    Returns : list [possible moves for selected piece, piece color]
    """
    num_input_error = 0 # If the user makes too many mistakes we give hints
    while True:
        if num_input_error >= 5:
            # If a player gives a wrong input 5 times, we give them a way
            # to exit from the game.
            console.print("[bold yellow]Hint:[/bold yellow] If stuck," +
                " typing [magenta]<exit>[/magenta] will exit you from " +
                "the game.")
        if color.name == "BLACK":
            col = "Blue"
        else:
            col = "Red"
        v = input(f"{col}'s Turn> ")
        if v == "exit":
            # If player types exit, raise an error to end the game
            raise ExitError
        try:
            if v == "draw":
                # If a player types draw, prompt a draw acceptance.
                if opp_type in ('Smart Bot', 'Random Bot'):
                    # Bots always accept draw offers
                    return 'draw'
                # If opponent is human, ask them if they accept
                console.print("Type [lime]'yes'[/lime] to accept, " +
                    "[red]'no'[/red] to refuse")
                v2 = input("Do you accept?> ")
                if v2 == "yes":
                    return 'draw'
                continue
            if v == "resign":
                # If a player types resign, they resign the game and lose
                return 'resign'

            out = v.split('|')
            col = ALP_INT[out[0]]
            row = int(out[1])
            pos = game.get_board().board[row][col]
            if color != game.get_board().board[row][col].piece.color:
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
            moves = game.piece_valid_moves((col, row), color)
            if moves[2].can_execute():
                # If we reach here a valid move was inputted.
                return [moves, color]
            # If we reach here, the input has no valid moves.
            console.print("[bold red]ERROR:[/bold red] Location "
                "does not have any valid moves, please try again")
            if num_input_error >= 2:
                console.print("[bold i yellow]Hint: Check for jump "
                    "moves! [/bold i yellow]")
            num_input_error += 1
            continue
        except Exception:
            # If we reach here, there was some error with the input.
            console.print("[bold red]ERROR:[/bold red] Please try again.")
            num_input_error += 1

def do_move(moves, color, game):
    """
    Gets a move from the current human player. Once a move is inputted, execute
    that single move. Repeat this process until there are no possible move
    continuations remaining.

    Args:
        moves: possible moves for our selected piece
        color: color of the moving player
        game: game being played

    Returns: None
    """
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

        if v == "exit":
            # If the input was "exit", we raise an ExitError
            raise ExitError
        try:
            out = v.split('|')
            col = ALP_INT[out[0]]
            row = int(out[1])
            #pos = board._board[row][col]
            valid = False
            move_index = 0

            for move in moves[2].children:
                if col == move.location.col and row == move.location.row:
                    # If the input has a valid row and column, execute move.
                    game.execute_single_move(moves[2], move_index)

                    # Now we change moves to the subtree.
                    nxt = moves[2].children[move_index]
                    moves = (nxt.location.col, nxt.location.row, nxt)
                    valid = True
                    print_board(game)
                    continue
                move_index += 1
            if not valid:
                console.print("[bold red]ERROR:[/bold red] Did not " +
                    "enter a valid move. Please try again.")
        except Exception:
            # If we reach here, there was some error with the input.
            console.print("[bold red]ERROR:[/bold red] Please try again.")
            #num_imput_error += 1

def human_turn(game: Checkers, curr, non_curr):
    """
    Handles the minor logistics of a human's turn. Checks for draws and
    resignations, also does moves.

    Args:
        game : Checkers game instance
        curr : current player
        non_curr : player whose turn it isn't
    Returns: None
    """
    info = select_piece(game, curr, non_curr)
    if info == 'draw':
        # Call checkers draw game
        game.draw_game()
        return None
    if info == 'resign':
        game.resign_game(curr)
        return None
    do_move(info[0], info[1], game)

def bot_turn(game, bot):
    """
    Handles turns for both types of bots.

    Args:
        game : Checkers, the current game being played.
        bot : SmartBot|RandomBot, the bot whose turn it is.
    Returns: None
    """
    move = bot.suggest_move()
    game.execute_single_move_rand(move[0], move[1])
    print_board(game)

def print_board(game: Checkers) -> None:
    """
    Prints the board to the screen.

    In the checkers.py file, there exists a __str__ method, which produces a
    string representation of the board. print_board uses this and then adds
    color and spacing to make the board more comprehensible.

    Args:
        game: The game to print
    Returns: None
    """
    size = game.get_board_dim()  - 1
    s = []
    count = 0
    for row in game.get_board().board:
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
            bottom.append(" [bold cyan]" + ALPH[num - 4] + "[/bold cyan] ")
    # Finally we combine the two strings and print
    console.print(final_s + ''.join(bottom))
    console.print("Input format: [bold yellow]<x-coord>[/bold yellow] "
        "[bold red]|[/bold red] [bold yellow]<y-coord>[/bold yellow]")

def print_message(color, game_over=False):
    """
    Produces a start message saying which color goes first, and a message for
    whoever the winner is.

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

def play_checkers(game: Checkers, player1: str, player2: str, depth1: int,
    depth2: int) -> None:
    """
    Plays a game of Checkers on the terminal

    Args:
        game: The Checkers game to play
        player1: String type for player 1 (either "Human", "Smart Bot", or
            "Random Bot".)
        player2: String type for player 2 (either "Human", "Smart Bot", or
            "Random Bot".)
        depth1: If player1 is a Smart Bot, this is its depth. Otherwise None
        depth2: If player2 is a Smart Bot, this is its depth. Otherwise None

    Returns: None
    """
    col_pl = {PieceColor.BLACK : player1,
                  PieceColor.RED : player2}
    depths = {player1 : depth1, player2 : depth2}

    # The starting player is BLACK
    current = PieceColor.BLACK
    non_current = PieceColor.RED

    # Print the starting message
    print_message(current)
    time.sleep(1)
    # Print the starting board
    print()
    print_board(game)
    print()

    # Keep playing until there is a winner:
    while not game.is_done(current):
        # Get move from current player
        if col_pl[current] == "Human":
            human_turn(game, current, col_pl[non_current])
        elif col_pl[current] == "Random Bot":
            rbot = RandomBot(game, current)
            bot_turn(game, rbot)
        elif col_pl[current] == "Smart Bot":
            sbot = SmartBot(game, current, non_current, depths[col_pl[current]])
            bot_turn(game, sbot)
        else:
            console.print(':pile_of_poo: Everybody Dance! :pile_of_poo:')

        # Update the player
        if current.value == PieceColor.BLACK.value:
            current = PieceColor.RED
            non_current = PieceColor.BLACK
        elif current.value == PieceColor.RED.value:
            current = PieceColor.BLACK
            non_current = PieceColor.RED


    # Escaped loop, game is over, print final board state
    print_board(game)
    print()
    print()

    # Find winner and print winner or tie
    if game.get_winner() is None:
        console.print("Draw")
    elif game.get_winner() == PieceColor.BLACK:
        print_message(PieceColor.BLACK, game_over=True)
    elif game.get_winner() == PieceColor.RED:
        print_message(PieceColor.RED, game_over=True)

    # Instruct user on how to play again
    print()
    print()
    console.print("[bold i yellow]Reimport to play again![/bold i yellow]")

def start_tui():
    """
    When tui.py is loaded in terminal as main, this function is called to set up
    the game for the user. First start_tui asks the user for information (what
    the user wants the player types to be, how big the board should be, etc.),
    and then once start_tui has all of the information from the player, it makes
    a new game and initializes the game by calling play_checkers().

    Args: None
    Returns: None
    """
    console.print("[bold magenta]Welcome![/bold magenta]")
    console.print("Before you can play checkers, you first need to help us " +
        "set up the board.")

    player_types = ['Human', 'Smart Bot', 'Random Bot']

    player1 = ''
    while player1 not in player_types:
        player1 = input("Enter 'Human', 'Smart Bot', or 'Random Bot' for " +
            "player One. > ")
        if player1 not in player_types:
            console.print("Please enter a valid player type.")
            console.print("Valid entries are [turquoise]'Human'[/turquoise], " +
                "[turquoise]'Smart Bot'[/turquoise], and [turquoise]'Random " +
                "Bot'[/turquoise].")

    depth1 = None
    if player1 == 'Smart Bot':
        console.print('[yellow i]Reminder: A high depth will make the game ' +
            "incredibly slow! Recoomended depth: 2[/yellow i]")
        depth1 = int(input("Enter the depth for player 1 (smart bot depth) > "))

    player2 = ''
    while player2 not in player_types:
        player2 = input("Enter 'Human', 'Smart Bot', or 'Random Bot' for "+
            "player Two. > ")
        if player2 not in player_types:
            console.print("Please enter a valid player type.")
            console.print("Valid entries are [turquoise]'Human'[/turquoise], " +
                "[turquoise]'Smart Bot'[/turquoise], and [turquoise]'Random " +
                "Bot'[/turquoise].")

    depth2 = None
    if player2 == 'Smart Bot':
        console.print('[yellow i]Reminder: A high depth will make the game ' +
            'incredibly slow! Recoomended depth: 2[/yellow i]')
        depth2 = int(input("Enter the depth for player 2 (smart bot depth) > "))

    size = 3
    console.print("Now you must select how many rows of pieces each player " +
        "will have. In a standard game of checkers each player has 3 rows of " +
        "pieces, meaning you would enter '3'.")
    size = int(input("How many rows of pieces will each player have? > "))

    game = Checkers(size)
    play_checkers(game, player1, player2, depth1, depth2)



if __name__ == "__main__":
    start_tui()
