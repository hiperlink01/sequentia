from random import randint

class Board:

    def __init__(self, dimensions: dict, sequence: str):

        self._line_qtt: int = dimensions["lin"]
        self._collumn_qtt: int = dimensions["col"]
        
        self._last_line: int = self._line_qtt - 1
        self._last_collumn: int = self._collumn_qtt - 1
        
        self._seq: str = sequence
        self._turn = 0
        self._board: list[list[int]] = self._generate_board(self._line_qtt, self._collumn_qtt)
        self._occupied_positions: set[tuple[int,int]]= {(-1,-1)}
        self._any_change: bool = False

        self._new_term()
        self._update_occupied_positions()
        self._new_turn()
        
    def __str__(self) -> str:
        repr = ""

        for line in self._board:
            repr += '|'
            repr += str(line).replace(']', '').replace('[', '').replace(',', ' ')
            repr += '|'
            repr += '\n'

        return repr

    def swipe(self, direction: str) -> str:

        match direction:
            case 'W':
                self._transpose()
            case 'A':
                pass
            case 'S': 
                self._transpose()
                self._mirror()
            case 'D':
                self._mirror()
        
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
            if self._seek_arr_prog(i): self._any_change = True
            if self._seek_arr_reloc(i): self._any_change = True
            #if the progression phase or the relocation phase flags any changes
            #we will update the turn later in the code
           
        match direction:
            case 'W':
                self._transpose()
            case 'A':
                pass
            case 'S':
                self._mirror() 
                self._transpose()
            case 'D':
                self._mirror()
        
        if not self._any_change:    
            if self._line_qtt*self._collumn_qtt == len(self._occupied_positions):
                return 'L'
            else:
                return 'C'
        else:
            for line in self._board:
                if 2048 in line: 
                    self._any_change = False
                    return 'W'
            else: 
                self._update_occupied_positions()
                self._new_term()
                self._new_turn()
                self._any_change = False
                return 'C'
        #at the end of ._new_term(),
        #the i,j pair of the new term
        #is added to ._occupied_positions 
        
    def _seek_arr_prog(self, i):

        change = False

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
                            change = True
                            #flag the change
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

        return change

    def _seek_arr_reloc(self, i):

        change = False

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
                                change = True
                                #flag the change
                            else: pass
                            #do nothing if it is immediately next

                            break
                            #in any case, we stop the iteration because the farthest possible position was found

                        elif snd_seeker_reloc == 0:
                        #if we are here, it means the border is zero, and thus we can send the item here no problem
                            self._board[i][0] = right_item_reloc
                            self._board[i][fst_seeker_reloc] = 0
                            change = True
                            #flag the change

                            break
                            #this break is written for explicitness; it is unnecessary strictly speaking

                        else: pass
                        #in other cases we are dealing necessarily with a zero item,
                        #just keep searching until the border or a non-zero is found
                
                else: pass
                #if a 0 item is found, do nothing, just go for the next

        return change

    def _generate_board(self, line_qtt, collumn_qtt) -> list[list[int]]:
        
        board: list[list[int]] = []

        for i in range(line_qtt):
            board.append([])
            for j in range(collumn_qtt):
                board[i].append(0)

        return board

    def _update_occupied_positions(self):
        
        for i in range(self._line_qtt):
            for j in range(self._collumn_qtt):
                if self._board[i][j] != 0:
                    self._occupied_positions.add((i,j))
                else:
                    self._occupied_positions.discard((i,j))

    def _new_term(self):

        how_many: int

        if self._turn == 0:
        #if no turns exist, it means the board is newly generated,
            how_many = 2
            #so we initiate 2 elements to the board
            self._occupied_positions.remove((-1,-1))
            #and remove the dummy coordinate (-1,-1);
        else: how_many = 1
            #but if there are any turns, it means we're in the middle of the game,
            #therefore only 1 element will be initiated
            #ps.:
            #._turn is incremented by ._new_turn() 

        for term in range(how_many):

            new: tuple[int,int] = (randint(0, self._last_line),  randint(0, self._last_collumn))

            while(new in self._occupied_positions):
            #until it's different from an occupied position.
                new = (randint(0, self._last_line),  randint(0, self._last_collumn))
                #randomize pairs

            self._board[new[0]][new[1]] = 2 if randint(1, 100) <= 90 else 4
            #in the unnocuppied position:
            #insert either a 2 (90% chance); or a 4 (10% chance)

            self._occupied_positions.add(new)
            #update with the newly occupied position
            #(especially important when initialing the board)

    def _new_turn(self):
        #this method is expected to receive more tasks than this
        self._turn+=1

    def _transpose(self):

        aux = []

        for j in range(self._collumn_qtt):
            aux.append([])
            for i in range(self._line_qtt):
                aux[j].append(self._board[i][j])
        
        self._board = aux[::]

        aux = self._line_qtt
        self._line_qtt = self._collumn_qtt
        self._collumn_qtt = aux

        aux = self._last_line
        self._last_line = self._last_collumn
        self._last_collumn = aux

    def _mirror(self):

        aux_mtx = self._generate_board(self._line_qtt, self._collumn_qtt)

        for i in range(self._line_qtt):
            for j in range(self._collumn_qtt):
                aux_mtx[i][self._last_collumn - j] = self._board[i][j]

        self._board = aux_mtx[::]