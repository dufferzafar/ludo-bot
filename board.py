import sys

# PyQt Imports
from PyQt5 import QtCore as QtC
from PyQt5 import QtGui as QtG
from PyQt5 import Qt

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsScene

# Our Code
from config import Color


class BoardScene(QGraphicsScene):

    def __init__(self):
        QGraphicsScene.__init__(self)
        self.setSceneRect(0, 0, 900, 900)

    def addSquare(self, x, y, size, color, border_color=Color.BLACK, border_width=2):
        """Add a colored square to a scene."""
        pen = QtG.QPen(QtG.QColor(border_color))
        pen.setWidthF(border_width)
        MiterJoin = 0x00
        pen.setJoinStyle(MiterJoin)

        self.addRect(x, y, size, size, pen=pen, brush=QtG.QBrush(QtG.QColor(color)))

    # Overriding addPolygon Method
    def addPolygon(self, points, color, border_color=Color.BLACK):
        """Add a colored polygon to a scene"""
        qpoints = [Qt.QPointF(x, y) for (x, y) in points]
        polygon = Qt.QPolygonF(qpoints)

        super(BoardScene, self).addPolygon(
            polygon,
            pen=QtG.QPen(QtG.QColor(border_color)),
            brush=QtG.QBrush(QtG.QColor(color))
        )


class BoardView(QGraphicsView):

    def __init__(self):
        QGraphicsView.__init__(self)

        # Window's dimensions
        self.setGeometry(QtC.QRect(500, 100, 904, 904))

        # Prevent Window Resize
        self.setFixedSize(self.size())

        self.board = BoardScene()
        self.setScene(self.board)
        self.paint()

    def paint(self):
        SIZE_BIG_SQUARE = 360
        SIZE_UNIT_SQUARE = 60
        SIZE_FINISH_SQUARE = 180
        SIZE_YARD_SUBSQUARE = 102
        # White Squares
        # Must be drawn before any other colored unit suare
        # Rows
        for i in range(3):
            self.add_squares((0, 360 + 60 * i), SIZE_UNIT_SQUARE, Color.WHITE, 15)
            self.add_squares((360 + 60 * i, 0), SIZE_UNIT_SQUARE, Color.WHITE, 15, row=False)

        # Add Home Columns
        self.add_squares((60, 420), SIZE_UNIT_SQUARE, Color.RED, 5)
        self.add_squares((540, 420), SIZE_UNIT_SQUARE, Color.YELLOW, 5)
        self.add_squares((420, 60), SIZE_UNIT_SQUARE, Color.GREEN, 5, row=False)
        self.add_squares((420, 540), SIZE_UNIT_SQUARE, Color.BLUE, 5, row=False)

        # Add starting squares (Colored)
        self.board.addSquare(60, 360, SIZE_UNIT_SQUARE, Color.RED)
        self.board.addSquare(780, 480, SIZE_UNIT_SQUARE, Color.YELLOW)
        self.board.addSquare(480, 60, SIZE_UNIT_SQUARE, Color.GREEN)
        self.board.addSquare(360, 780, SIZE_UNIT_SQUARE, Color.BLUE)

        # Add Finishing square
        self.board.addSquare(360, 360, SIZE_FINISH_SQUARE, Color.WHITE, border_width=4)

        # Add Finishing Triangles
        points = [(363, 366), (363, 534), (447, 450)]
        self.board.addPolygon(points, Color.RED, border_color=Color.WHITE)
        points = [(537, 366), (537, 534), (453, 450)]
        self.board.addPolygon(points, Color.YELLOW, border_color=Color.WHITE)
        points = [(366, 363), (534, 363), (450, 447)]
        self.board.addPolygon(points, Color.GREEN, border_color=Color.WHITE)
        points = [(366, 537), (534, 537), (450, 453)]
        self.board.addPolygon(points, Color.BLUE, border_color=Color.WHITE)

        # Add Safe Squares as per board image on piazza
        # https://d1b10bmlvqabco.cloudfront.net/attach/j5drxbfmuwn490/ir1vkh6c6md2vf/j7rvzmnrnu4x/ff8ce7ca004f619b451bd93be3370f6eludomybestfriend.jpg
        self.board.addSquare(120, 480, SIZE_UNIT_SQUARE, Color.RED)
        self.board.addSquare(720, 360, SIZE_UNIT_SQUARE, Color.YELLOW)
        self.board.addSquare(360, 120, SIZE_UNIT_SQUARE, Color.GREEN)
        self.board.addSquare(480, 720, SIZE_UNIT_SQUARE, Color.BLUE)

        # Add 4 Big Squares
        self.board.addSquare(0, 0, SIZE_BIG_SQUARE, Color.RED, border_width=6)
        self.board.addSquare(540, 0, SIZE_BIG_SQUARE, Color.GREEN, border_width=6)
        self.board.addSquare(0, 540, SIZE_BIG_SQUARE, Color.BLUE, border_width=6)
        self.board.addSquare(540, 540, SIZE_BIG_SQUARE, Color.YELLOW, border_width=6)

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
            self.board.addSquare(x, y, SIZE_YARD_SUBSQUARE, color, border_color=Color.WHITE, border_width=border_width)
            self.board.addSquare(x + 102, y, SIZE_YARD_SUBSQUARE, color, border_color=Color.WHITE, border_width=border_width)
            self.board.addSquare(x, y + 102, SIZE_YARD_SUBSQUARE, color, border_color=Color.WHITE, border_width=border_width)
            self.board.addSquare(x + 102, y + 102, SIZE_YARD_SUBSQUARE, color, border_color=Color.WHITE, border_width=border_width)

    def add_squares(self, start, size, color, count, row=True):
        for i in range(count):
            x = start[0] + 60 * i * int(row)
            y = start[1] + 60 * i * int(not row)
            self.board.addSquare(x, y, size, color)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    view = BoardView()
    view.show()

    sys.exit(app.exec_())
