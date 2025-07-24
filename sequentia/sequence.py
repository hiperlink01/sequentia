from abc import ABC, abstractmethod 

class Sequence(ABC):

    """
    Sequences are constituted of two main things:
    - Terms
    - A rule

    Terms can be described by their value and their index;
    There must also be a first arbitrary term.
    Thus, be these our three main instance attributes

    Sequence rules, for the matter of this game, must be recursive relations;
    Otherwise, this becomes purely a guessing game (how to know if the sequence is A-R-M or R-A-M?).
    This must be our main method
    """

    def __init__(self, first_term) -> None:
        if not isinstance(first_term, int):
            raise TypeError(f"Must be an integer sequence; first term: {first_term} violates.")
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

class ArithmeticProg(Sequence):
    """
    arithmetic progressions doesn't seem to work;
    relying on constants,
    losing the game with such a sequence is impossible.
    Also, a tile for constants would have to be spawned.

    a completely different gamemode logic is to be made to implement them.

    "arithmeticum convivium":
    """
    pass

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

    def __init__(self, first_term, ratio):
        if first_term == 0 or ratio == 0:
            raise ValueError(f"First term: {first_term} or ratio: {ratio} must never be 0.")
        elif ratio == 1:
            raise ValueError(f"Ratio must never be 1.")
        else:
            super().__init__(first_term)
            self._ratio = ratio

class SumOfTwoTerms(Sequence):
    """
    Sequences such as Fibonacci
    """
    pass