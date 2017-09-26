"""This module controls the entire Ludo Game and interfaces with the provided client."""

# stdlib
import sys
import logging

from random import randint

# Our Code
from player import Player
from color_log import ColoredLogs

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(ColoredLogs(sys.stderr))


# These are used to interact with the client
def read_line():
    return sys.stdin.readline().strip()


def read_moves():
    return read_line().split("<next>")


def write_output(txt):
    sys.stdout.write(txt + "\n")
    sys.stdout.flush()


class LudoGame:

    def __init__(self):
        # Read initial parameters from the client
        self.my_player_id, self.time_limit, self.game_mode = map(int, read_line().split(' '))
        log.debug("Time Limit: %d", self.time_limit)
        log.debug("My Player ID: %d", self.my_player_id)
        log.debug("Game Mode: %d", self.game_mode)

        # Our games will only ever have 2 players
        # TODO: We could just use two variables player & opponent?
        if self.game_mode == 0:
            self.players = [Player("RED"), Player("YELLOW")]
        else:
            self.players = [Player("BLUE"), Player("GREEN")]

        # Position of each coin on the board is the core state of the game
        # Store references to all coins
        self.coins = {
            str(coin): coin
            for player in self.players
            for coin in player.coins
        }

    def randomize_board(self):
        """
        Assign random positions to coins.

        Used while debugging etc.
        """
        for coin in self.coins.values():
            coin.rel_pos = randint(0, 57)

    def move(self, move_str):
        """
        Make a coin move.

        Takes in a move string of the form: "<Coin ID>_<Die Roll>"
        eg: "R0_1" will move Coin 0 of Player Red 1 position ahead.

        Since these moves will be read from the client,
        they are assumed to be valid.
        """
        coin_name, die = move_str.split('_')
        self.coin_names[coin_name] += die

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
