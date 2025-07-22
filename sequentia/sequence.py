from abc import ABC, abstractmethod 

class Sequence(ABC):

    """
    Sequences are constituted of two main things:
    - Terms
    - A rule

    Terms can be described by their value and their index;
    There must be a first arbitrary term.
    These must, therefore, be three of our main pieces of data (attributes)

    Sequence rules, for the matter of this game, must be recursive relations;
    Otherwise, this becomes purely a guessing game (how to know if the sequence is A-R-M or R-A-M?).
    This must also be another main piece of data (a method).
    """

    def __init__(self, first_term) -> None:
        self._first_term = first_term
        self._current_term = first_term
        self._current_term_index = 0
        #when instatiating a new sequence object,
        #the current term will always be the first
        #(indexing will start from 0 for standardization)

    @abstractmethod 
    def _rule(self):
        """
        Sequence rules must be in the form:
        'current_term'
        makes operation with
        'other_number'
        (this can be many constants, terms, and many operations)
        resulting in
        'next_term'
        (then 'current_term' becomes 'next_term')
        """
        pass

"""
arithmetic progressions doesn't seem to work;
relying on constants,
losing the game with such a sequence is impossible.
Also, a tile for constants would have to be spawned.

a completely different gamemode logic is to be made to implement them.

"arithmeticum convivium":

class ArithmeticProg(Sequence):

    def __init__(self, first_term, difference) -> None:
        self._current_term = first_term
        self._constant = difference

    def _rule(self):
        next_term = self._current_term

    pass
"""
class GeometricProg(Sequence):

    """
    These have a common ratio and a first term.
    
    For games in 2048 or Threes' form (sum two equals to get the next term),
    Ratio determines the amount of tiles you must merge for next term.
    
    Thus, for these kind of games, we ought to have a common ratio of 2.
    An option of 3 for more hardcore games.
    With 4 upwards, games in this form will simply become insufferable.

    For more varied geometric sequences,
    those with common ratios of 4 onwards
    ought to be in Arithmeticum Convivium form.
    
    A special arithmeticum convivium can be made
    With arithmetic and geometric sequences in a same game.
    """

    def __init__(self) -> None:
        self._first_term

class Sum(Sequence):
    pass