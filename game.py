"""This module controls the entire Ludo Game and interfaces with the provided client."""

from player import Player

# TODO: enum? Some other defintion?
colors = ["Red", "Green", "Blue", "Yellow"]


class LudoGame:

    def __init__(self):

        # A Game has 4 players
        # TODO: Since our games will only ever have 2 players
        # We could just use two variables player, opponent?
        self.players = [Player(color) for color in colors]

    def play(self):

        # while not self.finished():
        while True:

            # Decide whether it is my turn or my opponents

            # Read die rolls from client (stdin)
            die_rolls = []

            # it is opponent's turn
            # wait for their move
            # move opponent's pieces

            # else (it is my turn)
            moves = self.players[0].move(die_rolls, self.players[1:])

            # send the moves to client (stdout)
            moves = ["%s_%d" % (coin, die_roll) for (coin, die_roll) in moves]
            moves = "\n".join(moves)
