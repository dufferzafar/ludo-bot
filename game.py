"""This module controls the entire Ludo Game and interfaces with the provided client."""

# stdlib
import sys
import time
import logging

from random import randint

# Our Code
from player import Player, Coin
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
        init = list(map(int, read_line().split(' ')))

        self.my_player_id = init[0]
        self.time_limit = init[1]
        self.game_mode = init[2]
        self.draw_board = bool(init[3])

        log.debug("Time Limit: %d", self.time_limit)
        log.debug("My Player ID: %d", self.my_player_id)
        log.debug("Game Mode: %d", self.game_mode)
        log.debug("Drawing Board: %d", self.draw_board)

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

    def dump_state(self):
        """Serialize the state of the game."""
        s = ""
        # TODO: Players is not really required in state ?
        s += "Players: " + ", ".join([p.color for p in self.players])
        s += "\n"
        s += "Coins: " + ", ".join(["%s_%d" % (c, c.rel_pos) for c in self.coins.values()])
        return s

    def load_state(self, state):
        """Load the state of the game from a dump."""
        players, coins, _ = state.strip().split("\n")
        # Break second part into a list
        _list = lambda s: s.strip().split(": ")[1].split(", ")

        self.players = [Player(color) for color in _list(players)]

        # A list of coin states
        coin_objects = {}
        for cs in _list(coins):
            coin = Coin(cs[0], int(cs[1]))
            coin.rel_pos = int(cs.split("_")[1])
            coin_objects[str(coin)] = coin

        self.coins = coin_objects

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
        if "NA" in moves:
            moves.remove("NA")

        for move in moves:
            log.debug("Making Move: %s" % move)
            move_coin_name, die = move.split('_')
            self.coins[move_coin_name] += int(die)

            for coin_name in self.coins:
                if coin_name != move_coin_name and self.coins[coin_name].abs_pos == self.coins[move_coin_name].abs_pos:
                    self.coins[coin_name].rel_pos = 0

    def run(self, board_drawn=True):

        # I'm the 2nd player
        if self.my_player_id == 2:
            dice = read_line()
            moves = read_moves()

            # Update coin positions using these moves
            self.make_moves(moves)

        # Track whether the 2nd player is repeating
        opponent_repeating = False
        opponents = [player for i, player in enumerate(self.players)
                     if i != self.my_player_id - 1]
        # Now it is my turn!
        while True:

            log.warn(self.dump_state())

            # 2nd player is not repeating, so it is my turn!
            if not opponent_repeating:

                # Roll the die
                write_output("<THROW>")

                # Read die rolls from client (stdin)
                die_rolls = read_die()
                log.info("Received Roll: %s", die_rolls)

                # handle ducks! [0] is returned on rolling 3 sixes
                # if die_rolls == [0]:
                #     raise NotImplementedError

                # Apply strategies to find what next move should be
                all_moves = []
                for dieroll in die_rolls:  # for each dieroll
                    moves = self.players[self.my_player_id - 1].get_move([dieroll], opponents)  # get possible move

                    # if move possible
                    if moves != []:
                        moves = ["%s_%d" % (coin, die_roll) for (coin, die_roll) in moves]
                        all_moves += moves  # add it to list of all moves
                        self.make_moves(moves)  # perform those move ( so that next die roll takes decision based on new board state)

                # if no move possible
                if(all_moves == []):
                    all_moves = "NA"
                else:
                    all_moves = "<next>".join(all_moves)
                log.info("Sending Moves: %s", all_moves)
                # Send the all_moves to client (stdout)
                write_output(all_moves)

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

            if board_drawn:
                time.sleep(0.25)
                self.update_board.emit(self.coins)


if __name__ == '__main__':
    # Test Board states
    g = LudoGame()
    log.warn(g.dump_state())

    st = """
    Players: RED, YELLOW
    Coins: Y3_2, R3_4, Y1_8, R1_0, Y2_0, R0_9, R2_18, Y0_0
    """
    g.load_state(st)
    log.warn(g.dump_state())
