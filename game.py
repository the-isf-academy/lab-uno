#game.py
#by Jacob Wolf

# Runs the Uno card game

from deck import Deck
from card import Card
from player import HumanPlayer, ComputerPlayer, RandomComputerPlayer, StrategicComputerPlayer
from random import choice
from view import TerminalView
import sys, getopt

class UnoGame():
    """Creates an instance of an UnoGame which runs the logic of the game to give
    players turn, make sure players play valid cards, and determine when a player wins.
    The UnoGame also enforces the rules of special cards in Uno like reverse or
    draw four.

    Args:
        deck_file (str): The filepath to the deck of cards
        total_rounds (int): The number of rounds to play before ending the game
        human_names (list of str): names of human player (up to 4)
        computer_strategies (list of str): names of strategies for computer players ()

    """
    START_CARDS = 7
    NUM_PLAYERS = 4
    CLOCKWISE = 1
    ANTICLOCKWISE = -1
    COLORS = ["red", "blue", "green", "yellow"]

    def __init__(self, game_view, human_names, computer_strategy, deck_file=None, total_turns=10):
        self.view = game_view
        self.turns_remaining = total_turns
        self.deck = Deck(deck_file)
        self.discard = Deck()
        self.direction = self.CLOCKWISE
        self.current_player_index = 0
        self.top_card = self.deal_one_card()

        if "wild" in self.top_card.special:
            self.top_card.color = choice(self.COLORS)
        self.players = []

        if human_names != None:
            self.players.append(HumanPlayer(name))
            
        for i in range(1,3):
            if computer_strategy == "random":
                self.players.append(RandomComputerPlayer("Computer {}".format(i, computer_strategy)))

            elif computer_strategy == "strategic":
                self.players.append(StrategicComputerPlayer("Computer {}".format(i, computer_strategy)))

            else:
                self.players.append(ComputerPlayer("Computer {}".format(i, computer_strategy)))

    def play(self):
        """ Plays an uno game

        Returns:
            (str) name of the game winner
        """
        self.view.setup()

        self.deal_starting_cards()

        win = False

        while self.turns_remaining > 0 and not win:
            win = self.play_turn()
            self.turns_remaining -= 1

        if win:
            winner = self.players[self.current_player_index]
            self.view.show_winning_game(winner)
            return winner.name

    def deal_starting_cards(self):
        """
        Deals cards to all players to begin the games
        """
        if self.deck.get_num_cards() < self.START_CARDS*self.NUM_PLAYERS:
            self.view.show_out_of_cards()
            return False

        for i in range(self.START_CARDS):
            for player in self.players:
                self.deal_one_card(player)

    def play_turn(self):
        """ Plays one round of uno

        Returns:
            (bool) whether the game has been won by the current player
        """
        player = self.current_player()
        self.view.show_beginning_turn(player, self.top_card)

        if type(player) == HumanPlayer:
            card = player.choose_card(self.view,self.top_card)
        else:
            card = player.choose_card()




        if card:
            self.view.show_played_card(player, card)
            if self.valid_card_choice(card):
                if self.top_card.special == 'wild' or self.top_card.special == 'wild-draw-four':
                    self.top_card.color = None   #reseting the color of the wild card before it goes into the discard pile
                self.discard.add_card(self.top_card)
                self.top_card = card

                if len(player.hand) == 0:
                    return True
                if card.special:
                    self.special_card_action(card)

            else:
                self.view.show_invalid_card(player, card, self.top_card)
                player.add_to_hand(card)
                self.deal_n_cards(2, player)
        else:
            self.deal_n_cards(1, player)

        self.increment_player_num()
        return False

    def deal_n_cards(self, n, player=None):
        """ Takes n cards from the Deck and deals them to a Player or returns the
        Card(s) if no Player is specified.
        If the deck is empty, the discard pile is shuffled and becomes the deck

        Args:
            n (int): number of cards to deal
            player (Player): Player to deal the card (None if no Player)

        Returns:
            Card or list of Card: the drawn card(s)
        """
        cards = []
        for i in range(n):
            if self.deck.get_num_cards() == 0:
                if self.discard.get_num_cards() == 0:
                    self.view.show_empty_decks()
                    return None
                self.view.show_shuffling_deck()
                self.discard.shuffle_deck()
                empty_deck = self.deck
                self.deck = self.discard
                self.discard = empty_deck
            card = self.deck.get_top_card()
            cards.append(card)
            if player:
                player.add_to_hand(card)
                self.view.show_drawing_card(player)
        return cards

    def deal_one_card(self, player=None):
        """Just makes life a little easier.

        Args:
            player (Player): optional player to deal the card to
        """
        return self.deal_n_cards(1, player)[0]

    def increment_player_num(self):
        """ Increments/decrements the current_player_index depending on the direction
        of the game. Resets when number drops below 0 or goes over 3.
        """
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)

    def current_player(self):
        """Returns the current Player object.
        """
        return self.players[self.current_player_index]

    def next_player(self):
        """Returns the next Player object depending on the direction of the game
        """
        next_player_index = (self.current_player_index + self.direction) % len(self.players)
        return self.players[next_player_index]

    def valid_card_choice(self, card_choice):
        """ Check to see if the card is playable given the top card

        Args:
            card_choice (Card): a potentially playable Card

        Returns:
            (bool) for whether the card is playable
        """
        if card_choice:
            if card_choice.special == "wild" or card_choice.special == "wild-draw-four":
                return True
            if (self.top_card.number and self.top_card.number == card_choice.number) or (self.top_card.color and self.top_card.color == card_choice.color) or (self.top_card.special and self.top_card.special == card_choice.special):
                return True
        return False

    def wild(self):
        """Allows the current player to change the top card color.

        NOTE: this sets the color of the wild card to the players choice to maintain game state.
        """
        new_color = self.current_player().choose_color()
        self.top_card.color = new_color

    def skip(self):
        """ Skips the next player's turn
        """
        self.increment_player_num()

    def reverse(self):
        """ Reverses the direction of the game
        """
        self.direction *= -1

    def special_card_action(self, card):
        """ Deals with a special card's action

        Args:
            card (Card): they special card that was played
        """
        if card.special == 'wild':
            self.wild()
        elif card.special == 'skip':
            self.skip()
        elif card.special == 'reverse':
            self.reverse()

        ### 💻 YOUR CODE GOES HERE 💻 ###
        # Edit this function to include calls to your special card functions
        # The game expects the special cards in the following format: 'wild', 'skip', 'reverse', 'wild-draw-four', 'draw-two'

        else:
            raise ValueError("UnoGame doesn't know how to play special card: {}".format(card.special))
        self.view.show_card_action(self.current_player(), self.next_player(), self.top_card)

    
    ### 💻 YOUR CODE GOES HERE 💻 ###

    # Define draw_two() method here


    # Define wild_draw_four() method here



# -------------------- END OF PART 2️⃣ CODE ⬆️ --------------------


if __name__ == "__main__":
    view = TerminalView()

    view.welcome()

    rounds = int(view.get_input("How many rounds do you want to play for?"))

    deck_file = view.menu("Choose a deck",["basic deck","special deck"])

    if deck_file == "basic deck":
        deck_file = "uno_cards_basic.csv"
    elif deck_file == "special deck":
        deck_file = "uno_cards_special_no_draw.csv"
    
    human_players = view.menu("Do you want a human player?",["yes","no"])
    if human_players == "yes":
        name = view.get_input("What is your name?")
    else:
        name = None

    computer_strategy = view.menu("What strategy should the Computers use? ",["basic","random","strategic"])
    

    game = UnoGame(view, name, computer_strategy, deck_file, rounds*3)

    game.play()

    view.end_game()

