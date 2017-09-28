"""This module controls the entire Ludo Game and interfaces with the provided client."""

# stdlib
import sys
import time

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

    def __init__(self):

        # Read initial parameters from the client
        init = list(map(int, read_line().split(' ')))

        self.my_id = init[0]
        self.time_limit = init[1]
        self.game_mode = init[2]
        self.draw_board = bool(init[3])

        log.debug("Time Limit: %d", self.time_limit)
        log.debug("My Player ID: %d", self.my_id)
        log.debug("Game Mode: %d", self.game_mode)
        log.debug("Drawing Board: %d", self.draw_board)

        # Our games will only ever have 2 players
        if self.game_mode == 0:
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

    def run(self, board_drawn=True):

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

                # TODO: Consider all possible combinations of moves!
                all_moves = self.player.get_multiple_moves(die_rolls, self.opponent)

                # if no move possible
                if not all_moves:
                    all_moves = "NA"
                else:
                    all_moves = "<next>".join(all_moves)

                # Send the all_moves to client (stdout)
                log.info("Sending Moves: %s", all_moves)
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

                self.opponent.make_moves(moves, self.player)

            if board_drawn:
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
