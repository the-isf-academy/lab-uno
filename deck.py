# deck.py
# by Jacob Wolf

# A deck of Uno cards

from card import Card
from random import shuffle
import pandas as pd

class Deck(object):
    """Creates a uno Deck object. This reads in cards from a CSV file and stores them
    for use by the UnoGame object.

    Args:
        filename (str): Path to the file containing uno cards as strings
        empty (bool): Whether the deck is generated with or without cards
    """

    def __init__(self, filename=None):
        if filename:
            self.cards = self.read_cards_from_file(filename)
        else:
            self.cards = []
        self.shuffle_deck()

    def read_cards_from_file(self, filename):
        """ Reads cards from text file. Uses basic deck if execption encountered during read.
        Cards should be in the form COLOR,NUMBER,SPECIAL-TYPE (i.e red,1, or red,,draw-four)

        Args:
            filename (str): file to look for cards in

        Returns:
            list of Card: The list of cards created in the deck
        """
        try:
            cards = []
            deckDF = pd.read_csv(filename).fillna('')
            for index, row in deckDF.iterrows():
                cards.append(Card(row.color, row.number, row.special))
            return cards
        except Exception as e:
            print("Exception while reading deck: ", e)

    def add_card(self, card):
        """ Adds a card to the deck

        Args:
            card (Card): card to add to the deck
        """
        self.cards.append(card)

    def shuffle_deck(self):
        """ Shuffles the deck of cards
        """
        shuffle(self.cards)

    def get_top_card(self):
        """ Removes the top card from the deck
        """
        return self.cards.pop()  # TODO: explain this

    def get_num_cards(self):
        """ Returns the number of cards left in the deck
        """
        return len(self.cards)
