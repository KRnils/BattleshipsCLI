
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
        self.size = size
        self.grid = [list("."*size) for i in range(0, size)]
        self.grid += [list("-"*size)]
        self.grid += [list("."*size) for i in range(0, size)]

    def getStrings(self):
        return self.grid

    def add_ship(self, y, x):
        if self.grid[y][x] == ".":
            self.grid[y][x] = "§"

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
            window.addstr(i, j, str(board.grid[i][j]))

    window.refresh()


def start_game(window):
    """
    Main game loop runs here
    """

    # Cursor start position. Puts the cursor at bottom of the players board.
    cursor_x, cursor_y = 1, 1

    # Create the board
    board = Board(size=board_size)

    # Game setup phase
    placed_ships = 0
    window.addstr(0, board_size+2, "Place your ships")
    while (placed_ships < ships_count):
        redraw(window, board)
        window.move(cursor_y, cursor_x)
        window.addstr(
            1, board_size+2,
            "Remaing ships "+str(ships_count-placed_ships))
        action = window.getkey(cursor_y, cursor_x)
        if action == "q":
            return
        elif action == "KEY_UP":
            if (cursor_y > 0):
                cursor_y -= 1
        elif action == "KEY_DOWN":
            if (cursor_y < board_size-1):
                cursor_y += 1
        elif action == "KEY_LEFT":
            if (cursor_x > 0):
                cursor_x -= 1
        elif action == "KEY_RIGHT":
            if (cursor_x < board_size-1):
                cursor_x += 1
        elif action == "\n":
            action_location = window.getyx()
            window.addstr(3, board_size+2, str(action_location))
            board.add_ship(*action_location)
            placed_ships += 1

    playing = True
    while (playing):
        redraw(window, board)
        window.move(cursor_y, cursor_x)
        try:
            action = window.getkey(cursor_y, cursor_x)
            if action == "q":
                break
            elif action == "KEY_UP":
                if (cursor_y > 0):
                    cursor_y -= 1
            elif action == "KEY_DOWN":
                if (cursor_y < board_size-1):
                    cursor_y += 1
            elif action == "KEY_LEFT":
                if (cursor_x > 0):
                    cursor_x -= 1
            elif action == "KEY_RIGHT":
                if (cursor_x < board_size-1):
                    cursor_x += 1
            elif action == "KEY_ENTER":
                action_location = window.getyx()
        except ValueError as error:   # does nothing right now :p
            print(error)
            break

    # Undo changes to terminal output, might not be needed
    # since we have the wrapper.
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
                input("select game board square size (min 3, max 10):\n")
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
