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
                for j in range(len(board)):
                    aux_board.append([])
                    for i in range(len(board[0])):
                        aux_board[j].append(board[i][j])

            case 'm':

                last_collumn = len(board[0])-1

                for i in range(len(board)):
                    for j in range(len(board[0])):
                        aux_board[i][last_collumn-j] = board[i][j]

            case 'tm':

                aux_aux_board = []

                for j in range(len(board)):
                    aux_aux_board.append([])
                    for i in range(len(board[0])):
                        aux_aux_board[j].append(board[i][j])

                aux_board = aux_aux_board[::]

                last_collumn = len(aux_aux_board[0])-1

                for i in range(len(aux_aux_board)):
                    for j in range(len(aux_aux_board[0])):
                        aux_board[i][last_collumn-j] = aux_aux_board[i][j]
            
            case 'ntm':
                #(reads: "normalize transposed-mirrored")
                #special case for normalizing a transposed-mirrored matrix back to its regular form

                aux_aux_board = board[::]

                last_collumn = len(board[0])-1

                for i in range(len(board)):
                    for j in range(len(board[0])):
                        aux_aux_board[i][last_collumn-j] = board[i][j]

                for j in range(len(board)):
                    aux_board.append([])
                    for i in range(len(board[0])):
                        aux_board[j].append(aux_aux_board[i][j])


        print(aux_board)

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