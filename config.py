
class Color():

    WHITE = "#e3e3e3"
    BLACK = "#000000"

    # Stolen from:
    # https://img15.deviantart.net/3574/i/2010/096/2/1/ludo_board_by_markhal.jpg
    RED = "#da251c"
    GREEN = "#85c226"
    BLUE = "#0093dd"
    YELLOW = "#f8c301"


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
