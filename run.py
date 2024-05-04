# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
from random import randint
import curses
from curses import wrapper

board_size = 0
ships_count = 0

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


def start_game(window):
    """
    Main game loop runs here
    """

    # Cursor start position. Puts the cursor at bottom of the players board.
    cursor_x, cursor_y = 1, 1

    # Initialize curses
    window.addstr(0, 0, "Enter board square dimension (max 15): ")
    window.move(0, 40)
    
    # Temporarily allow ordinary input buffer
    window.clear()
    curses.noecho()
    curses.cbreak()
    window.keypad(True)

    # Create the board
    board = Board(size=board_size)

    # Game logic
    playing = True
    while (playing):
        redraw(window, board)
        if (cursor_y < 0):
            pass
        window.move(cursor_y, cursor_x)
        try:
            action = window.getkey(cursor_y, cursor_x)
            if action == "q":
                break
            elif action == "KEY_UP":
                cursor_y -= 1
            elif action == "KEY_DOWN":
                cursor_y += 1
            elif action == "KEY_LEFT":
                cursor_x -= 1
            elif action == "KEY_RIGHT":
                cursor_x += 1
            elif action == "KEY_ENTER":
                action_location = window.getyx()
        except ValueError as error:
            print(error)
            break
    
    # Undo changes to terminal output
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()


def main():
    global board_size
    global ships_count
    while (board_size < 3 or board_size > 12):
        try:
            board_size = int(
                input("select game board square size (min 3, max 12):\n")
                )
        except ValueError as error:
            print(f"Invalid input: {error} please try again")
    
    while (ships_count < 1 or ships_count > board_size**2):
        try:
            ships_count = int(
                input(
                    "Select the amount of ships per player"
                    f"(min 1, max {board_size**2}):\n"
                    ))
            if ships_count < 1:
                print(
                    "Can't play with 0 or less ships,"
                    "please put at least 1 ship"
                    )
            elif ships_count > board_size**2:
                print("That's way too many ships, please put a lower number")
        except ValueError as error:
            print(f"Invalid input: {error} please try again")

    wrapper(start_game)


main()
