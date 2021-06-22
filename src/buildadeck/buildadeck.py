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
        self._suits = suits
        self._ranked_cards = ranked_cards
        self._wildcards = wildcards

    @property
    def suits(self):
        return self._suits

    @property
    def ranked_cards(self):
        return self._ranked_cards

    @property
    def wildcards(self):
        return self._wildcards
    
    @cached_property
    def cards(self):
        ranks_per_suit = self.ranked_cards / len(self.suits)
        value_range = range(1, ranks_per_suit + 1)
        if not ranks_per_suit.is_integer():
            raise ValueError('ranked_cards must be evenly divisible by number of suits')
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

# class WeightedDeck(Deck):
#     '''similar to a Deck object, weights are applied to the number of cards created per suit
#     useful when a deck should have an uneven distribution of cards'''
#     def __init__(self, weights, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if not weights:
#             distributed_weight = 1 / len(suits)
#             default_weights = [distributed_weight for _ in range(len(suits))]
#         self.weights = weights or default_weights
#         ...

class Shoe(Sequence):
    def __init__(self, deck, deck_count):
        self._deck = deck
        self._deck_count = deck_count

    @property
    def deck(self):
        '''the deck assigned to this shoe'''
        return self._deck

    @property
    def deck_count(self):
        '''the number of packs in this shoe'''
        return self._deck_count

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

def _prints():
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    aces = [(Card(suit, 1), Card(suit, 11)) for suit in suits]
    ace = Card(suits[0], 1)
    ace_print = [
        f'str: {str(ace)}',
        f'repr: {repr(ace)}',
        f'eval: {eval(repr(ace))}',
        f'aces: {aces}'
    ]

    deck = Deck(suits, 52, wildcards=len(suits))
    deck_print = [
        f'str: {str(deck)}',
        f'repr: {repr(deck)}',
        f'eval: {eval(repr(deck))}',
        f'cards ({len(deck)}): {deck.cards}'
    ]

    shoe = Shoe(deck, 4)
    shoe_print = [
        f'str: {str(shoe)}',
        f'repr: {repr(shoe)}',
        f'eval: {eval(repr(shoe))}',
        f'deck: {shoe.deck}',
        f'total: {len(shoe)}'
    ]

    import inspect
    import collections.abc
    from collections import Counter
    col = lambda o: [f'{o} is {obj}'
        for name, obj in inspect.getmembers(collections.abc)
        if inspect.isclass(obj) and isinstance(o, obj)]

    print(*ace_print,
          '',
          *deck_print,
          '',
          *shoe_print,
          '',
          *col(ace),
          '',
          *col(deck),
          '',
          *col(shoe),
          '',
          f'deck ({len(cards_deck := [card for card in deck])}):\n{cards_deck}',
          '',
          f'shoe ({len(cards_shoe := [card for card in shoe])}):\n{cards_shoe}',
          '',
          f'shoe counted ({len(shoe_count := Counter([card for card in shoe]))}):\n{shoe_count}',
          '',
          *[sc for sc in shoe_count.items()],
          '',
          f'shuffled ({len(shuffled := [card for card in shoe.shuffled()])}):\n{shuffled}',
          '',
          f'shuffled counted ({len(shuffled_count := Counter([card for card in shoe.shuffled()]))}):\n{shuffled_count}',
          '',
          *[sc for sc in shuffled_count.items()],
          '',
          f'set length: {len(set(shuffled))}',
          sep='\n')



if __name__ == '__main__':
    _prints()
