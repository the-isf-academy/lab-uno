# player.py
# by Jacob Wolf

# Class for an UnoGame players

from random import shuffle, choice

class Player(object):
    """A human or computer Player in a UnoGame.

    Args:
        name (str): the name of the player
        strategy (str): "human" if the player is human or "computer" otherwise
    """

    def __init__(self, name, strategy="computer"):
        """ Creates a Player object
        """
        self.name = name
        self.strategy = strategy
        self.hand = []

    def add_to_hand(self, card):
        """ Adds a card to a player's hand.

        Args:
            card (Card): card to add to the player's hand
        """
        self.hand.append(card)

    def play_turn(self, top_card):
        """ Plays one turn of Uno

        Args:
            top_card (Card): the top card currently displayed on the deck
        """
        if self.strategy == "computer":
            return self.play_computer_turn(top_card)
        else:
            return self.play_human_turn(top_card)

    def pick_color(self):
        """Asks the player to choose a color
        """
        if self.strategy != "computer":
            new_color = None
            while new_color != 'red' and new_color != 'green' and new_color != 'blue' and new_color != 'yellow':
                new_color = input("{}, what is the new color (red, yellow, blue, or green)? ".format(self.name))
                new_color = new_color.lower()
            return new_color
        else:
            return choice(["red","yellow","green","blue"])

    def play_human_turn(self, top_card):
        """Asks the player to choose a card from hand and enforces the rules of Uno

        Args:
            top_card (Card): the top card currently displayed on the deck

        Returns:
            (Card) a valid choice of Card
        """
        input("Press enter to see your hand.")
        self.print_hand()
        card_choice = None
        while not self.valid_card_choice(card_choice, top_card):
            card_choice_num = "n"
            while not card_choice_num.isdigit() or (int(card_choice_num) <= 0 or int(card_choice_num) >= len(self.hand)):
                card_choice_num = input("Input card number or type \'draw\' to draw new card: ")
                if card_choice_num == "draw":
                    return None
            card_choice = self.hand[int(card_choice_num)]
        self.hand.remove(card_choice)
        return card_choice

    def play_computer_turn(self, top_card):
        """ Plays one turn by randomly choosing a card from hand.

        Args:
            top_card (Card): the top card currently displayed on the deck

        Returns:
            (Card) a valid choice of Card
        """
        shuffle(self.hand)
        for card in self.hand:
            if self.valid_card_choice(card, top_card):
                self.hand.remove(card)
                return card
        return None

    def valid_card_choice(self, card_choice, top_card):
        """ Check to see if the card is playable given the top card

        Args:
            card_choice (Card): a potentially playable Card
            top_card (Card): Card at the top of the deck

        Returns:
            (bool) for whether the card is playable
        """
        if card_choice:
            if card_choice.special == "wild" or card_choice.special == "wild-draw-four":
                return True
            if (top_card.number and top_card.number == card_choice.number) or (top_card.color and top_card.color == card_choice.color) or (top_card.special and top_card.special == card_choice.special):
                return True
        return False

    def print_hand(self):
        """ Prints the player's current hand to the console
        """
        for i, card in enumerate(self.hand):
            print("{}: {}".format(i,card))
