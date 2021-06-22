import unittest

from buildadeck import Card, wildcard, Deck, Shoe
from types import SimpleNamespace as SN

class DeckTests(unittest.TestCase):

    def setUp(self):
        self.longMessage = True
        self.data = SN(
            suits = ['s1', 's2', 's3', 's4'],
            ranked_cards = 52,
            ranks_per_suit = 13,
            value_range = range(1,14),
            wildcards = 4,
            total_size = 56,
            )
        self.deck = Deck(
            suits=self.data.suits,
            ranked_cards=self.data.ranked_cards,
            wildcards=self.data.wildcards,
            )

    def test_deck_length(self):
        '''test that len(deck) returns the expected number of cards'''
        self.assertEqual(
            self.data.total_size, len(self.deck), "unexpected deck length")

    def test_wild_cards_count(self):
        '''test that the expected number of wild cards exist in the deck'''
        wildcards = [wildcard() for _ in range(self.data.wildcards)]
        self.assertCountEqual(
            wildcards,
            [card for card in self.deck.cards if card.suit is None],
            "unexpected wild card count")

    def test_ranked_cards_count(self):
        '''test that the expected number of ranked cards exist in the deck'''
        suited_cards = [
            Card(suit, rank)
            for suit in self.data.suits
            for rank in self.data.value_range]
        self.assertCountEqual(
            suited_cards,
            [card for card in self.deck.cards if card.suit is not None],
            "unexpected ranked card count")

class ShoeTests(unittest.TestCase):

    def setUp(self):
        self.longMessage = True
        deck = SN(
            suits = ['s1', 's2', 's3', 's4'],
            ranked_cards = 52,
            ranks_per_suit = 13,
            value_range = range(1,14),
            wildcards = 0,
            total_size = 52,
            )
        self.data = SN(
            deck = deck,
            deck_count = 4,
            total_size = 208,
            index_range = range(-208, 208),
            )
        self.shoe = Shoe(
            deck=Deck(
                suits=deck.suits,
                ranked_cards=deck.ranked_cards,
                wildcards=deck.wildcards,
                ),
            deck_count=self.data.deck_count,
            )

    def test_len(self):
        '''test that len(shoe) returns the expected number of cards'''
        self.assertEqual(
            self.data.total_size, len(self.shoe), "unexpected shoe length")

    def test_index_range(self):
        '''test that shoe.__getitem__ allows the expected range of indices
        and raises IndexError outside of that range'''
        self.assertEqual(
            self.data.index_range,
            range(-(len(self.shoe)), len(self.shoe)),
            "unexpected index range")
        with self.assertRaises(IndexError, msg="unexpected negative boundary"):
            neg_out_of_bounds = self.shoe[-(self.data.total_size + 1)]
        with self.assertRaises(IndexError, msg="unexpected positive boundary"):
            pos_out_of_bounds = self.shoe[self.data.total_size]

    def test_shuffled_len(self):
        '''test that shoe.shuffled() generates the expected number of cards'''
        shuffled = list(self.shoe.shuffled())
        self.assertEqual(
            self.data.total_size, len(shuffled), "unexpected shuffle length")

    def test_shuffled_cards(self):
        '''test that shoe.shuffled() contains the expected number of each card
        in relation to the number of decks'''
        self.assertCountEqual(
            self.shoe, self.shoe.shuffled(), "unexpected shuffled card count")
