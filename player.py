"""
This module deals with the logical representation of a Board, Player and Coins.
"""

from config import PLAYER_COLORS


class Board(object):

    """Logical representation of a board."""

    # There is no __init__ because we'll never create a board
    # but only use methods & variables defined on it.

    # Starting squares & Star squares
    safe_squares = [1, 9, 14, 22, 27, 35, 40, 48]
    home_column = list(range(52, 58))

    @staticmethod
    def is_safe(self, rel_pos):
        """Checks whether a given relative position is safe or not?"""
        if rel_pos in Board.safe_squares + Board.home_column:
            return True

        return False


class Player(object):

    """Represent a player."""

    def __init__(self, color):

        # Player's Color: Red, Green, Blue, Yellow
        self.color = color

        # Each Player has 4 Coins
        self.coins = [Coin(color, idx) for idx in range(0, 4)]

    @property
    def percent(self):
        """How much game have I completed?"""
        return sum([25 * (c.rel_pos / 57) for c in self.coins])

    @property
    def in_jail(self):
        """Which coins are still in the Jail?"""
        return [c for c in self.coins if c.rel_pos == 0]

    @property
    def finished_coins(self):
        """Which coins have reached finishing square?"""
        return [c for c in self.coins if c.rel_pos == 57]

    @property
    def on_home_col(self):
        """Which coins are on home column?"""
        return [c for c in self.coins if 52 <= c.rel_pos <= 56]

    def can_kill(self, die_roll, other_players):
        """Who can i kill with this die_roll
           Returns a list of tuple : (killer_coin, target_coin)
        """
        # my coins that can kill
        killer_coins = [coin for coin in self.coins
                        if coin not in self.on_home_col and  # not in home column
                        coin not in self.finished_coins and  # not finished
                        coin not in self.in_jail and  # not in jail
                        not self.is_safe(coin.rel_pos + die_roll)
                        # if my future position does not lands on some safe spot
                        # i.e star or home or starting pos
                        ]

        # target positions of my killers as per this die roll
        kill_spots = [coin.rel_to_abs(coin.rel_pos + die_roll)
                      for coin in killer_coins]

        opponent_coins = []  # all the coins of all the opponents
        for opponent in other_players:
            for coin in opponent.coins:
                opponent_coins.append(coin)

        possible_kills = []
        for killer_coin, kill_spot in zip(killer_coins, kill_spots):
            for target_coin in opponent_coins:
                if kill_spot == target_coin.abs_pos:
                    possible_kills.append((killer_coin, target_coin))

        return possible_kills

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

    def rel_to_abs(self, rel_pos):
        """
        Convert relative position to absolute position.

        The formula is based on the color (player number) of this coin.

        This is used in functions that need to check where two coins
        (of different colors) are with respect to one another.
        """
        mycolor_index = PLAYER_COLORS.index(self.color)

        if rel_pos == 0:     # Inside yard
            abs_pos = 0
        elif rel_pos >= 52:  # Inside home column
            abs_pos = -1
            # -1 can be used directly to check whether a coin is
            # inside home column or not
        else:
            abs_pos = (rel_pos - 1 + 13 * mycolor_index) % 52 + 1
            # Subtracting 1 to make it 0 based then adding 1 to make it 1 based again
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
        if self._rel_pos is 57:
            return

        self._rel_pos = square

        # Update absolute position
        self.abs_pos = self.rel_to_abs(self._rel_pos)
