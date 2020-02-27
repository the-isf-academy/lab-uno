
class TerminalView:
    """Handles input and output from a Game.
    This could be pedagogically valuable because it would simplify code in
    `UnoGame` and because it would reinforce the idea that the same UnoGame could be
    used as the backend of a GUI or web-based implementation.
    Students could switch into a different mode while reading this file: here, it's about
    re-skinning the game (e.g. making it snarky), whereas over in game.py it's about the
    algorithms and interactions.
    It's also another straightforward example of objects interacting.

    Most important point: The View has no idea what is going on.
    """

    CARD_ACTION_MESSAGES = {
        "wild-draw-four": "{player.name} drew four cards and set the color to {card.color}",
        "draw-two": "{player.name} drew two cards!",
        "wild": "{player.name} set the color to {card.color}",
        "skip": "Skipped {next_player.name}!",
        "reverse": "Change directions!",
    }

    def show_beginning_turn(self, player, top_card):
        print("")
        print("----------------")
        print("The top card is {}.".format(top_card))
        print("{}, it is your turn.".format(player.name))

    def show_played_card(self, player, card):
        print("{} played {}.".format(player.name, card))

    def show_drawing_card(self, player):
        print("{} drew a card.".format(player.name))

    def show_invalid_card(self, player, card, top_card):
        print("{} can't be played on {}. {} must draw 2 cards.".format(card, top_card, player.name))

    def show_shuffling_deck(self):
        print("Deck is out of cards! Shuffling discard pile.")

    def show_empty_decks(self):
        print("All cards have been dealt! Someone play a card!")

    def show_ending_turn(self, player):
        print("{}, your turn is over.".format(player.name))
        print("----------------")

    def show_winning_game(self, player):
        print("🎉{} WINS!!!🎉".format(player.name))

    def show_out_of_cards(self):
        print("Not enough cards in deck. Ending game.")

    def show_card_action(self, player, next_player, card):
        message = self.CARD_ACTION_MESSAGES[card.special]
        print(message.format(player=player, next_player=next_player, card=card))
