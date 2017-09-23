"""This module controls the entire Ludo Game and interfaces with the provided client."""

from player import Player

from config import PLAYER_COLORS


class LudoGame:

    def __init__(self, board):

        # from board_view import BoardView
        self.board = board

        # A Game has 4 players
        # TODO: Since our games will only ever have 2 players
        # We could just use two variables player, opponent?
        self.players = [Player(color) for color in PLAYER_COLORS]

        self.coins = []
        for player in self.players:
            self.coins.extend(player.coins)

        self.board.paint(self.coins)

    def play(self):

        # while not self.finished():
        while True:

            # Decide whether it is my turn or my opponents

            # Read die rolls from client (stdin)
            die_rolls = []

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

            # handle THROW / REPEAT messages
