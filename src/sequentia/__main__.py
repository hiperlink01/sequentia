from .board import Board
from time import sleep
import os

def main():
    board = Board({"lin":4,"col":4}, "2048")

    os.system("clear")

    print(board)

    turn_result: str = 'C'

    while turn_result == 'C':

        player_action = input("enter an action\n>>").upper()

        turn_result = board.swipe(player_action)

        os.system("clear")

        print(board)

    if turn_result == 'W': print("You win!")
    elif turn_result == 'L': print("You lose...")
    sleep(2)

if __name__ == "__main__":
    main()