"""
This module deals with the logical representation of a Player and Coins.
"""

from config import PLAYER_COLORS


class Player:

    """Represent a player."""

    def __init__(self, color):

        # Player's Color: Red, Green, Blue, Yellow
        self.color = color

        # Each Player has 4 Coins
        self.coins = [Coin(color, idx) for idx in range(0, 4)]

    @property
    def percent(self):
        """How much game has this player completed?"""
        return sum([25 * (coin.rel_pos / 57) for coin in self.coins])

    @property
    def in_jail(self):
        """Who is still in the Jail"""
        return [coin for coin in self.coins if coin.rel_pos is 0]
    def move(self, die_rolls, other_players):
        """
        Use positions of other players to make a move.

        Returns a list of tuples: [(coin, die_roll), ...]

        TODO: Strategies & All decision making
        """
        raise NotImplementedError

        # TODO: Each of these functions will be called for all die rolls?
        # Some will need to called for combinations of inputs?

        # Alvi's "expert" ludo player

        # if self.can_open(): open
        # elif self.can_kill(): kill
        # elif self.can_die(): protect
        # else: move fastest


class Coin:

    """Represent a player's coin piece."""

    def __init__(self, color, idx):
        # The (color, num) pair can uniquely identify a coin
        self.color = color
        self.num = idx

        # Position of the coin on the board
        self._rel_pos = 0
        self.abs_pos = 0

    def __repr__(self):
        return self.color[0] + str(self.num)

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

        # if in finishing block stays in finishing block
        if self._rel_pos is 57:
            return

        self._rel_pos = square

        # updating absolute position
        mycolor_index = PLAYER_COLORS.index(self.color)
        if square == 0:
            # inside yard
            self.abs_pos = 0
        elif square >= 52:
            # inside home column
            self.abs_pos = -1
            # can be used directly to check whether inside home column or not
        else:
            self.abs_pos = (self._rel_pos - 1 + 13 * mycolor_index) % 52 + 1
            # subtracting 1 to make it 0 based then adding 1 to make it 1 based again
