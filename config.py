
# Setup Colored logging to stderr
import sys
import logging

from color_log import ColoredLogs

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(ColoredLogs(sys.stderr))

PLAYER_COLORS = ["RED", "GREEN", "YELLOW", "BLUE"]


class Color():

    WHITE = "#e3e3e3"
    BLACK = "#000000"

    RED = "#e31e25"
    GREEN = "#62b446"
    BLUE = "#1e70b9"
    YELLOW = "#fecd07"


class Board():

    """Parameters related to our board."""

    # Size of a single small square
    SQUARE_SIZE = 60

    # Size of finishing square / home
    FINISH_SQUARE_SIZE = SQUARE_SIZE * 3

    # Size of the entire board
    # Note that there are 15 small squares on the board
    BOARD_SIZE = 15 * SQUARE_SIZE

    # Location of the logical origin of the board
    X_CENTER = BOARD_SIZE / 2
    Y_CENTER = BOARD_SIZE / 2

    # Location of the top-left corner of square numbered 0
    X_0 = 0
    Y_0 = 6 * SQUARE_SIZE

    # Size of yard/jail
    YARD_SIZE = SQUARE_SIZE * 6

    # Size of yard/jail
    YARD_SUBSQUARE_SIZE = SQUARE_SIZE * 2

    # Location of sub sqaures in the yard
    YARD_COIN_OFF = SQUARE_SIZE * 1.5
    YARD_COINS = [
        (YARD_COIN_OFF, YARD_COIN_OFF),
        (YARD_SUBSQUARE_SIZE + YARD_COIN_OFF, YARD_COIN_OFF),
        (YARD_COIN_OFF, YARD_SUBSQUARE_SIZE + YARD_COIN_OFF),
        (YARD_SUBSQUARE_SIZE + YARD_COIN_OFF, YARD_SUBSQUARE_SIZE + YARD_COIN_OFF),
    ]
