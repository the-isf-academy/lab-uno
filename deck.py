# deck.py
# by Jacob Wolf

# A deck of Uno cards

from card import Card
from random import shuffle

class Deck(object):
    """Creates a uno Deck object.

    Args:
        filename (str): Path to the file containing uno cards as strings
        empty (bool): Whether the deck is generated with or without cards
    """

    basic_deck = [Card("red",1),Card("red",2),Card("red",3),Card("blue",1),Card("blue",2),Card("blue",3),Card("yellow",'reverse'),Card(None, None, "wild")]

    def __init__(self, filename=None, empty=False):
        self.cards = []
        if not empty:
            if filename:
                self.cards = self.read_cards_from_file(filename)
            else:
                self.cards = self.basic_deck
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
            f = open(filename, "r")
            cards =[]
            for card_string in f.readlines():
                card_string = card_string.strip("\n")
                card_list = card_string.split(',')
                color = None if card_list[0] == '' else card_list[0]
                number = None if card_list[1] == '' else int(card_list[1])
                special = None if card_list[2] == '' else card_list[2]
                card = Card(color, number, special)
                cards.append(card)
            f.close()
            return cards
        except Exception as e:
            print("Exception while reading deck: ", e)
            print("Using basic deck instead.")
            return self.basic_deck

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
