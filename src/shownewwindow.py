#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import sys


class Second(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)


class First(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)
        self.pushButton = QtGui.QPushButton("click me")

        self.setCentralWidget(self.pushButton)

        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.dialog = Second(self)

    def on_pushButton_clicked(self):
        self.dialog.show()


def main():
    app = QtGui.QApplication(sys.argv)
    main = First()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()