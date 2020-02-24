#game.py
#by Jacob Wolf

# Runs the Uno card game

from deck import Deck
from card import Card
from player import Player
from random import choice


class UnoGame(object):
    """Creates an instance of an UnoGame.
    Args:
        deck_file (str): The filepath to the deck of cards
        total_rounds (int): The number of rounds to play before ending the game
        human_names (list of str): names of human player (up to 4)

    """
    START_CARDS = 7
    NUM_PLAYERS = 4

    def __init__(self, human_names, deck_file=None, total_turns=10):
        self.turns_remaining = total_turns
        self.deck = Deck(deck_file)
        self.discard = Deck(empty=True)
        self.direction = 1
        self.curr_player_num = 0
        self.top_card = self.deal_n_cards(1,None)[0]
        self.players = []
        for name in human_names:
            self.players.append(Player(name, "human"))
        for i in range(self.NUM_PLAYERS-len(human_names)):
            self.players.append(Player("Computer {}".format(i)))   # Computer strategy choice will ultimately go here

    def play(self):
        """ Plays an uno game
        """
        if self.deck.get_num_cards() < self.START_CARDS*self.NUM_PLAYERS:
            print("Not enough cards in deck. Ending game.")
            return False
        for i in range(self.START_CARDS):
            for player in self.players:
                self.deal_n_cards(1, player)
        win = False
        while self.turns_remaining > 0 and not win:
            win = self.play_turn()
            self.turns_remaining -= 1

        if win:
            print("🎉{} WINS!!!🎉".format(self.players[self.curr_player_num].name))

    def play_turn(self):
        """ Plays one round of uno
        """
        print("")
        print("----------------")
        player = self.players[self.curr_player_num]
        print("The top card is {}.".format(self.top_card))
        print("{}, it is your turn.".format(player.name))
        card = player.play_turn(self.top_card)
        if card:
            print("{} played {}.".format(player.name, card))
            if self.top_card.special == 'wild' or self.top_card.special == 'wild-draw-four':
                self.top_card.color = None   #reseting the color of the wild card before it goes into the discard pile
            self.discard.add_card(self.top_card)
            self.top_card = card

            if len(player.hand) == 0:
                return True
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
            self.deal_n_cards(1, player)
            print("{} drew a card.".format(player.name))
        self.increment_player_num()
        print("{}, your turn is over.".format(player.name))
        print("----------------")
        return False

    def deal_n_cards(self, n, player):
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
                print("Deck is out of cards! Shuffling discard pile.")
                self.discard.shuffle_deck()
                empty_deck = self.deck
                self.deck = self.discard
                self.discard = empty_deck
            card = self.deck.get_top_card()
            if player:
                player.add_to_hand(card)
            else:
                cards.append(card)
        return cards

    def increment_player_num(self):
        """ Increments/decrements the curr_player_num depending on the direction
        of the game. Resets when number drops below 0 or goes over 3.
        """
        self.curr_player_num = (self.curr_player_num + self.direction)%4
        if self.curr_player_num < 0:
            self.curr_player_num += 4

    def next_player(self):
        """returns the next Player object depending on the direction of the game
        """
        next_player_num = (self.curr_player_num + self.direction)%4
        if next_player_num < 0:
            next_player_num += 4
        return self.players[next_player_num]

    def wild(self):
        """Allows the current player to change the top card color.

        NOTE: this sets the color of the wild card to the players choice to maintain game state.
        """
        new_color = self.players[self.curr_player_num].pick_color()
        self.top_card.color = new_color
        print("The new color is {}.".format(new_color))

    def skip(self):
        """ Skips the next player's turn
        """
        self.increment_player_num()
        print("Skipped {}!".format(self.players[self.curr_player_num].name))

    def reverse(self):
        """ Reverses the direction of the game
        """
        self.direction *= -1
        print("Change directions!")

    def draw_two(self):
        """ causes the next player to draw 2 cards.
        """
        next_player = self.next_player()
        self.deal_n_cards(2, next_player)
        print("{} drew two cards!".format(next_player.name))

    def wild_draw_four(self):
        """ changes the top card color and makes the next player draw 4 card
        """
        self.wild()
        next_player = self.next_player()
        self.deal_n_cards(4, next_player)
        print("{} drew four cards!".format(next_player.name))



if __name__ == "__main__":
    rounds = input("How many turns do you want to play for? ")
    deck_file = input("Input the filepath of the deck you want to use (enter to use basic deck): ")
    no_players = input("How many human players (up to 4)? ")
    names = []
    for i in range(int(no_players)):
        names.append(input("What is the name of human player {}? ".format(i)))
    game = UnoGame(names, deck_file if deck_file != '' else None, int(rounds))
    game.play()
