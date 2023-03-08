# project-nmatheos-ayl-lwtucker-dchn

This respository contains a design and implementation for big checkers 
(a general implementation of [Checkers](https://en.wikipedia.org/wiki/Checkers)).
This project is for CMSC 14200.

The responsibility split is Daniel - Game Logic, Niko - TUI, Althea - GUI, Lucas - Bot
# Setup

Our implementation uses the following libraries that may need installing:

    rich
    pygame
    click

You can install these with

    pip install rich pygame click

# Running the TUI

To run the TUI, navigate to the root of the repository, and run

    python3 src/tui.py

When opened, the user will be faced with a series of questions, asking them to
help set up the game. Questions will ask the user what the types of the two
players are (either "Human", "Random Bot", or "Smart Bot"), the board size (int
between 1 and 12), and in the case where a Smart Bot was selected, what depth
the bot should run at.

The user should note that complexity increases with increased board size and
increased smart bot depth. As such, we recommend that on board sizes >4, bot
depth should not exceed 2. On board sizes <=4, one can try using a higher depth,
but should expect slower runtimes.

The TUI displays a representation of the board and asks for a human player's 
next move. Players input moves according to the axes of the board. For example,

    a|1

asks the tui to move the piece at ``a|1``. Then, the TUI will prompt the player
to input the location where the piece is moving to. In the case of a
multi-jump move, this may happen multiple tim

If at any time the location input is not valid, the TUI will prompt
again for a correct move.

If for any reason one needs to exit the game, inputting ``exit`` will accomplish
this.

A Human player can offer a draw by inputting ``draw``. Bots always accept draw
offers, while a Human opponent is prompted to accept of not accept the draw.

A Human player can resign by inputting ``resign``.

Once the game finishes, one can replay by typing

    python3 src/tui.py

into the terminal again.

Canonically, Black (displayed blue because dark terminals are popular)
plays first: see 
[American Checkers](https://en.wikipedia.org/wiki/Checkers#No_flying_kings;_men_cannot_capture_backwards). 
As such, we have black play first as well.


# Running bot_minimax

To stimulate two bots playing against each other multiple times, run

    python3 src/bot_minimax.py

You will be prompted with instructions on how to play the two bots against one
another (random, smart, depth, number of games) and you will recieve the 
game outcomes as percentages.
