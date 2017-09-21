"""
This module provides the main entry point to the Ludo Application.

This is what should be run from the CLI: python main.py
"""

import sys

# PyQt Imports
from PyQt5 import QtCore as QtC

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGraphicsView

# Our Code
from board_view import BoardView


class LudoApp(QGraphicsView):

    def __init__(self):
        QGraphicsView.__init__(self)

        # Window's dimensions
        self.setGeometry(QtC.QRect(500, 100, 904, 904))

        # Prevent Window Resize
        self.setFixedSize(self.size())

        # Add the board
        self.setScene(BoardView())


if __name__ == '__main__':

    app = QApplication(sys.argv)

    view = LudoApp()
    view.show()

    sys.exit(app.exec_())