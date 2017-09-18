import sys

# PyQt Imports
from PyQt5 import QtCore as QtC
from PyQt5 import QtGui as QtG

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsScene

# Our Code
from config import Color


class Board(QGraphicsView):

    def __init__(self):
        QGraphicsView.__init__(self)

        # Window's dimensions
        self.setGeometry(QtC.QRect(500, 100, 904, 904))

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 900, 900)
        self.setScene(self.scene)

        # Add 4 Big Squares
        SIZE_BIG_SQUARE = 360
        self.addSquare(0  , 0  , SIZE_BIG_SQUARE, Color.RED)
        self.addSquare(540, 0  , SIZE_BIG_SQUARE, Color.GREEN)
        self.addSquare(0  , 540, SIZE_BIG_SQUARE, Color.BLUE)
        self.addSquare(540, 540, SIZE_BIG_SQUARE, Color.YELLOW)

    def addSquare(self, x, y, size, color):
        """Add a colored square to a scene."""
        self.scene.addRect(x, y, size, size, brush=QtG.QBrush(QtG.QColor(color)))

    def drawBackground(self, painter, rect):
        """Set White Background"""
        white = QtG.QBrush(QtG.QColor(Color.WHITE))
        painter.fillRect(rect, white)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    view = Board()
    view.show()

    sys.exit(app.exec_())
