
from random import randint
import curses
from curses import wrapper
from time import sleep

board_size = 0
ships_count = 0


class Board:
    """
    Board class that holds the current status of the game board
    """

    def __init__(self, size, ships):
        """
        Initialize board based on board size and ship count
        """
        self.size = size
        self.grid = [list("."*size) for i in range(0, size)]
        self.grid += [list("-"*size)]
        self.grid += [list("."*size) for i in range(0, size)]
        self.hidden_ships = []
        while (len(self.hidden_ships) < ships):
            tup = (randint(0, size), randint(0, size))
            if tup not in self.hidden_ships:
                self.hidden_ships.append(tup)

    def add_ship(self, y, x):
        """
        For adding ships during the setup phase.
        If the spot is empty, add ship and return True
        """
        if self.grid[y][x] == ".":
            self.grid[y][x] = "§"
            return True
        else:
            return False
    
    def attack_pos(self, y, x):
        """
        Check for a hit, update the grid to show an x if there's a ship there and return True.
        If there is no ship there update the grid to show a zero.
        If that spot has already been attacked return False.
        """
        if self.grid[y][x] == ".":
            if (y, x) in self.hidden_ships:
                self.grid[y][x] == "x"
                return "hit"
            else:
                self.grid[y][x] == "0"
                return "miss"
        else:
            return False

    def check_hit():
        print(randint(0, 10))
        pass


def redraw(window, board):
    """
    Redraws the game area, this should be called for every input or update to
    the board.
    """
    window.clear()
    for i in range(0, len(board.grid)):
        for j in range(0, len(board.grid[0])):
            window.addstr(i, j, str(board.grid[i][j]))

    window.refresh()


def start_game(window):
    """
    Main game loop runs here
    """

    # Cursor start position. Puts the cursor at bottom of the players board.
    cursor_x, cursor_y = 0, board_size*2

    # Create the board
    board = Board(size=board_size, ships=ships_count)

    # Game setup phase
    placed_ships = 0
    playing = True
    while (placed_ships < ships_count and playing):
        redraw(window, board)
        window.move(cursor_y, cursor_x)
        window.addstr(0, board_size+2, "Place your ships")
        window.addstr(
            1, board_size+2,
            "Remaing ships "+str(ships_count-placed_ships))
        action = window.getkey(cursor_y, cursor_x)
        if action == "q":
            return
        elif action == "KEY_UP":
            if (cursor_y > board_size+1):
                cursor_y -= 1
        elif action == "KEY_DOWN":
            if (cursor_y < board_size*2):
                cursor_y += 1
        elif action == "KEY_LEFT":
            if (cursor_x > 0):
                cursor_x -= 1
        elif action == "KEY_RIGHT":
            if (cursor_x < board_size-1):
                cursor_x += 1
        elif action == "\n" or action == " ":
            action_location = window.getyx()
            window.addstr(3, board_size+2, str(action_location))
            if board.add_ship(*action_location):
                placed_ships += 1
            else:
                pass
        window.clear()

    # Intermission phase
    curses.curs_set(0)
    redraw(window, board)
    window.addstr(0, board_size+2, "Ships placed, get ready for battle!")
    window.refresh()
    sleep(2.5)

    # Set up board and cursor for battle phase
    curses.curs_set(2)
    cursor_y, cursor_x = 0, 0

    # battle phase
    while (playing):
        redraw(window, board)
        window.move(cursor_y, cursor_x)
        window.addstr(0, board_size+2, "Select a position to attack")
        action = window.getkey(cursor_y, cursor_x)
        if action == "q":
            playing = False
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
        elif action == "\n" or action == " ":
            action_location = window.getyx()
            if board.attack_pos(*action_location):
                pass
            else:
                window.addstr(
                            1, board_size+2,
                            "Already attacked there!")

    # Undo changes to terminal output, might not be needed
    # since we have the wrapper.
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()


def main():
    """
    Sets up the game by asking the user for board size and ship count.
    This is done before entering the curses wrapper,
    so the terminal still behaves normally.
    """
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
