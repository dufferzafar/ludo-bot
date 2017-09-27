"""This module controls the entire Ludo Game and interfaces with the provided client."""

# stdlib
import sys
import time
import logging

from random import randint

# Our Code
from player import Player
from color_log import ColoredLogs

# Setup Colored logging to stderr
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


def read_die():
    return list(map(int, read_line().split(" ")[2:]))


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

    def make_moves(self, moves):
        """
        Make a coin move.

        Takes in a list of move strings of the form: "<Coin ID>_<Die Roll>"
        eg: "R0_1" will move Coin 0 of Player Red 1 position ahead.

        Since these moves will be read from the client,
        they are assumed to be valid.
        """
        for move in moves:
            log.debug("Making Move: %s" % move)
            coin_name, die = move.split('_')
            self.coins[coin_name] += int(die)

    def run(self):

        coin_num = 0

        # I'm the 2nd player
        if self.my_player_id == 2:
            dice = read_line()
            moves = read_moves()

            # Update coin positions using these moves
            self.make_moves(moves)

        # Track whether the 2nd player is repeating
        opponent_repeating = False

        # Now it is my turn!
        while True:

            # 2nd player is not repeating, so it is my turn!
            if not opponent_repeating:

                # Roll the die
                write_output("<THROW>")

                # Read die rolls from client (stdin)
                die_rolls = read_line()
                log.info("Received Roll: %s", die_rolls)

                # handle ducks! [0] is returned on rolling 3 sixes
                # if die_rolls == [0]:
                #     raise NotImplementedError

                # Apply strategies to find what next move should be
                # moves = self.players[0].get_move(die_rolls, self.players[1:])

                # Send the moves to client (stdout)
                # moves = ["%s_%d" % (coin, die_roll) for (coin, die_roll) in moves]
                # moves = "\n".join(moves)

                coin = self.players[self.my_player_id - 1].coins[coin_num]

                write_output(str(coin) + "_1")

                coin += 1

                if coin.rel_pos == 57:
                    coin_num += 1

            else:
                opponent_repeating = False

            # Now read in opponent's dice rolls & moves
            dice = read_line()

            # If the moves I played didn't result in a REPEAT
            # The opponent will now get another chance
            if dice != "REPEAT":
                moves = read_moves()

                # Opponent made a move that resulted in a REPEAT!
                # So the next turn won't be mine
                if moves[-1] == 'REPEAT':
                    opponent_repeating = True

                    # Remove "REPEAT" from moves list
                    moves.pop()

                self.make_moves(moves)

            # TODO: Remove these later?
            self.update_board.emit(self.coins)
            time.sleep(0.05)
