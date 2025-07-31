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
    def _generate_sequence(self):
        pass

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

class TwoTerm(Sequence):
    
    """
    In a recursive two term sequence:

    One must declare the relation between two terms,
    So that the next term is found by operating two terms that respect such relation;
    
    One must also declare the operation to be performed by the two terms;

    Finally, a list of all first terms necessary to start the sequence flow must be given.

    e.g.:
    In Fibonacci,
    We have a relation between terms of 1,
    A sum operation,
    And as first terms 1 and 1;
    Meaning that:
    We must sum two terms,
    One next to the other in the sequence,
    And the first ones we must sum are 1 and 1.
    So: 1+1 = 2, 1+2 = 3, 2+3 = 5, 3+5 = 8
    etc.
    (1, 1, 2, 3, 5, 8)

    If we had a relation of 2,
    Everything else being equal,
    We would sum two terms,
    But not terms that are immediately next to one another;
    Instead, terms that have one other term inbetween them.

    e.g:
    If we had 1, 1, 2 as first terms,
    (the first "1") 1 + 2 = 3,
    (the second "1") 1 + 3 = 4,
    2 + 4 = 6
    etc.
    (1, 1, 2, 3, 4, 6)

    This is why our constructor is set as it is, to enable modularity.
    """
    
    def __init__(self, index_relation: int = 0, operation: str = '+', fst_terms: list[int] = [2], index_of_last=10) -> None:
        
        self._terms = self._generate_sequence (
            fst_terms,
            index_relation,
            operation,
            index_of_last
        )

    def _generate_sequence(self, terms, index_relation, operation, index_of_last, ant_index=0):

        post_index = ant_index + index_relation

        self._rule(terms, ant_index, post_index, operation)

        if post_index < index_of_last:
            
            ant_index+=1
            self._generate_sequence(
                terms,
                index_relation,
                operation,
                index_of_last,
                ant_index=ant_index
            )

        else: return terms

    def _rule(self, terms: list[int], ant_index, post_index, operation: str):

        ant = terms[ant_index]
        #anterior term
        post = terms[post_index]
        #posterior term

        match operation:
            case '+': terms.append(ant + post)
            case '-': terms.append(ant - post)
            case '*': terms.append(ant * post)
        #to get next term, operate on the anterior and posterior terms

class ThreeTerm:
    pass


    """
    class ArithmeticProg(Sequence):
        
        arithmetic progressions doesn't seem to work;
        relying on constants,
        losing the game with such a sequence is impossible.
        Also, a tile for constants would have to be spawned.

        a completely different gamemode logic is to be made to implement them.

        "arithmeticum convivium":
        
        pass
    
    
    class GeometricProg(Sequence):

        
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
        

        def __init__(self, first_term, ratio):
            if first_term == 0 or ratio == 0:
                raise ValueError(f"First term: {first_term} or ratio: {ratio} must never be 0.")
            elif ratio == 1:
                raise ValueError(f"Ratio must never be 1.")
            else:
                super().__init__(first_term)
                self._ratio = ratio
    """