#game.py
#by Jacob Wolf

# Runs the Uno card game

from deck import Deck
from card import Card
from player import Player
from random import choice
from view import TerminalView


class UnoGame(object):
    """Creates an instance of an UnoGame.
    Args:
        deck_file (str): The filepath to the deck of cards
        total_rounds (int): The number of rounds to play before ending the game
        human_names (list of str): names of human player (up to 4)

    """
    START_CARDS = 7
    NUM_PLAYERS = 4
    CLOCKWISE = 1
    ANTICLOCKWISE = -1

    def __init__(self, human_names, deck_file=None, total_turns=10):
        self.view = TerminalView()
        self.turns_remaining = total_turns
        self.deck = Deck(deck_file)
        self.discard = Deck()
        self.direction = self.CLOCKWISE
        self.current_player_index = 0
        self.top_card = self.deal_one_card()
        self.players = []
        for name in human_names:
            self.players.append(Player(name, "human"))
        for i in range(self.NUM_PLAYERS-len(human_names)):
            self.players.append(Player("Computer {}".format(i)))   # Computer strategy choice will ultimately go here

    def play(self):
        """ Plays an uno game
        """
        if self.deck.get_num_cards() < self.START_CARDS*self.NUM_PLAYERS:
            self.view.show_out_of_cards()
            return False
        for i in range(self.START_CARDS):
            for player in self.players:
                self.deal_one_card(player)
        win = False
        while self.turns_remaining > 0 and not win:
            win = self.play_turn()
            self.turns_remaining -= 1

        if win:
            winner = self.players[self.current_player_index]
            self.view.show_winning_game(winner)

    def play_turn(self):
        """ Plays one round of uno
        """
        player = self.current_player()
        self.view.show_beginning_turn(player, self.top_card)
        card = player.play_turn(self.top_card)
        if card:
            self.view.show_played_card(player, card)
            if self.top_card.special == 'wild' or self.top_card.special == 'wild-draw-four':
                self.top_card.color = None   #reseting the color of the wild card before it goes into the discard pile
            self.discard.add_card(self.top_card)
            self.top_card = card
            if len(player.hand) == 0:
                return True
            if card.special:
                self.special_card_action(card)
        else:
            self.deal_n_cards(1, player)
        self.increment_player_num()
        return False

    def special_card_action(self, card):
        """ Deals with a special card's action
        """
        if card.special == 'wild-draw-four':
            self.wild_draw_four()
        elif card.special == 'draw-two':
            self.draw_two()
        elif card.special == 'wild':
            self.wild()
        elif card.special == 'skip':
            self.skip()
        elif card.special == 'reverse':
            self.reverse()
        else:
            raise ValueError("UnoGame doesn't know how to play special card: {}".format(card.special))

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
        "Just makes life a little easier."
        return self.deal_n_cards(1, player)[0]

    def increment_player_num(self):
        """ Increments/decrements the current_player_index depending on the direction
        of the game. Resets when number drops below 0 or goes over 3.
        """
        self.current_player_index = (self.current_player_index + self.direction)%4

    def current_player(self):
        """Returns the current Player object.
        """
        return self.players[self.current_player_index]

    def next_player(self):
        """returns the next Player object depending on the direction of the game
        """
        next_player_index = (self.current_player_index + self.DIRECTION) % len(self.players)
        return self.players[next_player_index]

    def wild(self):
        """Allows the current player to change the top card color.

        NOTE: this sets the color of the wild card to the players choice to maintain game state.
        """
        self.current_player().pick_color()
        new_color = self.players[self.current_player_index].pick_color()
        self.top_card.color = new_color
        self.view.show_wild_card_played(self.current_player())

    def skip(self):
        """ Skips the next player's turn
        """
        self.increment_player_num()

    def reverse(self):
        """ Reverses the direction of the game
        """
        self.direction *= -1

    def draw_two(self):
        """ causes the next player to draw 2 cards.
        """
        next_player = self.next_player()
        self.deal_n_cards(2, next_player)

    def wild_draw_four(self):
        """ changes the top card color and makes the next player draw 4 card
        """
        self.wild()
        next_player = self.next_player()
        self.deal_n_cards(4, next_player)

def set_up_game():
    rounds = input("How many turns do you want to play for? ")
    deck_file = input("Input the filepath of the deck you want to use (enter to use basic deck): ").strip()
    if not deck_file:
        deck_file = "uno_cards_basic.csv"
    no_players = input("How many human players (up to 4)? ")
    names = []
    for i in range(int(no_players)):
        names.append(input("What is the name of human player {}? ".format(i)))
    game = UnoGame(names, deck_file, int(rounds))
    game.play()

if __name__ == "__main__":
    game = UnoGame(['Chris'], "uno_cards_basic.csv", 10)
    game.play()

