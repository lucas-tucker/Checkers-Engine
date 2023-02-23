"""
Learning how to use ncurses for implementing TUI. Tutorial from

Current Status : In progress

Done By : Niko
"""
from checkers import Board, Square, Piece, Moves
from rich.console import Console

console = Console()

def hello_world():
    console.print("Hello, World!")
    console.print("Hello, [bold magenta] World![/bold magenta]")
    console.print("Hello", "World!", style="bold red")
    console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
    b = checkers.Board(3)
    print(b)
    print("hi")
    return None

def print_board():
    b = checkers.Board(3)
    print(b)
    return None
    


"""

some stuff I did. In order for this stuff to work you need to
from rich.console import Console

console = Console()

in Square class
    def __str__(self) -> str:
        """ Returns a string representation of what is on the square."""
        if self.piece == None:
            return " [bold yellow]□[/bold yellow] "
        if self.piece.color is PieceColor.RED:
            color = "red"
        else:
            color = "blue"
        if self.piece.is_king:
            return " [green]" + self.piece.color.name[0] + "[/green] "

in board class

    def nice_print(self): # -> str:
        """
        Represents the board as a string.

        Returns:
            str
        """
        s = ""
        for row in self._board:
            for square in row:
                s += str(square)
            s += "\n"
        console.print(s)
        return None
"""