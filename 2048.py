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

    def swipe(self, direction: str):

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

board = Board({"lin":4,"col":4}, "2048")

board._board = [
    
    [0,2,0,0],
    [0,4,0,4],
    [0,0,0,0],
    [8,4,2,0]
]

for line in board._board:
    print(f"{line}")

while True:
    player_action = input("enter an action\n>>")

    board.swipe(player_action)

    for line in board._board:
        print(f"{line}")