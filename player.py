"""
This module deals with the logical representation of a Board, Player and Coins.
"""

from config import PLAYER_COLORS
from config import log


class Board(object):

    """Logical representation of a board."""

    # There is no __init__ because we'll never create a board
    # but only use methods & variables defined on it.

    # Starting squares & Star squares
    safe_squares = [1, 9, 14, 22, 27, 35, 40, 48]
    home_column = list(range(52, 58))

    @staticmethod
    def is_safe(rel_pos):
        """Checks whether a given relative position is safe or not?"""
        if rel_pos in Board.safe_squares + Board.home_column + [0]:
            return True

        return False


class Player(object):

    """Represent a player."""

    def __init__(self, color):

        # Player's Color: Red, Green, Blue, Yellow
        self.color = color

        # Each Player has 4 Coins
        self.coins = {}
        for idx in range(0, 4):
            coin = Coin(color, idx)
            self.coins[str(coin)] = coin

    @property
    def percent_complete(self):
        """How much game have I completed?"""
        return sum([25 * (c.rel_pos / 57) for c in self.coins.values()])

    @property
    def in_jail(self):
        """Which coins are still in the Jail?"""
        return [c for c in self.coins.values() if c.rel_pos == 0]

    @property
    def finished_coins(self):
        """Which coins have reached finishing square?"""
        return [c for c in self.coins.values() if c.rel_pos == 57]

    @property
    def on_home_col(self):
        """Which coins are on home column?"""
        return [c for c in self.coins.values() if 52 <= c.rel_pos <= 56]

    def movable_coins(self, die):
        """Coins which can move on a die roll."""

        return [
            coin for coin in self.coins.values()
            if (
                coin not in self.finished_coins and  # not finished
                coin not in self.in_jail and         # not in jail
                coin.rel_pos <= 57 - die             # move is allowed
            )
        ]

    def can_finish(self, die):
        """Coins which can finish on a die roll."""
        return [coin for name, coin in self.coins.items() if coin.rel_pos + die == 57]

    def in_danger(self, opponent):
        """Coins which can get_killed in the next die roll"""
        in_danger = [coin for coin in self.coins.values() if self.threat(coin.rel_pos, opponent) > 0]
        # sorted in increasing order of relative position
        return sorted(in_danger, key = lambda coin: coin.rel_pos)

    def threat(self, relpos, opponent):
        """Returns threat at a relpos"""
        if relpos > 57:
            relpos = 57

        # if this position is safe then no threat
        if Board.is_safe(relpos):
            return 0

        abs_pos = self.coins.itervalues().next().rel_to_abs(relpos)

        threat = 0
        for coin in opponent.coins.values():
            if (coin.rel_pos >= 1 and  # not in yard
                    coin.rel_pos <= 51 and  # not in home column or finished
                    coin.rel_to_abs(coin.rel_pos + 6) >= abs_pos):  # and can reach abs_pos in one die roll
                threat += 1

        return threat

    def can_kill(self, die, opponent):
        """Who can i kill with this die roll
           Returns a list of tuple : (killer_coin, target_coin)
        """

        # My coins that can kill
        killers = [
            # Coin and the Position it will move to
            (coin, coin.rel_to_abs(coin.rel_pos + die))
            for coin in self.movable_coins(die)
            if (
                coin not in self.on_home_col and       # not on home column
                not Board.is_safe(coin.rel_pos + die)  # does not land on a safe square
            )
        ]

        possible_kills = []
        for killer, kill_spot in killers:
            for target in opponent.coins.values():
                if kill_spot == target.abs_pos:
                    possible_kills.append((killer, target))

        # Sort the possible kills in ascending order of rel_pos of targets
        return sorted(possible_kills, key=lambda target: target[1].rel_pos)

    def make_moves(self, moves, opponent):
        """
        Make a coin move.

        Takes in a list of move strings of the form: "<Coin ID>_<Die Roll>"
        eg: "R0_1" will move Coin 0 of Player Red 1 position ahead.

        Since these moves will be read from the client,
        they are assumed to be valid.
        """
        # No move to play
        if "NA" in moves:
            return

        for move in moves:
            log.debug("Making Move: %s" % move)

            move_coin_name, die = move.split('_')
            coin_to_move = self.coins[move_coin_name]

            # Even if you open with 6, you still move 1 step
            if coin_to_move.rel_pos == 0 and die == '6':
                die = '1'

            # Move my coin
            coin_to_move += int(die)

            # If my coin killed someone then place them back in their yards
            for coin in opponent.coins.values():
                if (coin.abs_pos == coin_to_move.abs_pos and
                        not Board.is_safe(coin.rel_pos)):
                    coin.rel_pos = 0

    def get_multiple_moves(self, die_rolls, opponent):
        """
        Extends get_move to a list of die rolls.
        """
        all_moves = []

        # Play each roll consecutively
        for die in die_rolls:

            # Apply strategies to find what next move should be
            move = self.get_move(die, opponent)

            # If moves are possible
            if move:
                # Convert them to a representation that others understand
                move = "%s_%d" % (move[0], move[1])

                # Perform them on the board
                # So that next decision is based on updated board state
                self.make_moves([move], opponent)

                all_moves.append(move)

        return all_moves

    def non_stacking_moves(self, die):
        """Returns a list of movable coins that wont cause stacking"""
        # Remove coins which if moved will cause stacking
        rel_pos_of_my_coins = [
            coin.rel_pos
            for coin in self.coins.values()
        ]

        log.info("Movable: %s", self.movable_coins(die))

        movable_coins = [
            coin
            for coin in self.movable_coins(die)
            # either this coin moves to a safe square
            # (where stacking is allowed)
            if Board.is_safe(coin.rel_pos + die) or
            # or it does not cause stacking
            (coin.rel_pos + die) not in rel_pos_of_my_coins
        ]
        return movable_coins

    def get_move(self, die, opponent):
        """
        Use positions of other players to make a move.

        This only works for a single die roll and is extended by get_multiple_moves.

        Returns a list of tuples: [(coin, die_roll), ...]
        """
        # Find all possible kills I can make using this die
        possible_kills = self.can_kill(die, opponent)

        # Find all possible coins that can finish using this die
        coin_to_finish = self.can_finish(die)

        # Find all non stacking movable_coins
        movable_coins = self.non_stacking_moves(die)

        # Find all my coins that can get killed
        can_get_killed = self.in_danger(opponent)

        # Move coin that can finish
        if coin_to_finish:
            log.info("Finishing Move: %s", coin_to_finish[0])
            # move any coin that can finish
            return (coin_to_finish[0], die)

        # Open
        elif (die in [1, 6]) and self.in_jail:
            log.info("Opening Move: %s", self.in_jail[0])
            # Open the lowest coin from jail
            return (self.in_jail[0], die)

        # Kill
        elif possible_kills:
            # Kill opponent's farthest possible coin
            log.info("Killing Move: %s -> %s", possible_kills[-1][0], possible_kills[-1][1])
            return (possible_kills[-1][0], die)

        # if in danger save that coin
        elif can_get_killed:
            # save the farthest coin in danger
            log.info("Defensive move, Saving %s", can_get_killed[-1])
            return (can_get_killed[-1], die)

        # Modified Fast
        else:
            log.info("Fast Move")

            log.info("Movable: %s", movable_coins)

            # Choose the coin that has moved farthest
            if movable_coins:
                movable_coins.sort(key=lambda c: c.rel_pos)

                # if at least two coins movable
                if (len(movable_coins) > 1 and
                    # threat at future pos of second farthest coin is less than
                    # the threat at future pos of the farthest coin
                    self.threat(movable_coins[-2].rel_pos + die, opponent) <
                        self.threat(movable_coins[-1].rel_pos + die, opponent)):
                    return (movable_coins[-2], die)  # move second farthest coin

                return (movable_coins[-1], die)


class Coin(object):

    """Represent a player's coin piece."""

    def __init__(self, color, idx):
        # The (color, num) pair can uniquely identify a coin
        self.color = color
        self.num = idx

        # Position of the coin on the board
        self._rel_pos = 0
        self.abs_pos = 0

    def __str__(self):
        return self.color[0] + str(self.num)

    def __repr__(self):
        return "<Coin: %s>" % self.__str__()

    def __iadd__(self, die):
        self.rel_pos += die
        return self

    def rel_to_abs(self, rel_pos):
        """
        Convert relative position to absolute position.

        The formula is based on the color (player number) of this coin.

        This is used in functions that need to check where two coins
        (of different colors) are with respect to one another.
        """
        for idx, color in enumerate(PLAYER_COLORS):
            if color[0] == self.color[0]:
                mycolor_index = idx

        if rel_pos == 0:     # Inside yard
            abs_pos = 0
        elif rel_pos >= 52:  # Inside home column
            abs_pos = -1
            # -1 can be used directly to check whether a coin is
            # inside home column or not
        else:
            abs_pos = (rel_pos - 1 + 13 * mycolor_index) % 52 + 1
            # Subtract 1 to make it 0 based; add it back to make 1 based again
        return abs_pos

    @property
    def rel_pos(self):
        """
        Position of this coin relative to the a player.

        Is in range(0, 58)

        Some functions are simpler when using the relative position.
        While some need an absolute position which is calculated later.
        """
        return self._rel_pos

    @rel_pos.setter
    def rel_pos(self, square):

        # if in finishing square, then stay in finishing square
        self._rel_pos = square

        # Update absolute position
        self.abs_pos = self.rel_to_abs(self._rel_pos)


def main():
    p1 = Player("RED")
    p2 = Player("GREEN")
    p1.coins["R1"].rel_pos = 15
    p1.coins["R2"].rel_pos = 23
    p1.coins["R3"].rel_pos = 38
    # print(p1.get_move([3], [p2]))
    p2.coins["G1"].rel_pos = 8
    p2.coins["G2"].rel_pos = 1
    p2.coins["G3"].rel_pos = 23
    print(p1.in_danger(p2))
    # print(p1.threat(0,p2))


if __name__ == '__main__':
    main()
