# Testing file for bank lab
# By: Chris Proctor and Jacob Wolf

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

class TestUnoLab(unittest.TestCase):

    def test_draw_two(self):
        """
        Test checking the implementation of the draw_two() function.
        """
        pass

    def test_wild_draw_four(self):
        """
        Test checking the implementation of the wild_draw_four() function.
        """
        pass

    def test_strategy(self):
        """
        Test to see if student strategy can beat the random strategy
        """
        print("\n\nTESTING STUDENT'S COMPUTER STRATEGY.")
        print("PLAYING 1000 STUDENT (ComputerO) vs RANDOM GAMES:")
        game_stats = defaultdict(lambda : 0)
        for i in tqdm(range(1000)):
            stdout = sys.stdout
            sys.stdout = io.StringIO()
            game = UnoGame([], ['student','random','random','random'], "uno_cards.csv", 500)
            winner = game.play()
            game_stats[winner] += 1
            sys.stdout = stdout
            # if i%25 == 0:
            #     sys.stdout.write(".")
            #     sys.stdout.flush()
        print("\nTEST COMPLETE. GAME STATS:")
        print("______________________")
        print("| Player.......Win % |")
        for player, wins in game_stats.items():
            print("| {}...{}% |".format(player, round(wins/1000*100,2)))
        print("|____________________|")
        self.assertTrue(game_stats["Computer0"]/1000 > 0.5)


unittest.main()
