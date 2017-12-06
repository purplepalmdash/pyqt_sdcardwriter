#!/usr/bin/env python
#-*- coding:utf-8 -*-
import csv
#print(csv.__file__)
import sys
import math
reload(sys)

import time
# copy files to someplace
from shutil import copyfile

sys.setdefaultencoding('utf8')

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *


import csv

import operator

from PyQt4.QtCore import QSize
from PyQt4.QtGui import QApplication, QLabel, QMovie, QPainter, QFontMetrics

####################### Play Movie(gif) ################################
class QTextMovieLabel(QLabel):
    def __init__(self, text, fileName):
        QLabel.__init__(self)
        self._text = text
        m = QMovie(fileName)
        m.start()
        self.setMovie(m)

    def setMovie(self, movie):
        QLabel.setMovie(self, movie)
        s=movie.currentImage().size()
        self._movieWidth = s.width()
        self._movieHeight = s.height()

    def paintEvent(self, evt):
        QLabel.paintEvent(self, evt)
        p = QPainter(self)
        p.setFont(self.font())
        x = self._movieWidth + 6
        y = (self.height() + p.fontMetrics().xHeight()) / 2
        p.drawText(x, y, self._text)
        p.end()

    def sizeHint(self):
        fm = QFontMetrics(self.font())
        return QSize(self._movieWidth + 6 + fm.width(self._text),
                self._movieHeight)

    def setText(self, text):
        self._text = text


#################### csv sorting function starts here ##################

def sort_by_column(csv_cont, col, reverse=False):
    header = csv_cont[0]
    body = csv_cont[1:]
    if isinstance(col, str):
        col_index = header.index(col)
    else:
        col_index = col
    body = sorted(body,
                  key=operator.itemgetter(col_index),
                  reverse=reverse)
    body.insert(0, header)
    return body


def csv_to_list(csv_file, delimiter=','):
    with open(csv_file, 'r') as csv_con:
        reader = csv.reader(csv_con, delimiter=delimiter)
        return list(reader)

def print_csv(csv_content):
    print(50*'-')
    for row in csv_content:
        row = [str(e) for e in row]
        print('\t'.join(row))
    print(50*'-')


def write_csv(dest, csv_cont):
    """ New CSV file. """
    with open(dest, 'w') as out_file:
        writer = csv.writer(out_file, delimiter=',')
        for row in csv_cont:
            writer.writerow(row)

#################### csv sorting function stops here ##################

#################### Write SD Window ##################
class WriteSDWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(WriteSDWindow, self).__init__(parent)

        # Draw something in this new button
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

        self.textBrowser = QtGui.QTextBrowser(self)
        self.textBrowser.append("This is a QTextBrowser!")

        self.verticalLayout = QtGui.QVBoxLayout(self)
        # Animation start here.
        self.l = QTextMovieLabel('Loading...', '/home/dash/Downloads/iDev_planned_release_vs_critical_bug_Clue.gif')
        self.verticalLayout.addWidget(self.l)
        self.l.hide()
        # Animation stops here.
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.buttonBox)

        # Connect the signal/slot of button clicking
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


    # buttonbox for button clicked
    @QtCore.pyqtSlot()
    def accept(self):
        print "a you clicked accept"
        # todo: demo for sleep 3 seconds and exit
        # Display the image, then automatically exit
        # Copy the generated files into the SD Card
        copyfile('python.jpg', '/tmp/python.jpg')
        self.l.show()
        # todo: do something here
        #time.sleep(3)
        #self.close()
        # todo: after things done, hide the animation
        # todo: self.close() and return to main window.

#################### Main Window ##################
class MyWindow(QtGui.QWidget):
    def __init__(self, fileName, parent=None):
        super(MyWindow, self).__init__(parent)
        self.fileName = fileName

        self.model = QtGui.QStandardItemModel(self)

        self.tableView = QtGui.QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)

        # load csv file button
        #self.pushButtonLoad = QtGui.QPushButton(self)
        #self.pushButtonLoad.setText("Load Csv File!")
        #self.pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)

        self.pushButtonWriteSD = QtGui.QPushButton(self)
        self.pushButtonWriteSD.setText("Write SD Card!")
        self.pushButtonWriteSD.clicked.connect(self.on_pushButtonWriteSD_clicked)


        self.pushButtonWrite = QtGui.QPushButton(self)
        self.pushButtonWrite.setText("Write Csv File!")
        self.pushButtonWrite.clicked.connect(self.on_pushButtonWrite_clicked)

        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.tableView)
        #self.layoutVertical.addWidget(self.pushButtonLoad)
        self.layoutVertical.addWidget(self.pushButtonWriteSD)
        self.layoutVertical.addWidget(self.pushButtonWrite)
        self.loadCsv(self.fileName)
        self.dialog = WriteSDWindow(self)

    def loadCsv(self, fileName):
        # Always sorted via username
        csv_cont = csv_to_list(fileName)
        #print_csv(csv_cont)
        # Sort via Name
        csv_sorted = sort_by_column(csv_cont, 'Name')
        for row in csv_sorted:
            # Only display the non-blank line
            if row[0] and row[0].strip():
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)
            else:
                pass
        for i in range(3):
            self.model.appendRow('')


        #with open(fileName, "rb") as fileInput:
        #    for row in csv.reader(fileInput):
        #        # Only display the non-blank line
        #        if row[0] and row[0].strip():
        #            items = [
        #                QtGui.QStandardItem(field)
        #                for field in row
        #            ]
        #            self.model.appendRow(items)
        #        else:
        #            pass
        #for i in range(3):
        #    self.model.appendRow('')

    def writeCsv(self, fileName):
        with open(fileName, "wb") as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.model.rowCount()):
                fields = [
                    self.model.data(
                        self.model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(self.model.columnCount())
                ]
                writer.writerow(fields)


    @QtCore.pyqtSlot()
    def on_pushButtonWrite_clicked(self):
        self.writeCsv(self.fileName)

    # Leave slot here, we actually don't use this slot
    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.loadCsv(self.fileName)

    @QtCore.pyqtSlot()
    def on_pushButtonWriteSD_clicked(self):
        # get row index
        #rows=[idx.row() for idx in self.tableView.selectionModel().selectedRows()]
        #print type(rows)
        #for i in rows:
        #    print i
        # Another method
        #indexes = self.tableView.selectionModel().selectedRows()
        #print type(indexes)
        #for index in sorted(indexes):
        #    print('Row %d is selected' % index.row())
        # Get selected row content, notice if you selecte multiple lines, we only use the first one for writing
        howmany = 0
        print "kkkkkkkkkkkkkkkkkkkk"
        print(len(self.tableView.selectedIndexes()))
        print "kkkkkkkkkkkkkkkkkkkk"
        for i in range(len(self.tableView.selectedIndexes())):
            howmany+=1
            index = self.tableView.selectedIndexes()[i]
            row_content = str(self.tableView.model().data(index))
            print row_content
        print "*************"
        print howmany
        print "*************"
        ### todo: multiple lines could be selected, while we only want to use the first line.
        #lenth = len(self.tableView.selectedIndexes())
        #for i in self.tableView.selectedIndexes():
        #    print str(i)
        #print lenth
        #index = self.tableView.selectedIndexes()[0]
        #row_content = str(self.tableView.model().data(index))
        #print (row_content)
        #user_elements=row_content.split()
        #print(type(user_elements))
        #for i in user_elements:
        #    print i+"**"
        #print "**************************"
        # Data Processing Routing goes from here.
        ### todo: judget the content
        # Write SD comes from here
        # PoP up the write content window
        self.dialog.show()

###################### Play a gif function ###########################
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


###################### main functionality ############################
if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow("/home/dash/name2.csv")
    main.show()

    sys.exit(app.exec_())