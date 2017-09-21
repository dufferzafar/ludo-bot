
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

    # Size of yard/jail
    YARD_SIZE = SQUARE_SIZE * 6

    # Size of finishing square / home
    FINISH_SQUARE_SIZE = SQUARE_SIZE * 3

    # Size of yard/jail
    YARD_SUBSQUARE_SIZE = SQUARE_SIZE * 2 - 12

    # Size of the entire board
    # NOTE: There are 15 small squares on the board
    BOARD_SIZE = 15 * SQUARE_SIZE

    # Location of the logical origin of the board
    # There are total
    X_CENTER = BOARD_SIZE / 2
    Y_CENTER = BOARD_SIZE / 2

    # Location of the top-left corner of square numbered 0
    X_0 = 0
    Y_0 = 6 * SQUARE_SIZE

    # Location of sub sqaures in the yard
    YARD_X_0 = SQUARE_SIZE + 12
    YARD_Y_0 = SQUARE_SIZE + 12

    YARD_X_1 = SQUARE_SIZE * 3
    YARD_Y_1 = SQUARE_SIZE + 12

    YARD_X_2 = SQUARE_SIZE + 12
    YARD_Y_2 = SQUARE_SIZE * 3

    YARD_X_3 = SQUARE_SIZE * 3
    YARD_Y_3 = SQUARE_SIZE * 3
