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

from checkers import Checkers, Board, Square, Piece, Moves, PieceColor
from bot_minimax import SmartBot, RandomBot, BotPlayer, Move_Tree
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

def select_piece(game, color, opp_type):
    """
    At the start of a players move they must select a piece to then move.

    Returns : list [possible moves for selected piece, piece color]
    """
    if True:
        num_input_error = 0 # If the user makes too many mistakes we give hints
        while True:
            if num_input_error >= 5:
                # If a player gives a wrong input 5 times, we give them a way
                # to exit from the game.
                console.print("[bold yellow]Hint:[/bold yellow] If stuck," +
                    " typing [magenta]<exit>[/magenta] will exit you from " +
                    "the game.")
            #col = ""
            if color.name == "BLACK":
                col = "Blue"
            else:
                col = "Red"
            v = input(f"{col}'s Turn> ")
            try:
                if v == "exit":
                    # If player types exit, raise an error to end the game.
                    raise ExitError
                if v == "draw":
                    # If a player types draw, prompt a draw acceptance.
                    if (opp_type == 'Smart Bot') or (opp_type == 'Random Bot'):
                        return 'draw'
                    else:
                        console.print("Type [lime]'yes'[/lime] to accept, [red]'no'[/red] to refuse")
                        v2 = input("Do you accept?>")
                        if v2 == "yes":
                            return 'draw'
                        else:
                            continue
                if v == "resign":
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
    
def do_move(moves, color, game):
    """
    Gets a move from the current player.
    
    If current player is a bot, then update the board state after a delay.
    If current player is human, prompt them for a move.

    Args: 
        moves: possible moves for our selected piece
        color: color of the moving player
        game: game being played

    Returns: None
    """
    if True:
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
            except:
                # If we reach here, there was some error with the input.
                console.print("[bold red]ERROR:[/bold red] Please try again.")
                num_imput_error += 1

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
    size = game._board_dim  - 1
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
    

def play_checkers(game: Checkers, player1: str, player2: str, depth1: int, 
    depth2: int) -> None:
    """ Plays a game of Connect Four on the terminal
    Args:
        board: The board to play on
        players: A dictionary mapping piece colors to
            TUIPlayer objects.
    Returns: None
    """
    color_player = {PieceColor.BLACK : player1,
                  PieceColor.RED : player2}
    depths = {player1 : depth1, player2 : depth2}

    # Save the starting board state to restart at the end of game.
    #start_board = Checkers(game._size)

    # The starting player is BLACK
    current = PieceColor.BLACK
    non_current = PieceColor.RED
    start_message(current)
    time.sleep(1)

    # Print the starting board
    print()
    print_board(game)
    print()
    
    # Keep playing until there is a winner:
    while not game.is_done(current):
        # Get move from current player
        if color_player[current] == "Human":
            info = select_piece(game, current, color_player[non_current])       
            if info == 'draw':
                # Call checkers draw game
                game.draw_game()
                continue
            if info == 'resign':
                game.resign_game(current)
                continue
            do_move(info[0], info[1], game)
        elif color_player[current] == "Random Bot":
            rbot = RandomBot(game, current)
            move = rbot.suggest_move()
            game.execute_single_move_rand(move[0], move[1])
            print_board(game)
        elif color_player[current] == "Smart Bot":
            sbot = SmartBot(game, current, non_current, depths[color_player[current]])
            move = sbot.suggest_move()
            game.execute_single_move_rand(move[0], move[1])
            print_board(game)
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

    # Find winner and print winner or tie
    print()
    print()

    if game.get_winner() == None:
        console.print("Draw")
    elif current == PieceColor.BLACK:
        start_message(PieceColor.RED, game_over=True)
    elif current == PieceColor.RED:
        start_message(PieceColor.BLACK, game_over=True)
    else:
        console.print(":pile_of_poo:")

    # Reset board
    print()
    print()
    console.print("[bold i yellow]Remember to reset the board![/bold i yellow]")


def bot_v_bot(game, n, bots, dim):
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
            print_board(game)
            move, index = current.bot.suggest_move()
            game.execute_single_move_rand(move, index)

            # Alternate turns by switching bots
            if current.color == PieceColor.BLACK:
                current = bots[PieceColor.RED]
            elif current.color == PieceColor.RED:
                current = bots[PieceColor.BLACK]
        
        # Escaped loop, game is over, print final board state
        print_board(game)

        # Find winner and print winner or tie
        print()
        print()

        if game.get_winner() == None:
            console.print("Draw")
        elif current == PieceColor.BLACK:
            start_message(PieceColor.RED, game_over=True)
        elif current == PieceColor.RED:
            start_message(PieceColor.BLACK, game_over=True)
        else:
            console.print(":pile_of_poo:")

        # Get the winner from the Checkers object
        winner = game._winner
        if winner is not None:
            bots[winner].wins += 1

console = Console()




def start_tui():
    """
    Sets up game.
    """
    console.print("[bold magenta]Welcome![/bold magenta]")
    console.print("Before you can play checkers, you first need to help us " +
        "set up the board.")

    player_types = ['Human', 'Smart Bot', 'Random Bot']
    bots = [player_types[1], player_types[2]]

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
                "[turquoise]'Smart Bot'[/turquoise], and [turquoise]'Random Bot' " +
                "[/turquoise].") 
    

    depth2 = None
    if player2 == 'Smart Bot':
        console.print('[yellow i]Reminder: A high depth will make the game ' +
            'incredibly slow! Recoomended depth: 2[/yellow i]')
        depth2 = int(input("Enter the depth for player 2 (smart bot depth) > "))


    """ 
    num_games = 1
    if (player1 in bots) and (player2 in bots):
        console.print("Both selected players are bots!")
        num_games = int(input("How many games would you like to run? >"))
    """


    size = 3
    console.print("Now you must select how many rows of pieces each player " +
        "will have. In a standard game of checkers each player has 3 rows of " +
        "pieces, meaning you would enter '3'.")
    size = int(input("How many rows of pieces will each player have? > "))

    """
    if (player1 in bots) and (player2 in bots):
        board = Checkers(size)
        bot1 = BotPlayer(player1, board, PieceColor.RED, PieceColor.BLACK, depth1)
        bot2 = BotPlayer(player2, board, PieceColor.BLACK, PieceColor.RED, depth2)

        bots = {PieceColor.RED: bot1, PieceColor.BLACK: bot2}

        #bot_minimax.simulate(board, num_games, bots, board_size)
        bot_v_bot(board, num_games, bots, size)

        bot1_wins = bots[PieceColor.RED].wins
        bot2_wins = bots[PieceColor.BLACK].wins
        ties = num_games - (bot1_wins + bot2_wins)

        print(f"Bot 1 ({player1}) wins: {100 * bot1_wins / num_games:.2f}%")
        print(f"Bot 2 ({player2}) wins: {100 * bot2_wins / num_games:.2f}%")
        print(f"Ties: {100 * ties / num_games:.2f}%")
    
    else:
    """
    game = Checkers(size)
    play_checkers(game, player1, player2, depth1, depth2)

    

if __name__ == "__main__":
    start_tui()