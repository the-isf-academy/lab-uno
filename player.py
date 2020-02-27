# player.py
# by Jacob Wolf

# Class for an UnoGame player

from random import shuffle, choice

class Player(object):
    """A human or computer Player in a UnoGame.

    Args:
        name (str): the name of the player
        strategy (str): "human" if the player is human or "computer" otherwise
    """

    def __init__(self, name):
        """ Creates a Player object
        """
        self.name = name
        self.hand = []

    def add_to_hand(self, card):
        """ Adds a card to a player's hand.

        Args:
            card (Card): card to add to the player's hand
        """
        self.hand.append(card)

    def print_hand(self):
        """ Prints the player's current hand to the console
        """
        for i, card in enumerate(self.hand):
            print("{}: {}".format(i,card))

class HumanPlayer(Player):
    """HummanPlayer extends the Player class. A HumanPlayer can do everything
    a Player can do and more.
    """

    def choose_color(self):
        """Asks the player to choose a color
        """
        new_color = None
        while new_color != 'red' and new_color != 'green' and new_color != 'blue' and new_color != 'yellow':
            new_color = input("{}, what is the new color (red, yellow, blue, or green)? ".format(self.name))
            new_color = new_color.lower()
        return new_color

    def choose_card(self, top_card):
        """Asks the player to choose a card from hand and enforces the rules of Uno

        Args:
            top_card (Card): the top card currently displayed on the deck

        Returns:
            (Card) a valid choice of Card
        """
        input("Press enter to see your hand.")
        self.print_hand()
        card_choice_num = "n"
        while not card_choice_num.isdigit() or (int(card_choice_num) < 0 or int(card_choice_num) >= len(self.hand)):
            card_choice_num = input("Input card number or type \'draw\' to draw new card: ")
            if card_choice_num == "draw":
                return None
        card_choice = self.hand[int(card_choice_num)]
        self.hand.remove(card_choice)
        return card_choice

class ComputerPlayer(Player):
    """ComputerPlayer extends the ComputerPlayer class. AComputerPlayer can do
    everything a Player can do and more. Uses a basic (read: bad) strategy for choices.
    """

    def choose_color(self):
        """Asks the player to choose a color
        """
        return "red"

    def choose_card(self, top_card):
        """ Plays one turn by randomly choosing a card from hand.

        Args:
            hand (list of Card): the calling player's hand
            top_card (Card): the top card currently displayed on the deck

        Returns:
            (Card) a valid choice of Card
        """
        return self.hand.pop()

class RandomComputerPlayer(ComputerPlayer):
    """RandomComputerPlayer extends the ComputerPlayer class.
    The RandomComputerPlayer overrides the ComputerPlayer choice functions to
    randomly choose a color or valid card.
    """

    def __init__(self, name, valid_card_choice_function):
        """ Creates a ComputerPlayer object
        """
        super().__init__(name)
        self.valid_card_choice = valid_card_choice_function

    def choose_color(self):
        """Asks the player to choose a color
        """
        return choice(["red","yellow","green","blue"])

    def choose_card(self, top_card):
        """ Plays one turn by randomly choosing a card from hand.

        Args:
            hand (list of Card): the calling player's hand
            top_card (Card): the top card currently displayed on the deck

        Returns:
            (Card) a valid choice of Card
        """
        shuffle(self.hand)
        for card in self.hand:
            if self.valid_card_choice(card):
                self.hand.remove(card)
                return card
        return None
