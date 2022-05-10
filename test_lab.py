# Testing file for bank lab
# By: Chris Proctor and Jacob Wolf and Emma Brown

# =============================================================================
# ☕️ More-Than-You-Need-To-Know Lounge ☕️
# =============================================================================
# Welcome to the More-Than-You-Need-To-Know Lounge, a chill place for code that
# you don't need to understand.

# Thanks for stopping by, we hope you find something that catches your eye.
# But don't worry if this stuff doesn't make sense yet -- as long as we know
# how to use code, we don't have to understand everything about it.

# Of course, if you really like this place, stay a while. You can ask a
# teacher about it if you're interested.
#
# =============================================================================

import unittest
import sys, io
from tqdm import tqdm
from collections import defaultdict


from game import UnoGame
from card import Card
from view import TerminalView

class TestUnoLab(unittest.TestCase):

    def test_draw_two(self):
        """
        Test checking the implementation of the draw_two() function.
        """
        game = UnoGame(TerminalView(), None,['basic','basic','basic'], "uno_cards_special_with_draw.csv", 10)
        draw_two = Card("red", None, "draw-two")
        game.top_card = draw_two
        game.special_card_action(draw_two)
        next_player = game.next_player()
        self.assertTrue(len(next_player.hand) == 2)
        game.special_card_action(draw_two)
        self.assertTrue(len(next_player.hand) == 4)
        game.increment_player_num()
        game.special_card_action(draw_two)
        next_player = game.next_player()
        self.assertTrue(len(next_player.hand) == 2)
        reverse = Card("red", None, "reverse")
        game.top_card = reverse
        game.special_card_action(reverse)
        game.top_card = draw_two
        game.special_card_action(draw_two)
        next_player = game.next_player()

        self.assertTrue(len(next_player.hand) == 4)


    def test_wild_draw_four(self):
        """
        Test checking the implementation of the wild_draw_four() function.
        """
        game = UnoGame(TerminalView(), None,['basic','basic','basic'], "uno_cards_special_with_draw.csv", 10)
        wild_draw_four = Card(None, None, "wild-draw-four")
        game.top_card = wild_draw_four
        game.special_card_action(wild_draw_four)
        next_player = game.next_player()
        self.assertTrue(len(next_player.hand) == 4)
        self.assertTrue(game.top_card.color == "red")
        game.special_card_action(wild_draw_four)
        self.assertTrue(len(next_player.hand) == 8)
        self.assertTrue(game.top_card.color == "red")
        game.increment_player_num()
        game.special_card_action(wild_draw_four)
        next_player = game.next_player()
        self.assertTrue(len(next_player.hand) == 4)
        reverse = Card("red", None, "reverse")
        game.top_card = reverse
        game.special_card_action(reverse)
        game.top_card = wild_draw_four
        game.special_card_action(wild_draw_four)
        next_player = game.next_player()
        self.assertTrue(len(next_player.hand) == 4)


    def test_strategy(self):
        """
        Test to see if student strategy can beat the random strategy
        """
        print("\n\nTESTING STUDENT'S COMPUTER STRATEGY.")
        print("STUDENT'S COMPUTER STRATEGY SHOULD WIN AT LEAST 30% OF GAMES.")
        print("PLAYING 1000 Strategy (Computer O) vs RANDOM GAMES:")
        game_stats = defaultdict(lambda : 0)
        for i in tqdm(range(1000)):
            stdout = sys.stdout
            sys.stdout = io.StringIO()

            game = UnoGame(TerminalView(), None, ['strategic','random','random','random'],  "uno_cards_special_with_draw.csv", 500)
  
            winner = game.play()
            game_stats[winner] += 1
            sys.stdout = stdout

        print("\nTEST COMPLETE. GAME STATS:")
        print("_______________________________")
        print("| Player.................Win % |")
        for player, wins in game_stats.items():
            print("| {}...{}% |".format(player, round(wins/1000*100,2)))
        print("|______________________________|")
        self.assertTrue(game_stats["Computer 0 (strategic)"]/1000 > 0.3)


unittest.main()
