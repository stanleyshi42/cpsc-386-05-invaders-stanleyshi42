# Stanley Shi
# CPSC 386-01
# 2021-11-24
# stanleyshi@csu.fullerton.edu
# @stanleyshi42
#
# Lab 05
#
# A game of Space Invaders
#

"""Entry point for a game of Space Invaders"""

from invaders_game import InvadersGame


def main():
    game = InvadersGame()
    return game.run()


if __name__ == "__main__":
    main()
