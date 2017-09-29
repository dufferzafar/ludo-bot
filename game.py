"""This module controls the entire Ludo Game and interfaces with the provided client."""

# stdlib
import sys
import time

from itertools import permutations

# Our Code
from player import Player, Coin
from config import log


# These are used to interact with the client
def read_line():
    return sys.stdin.readline().strip()


def read_moves():
    return read_line().split("<next>")


def write_output(txt):
    sys.stdout.write(txt + "\n")
    sys.stdout.flush()


def read_die():
    die = read_line()
    if "DUCK" in die:
        return []
    return list(map(int, die.split(" ")[2:]))


class LudoGame:

    def __init__(self, player_id, game_mode):

        self.my_id = player_id

        # Our games will only ever have 2 players
        if game_mode == 0:
            colors = ["RED", "YELLOW"]
        else:
            colors = ["BLUE", "GREEN"]

        self.player = Player(colors[(self.my_id + 1) % 2])
        self.opponent = Player(colors[self.my_id % 2])

        # Position of each coin on the board is the core state of the game
        # Store references to all coins
        self.coins = self.player.coins.copy()
        self.coins.update(self.opponent.coins)

    def dump_state(self):
        """Serialize the state of the game."""
        s = ""
        # TODO: Players is not really required in state ?
        s += "Players: " + "%s, %s" % (self.player.color, self.opponent.color)
        s += "\n"
        s += "Coins: " + ", ".join(["%s_%d" % (c, c.rel_pos) for c in self.coins.values()])
        return s

    def load_state(self, state):
        """Load the state of the game from a dump."""
        players, coins, _ = state.strip().split("\n")
        # Break second part into a list
        _list = lambda s: s.strip().split(": ")[1].split(", ")

        self.player = Player(_list(players)[0])
        self.opponent = Player(_list(players)[1])

        # A list of coin states
        coin_objects = {}
        for cs in _list(coins):
            coin = Coin(cs[0], int(cs[1]))
            coin.rel_pos = int(cs.split("_")[1])
            coin_objects[str(coin)] = coin

        self.coins = coin_objects

    def run(self, no_board=False):

        # I'm the 2nd player
        if self.my_id == 2:
            dice = read_line()
            moves = read_moves()

            # Update coin positions using these moves
            self.opponent.make_moves(moves, self.player)

        # Track whether the 2nd player is repeating
        opponent_repeating = False

        while True:

            log.warn(self.dump_state())

            # 2nd player is not repeating, so it is my turn!
            if not opponent_repeating:

                # Roll the die
                write_output("<THROW>")

                # Read die rolls from client (stdin)
                die_rolls = read_die()

                log.info("Received Roll: %s", die_rolls)

                # Save state
                saved_positions = {
                    name: coin.rel_pos
                    for (name, coin) in self.coins.items()
                }

                # Store: [(possible_moves, benefit)]
                all_possible_moves = []

                # Consider all possible unique permutations of moves!
                for possible_rolls in set(permutations(die_rolls)):

                    # Find all moves possible for this permutation of the rolls
                    possible_moves = self.player.get_multiple_moves(possible_rolls, self.opponent)

                    # TODO: Use heuristics to calculate benefit of each list of possible_moves
                    benefit = 0

                    # Use percent_complete & profits of each move

                    # self.player.percent_complete
                    # self.opponent.percent_complete

                    # Add it to list
                    if possible_moves:
                        all_possible_moves.append((possible_moves, benefit))

                    log.warn("State After these moves")
                    log.warn(self.dump_state())
                    # Reset state
                    for name, coin in self.coins.items():
                        coin.rel_pos = saved_positions[name]

                    log.warn("State Reset")
                    log.warn(self.dump_state())
                # if no move possible
                if not all_possible_moves:
                    moves = "NA"
                else:
                    # Only keep possible moves of maximal length
                    maximal = max(all_possible_moves, key=lambda t: len(t[0]))
                    max_len = len(maximal[0])
                    all_valid_moves = filter(lambda t: len(t[0]) == max_len, all_possible_moves)

                    # log.critical("Max len: %r", max_len)
                    # log.critical("Possible: %r", all_possible_moves)
                    # log.critical("Valid: %r", all_valid_moves)

                    # Sort all_valid_moves based on benefit
                    moves = sorted(all_valid_moves, key=lambda t: t[1])[-1][0]

                    # Play finally decided moves
                    self.player.make_moves(moves, self.opponent)

                    # Convert to a format that the external client understands
                    moves = "<next>".join(moves)

                # Send the moves to client (stdout)
                log.info("Sending Moves: %s", moves)
                write_output(moves)

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

                self.opponent.make_moves(moves, self.player)

            if not no_board:
                self.update_board.emit(self.coins)
                time.sleep(1)


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
