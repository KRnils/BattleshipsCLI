from random import randint
import curses
from curses import wrapper
from time import sleep

# Global variables for board size and ship count.
# This solutions was chosen to deal with the curses wrapper,
# combined with the board size and ship count choices for the player.
# It's possible to create an in-wrapper input for those choices,
# but it would take more time.
# So currently those choices are made "outside" the game.
board_size = 0
ships_count = 0


class Board:
    """ Board class that holds the current status of the game board """

    def __init__(self, size, ships):
        """ Initialize board based on board size and ship count """
        self.size = size
        self.grid = [list("."*size) for i in range(0, size)]
        self.grid += [list("-"*size)]
        self.grid += [list("."*size) for i in range(0, size)]

        # This creates the list of locations for the computer side's ships
        self.hidden_ships = []
        while (len(self.hidden_ships) < ships):
            tup = (randint(0, size-1), randint(0, size-1))
            if tup not in self.hidden_ships:
                self.hidden_ships.append(tup)

    def add_ship(self, y, x):
        """
        For adding ships during the setup phase.
        If the spot is empty, add ship and return True.
        """
        if self.grid[y][x] == ".":
            self.grid[y][x] = "§"
            return True
        else:
            return False

    def attack_pos(self, y, x):
        """
        Check for a hit, update the grid to show an x if there's a ship there
        and return True.
        If there is no ship there update the grid to show a zero.
        If that spot has already been attacked return "none".
        Used for both player and computer ships.
        """
        if self.grid[y][x] == ".":
            if (y, x) in self.hidden_ships:
                self.grid[y][x] = "x"
                return "hit"
            else:
                self.grid[y][x] = "0"
                return "miss"
        elif self.grid[y][x] == "§":
            self.grid[y][x] = "X"
            return "hit"
        else:
            return "none"


def redraw(window, board):
    """
    Redraws the game area, this should be called for every input or update to
    the board. Takes a window and board as arguments
    so the board grid can be drawn in the window.
    """
    window.clear()
    for i in range(0, len(board.grid)):
        for j in range(0, len(board.grid[0])):
            window.addstr(i, j, str(board.grid[i][j]))

    window.refresh()


def start_game(window):
    """
    Main game logic is here.
    Sets up the board and writes the status of the game.
    """
    # Create the board
    board = Board(size=board_size, ships=ships_count)

    # Start scores for calculating end of game and winner.
    player_score = 0
    computer_score = 0

    # Cursor start position. Puts the cursor at bottom of the players board.
    cursor_x, cursor_y = 0, board_size*2

    # Game setup phase loop
    placed_ships = 0
    while (placed_ships < ships_count):
        redraw(window, board)
        window.addstr(0, board_size+2, "Place your ships")
        window.addstr(
            1, board_size+2,
            "Remaing ships "+str(ships_count-placed_ships))

        # wait for player input and move cursor or place ship based on the key
        action = window.getkey(cursor_y, cursor_x)
        if action in ("q", "Q"):
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
            if board.add_ship(cursor_y, cursor_x):
                placed_ships += 1
                window.addstr(1, board_size+2,
                              "Remaing ships "+str(ships_count-placed_ships))
                window.refresh()
            else:
                pass

    # Set up board and cursor for battle phase.
    cursor_y, cursor_x = 0, 0
    window.addstr(0, board_size+2, "Get ready for battle!")
    window.refresh()
    sleep(2)

    # Battle phase while loop. Redraws the board,
    # waits for player input and performs computer action.
    while (player_score < ships_count and computer_score < ships_count):
        redraw(window, board)
        window.move(cursor_y, cursor_x)
        window.addstr(0, board_size+2, "Select a position to attack")
        window.addstr(5, board_size+2, "Ships left:")

        # Show current game status displayed as remaining ships.
        window.addstr(
            6, board_size+2,
            f"Player: {ships_count-computer_score} "
            f"Computer: {ships_count-player_score}"
            )

        # Wait for player input, then move cursor or attack a position.
        action = window.getkey(cursor_y, cursor_x)
        if action in ("q", "Q"):
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
        elif action == "\n" or action == " ":
            hitormiss = board.attack_pos(cursor_y, cursor_x)
            if hitormiss == "hit":
                window.addstr(1, board_size+2, "It's a hit!")
                window.refresh()
                player_score += 1
                sleep(1)
                if player_score == ships_count:
                    break
            elif hitormiss == "miss":
                window.addstr(1, board_size+2, "It's a miss!")
                window.refresh()
                sleep(1)
            else:
                window.addstr(1, board_size+2, "Already attacked that"
                              " position, pick another.")
                window.refresh()
                sleep(1)
            if hitormiss != "none":
                redraw(window, board)
                window.addstr(0, board_size+2, "Computer's turn...")
                window.refresh()
                sleep(1)
                hitormiss = "none"
                while (hitormiss == "none"):
                    attack = (randint(board_size+1,
                                      board_size*2), randint(0, board_size-1))
                    hitormiss = board.attack_pos(*attack)
                if hitormiss == "hit":
                    redraw(window, board)
                    window.addstr(0, board_size+2, "Computer's turn...")
                    window.addstr(1, board_size+2, "It's a hit!")
                    computer_score += 1
                elif hitormiss == "miss":
                    redraw(window, board)
                    window.addstr(0, board_size+2, "Computer's turn...")
                    window.addstr(1, board_size+2, "It's a miss!")
                window.refresh()
                sleep(1)

    # Final redraw to show the board along with the game outcome.
    redraw(window, board)

    if computer_score < player_score:
        # Win message.
        window.addstr(0, board_size+2, "You won!")
        window.refresh()
        sleep(0.5)
        window.addstr(1, board_size+2, "Congratulations!")
        window.refresh()
        sleep(2)
    elif computer_score > player_score:
        # Loss message.
        window.addstr(0, board_size+2, "You lose!")
        window.refresh()
        sleep(0.5)
        window.addstr(1, board_size+2, ":(")
        window.refresh()
        sleep(2)
    else:
        # This should never happen but is here just in case.
        window.addstr(0, board_size+2, "It's a tie??")
        window.refresh()
        sleep(3)

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
    # Reset global variables, so repeat games work as intended
    board_size = 0
    ships_count = 0

    # Intro text
    intro_text = """Hi and welcome to BattleshipsCLI!
    a fully terminal based version of the classic board game.

    Your ships will be represented as a '§' symbol, while the computers ships
    will be invisible to you. A hit ship on either side looks like this 'X'.
    And finally a missed tile will be represented by a '0'.

    You and the computer will take turns trading shots until
    all ships on either side has been hit.

    First you will be asked to pick a board size and ship count, it's a good
    idea to keep the ship count below 10 or the game will take a long time to
    finish. However you are free to play with enough ships to fill the entire
    board if you like.

    Next you will place your ships on your side of the board (the lower half).
    The computer will place their ships quietly.
    After setup, when it's your turn, move the cursor with the arrow keys and
    press enter or space to select a position to attack.
    You can quit the game at any time by pressing q or Q on the keyboard"""

    print(intro_text)

    # Game size selection loop, loops until a valid size is selected
    while (board_size < 3 or board_size > 10):
        try:
            board_size = int(
                input("Select game board square size (min 3, max 10):\n")
                )
            if board_size > 10:
                print("Maybe pick a slightly smaller board size")
            elif board_size < 3:
                print("Please pick a bigger board size")
        except ValueError as error:
            print(f"Invalid input: {error} please try again")

    # Game ship count selection loop, runs until a valid ship count is selected
    while (ships_count < 1 or ships_count > board_size**2):
        try:
            ships_count = int(
                input(
                    "Select the amount of ships per player"
                    f"(min 1, max {board_size**2}):\n"
                    ))
            if ships_count < 1:
                print(
                    "Can't play with 0 or less ships, "
                    "please put at least 1 ship\n"
                    )
            elif ships_count > board_size**2:
                print("That's way too many ships, please put a lower number\n")
        except ValueError as error:
            print(f"Invalid input: {error} please try again")

    # curses wrapper that starts the game in a curses "window"
    wrapper(start_game)


if __name__ == '__main__':
    main()
    while (True):
        # anything other than y or Y is "no", no need for n specifically.
        if input("play again?(y/n)") in ("y", "Y"):
            main()
        else:
            print("bye!")
            sleep(0.5)
            break
