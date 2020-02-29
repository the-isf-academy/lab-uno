# card.py
# by Jacob Wolf

#class for uno cards

class Card(object):
    """A Deck has many Card objects.

    Args:
        color (str): Color of the card
        number (int): number on the card
        special (str): type of card if special (i.e. reverse, skip, draw four, wild)

    """

    def __init__(self, color, number, special=None):
        """constructor for new instance of Card
        """
        self.color = color
        self.number = number
        self.special = special

    def __str__(self):
        """ Defines how the object will be printed
        """
        if self.color:
            return "{} {}".format(self.color, (self.special or int(self.number)))
        else:
            return self.special
