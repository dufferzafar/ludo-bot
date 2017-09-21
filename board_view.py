"""
This module deals with drawing of the board.
"""

# PyQt Imports
from PyQt5 import Qt
from PyQt5 import QtGui as QtG

from PyQt5.QtWidgets import QGraphicsScene

# Our Code
from config import Color


class BoardView(QGraphicsScene):

    def __init__(self):
        QGraphicsScene.__init__(self)
        self.setSceneRect(0, 0, 900, 900)
        self.paint()

    def addSquare(self, x, y, size, color, border_color=Color.BLACK, border_width=2):
        """Add a colored square to the board."""
        pen = QtG.QPen(QtG.QColor(border_color))
        pen.setWidthF(border_width)
        MiterJoin = 0x00
        pen.setJoinStyle(MiterJoin)

        self.addRect(x, y, size, size, pen=pen, brush=QtG.QBrush(QtG.QColor(color)))

    def addSquares(self, start, size, color, count, row=True):
        """
        Add count no. of squares to the board.

        TODO: Fixup the row parameter!
        TODO: All functions take x, y seperately while this takes a tuple start
        """
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

    def addCoin(self, pos, color):
        """Add a coin piece to the board."""
        color = QtG.QColor(color)

        # Use a darker shade for the border
        pen = QtG.QPen(color.darker(165))
        pen.setWidthF(4)

        self.addEllipse(pos[0] + 8, pos[1] + 8, 45, 45, pen=pen, brush=QtG.QBrush(color))

    def paint(self):
        # TODO: Express all these values as multiples of h (60) ?
        SIZE_BIG_SQUARE = 360
        SIZE_UNIT_SQUARE = 60
        SIZE_FINISH_SQUARE = 180
        SIZE_YARD_SUBSQUARE = 108

        # White Squares
        # Must be drawn before any other colored unit suare
        # Rows
        for i in range(3):
            self.addSquares((0, 360 + 60 * i), SIZE_UNIT_SQUARE, Color.WHITE, 15)
            self.addSquares((360 + 60 * i, 0), SIZE_UNIT_SQUARE, Color.WHITE, 15, row=False)

        # Add Home Columns
        self.addSquares((60, 420), SIZE_UNIT_SQUARE, Color.RED, 5)
        self.addSquares((540, 420), SIZE_UNIT_SQUARE, Color.YELLOW, 5)
        self.addSquares((420, 60), SIZE_UNIT_SQUARE, Color.GREEN, 5, row=False)
        self.addSquares((420, 540), SIZE_UNIT_SQUARE, Color.BLUE, 5, row=False)

        # Add starting squares (Colored)
        self.addSquare(60, 360, SIZE_UNIT_SQUARE, Color.RED)
        self.addSquare(780, 480, SIZE_UNIT_SQUARE, Color.YELLOW)
        self.addSquare(480, 60, SIZE_UNIT_SQUARE, Color.GREEN)
        self.addSquare(360, 780, SIZE_UNIT_SQUARE, Color.BLUE)

        # Add Finishing square
        self.addSquare(360, 360, SIZE_FINISH_SQUARE, Color.WHITE, border_width=4)

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
        self.addSquare(120, 480, SIZE_UNIT_SQUARE, Color.RED)
        self.addSquare(720, 360, SIZE_UNIT_SQUARE, Color.YELLOW)
        self.addSquare(360, 120, SIZE_UNIT_SQUARE, Color.GREEN)
        self.addSquare(480, 720, SIZE_UNIT_SQUARE, Color.BLUE)

        # Add 4 Big Squares
        self.addSquare(0, 0, SIZE_BIG_SQUARE, Color.RED, border_width=6)
        self.addSquare(540, 0, SIZE_BIG_SQUARE, Color.GREEN, border_width=6)
        self.addSquare(0, 540, SIZE_BIG_SQUARE, Color.BLUE, border_width=6)
        self.addSquare(540, 540, SIZE_BIG_SQUARE, Color.YELLOW, border_width=6)

        # Add Sub Squares in the yard
        # change border width to change the thickness of yard subsquares
        border_width = 30
        yards = [
            (0, 0, Color.RED),
            (540, 0, Color.GREEN),
            (0, 540, Color.BLUE),
            (540, 540, Color.YELLOW)
        ]

        for x, y, color in yards:
            x += 72
            y += 72
            self.addSquare(x, y, SIZE_YARD_SUBSQUARE, color, border_color=Color.WHITE, border_width=border_width)
            self.addSquare(x + 108, y, SIZE_YARD_SUBSQUARE, color, border_color=Color.WHITE, border_width=border_width)
            self.addSquare(x, y + 108, SIZE_YARD_SUBSQUARE, color, border_color=Color.WHITE, border_width=border_width)
            self.addSquare(x + 108, y + 108, SIZE_YARD_SUBSQUARE, color, border_color=Color.WHITE, border_width=border_width)

        # Add coins
        self.addCoin(60, 360, Color.GREEN)
