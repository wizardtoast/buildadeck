# Build-a-Deck Workshop

from buildadeck.utils import simple_repr
from collections import namedtuple
from collections.abc import Sequence
from functools import cached_property
from secrets import randbelow
from types import SimpleNamespace

Card = namedtuple('Card', ['suit', 'rank'])

def wildcard():
    '''return a Card with no suit or rank'''
    return Card(None, None)

class Deck(Sequence):
    '''create a deck of cards that are evenly distributed to each suit
    wildcards are created in addition to suited cards'''

    def __init__(self, suits, ranked_cards, wildcards):
        self.suits = suits
        self.ranked_cards = ranked_cards
        self.wildcards = wildcards

    @cached_property
    def cards(self):
        suits_is_factor = ((self.ranked_cards % len(self.suits)) == 0)
        if not suits_is_factor:
            raise ValueError('length of suits must be a factor of ranked_cards')
        ranks_per_suit = self.ranked_cards // len(self.suits)
        value_range = range(1, ranks_per_suit + 1)
        wildcards = [
            wildcard()
            for _ in range(self.wildcards)]
        suited_cards = [
            Card(suit, rank)
            for suit in self.suits
            for rank in value_range]
        return [*wildcards, *suited_cards]

    def __getitem__(self, key):
        return self.cards[key]

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return simple_repr(self, suits=self.suits, ranked_cards=self.ranked_cards, wildcards=self.wildcards)

class Shoe(Sequence):

    def __init__(self, deck, deck_count):
        self.deck = deck
        self.deck_count = deck_count

    def shuffled(self):
        '''a generator that yields random cards from the shoe'''
        # create a list of indices corresponding to each card in the shoe
        indices = list(range(len(self)))
        # iterate until every index has been exhausted
        while indices:
            # use secrets prng to choose an index at random
            choice = randbelow(len(indices))
            # choice is popped from list to prevent it from being chosen again
            yield self[indices.pop(choice)]

    def __eq__(self, other):
        if not isinstance(other, Shoe):
            return NotImplemented
        result = all(
            self.deck == other.deck,
            self.deck_count == other.deck_count)
        return result

    def __len__(self):
        '''return the number of cards in this shoe'''
        return len(self.deck) * self.deck_count

    def __getitem__(self, key):
        '''
        using mod `%` will allow an index greater than the size of this shoe's deck,
        by up to `len(self)` before raising `IndexError`
        '''
        # if (key >= len(self)) or (-len(self) > -key):
        if not (-len(self) <= key < len(self)):
            raise IndexError('shoe index out of range')
        return self.deck[key % len(self.deck)]

    def __repr__(self):
        return simple_repr(self, deck=self.deck, deck_count=self.deck_count)
