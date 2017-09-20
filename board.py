import sys

# PyQt Imports
from PyQt5 import QtCore as QtC
from PyQt5 import QtGui as QtG

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
        self.board.addSquare(0  , 0  , SIZE_BIG_SQUARE, Color.RED)
        self.board.addSquare(540, 0  , SIZE_BIG_SQUARE, Color.GREEN)
        self.board.addSquare(0  , 540, SIZE_BIG_SQUARE, Color.BLUE)
        self.board.addSquare(540, 540, SIZE_BIG_SQUARE, Color.YELLOW)


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
