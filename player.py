"""
This module deals with the logical representation of a Player and Coins.
"""


class Player:

    """Represent a player."""

    def __init__(self, color):

        # Player's Color: Red, Green, Blue, Yellow
        self.color = color

        # Each Player has 4 Coins
        self.coins = [Coin(color, idx) for idx in range(0, 4)]

    def move(self, die_rolls, other_players):
        """
        Use positions of other players to make a move.

        Returns a list of tuples: [(coin, die_roll), ...]

        TODO: Strategies & All decision making
        """
        raise NotImplementedError


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
        self._rel_pos = square

        # TODO: Update absolute position
        self.abs_pos = square
