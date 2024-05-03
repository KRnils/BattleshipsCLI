# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
from random import randint
from pprint import pprint

class Board:

    def __init__(self, size):
        self.grid = [['.' for i in range(size)]]*size
    
    def printSelf(self):
        row = ""
        for i in self.grid:
            for j in i:
                row += ' '+(j)
            print(row)
            row = ""

def main(size):
    player_board = Board(size=size)
    computer_board = Board(size=size)
    player_board.printSelf()





if __name__ == '__main__':
    main(size=7)