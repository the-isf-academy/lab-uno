# player.py
# by Jacob Wolf

# Class for an UnoGame player

from random import shuffle, choice

class Player:
    """A human or computer Player in a UnoGame. This holds the basic details about
    a player and also some functions that the UnoGame object uses to interact with
    the Player.

    Args:
        name (str): the name of the player
        strategy (str): "human" if the player is human or "computer" otherwise
    """

    def __init__(self, name):
        """ Creates a Player object
        """
        self.name = name
        self.hand = []

    def choose_color(self):
        raise NotImplementedError

    def choose_card(self, top_card):
        raise NotImplementedError

    def get_valid_card_choices_from_hand(self, top_card):
        """ Check to see if the card is playable given the top card

        Args:
            top_card (Card): Card at the top of the deck

        Returns:
            (bool) for whether the card is playable
        """
        valid_cards = []
        for card in self.hand:
            if card.special == "wild" or card.special == "wild-draw-four":
                valid_cards.append(card)
            if (top_card.number and top_card.number == card.number) or (top_card.color and top_card.color == card.color) or (top_card.special and top_card.special == card.special):
                valid_cards.append(card)
        return valid_cards

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
    a Player can do and more: HumanPlayer gets input about choices from a user.
    """

    def choose_color(self):
        """Asks the player to choose a color
        """
        new_color = None
        while new_color != 'red' and new_color != 'green' and new_color != 'blue' and new_color != 'yellow':
            new_color = input("{}, what is the new color (red, yellow, blue, or green)? ".format(self.name))
            new_color = new_color.lower()
        return new_color

    def choose_card(self, view, top_card):
        """Asks the player to choose a card from hand and enforces the rules of Uno

        Args:
            top_card (Card): the top card currently displayed on the deck

        Returns:
            (Card) a valid choice of Card
        """

        card_chosen = False

        while card_chosen == False:
            choice = view.menu("\n[Player Menu]",["Play Card", "Draw Card"])

            if choice == "Play Card":
                hand_for_view = []
                for card in self.hand:
                    hand_for_view.append(str(card))
                card = view.menu("\n[Select a card]",hand_for_view)
                card_index = hand_for_view.index(card)

                card_choice = self.hand[card_index]

                if card_choice not in self.hand:
                    self.view.show_invalid_card(self.name,card_choice,top_card)

                self.hand.remove(card_choice)
                return card_choice
            elif choice == "Draw Card":
                return None

class ComputerPlayer(Player):
    """ComputerPlayer extends the ComputerPlayer class. A ComputerPlayer can do
    everything a Player can do and more: ComputerPlayer uses a basic (read: bad)
    strategy to make choices during a game.
    """

    def choose_color(self):
        """Asks the player to choose a color
        """
        return "red"

    def choose_card(self,top_card):
        """ Plays one turn by choosing the last card from hand.

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
    randomly choose a color or valid card (a much better, but still bad strategy).
    """

    ### 💻 YOUR CODE GOES HERE 💻 ###




class StrategicComputerPlayer(ComputerPlayer):
    """StrategicComputerPlayer extends the ComputerPlayer class.
    Can you get your computer player to consistently win more than 30% of games?
    """

    ### 💻 YOUR CODE GOES HERE 💻 ###
 