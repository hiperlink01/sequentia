from .board import Board
import os
import time

class Game:

    def __init__(self): self._start()

    def _start(self):

        self._board = Board({"lin":4,"col":4}, "2048")
        self._turn = 1
        self._result: str = 'C'

        self._game_time_counter = 0

        while self._result == 'C':
            print(self._turn)
            print(self._board)
            self._result = self._new_turn()
            os.system("clear")

        if self._result == 'W': print("You Win!")
        if self._result == 'L': print("You Lose.")

        time.sleep(2)

    def _new_turn(self):

        any_change = self._board.swipe(input("enter an action\n>>").upper())

        if any_change:
            self._turn+=1
            if self._check_for_win() == True: return 'W'
            if self._check_for_loss() == True: return 'L'
        
        return 'C'
    
    """
    In our present case,
    Ensuring single responsibility is more important than data hiding.
    Therefore,
    On these two functions below,
    Private variables from our ._board are collected for inspection.
    """

    def _check_for_win(self):

        grid = self._board._grid

        for line in grid:
            if 2048 in line: return True
        
        return False

    def _check_for_loss(self):

        #aliases for the private data inside our board; too verbose otherwise.
        
        grid: list[list[int]] = self._board._grid
        
        line_qtt = self._board._line_qtt
        collumn_qtt = self._board._collumn_qtt

        last_line = self._board._last_line
        last_collumn = self._board._last_collumn
        
        occupied_positions: set[tuple[int,int]] = self._board._occupied_positions

        if len(occupied_positions) != line_qtt * collumn_qtt:
            return False
        #if not all positions are occupied,
        #the player didn't lose
        else:
            #but if all possible positions are occupied,
            #we gotta check every neighboring pairs:
            for i in range(line_qtt-1):
                for j in range(collumn_qtt-1):
                    if grid[i][j] in (grid[i][j+1], grid[i+1][j]):
                        return False
            #after this, the seeker still has to check
            #the last line, horizontally
            #and the last collumn, vertically

            for j in range(collumn_qtt-1):
                if grid[last_line][j] == grid[last_line][j+1]:
                    return False
            #checking last line horizontally

            for i in range(line_qtt-1):
                if grid[i][last_collumn] == grid[i][last_collumn]:
                    return False
            #checking last collumn vertically
        
        return True
        #if we have a full board, 
        #and none of our checks flag a combination possibility,
        #we have a definite loss