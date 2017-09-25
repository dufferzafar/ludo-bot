"""This module controls the entire Ludo Game and interfaces with the provided client."""

# stdlib
import sys

from random import randint

# Our Code
from player import Player

from config import PLAYER_COLORS


# These are used to interact with the client
def read_input():
    return sys.stdin.readline().strip()


def write_output(txt):
    sys.stdout.write(txt+"\n")
    sys.stdout.flush()


class LudoGame:

    def __init__(self):
        # A Game has 4 players
        # TODO: Since our games will only ever have 2 players
        # We could just use two variables player, opponent?
        self.players = [Player(color) for color in PLAYER_COLORS]

        self.coins = []
        for player in self.players:
            self.coins.extend(player.coins)

    def randomize_board(self):
        """
        Assign random positions to coins.

        Used while debugging etc.
        """
        for coin in self.coins:
            coin.rel_pos = randint(0, 57)

    def play(self):

        # Read initial parameters from the client
        time_limit, my_player_id, game_mode = map(int, read_input().split(' '))

        # Decide whether it is my turn or opponents
        while True:

            # handle THROW / REPEAT messages

            # Roll the die
            write_output("<THROW>")

            # Read die rolls from client (stdin)
            die_rolls = read_input()

            # handle ducks! [0] is returned on rolling 3 sixes
            if die_rolls == [0]:
                raise NotImplementedError

            # it is opponent's turn
            # wait for their move
            # move opponent's pieces

            # else (it is my turn)
            moves = self.players[0].move(die_rolls, self.players[1:])

            # send the moves to client (stdout)
            moves = ["%s_%d" % (coin, die_roll) for (coin, die_roll) in moves]
            moves = "\n".join(moves)
