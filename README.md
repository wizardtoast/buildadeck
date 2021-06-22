# Build-a-Deck Workshop

 A humble deck creation station, easily create Decks of Cards and shuffle them in Shoes!

## Description

*Build-a-Deck* exposes several objects intended to simplify the creation of any standard playing-card style deck. **Cards** are defined by suit and rank. **Decks** evenly assign their given suits to as many incrementally ranked cards as you specify; creating a Deck with four suits and 52 ranked cards will assign cards ranking 1 to 13 for each suit. **Wildcards**, cards with a value of None for *both* suit and rank can be created in addition to ranked cards, however, even distribution of wildcards to suits is not enforced.

**Shoes** act as a sequence of multiple copies of one Deck; given a 52 card Deck and a count of four decks, a Shoe will behave as if it contains 208 cards. Shoes can also produce a secure shuffle using the *secrets* package and an implementation of the Fisher--Yates Shuffle.

## Getting Started
### Dependencies

* The **minimum python version is 3.8** as this package makes use of *functools.cached_property*

### Installation

###### Installing locally
1. Clone / download this repository to a convenient location
2. From the directory containing `setup.py` run the command `python -m pip install .`

### Usage
##### Creating a card
```py
>>> from buildadeck import Card
>>> ace_of_spades = Card(suit='Spades', rank=1)
>>> ace_of_spades.suit
'Spades'
>>> ace_of_spades.rank
1
>>> repr(ace_of_spades)
Card(suit='Spades', rank=1)
```
##### Creating a standard 52 card French deck
```py
>>> from buildadeck import Card, Deck
>>> french_suits = (
...    'Clubs', 'Diamonds', 'Hearts', 'Spades'
... )
>>> french_deck = Deck(
...     suits=french_suits,
...     ranked_cards=52,
...     wildcards=0
... )
>>> len(french_deck) == 52
True
>>> isinstance(french_deck[0], Card)
True
>>> french_deck[0] is french_deck.cards[0]
True
>>> french_deck[0] == french_deck[1]
False
```
##### Change the cards in an existing deck
```py
>>> from buildadeck import Deck
>>> deck = Deck(suits=range(4), ranked_cards=52, wildcards=0)
>>> cache = deck.cards  # a Deck's cards property is cached
>>> deck.suits = range(8)
>>> deck.ranked_cards = 104
>>> deck.cards == cache  # Deck attributes will not change value returned by cards
True
>>> len(deck)
52
>>> del deck.cards  # until the cached value has been deleted
>>> deck.cards == cache
False
>>> len(deck)
104
```
##### Using a Shoe secure shuffle
```py
from buildadeck import Deck, Shoe
>>> deck = Deck(range(4), 52, 0)
>>> shoe = Shoe(deck=deck, deck_count=4)  # create a Shoe containing Deck four times
>>> len(shoe)
208
>>> shuffle = shoe.shuffled()  # returns a generator
>>> for _ in range(len(shoe)):
...     shuffled_card = next(shuffle)
...     print(shuffled_card)
```
