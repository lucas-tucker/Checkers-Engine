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

The TUI displays a representation of the board and asks for a player's next
move. Players input moves according to the axes of the board. For example,

    a|1

asks the tui to move the piece at ``a|1``. Then, the TUI will prompt the player
to input the location where the piece is moving to. In the case of a
multi-jump move, this may happen multiple times.

If at any time the location input is not valid, the TUI will prompt
again for a correct move.

If for any reason one needs to exit the game, inputting ``exit`` will accomplish
this.

Once the game finishes, one can reset the board by inputting
    b = Board(<size>) # replace size with an integer between 1 and 11

Canonically, Black (displayed blue because dark terminals are popular)
plays first: see 
[American Checkers](https://en.wikipedia.org/wiki/Checkers#No_flying_kings;_men_cannot_capture_backwards). 
As such, we have black play first as well.

Currently, we have not integrated the bot. 

