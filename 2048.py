from random import randint
from enum import Enum
from typing import Optional

class PlayerAction(Enum):
    UP = 'W'
    LEFT = 'A'
    DOWN = 'S'
    RIGHT = 'D'

class Board:

    def _generate_board(self, line_qtt, collumn_qtt) -> list[list[int]]:
        
        #generating board representation ordered by lines, non-mirrored
        #(for processing left swipes)

        board: list[list[int]] = []

        for i in range(line_qtt):
            board.append([])
            for j in range(collumn_qtt):
                board[i].append(0)
        """
        #generating board representation ordered by lines, mirrored
        #(for processing right swipes)

        regular_mirrored: list[list[int]] = regular[::-1]

        #generating board representation ordered by collumns, non mirrored
        #(for processing upper swipes)

        transposed: list[list[int]] = []
        aux: list[list[int]] = []

        for i in range(collumn_qtt):
            transposed.append([])
            for j in range(line_qtt):
              transposed[i].append(0)
        
        transposed_mirrored: list[list[int]] = transposed[::-1]
        """

        return board

    def __init__(self, dimensions: dict, sequence: str):

        self._line_qtt: int = dimensions["lin"]
        self._collumn_qtt: int = dimensions["col"]
        
        self._last_line: int = self._line_qtt - 1
        self._last_collumn: int = self._collumn_qtt - 1
        
        self._seq: str = sequence
        self._board: list[list[int]] = self._generate_board(self._line_qtt, self._collumn_qtt)

    def _rotate_matrix(self, mtx_config_key: str, mtx_to_normalize = []) -> list[list[int]]:

        #this function is to rotate the board
        #rotating the board is useful so that we have only one swipe function that can deal with any swipe

        #regular board is for left swipes
        #transposed board is for upward swipes
        #mirrored board is for right swipes
        #transposed-mirrored board is for downward swipes
        
        #mtx_to_normalize is optional; it is to be used when falling back the board to its regular orientation

        if mtx_to_normalize == []:
            board = self._board[::]
        else:
            board = mtx_to_normalize[::]

        aux_board: list[list[int]] = []

        match mtx_config_key:
            case 'r':
                aux_board = board[::]

            case 't':
                for j in range(self._collumn_qtt):
                    aux_board.append([])
                    for i in range(self._line_qtt):
                        aux_board[j].append(board[i][j])

            case 'm':
                aux_board = board[::-1]

            case 'tm':

                aux_aux_board: list[list[int]] = []

                for j in range(self._collumn_qtt):
                    aux_aux_board.append([])
                    for i in range(self._line_qtt):
                        aux_aux_board[j].append(board[i][j])

                aux_board = aux_aux_board[::-1]
            
            case 'ntm':
                #(reads: "normalize transposed-mirrored")
                #special case for normalizing a transposed-mirrored matrix back to its regular form
                
                aux_aux_board: list[list[int]] = board[::-1]

                for j in range(self._collumn_qtt):
                    aux_board.append([])
                    for i in range(self._line_qtt):
                        aux_board[j].append(aux_aux_board[i][j])

        return aux_board

    def swipe(self, direction: str):

        aux_board: list[list[int]]
        
        aux_line_qtt: int
        aux_collumn_qtt: int

        mtx_config_key: str

        match direction:

            case 'W':
                mtx_config_key = "t"
                aux_line_qtt = self._collumn_qtt
                aux_collumn_qtt = self._line_qtt

            case 'A':
                mtx_config_key = "r"
                aux_line_qtt = self._line_qtt
                aux_collumn_qtt = self._collumn_qtt
            
            case 'S':
                mtx_config_key = "tm"
                aux_line_qtt = self._collumn_qtt
                aux_collumn_qtt = self._line_qtt

            case 'D':
                mtx_config_key = "m"
                aux_line_qtt = self._line_qtt
                aux_collumn_qtt = self._collumn_qtt

        aux_board = self._rotate_matrix(mtx_config_key)

        #every swipe has 2 phases:
        #one to progress the sequences (be it PROGRESSION PHASE)
        #and relocate items (be it RELOCATION PHASE)
        #variables will have suffixes to it indicating the phases;
        #e.g.:
        #fst_seek_prog, reads "first seeker of progression phase";
        #bottom_item_reloc, reads "bottom item of relocation phase")
        #etc
        
        for i in range(aux_line_qtt):
        #lock on a line

            # PROGRESSION PHASE

            for fst_seeker_prog in range(aux_collumn_qtt-1):
            #check each item (i.e. each collumn) on that line except the rightmost one (will be checked by 2nd seeker)
            #(this first iteration inside lines is only to progress the sequences.)

                left_item_prog = aux_board[i][fst_seeker_prog]
                #alias to make code more readable

                if left_item_prog != 0:
                #if a non-zero item is found

                    for snd_seeker_prog in range(fst_seeker_prog+1, aux_collumn_qtt, +1):
                    #start the second seeker, check every other item to the right 
                        
                        right_item_prog = aux_board[i][snd_seeker_prog]
                        #alias to make code more readable

                        if right_item_prog != 0:
                        #if another non-zero item is found
                            if right_item_prog == left_item_prog:
                            #and if it is equal to our left item
                                aux_board[i][fst_seeker_prog] += right_item_prog
                                #we add to the left item the value of the right (same as doubling the left)
                                aux_board[i][snd_seeker_prog] = 0
                                #and nulify the left item.
                            else: pass
                            #if it isn't equal, just leave it as is

                            fst_seeker_prog = snd_seeker_prog
                            #our first seeker is set to the position of the second.
                            #this is done so that, when reaching the first seeker's for statement, it is incremented
                            #(therefore, it starts from the next element, or shuts down if it exceeds the last iteration value)
                            
                            break
                            #stop second seeker so that first seeker can start from its place immediately 

                else: pass
                #if a zero item is found, do nothing, go for the next

            # REPOSITION PHASE:

            for fst_seeker_reloc in range(1, aux_line_qtt, +1):
            #check every item in the line except the leftmost (won't be repositioned)
            #(this second iteration is only to position non-zero numbers together.)
                
                right_item_reloc = aux_board[i][fst_seeker_reloc]
                #alias to make code more readable
                #(now we must check positions to the left of our first seeker, thus such an alias)

                if right_item_reloc != 0:
                #if non-zero value is found

                    for snd_seeker_reloc in range(fst_seeker_reloc-1, -1, -1):
                    #start the second seeker, checking positions to the left of the first

                        left_item_reloc = aux_board[i][snd_seeker_reloc]
                        #alias to make code more readable
                        
                        if left_item_reloc != 0:
                        #if another non-zero item is found
                            if snd_seeker_reloc+1 < fst_seeker_reloc:
                            #and it isn't immediately next our item to the right
                                aux_board[i][snd_seeker_reloc+1] = right_item_reloc
                                #move the right item immediately next to the left one
                                aux_board[i][fst_seeker_reloc] = 0
                                #and nulify the previous position of right item
                            else: pass
                            #do nothing if it is immediately next

                            break
                            #in any case, we stop the iteration because the farthest possible position was found

                        elif snd_seeker_reloc == 0:
                        #if we are here, it means the border is zero, and thus we can send the item here no problem
                            self._board[i][0] = right_item_reloc
                            self._board[i][fst_seeker_reloc] = 0

                            break
                            #this break is written for explicitness; it is unnecessary strictly speaking

                        else: pass
                        #in other cases we are dealing necessarily with a zero item,
                        #just keep searching until the border or a non-zero is found

                else: pass
                #if a 0 item is found, do nothing, just go for the next

        if mtx_config_key == "tm": mtx_config_key = "ntm"

        updated_board = self._rotate_matrix(mtx_config_key, aux_board)

        self._board = updated_board[::]

    def swipe_up(self):
    #every swipe function has 2 phases:
    #one to progress the sequences (be it PROGRESSION PHASE)
    #and relocate items (be it RELOCATION PHASE)
    #variables will have suffixes to it indicating the phases;
    #e.g.:
    #fst_seek_prog, reads "first seeker of progression phase";
    #bottom_item_reloc, reads "bottom item of relocation phase")
    #etc
        
        for j in range(self._collumn_qtt):
        #lock on a collumn

            # PROGRESSION PHASE

            for fst_seeker_prog in range(self._line_qtt-1):
            #check each item (i.e. each line) on that collumn except the lowermost one (will be checked by 2nd seeker)
            #(this first iteration inside collumns is only to progress the sequences.)

                top_item_prog = self._board[fst_seeker_prog][j]
                #alias to make code more readable

                if top_item_prog != 0:
                #if a non-zero item is found

                    for snd_seeker_prog in range(fst_seeker_prog+1, self._line_qtt, +1):
                    #check every other one below it 
                        
                        bottom_item_prog = self._board[snd_seeker_prog][j]
                        #alias to make code more readable 

                        if bottom_item_prog != 0:
                        #if another non-zero item is found
                            if bottom_item_prog == top_item_prog:
                            #and if it is equal to our top item
                                self._board[fst_seeker_prog][j] += bottom_item_prog
                                #we add to the top item the value of the bottom (same as doubling the top)
                                self._board[snd_seeker_prog][j] = 0
                                #and nulify the bottom item.
                            else: pass
                            #if it isn't equal, just leave it as is

                            fst_seeker_prog = snd_seeker_prog
                            #our first seeker is set to the position of the second.
                            #this is done so that, when reaching the first seeker's for statement, it is incremented
                            #(therefore, it starts from the next element, or shuts down if it exceeds the last iteration value)
                            
                            break
                            #stop second seeker so that first seeker can start from its place immediately 

                else: pass
                #if a zero item is found, do nothing, go for the next

            # REPOSITION PHASE:

            for fst_seeker_reloc in range(1, self._line_qtt, +1):
            #check every item in the collumn except the uppermost (won't be repositioned)
            #(this second iteration is only to position non-zero numbers together.)
                
                bottom_item_reloc = self._board[fst_seeker_reloc][j]
                #alias to make code more readable
                #(now we must check positions above our first seeker, thus such an alias)

                if bottom_item_reloc != 0:
                #if non-zero value is found

                    for snd_seeker_reloc in range(fst_seeker_reloc-1, -1, -1):
                    #start the second seeker, checking positions above the first

                        top_item_reloc = self._board[snd_seeker_reloc][j]
                        #alias to make code more readable
                        
                        if top_item_reloc != 0:
                        #if another non-zero item is found
                            if snd_seeker_reloc+1 < fst_seeker_reloc:
                            #and it isn't immediately above our bottom item
                                self._board[snd_seeker_reloc+1][j] = bottom_item_reloc
                                #put the bottom item in the position right below
                                self._board[fst_seeker_reloc][j] = 0
                                #and nulify the bottom position
                            else: pass
                            #do nothing if it is immediately above

                            break
                            #in any case, we stop the iteration because the farthest possible position was found

                        elif snd_seeker_reloc == 0:
                        #if we are here, it means the border is zero, and thus we can send the item here no problem
                            self._board[0][j] = bottom_item_reloc
                            self._board[fst_seeker_reloc][j] = 0

                            break
                            #this break is written for explicitness; it is unnecessary strictly speaking

                        else: pass
                        #in other cases we are dealing necessarily with a zero item,
                        #just keep searching until the border or a non-zero is found
                
                else: pass
                #if a 0 item is found, do nothing, just go for the next



    def swipe_left(self):
    #every swipe function has 2 phases:
    #one to progress the sequences (be it PROGRESSION PHASE)
    #and relocate items (be it RELOCATION PHASE)
    #variables will have suffixes to it indicating the phases;
    #e.g.:
    #fst_seek_prog, reads "first seeker of progression phase";
    #bottom_item_reloc, reads "bottom item of relocation phase")
    #etc
        
        for i in range(self._line_qtt):
        #lock on a line

            # PROGRESSION PHASE

            for fst_seeker_prog in range(self._collumn_qtt-1):
            #check each item (i.e. each collumn) on that line except the rightmost one (will be checked by 2nd seeker)
            #(this first iteration inside lines is only to progress the sequences.)

                left_item_prog = self._board[i][fst_seeker_prog]
                #alias to make code more readable

                if left_item_prog != 0:
                #if a non-zero item is found

                    for snd_seeker_prog in range(fst_seeker_prog+1, self._collumn_qtt, +1):
                    #start the second seeker, check every other item to the right 
                        
                        right_item_prog = self._board[i][snd_seeker_prog]
                        #alias to make code more readable

                        if right_item_prog != 0:
                        #if another non-zero item is found
                            if right_item_prog == left_item_prog:
                            #and if it is equal to our left item
                                self._board[i][fst_seeker_prog] += right_item_prog
                                #we add to the left item the value of the right (same as doubling the left)
                                self._board[i][snd_seeker_prog] = 0
                                #and nulify the left item.
                            else: pass
                            #if it isn't equal, just leave it as is

                            fst_seeker_prog = snd_seeker_prog
                            #our first seeker is set to the position of the second.
                            #this is done so that, when reaching the first seeker's for statement, it is incremented
                            #(therefore, it starts from the next element, or shuts down if it exceeds the last iteration value)
                            
                            break
                            #stop second seeker so that first seeker can start from its place immediately 

                else: pass
                #if a zero item is found, do nothing, go for the next

            # REPOSITION PHASE:

            for fst_seeker_reloc in range(1, self._line_qtt, +1):
            #check every item in the line except the leftmost (won't be repositioned)
            #(this second iteration is only to position non-zero numbers together.)
                
                right_item_reloc = self._board[i][fst_seeker_reloc]
                #alias to make code more readable
                #(now we must check positions to the left of our first seeker, thus such an alias)

                if right_item_reloc != 0:
                #if non-zero value is found

                    for snd_seeker_reloc in range(fst_seeker_reloc-1, -1, -1):
                    #start the second seeker, checking positions to the left of the first

                        left_item_reloc = self._board[i][snd_seeker_reloc]
                        #alias to make code more readable
                        
                        if left_item_reloc != 0:
                        #if another non-zero item is found
                            if snd_seeker_reloc+1 < fst_seeker_reloc:
                            #and it isn't immediately next our item to the right
                                self._board[i][snd_seeker_reloc+1] = right_item_reloc
                                #move the right item immediately next to the left one
                                self._board[i][fst_seeker_reloc] = 0
                                #and nulify the previous position of right item
                            else: pass
                            #do nothing if it is immediately next

                            break
                            #in any case, we stop the iteration because the farthest possible position was found

                        elif snd_seeker_reloc == 0:
                        #if we are here, it means the border is zero, and thus we can send the item here no problem
                            self._board[i][0] = right_item_reloc
                            self._board[i][fst_seeker_reloc] = 0

                            break
                            #this break is written for explicitness; it is unnecessary strictly speaking

                        else: pass
                        #in other cases we are dealing necessarily with a zero item,
                        #just keep searching until the border or a non-zero is found
                
                else: pass
                #if a 0 item is found, do nothing, just go for the next

    def swipe_down(self):
    #every swipe function has 2 phases:
    #one to progress the sequences (be it PROGRESSION PHASE)
    #and relocate items (be it RELOCATION PHASE)
    #variables will have suffixes to it indicating the phases;
    #e.g.:
    #fst_seek_prog, reads "first seeker of progression phase";
    #bottom_item_reloc, reads "bottom item of relocation phase")
    #etc
        
        for j in range(self._collumn_qtt):
        #lock on a collumn

            # PROGRESSION PHASE

            for fst_seeker_prog in range(self._last_line, 0, -1):
            #check, from bottom to top, each item (i.e. each line) on that collumn, except the uppermost one (will be checked by 2nd seeker)

                bottom_item_prog = self._board[fst_seeker_prog][j]
                #alias to make code more readable

                if bottom_item_prog != 0:
                #if a non-zero item is found

                    for snd_seeker_prog in range(fst_seeker_prog-1, -1, -1):
                    #start second seeker, check every other position above 
                        
                        top_item_prog = self._board[snd_seeker_prog][j]
                        #alias to make code more readable

                        if top_item_prog != 0:
                        #if another non-zero item is found
                            if top_item_prog == bottom_item_prog:
                            #and if it is equal to our bottom item
                                self._board[fst_seeker_prog][j] += top_item_prog
                                #we add to the bottom item the value of the top (same as doubling the bottom)
                                self._board[snd_seeker_prog][j] = 0
                                #and nulify the top item.
                            else: pass
                            #if it isn't equal, just leave it as is

                            fst_seeker_prog = snd_seeker_prog
                            #our first seeker is set to the position of the second.
                            #this is done so that, when reaching the first seeker's for statement, it is incremented
                            #(therefore, it starts from the next element, or shuts down if it exceeds the last iteration value)
                            
                            break
                            #stop second seeker so that first seeker can start from its place immediately 

                else: pass
                #if a zero item is found, do nothing, go for the next

            # REPOSITION PHASE:

            for fst_seeker_reloc in range(self._last_line-1, -1, -1):
            #check, from bottom to top, every item on the collumn except the bottommost (won't be repositioned)
                
                top_item_reloc = self._board[fst_seeker_reloc][j]
                #alias to make code more readable
                #(now we must check positions below our first seeker, thus such an alias)

                if top_item_reloc != 0:
                #if non-zero value is found

                    for snd_seeker_reloc in range(fst_seeker_reloc+1, self._line_qtt, +1):
                    #start the second seeker, checking positions below the first

                        bottom_item_reloc = self._board[snd_seeker_reloc][j]
                        #alias to make code more readable
                        
                        if bottom_item_reloc != 0:
                        #if another non-zero item is found
                            if snd_seeker_reloc-1 > fst_seeker_reloc:
                            #and it isn't immediately below our top item
                                self._board[snd_seeker_reloc-1][j] = top_item_reloc
                                #put the top item in the position right above
                                self._board[fst_seeker_reloc][j] = 0
                                #and nulify the top position
                            else: pass
                            #do nothing if it is immediately below

                            break
                            #in any case, we stop the iteration because the farthest possible position was found

                        elif snd_seeker_reloc == self._last_line:
                        #if we are here, it means the border is zero, and thus we can send the item here no problem
                            self._board[self._last_line][j] = top_item_reloc
                            self._board[fst_seeker_reloc][j] = 0

                            break
                            #this break is written for explicitness; it is unnecessary strictly speaking

                        else: pass
                        #in other cases we are dealing necessarily with a zero item,
                        #just keep searching until the border or a non-zero is found
                
                else: pass
                #if a 0 item is found, do nothing, just go for the next

    def swipe_right(self):
    #every swipe function has 2 phases:
    #one to progress the sequences (be it PROGRESSION PHASE)
    #and relocate items (be it RELOCATION PHASE)
    #variables will have suffixes to it indicating the phases;
    #e.g.:
    #fst_seek_prog, reads "first seeker of progression phase";
    #bottom_item_reloc, reads "bottom item of relocation phase")
    #etc
        
        for i in range(self._line_qtt):
        #lock on a line

            # PROGRESSION PHASE

            for fst_seeker_prog in range(self._last_collumn, 0, -1):
            #check, from right to left, each item (i.e. each collumn) on that line except the leftmost one (will be checked by 2nd seeker)

                right_item_prog = self._board[i][fst_seeker_prog]
                #alias to make code more readable

                if right_item_prog != 0:
                #if a non-zero item is found

                    for snd_seeker_prog in range(fst_seeker_prog-1, -1, -1):
                    #start the second seeker, check every other item to the left 
                        
                        left_item_prog = self._board[i][snd_seeker_prog]
                        #alias to make code more readable

                        if left_item_prog != 0:
                        #if another non-zero item is found
                            if left_item_prog == right_item_prog:
                            #and if it is equal to our item to the right
                                self._board[i][fst_seeker_prog] += left_item_prog
                                #we add to the right item the value of the left (same as doubling the right)
                                self._board[i][snd_seeker_prog] = 0
                                #and nulify the previous position of the left item.
                            else: pass
                            #if it isn't equal, just leave it as is

                            fst_seeker_prog = snd_seeker_prog
                            #our first seeker is set to the position of the second.
                            #this is done so that, when reaching the first seeker's for statement, it is incremented
                            #(therefore, it starts from the next element, or shuts down if it exceeds the last iteration value)
                            
                            break
                            #stop second seeker so that first seeker can start from its place immediately 

                else: pass
                #if a zero item is found, do nothing, go for the next

            # RELOCATION PHASE:

            for fst_seeker_reloc in range(self._last_line-1, -1, -1):
            #check every item in the line except the rightmost (won't be repositioned)
            #(this second iteration is only to position non-zero numbers together.)
                
                left_item_reloc = self._board[i][fst_seeker_reloc]
                #alias to make code more readable
                #(now we must check positions to the right of our first seeker, thus such an alias)

                if left_item_reloc != 0:
                #if non-zero value is found

                    for snd_seeker_reloc in range(fst_seeker_reloc+1, self._collumn_qtt, +1):
                    #start the second seeker, checking positions to the right of the first

                        right_item_reloc = self._board[i][snd_seeker_reloc]
                        #alias to make code more readable
                        
                        if right_item_reloc != 0:
                        #if another non-zero item is found
                            if snd_seeker_reloc-1 > fst_seeker_reloc:
                            #and it isn't immediately next our item to the left
                                self._board[i][snd_seeker_reloc-1] = left_item_reloc
                                #move the left item immediately next to the right one
                                self._board[i][fst_seeker_reloc] = 0
                                #and nulify the previous position of left item
                            else: pass
                            #do nothing if it is immediately next

                            break
                            #in any case, we stop the iteration because the farthest possible position was found

                        elif snd_seeker_reloc == self._last_collumn:
                        #if we are here, it means the border is zero, and thus we can send the item here no problem
                            self._board[i][self._last_collumn] = left_item_reloc
                            self._board[i][fst_seeker_reloc] = 0

                            break
                            #this break is written for explicitness; it is unnecessary strictly speaking

                        else: pass
                        #in other cases we are dealing necessarily with a zero item,
                        #just keep searching until the border or a non-zero is found
                
                else: pass
                #if a 0 item is found, do nothing, just go for the next

board = Board({"lin":4,"col":4}, "2048")

for line in board._board:
    print(f"{line}")

player_action = input("enter an action\n>>")

match player_action:
    case 'W':
        board.swipe_up()
    case 'A':
        board.swipe_left()
    case 'S':
        board.swipe_down()
    case 'D':
        board.swipe_right()

for line in board._board:
    print(f"{line}")