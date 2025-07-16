from time import sleep
def swipe_up(board, line_qtt, collumn_qtt, last_line, last_collumn):
#every swipe function has 2 phases:
#one to progress the sequences (be it PROGRESSION PHASE)
#and relocate items (be it RELOCATION PHASE)
#variables will have suffixes to it indicating the phases;
#e.g.:
#fst_seek_prog, reads "first seeker of progression phase";
#bottom_item_reloc, reads "bottom item of relocation phase")
#etc
    
    for j in range(collumn_qtt):
    #lock on a collumn

        # PROGRESSION PHASE

        for fst_seeker_prog in range(line_qtt-1):
        #check each item (i.e. each line) on that collumn except the lowermost one (will be checked by 2nd seeker)
        #(this first iteration inside collumns is only to progress the sequences.)

            top_item_prog = board[fst_seeker_prog][j]
            #alias to make code more readable

            if top_item_prog != 0:
            #if a non-zero item is found

                for snd_seeker_prog in range(fst_seeker_prog+1, line_qtt, +1):
                #check every other one below it 
                    
                    bottom_item_prog = board[snd_seeker_prog][j]
                    #alias to make code more readable 

                    if bottom_item_prog != 0:
                    #if another non-zero item is found
                        if bottom_item_prog == top_item_prog:
                        #and if it is equal to our top item
                            board[fst_seeker_prog][j] += bottom_item_prog
                            #we add to the top item the value of the bottom (same as doubling the top)
                            board[snd_seeker_prog][j] = 0
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

        for fst_seeker_reloc in range(1, line_qtt, +1):
        #check every item in the collumn except the uppermost (won't be repositioned)
        #(this second iteration is only to position non-zero numbers together.)
            
            bottom_item_reloc = board[fst_seeker_reloc][j]
            #alias to make code more readable
            #(now we must check positions above our first seeker, thus such an alias)

            if bottom_item_reloc != 0:
            #if non-zero value is found

                for snd_seeker_reloc in range(fst_seeker_reloc-1, -1, -1):
                #start the second seeker, checking positions above the first

                    top_item_reloc = board[snd_seeker_reloc][j]
                    #alias to make code more readable
                    
                    if top_item_reloc != 0:
                    #if another non-zero item is found
                        if snd_seeker_reloc+1 < fst_seeker_reloc:
                        #and it isn't immediately above our bottom item
                            board[snd_seeker_reloc+1][j] = bottom_item_reloc
                            #put the bottom item in the position right below
                            board[fst_seeker_reloc][j] = 0
                            #and nulify the bottom position
                        else: pass
                        #do nothing if it is immediately above

                        break
                        #in any case, we stop the iteration because the farthest possible position was found

                    elif snd_seeker_reloc == 0:
                    #if we are here, it means the border is zero, and thus we can send the item here no problem
                        board[0][j] = bottom_item_reloc
                        board[fst_seeker_reloc][j] = 0

                        break
                        #this break is written for explicitness; strictly, it is unnecessary

                    else: pass
                    #in other cases we are dealing necessarily with a zero item,
                    #just keep searching until the border or a non-zero is found
            
            else: pass
            #if a 0 item is found, do nothing, just go for the next



def swipe_left(board, line_qtt, collumn_qtt, last_line, last_collumn):
#every swipe function has 2 phases:
#one to progress the sequences (be it PROGRESSION PHASE)
#and relocate items (be it RELOCATION PHASE)
#variables will have suffixes to it indicating the phases;
#e.g.:
#fst_seek_prog, reads "first seeker of progression phase";
#bottom_item_reloc, reads "bottom item of relocation phase")
#etc
    
    for i in range(line_qtt):
    #lock on a line

        # PROGRESSION PHASE

        for fst_seeker_prog in range(collumn_qtt-1):
        #check each item (i.e. each collumn) on that line except the rightmost one (will be checked by 2nd seeker)
        #(this first iteration inside lines is only to progress the sequences.)

            left_item_prog = board[i][fst_seeker_prog]
            #alias to make code more readable

            if left_item_prog != 0:
            #if a non-zero item is found

                for snd_seeker_prog in range(fst_seeker_prog+1, collumn_qtt, +1):
                #start the second seeker, check every other item to the right 
                    
                    right_item_prog = board[i][snd_seeker_prog]
                    #alias to make code more readable

                    if right_item_prog != 0:
                    #if another non-zero item is found
                        if right_item_prog == left_item_prog:
                        #and if it is equal to our left item
                            board[i][fst_seeker_prog] += right_item_prog
                            #we add to the left item the value of the right (same as doubling the left)
                            board[i][snd_seeker_prog] = 0
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

        for fst_seeker_reloc in range(1, line_qtt, +1):
        #check every item in the line except the leftmost (won't be repositioned)
        #(this second iteration is only to position non-zero numbers together.)
            
            right_item_reloc = board[i][fst_seeker_reloc]
            #alias to make code more readable
            #(now we must check positions to the left of our first seeker, thus such an alias)

            if right_item_reloc != 0:
            #if non-zero value is found

                for snd_seeker_reloc in range(fst_seeker_reloc-1, -1, -1):
                #start the second seeker, checking positions to the left of the first

                    left_item_reloc = board[i][snd_seeker_reloc]
                    #alias to make code more readable
                    
                    if left_item_reloc != 0:
                    #if another non-zero item is found
                        if snd_seeker_reloc+1 < fst_seeker_reloc:
                        #and it isn't immediately next our item to the right
                            board[i][snd_seeker_reloc+1] = right_item_reloc
                            #move the right item immediately next to the left one
                            board[i][fst_seeker_reloc] = 0
                            #and nulify the previous position of right item
                        else: pass
                        #do nothing if it is immediately next

                        break
                        #in any case, we stop the iteration because the farthest possible position was found

                    elif snd_seeker_reloc == 0:
                    #if we are here, it means the border is zero, and thus we can send the item here no problem
                        board[i][0] = right_item_reloc
                        board[i][fst_seeker_reloc] = 0

                        break
                        #this break is written for explicitness; it is unnecessary strictly speaking

                    else: pass
                    #in other cases we are dealing necessarily with a zero item,
                    #just keep searching until the border or a non-zero is found
            
            else: pass
            #if a 0 item is found, do nothing, just go for the next

def swipe_down(board, line_qtt, collumn_qtt, last_line, last_collumn):
#every swipe function has 2 phases:
#one to progress the sequences (be it PROGRESSION PHASE)
#and relocate items (be it RELOCATION PHASE)
#variables will have suffixes to it indicating the phases;
#e.g.:
#fst_seek_prog, reads "first seeker of progression phase";
#bottom_item_reloc, reads "bottom item of relocation phase")
#etc
    
    for j in range(collumn_qtt):
    #lock on a collumn

        # PROGRESSION PHASE

        for fst_seeker_prog in range(last_line, 0, -1):
        #check, from bottom to top, each item (i.e. each line) on that collumn, except the uppermost one (will be checked by 2nd seeker)

            bottom_item_prog = board[fst_seeker_prog][j]
            #alias to make code more readable

            if bottom_item_prog != 0:
            #if a non-zero item is found

                for snd_seeker_prog in range(fst_seeker_prog-1, -1, -1):
                #start second seeker, check every other position above

                    top_item_prog = board[snd_seeker_prog][j]
                    #alias to make code more readable

                    if top_item_prog != 0:
                    #if another non-zero item is found
                        if top_item_prog == bottom_item_prog:
                        #and if it is equal to our bottom item
                            board[fst_seeker_prog][j] += top_item_prog
                            #we add to the bottom item the value of the top (same as doubling the bottom)
                            board[snd_seeker_prog][j] = 0
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

        for fst_seeker_reloc in range(last_line-1, -1, -1):
        #check, from bottom to top, every item on the collumn except the bottommost (won't be repositioned)

            top_item_reloc = board[fst_seeker_reloc][j]
            #alias to make code more readable
            #(now we must check positions below our first seeker, thus such an alias)

            if top_item_reloc != 0:
            #if non-zero value is found

                for snd_seeker_reloc in range(fst_seeker_reloc+1, line_qtt, +1):
                #start the second seeker, checking positions below the first

                    bottom_item_reloc = board[snd_seeker_reloc][j]
                    #alias to make code more readable
                    
                    if bottom_item_reloc != 0:
                    #if another non-zero item is found
                        if snd_seeker_reloc-1 > fst_seeker_reloc:
                        #and it isn't immediately below our top item
                            board[snd_seeker_reloc-1][j] = top_item_reloc
                            #put the top item in the position right above
                            board[fst_seeker_reloc][j] = 0
                            #and nulify the top position
                        else: pass
                        #do nothing if it is immediately below

                        break
                        #in any case, we stop the iteration because the farthest possible position was found

                    elif snd_seeker_reloc == last_line:
                    #if we are here, it means the border is zero, and thus we can send the item here no problem
                        board[last_line][j] = top_item_reloc
                        board[fst_seeker_reloc][j] = 0

                        break
                        #this break is written for explicitness; it is unnecessary strictly speaking

                    else: pass
                    #in other cases we are dealing necessarily with a zero item,
                    #just keep searching until the border or a non-zero is found
            
            else: pass
            #if a 0 item is found, do nothing, just go for the next

def swipe_right(board, line_qtt, collumn_qtt, last_line, last_collumn):
#every swipe function has 2 phases:
#one to progress the sequences (be it PROGRESSION PHASE)
#and relocate items (be it RELOCATION PHASE)
#variables will have suffixes to it indicating the phases;
#e.g.:
#fst_seek_prog, reads "first seeker of progression phase";
#bottom_item_reloc, reads "bottom item of relocation phase")
#etc
    
    for i in range(line_qtt):
    #lock on a line

        # PROGRESSION PHASE

        for fst_seeker_prog in range(last_collumn, 0, -1):
        #check, from right to left, each item (i.e. each collumn) on that line except the leftmost one (will be checked by 2nd seeker)

            right_item_prog = board[i][fst_seeker_prog]
            #alias to make code more readable

            if right_item_prog != 0:
            #if a non-zero item is found

                for snd_seeker_prog in range(fst_seeker_prog-1, -1, -1):
                #start the second seeker, check every other item to the left 
                    
                    left_item_prog = board[i][snd_seeker_prog]
                    #alias to make code more readable

                    if left_item_prog != 0:
                    #if another non-zero item is found
                        if left_item_prog == right_item_prog:
                        #and if it is equal to our item to the right
                            board[i][fst_seeker_prog] += left_item_prog
                            #we add to the right item the value of the left (same as doubling the right)
                            board[i][snd_seeker_prog] = 0
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

        # REPOSITION PHASE:

        for fst_seeker_reloc in range(last_collumn-1, -1, -1):
        #check every item in the line except the rightmost (won't be repositioned)
        #(this second iteration is only to position non-zero numbers together.)
            
            left_item_reloc = board[i][fst_seeker_reloc]
            #alias to make code more readable
            #(now we must check positions to the right of our first seeker, thus such an alias)

            if left_item_reloc != 0:
            #if non-zero value is found

                for snd_seeker_reloc in range(fst_seeker_reloc+1, collumn_qtt, +1):
                #start the second seeker, checking positions to the right of the first

                    right_item_reloc = board[i][snd_seeker_reloc]
                    #alias to make code more readable
                    
                    if right_item_reloc != 0:
                    #if another non-zero item is found
                        if snd_seeker_reloc-1 > fst_seeker_reloc:
                        #and it isn't immediately next our item to the left
                            board[i][snd_seeker_reloc-1] = left_item_reloc
                            #move the left item immediately next to the right one
                            board[i][fst_seeker_reloc] = 0
                            #and nulify the previous position of left item
                        else: pass
                        #do nothing if it is immediately next

                        break
                        #in any case, we stop the iteration because the farthest possible position was found

                    elif snd_seeker_reloc == last_collumn:
                    #if we are here, it means the border is zero, and thus we can send the item here no problem
                        board[i][last_collumn] = left_item_reloc
                        board[i][fst_seeker_reloc] = 0

                        break
                        #this break is written for explicitness; it is unnecessary strictly speaking

                    else: pass
                    #in other cases we are dealing necessarily with a zero item,
                    #just keep searching until the border or a non-zero is found
            
            else: pass
            #if a 0 item is found, do nothing, just go for the next

board = [
    [2,0,0,0],
    [0,0,4,0],
    [0,0,0,0],
    [0,2,0,0]
]

for line in board:
    print(f"{line}")

player_action = input("enter an action\n>>")

match player_action:
    case 'W':
        swipe_up(board, len(board), len(board[0]), len(board)-1, len(board[0])-1)
    case 'A':
        swipe_left(board, len(board), len(board[0]), len(board)-1, len(board[0])-1)
    case 'S':
        swipe_down(board, len(board), len(board[0]), len(board)-1, len(board[0])-1)
    case 'D':
        swipe_right(board, len(board), len(board[0]), len(board)-1, len(board[0])-1)

for line in board:
    print(f"{line}")