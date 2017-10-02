"""
This module provides the main entry point to our Ludo Bot.

This is what should be run from the CLI: python main.py

It takes in parameters from the provided client program
and decides whether to show the GUI or not.
"""

from game import LudoGame
from game import read_line

from config import log


if __name__ == '__main__':

    # Read initial parameters from the client
    init = list(map(int, read_line().split(' ')))

    log.critical(init)

    player_id = init[0]
    time_limit = init[1]
    game_mode = init[2]
    no_board = not bool(init[3])

    log.debug("My Player ID: %d", player_id)
    log.debug("Time Limit: %d", time_limit)
    log.debug("Game Mode: %d", game_mode)
    log.debug("Drawing Board: %d", no_board)

    if no_board:

        game = LudoGame(player_id, game_mode)
        game.run(no_board=True)

    else:

        # This makes the dependency on PyQt optional!
        # TODO: What if no_board is false; but PyQt was not found?
        import gui
        gui.run_gui(player_id, game_mode)
