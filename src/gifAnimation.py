#!/usr/bin/env python
#-*- coding:utf-8 -*-
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class ImagePlayer(QWidget):
    def __init__(self, filename, title, parent=None):
        QWidget.__init__(self, parent)

        # Load the file into a QMovie
        self.movie = QMovie(filename, QByteArray(), self)

        size = self.movie.scaledSize()
        self.setGeometry(200, 200, size.width(), size.height())
        self.setWindowTitle(title)

        self.movie_screen = QLabel()
        # Make label fit the gif
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)

        # Create the layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)

        self.setLayout(main_layout)

        # Add the QMovie object to the label
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()

if __name__ == "__main__":
    gif = "/home/dash/Downloads/iDev_planned_release_vs_critical_bug_Clue.gif"
    app = QApplication(sys.argv)
    player = ImagePlayer(gif, "was")
    player.show()
    sys.exit(app.exec_())