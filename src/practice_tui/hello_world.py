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