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

    def addSquare(self, x, y, size, color):
        """Add a colored square to a scene."""
        self.addRect(x, y, size, size, brush=QtG.QBrush(QtG.QColor(color)))

    # Overriding addPolygon Method
    def addPolygon(self, points, color):
        """Add a colored polygon to a scene"""
        qpoints = [Qt.QPointF(x, y) for (x, y) in points]
        polygon = Qt.QPolygonF(qpoints)

        super(BoardScene, self).addPolygon(
            polygon,
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

        # Add 4 Big Squares
        SIZE_BIG_SQUARE = 360
        SIZE_UNIT_SQUARE = 60
        SIZE_FINISH_SQUARE = 180

        self.board.addSquare(0, 0, SIZE_BIG_SQUARE, Color.RED)
        self.board.addSquare(540, 0, SIZE_BIG_SQUARE, Color.GREEN)
        self.board.addSquare(0, 540, SIZE_BIG_SQUARE, Color.BLUE)
        self.board.addSquare(540, 540, SIZE_BIG_SQUARE, Color.YELLOW)

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
        self.board.addSquare(360, 360, SIZE_FINISH_SQUARE, Color.WHITE)

        # Add Finishing Triangles
        points = [(363, 366), (363, 534), (447, 450)]
        self.board.addPolygon(points, Color.RED)
        points = [(537, 366), (537, 534), (453, 450)]
        self.board.addPolygon(points, Color.YELLOW)
        points = [(366, 363), (534, 363), (450, 447)]
        self.board.addPolygon(points, Color.GREEN)
        points = [(366, 537), (534, 537), (450, 453)]
        self.board.addPolygon(points, Color.BLUE)

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
