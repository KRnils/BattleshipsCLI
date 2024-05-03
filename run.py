# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
from random import randint
import curses
from curses import wrapper


class Board:
    """
    Board class that holds the current status of the game board
    """

    def __init__(self, size):
        self.ships = 5
        self.size = size
        self.grid = ["."*size for i in range(0, size)]
        self.grid += [" "*size]
        self.grid += ["-"*size]
        self.grid += [" "*size]
        self.grid += ["."*size for i in range(0, size)]

    def getStrings(self):
        return self.grid

    def add_ship(x, y):
        pass

    def check_hit():
        print(randint(0, 10))
        pass


def redraw(window, board):
    """
    Redraws the game area, this will be called for every input or update to 
    the board.
    """

    for i in range(0, len(board.grid)):
        for j in range(0, len(board.grid[0])):
            window.addstr(i, j, board.grid[i][j])

    window.refresh()


def main(window):
    """
    Main game loop runs here
    """
    # Create the board
    board = Board(size=8)

    # Cursor start position
    cursor_x = 1
    cursor_y = 1

    # Initialize curses
    window = curses.initscr()
    curses.noecho()
    curses.cbreak()
    window.keypad(True)
    window.move(cursor_y, cursor_x)

    # Game logic
    playing = True
    while (playing):
        redraw(window, board)
        action = window.getkey(cursor_y, cursor_x)
        if action == "q":
            break
        elif action == "KEY_UP":
            cursor_y -= 1
            window.move(cursor_y, cursor_x)
        elif action == "KEY_DOWN":
            cursor_y += 1
            window.move(cursor_y, cursor_x)
        elif action == "KEY_LEFT":
            cursor_x -= 1
            window.move(cursor_y, cursor_x)
        elif action == "KEY_RIGHT":
            cursor_x += 1
            window.move(cursor_y, cursor_x)
        elif action == "KEY_ENTER":
            action_location = window.getyx()
    
    # Undo changes to terminal output
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()


wrapper(main)
