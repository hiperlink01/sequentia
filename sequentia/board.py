from random import randint

class Board:

    def __init__(self, dimensions: dict, sequence: str):

        self._line_qtt: int = dimensions["lin"]
        self._collumn_qtt: int = dimensions["col"]
        
        self._last_line: int = self._line_qtt - 1
        self._last_collumn: int = self._collumn_qtt - 1
        
        self._seq: str = sequence
        self._grid: list[list[int]] = self._generate_grid(self._line_qtt, self._collumn_qtt)
        self._occupied_positions: set[tuple[int,int]]= {(-1,-1)}

        self._newly_computed_values: list[int] = []

        self._new_term()
        self._update_occupied_positions()
        
    def __str__(self) -> str:

        repr = ""

        """
        max_value = 0
        for line in self._grid:
            for item in line:
                if item > max_value:
                    max_value = item
        cell_size = len(str(max_value))
        """

        for i in range(self._line_qtt):

            if i == 0 or i == self._last_line:
                line = str(self._grid[i]).replace('[','[ ').replace('0,',' |').replace(',','|').replace('0]',' ]')
            else:
                line = str(self._grid[i]).replace('[','| ').replace('0,',' |').replace(',','|').replace('0]',' |').replace(']','|')
            

            repr += line + '\n'

        return repr

    @property
    def newly_computed_values(self):
        return self._newly_computed_values

    @property
    def grid(self):
        return self._grid
    
    @property
    def line_qtt(self):
        return self._line_qtt
    
    @property
    def collumn_qtt(self):
        return self._collumn_qtt
    
    @property
    def last_line(self):
        return self._last_line

    @property
    def last_collumn(self):
        return self._last_collumn
    
    @property
    def occupied_positions(self):
        return self._occupied_positions

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
        
        any_change = False
        self._newly_computed_values = []
        #in every new swipe still to be computed,
        #there is no change,
        #and no new terms found by tile merging.

        for i in range(self._line_qtt):
        #lock on a line
            if self._seek_arr_prog(i): any_change = True
            if self._seek_arr_reloc(i): any_change = True
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
        
        if any_change:
            self._update_occupied_positions()
            self._new_term()
            #at the end of ._new_term(),
            #the i,j pair of the new term
            #is added to ._occupied_positions 

        return any_change
        
    def _seek_arr_prog(self, i):

        change = False

        # PROGRESSION PHASE

        fst_seeker_prog: int = 0

        while fst_seeker_prog <= self._last_collumn-1:
        #check each item (i.e. each collumn) on that line except the rightmost one (will be checked by 2nd seeker)
        #(this first iteration inside lines is only to progress the sequences.)

            left_item_prog = self._grid[i][fst_seeker_prog]
            #alias to make code more readable

            if left_item_prog != 0:
            #if a non-zero item is found

                snd_seeker_prog: int = fst_seeker_prog+1

                while snd_seeker_prog <= self._last_collumn:
                #start the second seeker, check every other item to the right 
                    
                    right_item_prog = self._grid[i][snd_seeker_prog]
                    #alias to make code more readable

                    if right_item_prog != 0:
                    #if another non-zero item is found
                        if right_item_prog == left_item_prog:
                        #and if it is equal to our left item
                            self._grid[i][fst_seeker_prog] += right_item_prog
                            #we add to the left item the value of the right (same as doubling the left)
                            self._grid[i][snd_seeker_prog] = 0
                            #and nulify the left item.
                            self._newly_computed_values.append(self._grid[i][fst_seeker_prog])
                            #store the value of the new sequence term in a list;
                            #it will be gathered by Game and compute score.
                            change = True
                            #flag the change
                        else: pass
                        #if it isn't equal, just leave it as is

                        fst_seeker_prog = snd_seeker_prog-1
                        #our first seeker is set to the position before the second.
                        #this is done so that, when reaching the first seeker's increment statement, it is exactly on second seeker's previous position
                        #(therefore, it starts from the next element, or shuts down if it exceeds the last iteration value)
                        
                        break
                        #stop second seeker so that first seeker can start from its place immediately

                    snd_seeker_prog+=1 

            else: pass
            #if a zero item is found, do nothing, go for the next

            fst_seeker_prog+=1

        return change

    def _seek_arr_reloc(self, i):

        change = False

        fst_seeker_reloc = 1

        while fst_seeker_reloc <= self._last_line:
            #check every item in the line except the leftmost (won't be repositioned)
            #(this second iteration is only to position non-zero numbers together.)
                
            right_item_reloc = self._grid[i][fst_seeker_reloc]
            #alias to make code more readable
            #(now we must check positions to the left of our first seeker, thus such an alias)

            if right_item_reloc != 0:
            #if non-zero value is found

                snd_seeker_reloc = fst_seeker_reloc-1

                while snd_seeker_reloc >= 0:
                #start the second seeker, checking positions to the left of the first

                    left_item_reloc = self._grid[i][snd_seeker_reloc]
                    #alias to make code more readable
                    
                    if left_item_reloc != 0:
                    #if another non-zero item is found
                        if snd_seeker_reloc+1 < fst_seeker_reloc:
                        #and it isn't immediately next our item to the right
                            self._grid[i][snd_seeker_reloc+1] = right_item_reloc
                            #move the right item immediately next to the left one
                            self._grid[i][fst_seeker_reloc] = 0
                            #and nulify the previous position of right item
                            change = True
                            #flag the change
                        else: pass
                        #do nothing if it is immediately next

                        break
                        #in any case, we stop the iteration because the farthest possible position was found

                    elif snd_seeker_reloc == 0:
                    #if we are here, it means the border is zero, and thus we can send the item here no problem
                        self._grid[i][0] = right_item_reloc
                        self._grid[i][fst_seeker_reloc] = 0
                        change = True
                        #flag the change

                        break
                        #this break is written for explicitness; it is unnecessary strictly speaking

                    else: pass
                    #in other cases we are dealing necessarily with a zero item,
                    #just keep searching until the border or a non-zero is found

                    snd_seeker_reloc-=1
            
            else: pass
            #if a 0 item is found, do nothing, just go for the next

            fst_seeker_reloc+=1

        return change

    def _generate_grid(self, line_qtt, collumn_qtt) -> list[list[int]]:
        
        grid: list[list[int]] = []

        for i in range(line_qtt):
            grid.append([])
            for j in range(collumn_qtt):
                grid[i].append(0)

        return grid

    def _update_occupied_positions(self):
        
        for i in range(self._line_qtt):
            for j in range(self._collumn_qtt):
                if self._grid[i][j] != 0:
                    self._occupied_positions.add((i,j))
                else:
                    self._occupied_positions.discard((i,j))

    def _new_term(self):

        how_many: int

        if (-1,-1) in self._occupied_positions:
        #if the dummy coordinate is present, it means the board is newly generated,
            how_many = 2
            #so we initiate 2 elements to the board
            self._occupied_positions.remove((-1,-1))
            #and remove the dummy coordinate (-1,-1);
        else: how_many = 1
            #if there is no dummy coordinate, it means we're in the middle of the game,
            #therefore only 1 element will be initiated

        for term in range(how_many):

            new: tuple[int,int] = (randint(0, self._last_line),  randint(0, self._last_collumn))

            while(new in self._occupied_positions):
            #until it's different from an occupied position.
                new = (randint(0, self._last_line),  randint(0, self._last_collumn))
                #randomize pairs

            self._grid[new[0]][new[1]] = 2 if randint(1, 100) <= 90 else 4
            #in the unnocuppied position:
            #insert either a 2 (90% chance); or a 4 (10% chance)

            self._occupied_positions.add(new)
            #update with the newly occupied position
            #(especially important when initialing the board)

    def _transpose(self):

        aux = []

        for j in range(self._collumn_qtt):
            aux.append([])
            for i in range(self._line_qtt):
                aux[j].append(self._grid[i][j])
        
        self._grid = aux[::]

        aux = self._line_qtt
        self._line_qtt = self._collumn_qtt
        self._collumn_qtt = aux

        aux = self._last_line
        self._last_line = self._last_collumn
        self._last_collumn = aux

    def _mirror(self):

        aux_mtx = self._generate_grid(self._line_qtt, self._collumn_qtt)

        for i in range(self._line_qtt):
            for j in range(self._collumn_qtt):
                aux_mtx[i][self._last_collumn - j] = self._grid[i][j]

        self._grid = aux_mtx[::]