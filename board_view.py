"""
This module deals with drawing of the board.
"""

# Stdlib
import math
import functools

# PyQt Imports
from PyQt5 import Qt
from PyQt5 import QtGui as QtG

from PyQt5.QtWidgets import QGraphicsScene

# Our Code
from config import Color
from config import PLAYER_COLORS
from config import Board as BoardConfig


class BoardView(QGraphicsScene):

    def __init__(self):
        QGraphicsScene.__init__(self)
        self.setSceneRect(0, 0, 900, 900)

    def addSquare(self, x, y, size, color, border_color=Color.BLACK, border_width=2):
        """Add a colored square to the board."""
        pen = QtG.QPen(QtG.QColor(border_color))
        pen.setWidthF(border_width)
        MiterJoin = 0x00
        pen.setJoinStyle(MiterJoin)

        self.addRect(x, y, size, size, pen=pen, brush=QtG.QBrush(QtG.QColor(color)))

    def addSquares(self, start, size, color, count, row=True):
        """Add count no. of squares to the board."""
        for i in range(count):
            x = start[0] + 60 * i * int(row)
            y = start[1] + 60 * i * int(not row)

            self.addSquare(x, y, size, color)

    def addPolygon(self, points, color, border_color=Color.BLACK):
        """Add a colored polygon to the board."""
        polygon = Qt.QPolygonF([Qt.QPointF(x, y) for (x, y) in points])

        # Since this method is overridden,
        # we just call QGraphicsScene's addPolygon method
        super(BoardView, self).addPolygon(
            polygon,
            pen=QtG.QPen(QtG.QColor(border_color)),
            brush=QtG.QBrush(QtG.QColor(color))
        )

    def addCoin(self, pos, color, coin_num):
        """Add a coin piece to the board."""
        color = QtG.QColor(color).darker(150)

        # Use a darker shade for the border
        pen = QtG.QPen(color.darker(150))
        pen.setWidthF(4)

        self.addEllipse(pos[0] + 8, pos[1] + 8, 45, 45, pen=pen, brush=QtG.QBrush(color))

        # Add coin number to the coin
        font = QtG.QFont()
        font.setPointSize(20)

        text = self.addSimpleText(str(coin_num), font)
        text.setBrush(QtG.QBrush(QtG.QColor(Color.WHITE)))
        text.setPos(Qt.QPointF(pos[0] + 23, pos[1] + 12))

    def rotate(self, point, relative_to=0):
        """Rotate a point around the board's center."""

        theta = relative_to * math.pi / 2

        x = point[0] - BoardConfig.X_CENTER
        y = point[1] - BoardConfig.Y_CENTER

        new_x = x * math.cos(theta) - y * math.sin(theta) + BoardConfig.X_CENTER
        new_y = x * math.sin(theta) + y * math.cos(theta) + BoardConfig.Y_CENTER

        if relative_to == 1:
            new_x -= BoardConfig.SQUARE_SIZE
        elif relative_to == 2:
            new_x -= BoardConfig.SQUARE_SIZE
            new_y -= BoardConfig.SQUARE_SIZE
        elif relative_to == 3:
            new_y -= BoardConfig.SQUARE_SIZE

        return new_x, new_y

    def coordinatesOfSquare(self, square, relative_to=0):
        """Get coordinates for a square whose position is given relative to some player."""

        if (square == 0):
            rotate_relative = functools.partial(self.rotate, relative_to=relative_to)
            return list(map(rotate_relative, BoardConfig.YARD_COINS))

        # Get offset from (X_0, Y_0)
        if (1 <= square <= 5):
            x = square
            y = 0
        elif (square <= 11):
            x = 6
            y = 5 - square
        elif (square == 12):
            x = 7
            y = -6
        elif (square <= 18):
            x = 8
            y = square - 19
        elif (square <= 24):
            x = square - 10
            y = 0
        elif (square == 25):
            x = 14
            y = 1
        elif (square <= 31):
            x = 40 - square
            y = 2
        elif (square <= 37):
            x = 8
            y = square - 29
        elif (square == 38):
            x = 7
            y = 8
        elif (square <= 44):
            x = 6
            y = 47 - square
        elif (square <= 50):
            x = 50 - square
            y = 2
        elif (square == 51):
            x = 0
            y = 1
        elif (square <= 57):
            x = square - 51
            y = 1

        # Transform offsets into coordinates
        x = BoardConfig.X_0 + x * BoardConfig.SQUARE_SIZE
        y = BoardConfig.Y_0 + y * BoardConfig.SQUARE_SIZE

        return self.rotate((x, y), relative_to)

    def paint(self, coins={}):
        # White Squares
        # Must be drawn before any other colored unit suare
        # Rows
        for i in range(3):
            self.addSquares((0, 360 + 60 * i), BoardConfig.SQUARE_SIZE, Color.WHITE, 15)
            self.addSquares((360 + 60 * i, 0), BoardConfig.SQUARE_SIZE, Color.WHITE, 15, row=False)

        # Add Home Columns
        self.addSquares((60, 420), BoardConfig.SQUARE_SIZE, Color.RED, 5)
        self.addSquares((540, 420), BoardConfig.SQUARE_SIZE, Color.YELLOW, 5)
        self.addSquares((420, 60), BoardConfig.SQUARE_SIZE, Color.GREEN, 5, row=False)
        self.addSquares((420, 540), BoardConfig.SQUARE_SIZE, Color.BLUE, 5, row=False)

        # Add starting squares (Colored)
        self.addSquare(60, 360, BoardConfig.SQUARE_SIZE, Color.RED)
        self.addSquare(780, 480, BoardConfig.SQUARE_SIZE, Color.YELLOW)
        self.addSquare(480, 60, BoardConfig.SQUARE_SIZE, Color.GREEN)
        self.addSquare(360, 780, BoardConfig.SQUARE_SIZE, Color.BLUE)

        # Add Finishing square
        self.addSquare(360, 360, BoardConfig.FINISH_SQUARE_SIZE, Color.WHITE, border_width=4)

        # Add Finishing Triangles
        points = [(363, 366), (363, 534), (447, 450)]
        self.addPolygon(points, Color.RED, border_color=Color.WHITE)
        points = [(537, 366), (537, 534), (453, 450)]
        self.addPolygon(points, Color.YELLOW, border_color=Color.WHITE)
        points = [(366, 363), (534, 363), (450, 447)]
        self.addPolygon(points, Color.GREEN, border_color=Color.WHITE)
        points = [(366, 537), (534, 537), (450, 453)]
        self.addPolygon(points, Color.BLUE, border_color=Color.WHITE)

        # Add Safe Squares as per board image on piazza
        # https://d1b10bmlvqabco.cloudfront.net/attach/j5drxbfmuwn490/ir1vkh6c6md2vf/j7rvzmnrnu4x/ff8ce7ca004f619b451bd93be3370f6eludomybestfriend.jpg
        self.addSquare(120, 480, BoardConfig.SQUARE_SIZE, Color.RED)
        self.addSquare(720, 360, BoardConfig.SQUARE_SIZE, Color.YELLOW)
        self.addSquare(360, 120, BoardConfig.SQUARE_SIZE, Color.GREEN)
        self.addSquare(480, 720, BoardConfig.SQUARE_SIZE, Color.BLUE)

        # Add Yards / Jails
        yards = [
            (0, 0, Color.RED),
            (540, 0, Color.GREEN),
            (0, 540, Color.BLUE),
            (540, 540, Color.YELLOW)
        ]
        for x, y, color in yards:
            # Yard
            self.addSquare(x, y, BoardConfig.YARD_SIZE, color, border_width=6)

            # Add Sub Squares in the yard
            x += BoardConfig.SQUARE_SIZE
            y += BoardConfig.SQUARE_SIZE
            border_width = 25
            yard_sub = BoardConfig.YARD_SUBSQUARE_SIZE

            self.addSquare(x, y, yard_sub, color, border_color=Color.WHITE, border_width=border_width)
            self.addSquare(x + yard_sub, y, yard_sub, color, border_color=Color.WHITE, border_width=border_width)
            self.addSquare(x, y + yard_sub, yard_sub, color, border_color=Color.WHITE, border_width=border_width)
            self.addSquare(x + yard_sub, y + yard_sub, yard_sub, color, border_color=Color.WHITE, border_width=border_width)

        # Add coins
        for coin in coins.values():
            coords = self.coordinatesOfSquare(coin.rel_pos, relative_to=PLAYER_COLORS.index(coin.color))

            # Coin is in yard, and we get a list of coords in that case
            if coin.rel_pos == 0:
                coords = coords[coin.num]

            color_hex = Color.__dict__[coin.color]
            self.addCoin(coords, color_hex, coin.num)
