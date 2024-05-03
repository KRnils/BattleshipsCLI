# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
from random import randint
import curses
from curses import wrapper


class Board:
    """
    Board class that holds the current status of a players board (both computer and player)
    """

    def __init__(self, size):
        self.ships = 5
        self.size = size
        self.grid = [['.' for i in range(size)]]*size

    def printSelf(self):
        row = ""
        for i in self.grid:
            for j in i:
                row += ' '+(j)
            print(row)
            row = ""

    def add_ship(x,y):
        pass

    def check_hit():
        print(randint(0,10))
        pass


def main(stdscr):
    """
    Main game loop runs here
    """
    # Draw the board
    size = 10
    board = ["."*size for i in range(0, size)]
    board += ["-"*size]
    board += ["."*size for i in range(0, size)]
    
    start_y, start_x = 8, 2  # Start position of the cursor (based on size)

    # initialize curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # game logic 
    for i in range(0, size):
        for j in range(0, size):
            stdscr.addstr(i, j, ".")
    
    playing = True
    while (playing):
        stdscr.refresh()
        stdscr.getkey()

    # end game logic and revert curses terminal settings
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

wrapper(main)
