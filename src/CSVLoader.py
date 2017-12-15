#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sip
sip.setapi(u'QString', 2)
sip.setapi(u'QVariant', 2)
import csv
from multiprocessing import Process
import sys
import threading
from threading import Thread
reload(sys)
sys.setdefaultencoding('utf8')
import time
# copy files to someplace
from shutil import copyfile
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import csv
import operator
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QApplication, QLabel, QMovie, QPainter, QFontMetrics
from glob import glob
from subprocess import check_output, CalledProcessError
import os
from distutils.dir_util import copy_tree
# Detect the platform
from sys import platform


####################### Only in windows, for detecting sd card #########
if platform == "win32":
    import ctypes

    # Drive types
    DRIVE_UNKNOWN     = 0  # The drive type cannot be determined.
    DRIVE_NO_ROOT_DIR = 1  # The root path is invalid; for example, there is no volume mounted at the specified path.
    DRIVE_REMOVABLE   = 2  # The drive has removable media; for example, a floppy drive, thumb drive, or flash card reader.
    DRIVE_FIXED       = 3  # The drive has fixed media; for example, a hard disk drive or flash drive.
    DRIVE_REMOTE      = 4  # The drive is a remote (network) drive.
    DRIVE_CDROM       = 5  # The drive is a CD-ROM drive.
    DRIVE_RAMDISK     = 6  # The drive is a RAM disk.

    # Map drive types to strings
    DRIVE_TYPE_MAP = { DRIVE_UNKNOWN     : 'DRIVE_UNKNOWN',
                       DRIVE_NO_ROOT_DIR : 'DRIVE_NO_ROOT_DIR',
                       DRIVE_REMOVABLE   : 'DRIVE_REMOVABLE',
                       DRIVE_FIXED       : 'DRIVE_FIXED',
                       DRIVE_REMOTE      : 'DRIVE_REMOTE',
                       DRIVE_CDROM       : 'DRIVE_CDROM',
                       DRIVE_RAMDISK     : 'DRIVE_RAMDISK'}


    # Return list of tuples mapping drive letters to drive types
    def get_drive_info():
        result = []
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for i in range(26):
            bit = 2 ** i
            if bit & bitmask:
                drive_letter = '%s:' % chr(65 + i)
                drive_type = ctypes.windll.kernel32.GetDriveTypeA('%s\\' % drive_letter)
                result.append((drive_letter, drive_type))
        return result
# end if platform == "win32":

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

#################### Get all mounted USB(Linux)###################
def get_usb_devices():
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    # Bug-fix: in ArchLinux, some usb item in 5, some items in 6
    usb_devices = (dev for dev in sdb_devices
        if 'usb' in dev.split('/')[6] or 'usb' in dev.split('/')[5])
    return dict((os.path.basename(dev), dev) for dev in usb_devices)

def get_mount_points(devices=None):
    devices = devices or get_usb_devices() # if devices are None: get_usb_devices
    output = check_output(['mount']).splitlines()
    is_usb = lambda path: any(dev in path for dev in devices)
    usb_info = (line for line in output if is_usb(line.split()[0]))
    return [(info.split()[0], info.split()[2]) for info in usb_info]

#################### Write SD Window ##################
class WriteSDWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(WriteSDWindow, self).__init__(parent)

        # Draw something in this new button
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.listWidget = QListWidget()

        # Fill in the items into the self.listWidget
        if platform == "linux":
            for i in get_mount_points():
                self.listWidget.addItem(i[1])
        elif platform == "win32":
            drive_info = get_drive_info()
            removable_drives = [drive_letter for drive_letter, drive_type in drive_info if
                                drive_type == DRIVE_REMOVABLE]
            for i in removable_drives:
                self.listWidget.addItem(i)
            print 'removable_drives = %r' % removable_drives

        self.verticalLayout = QtGui.QVBoxLayout(self)
        # Animation for waiting
        self.l = QTextMovieLabel('OnGoing?', './cheers.gif')
        self.verticalLayout.addWidget(self.l)
        self.l.show()
        self.verticalLayout.addWidget(self.listWidget)
        self.verticalLayout.addWidget(self.buttonBox)

        # Connect the signal/slot of button clicking
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    # buttonbox for button clicked
    @QtCore.pyqtSlot()
    def accept(self):
        # Detect if you have selected some item from listWidget
        item = self.listWidget.currentItem()
        #value = item.text()
        if item == None:
            QMessageBox.about(self, "Select One Disk", "Select Your Disk!!!")
        else:
            # Display the image, then automatically exit
            # Copy the generated files into t2017_12_06_17_30_01_319x95.jpghe SD Card
            # Destination directory
            dest = item.text() #+'/localboot1'
            copy_tree("./localboot",str(dest))
            copyfile('./config/config.wtc',str(dest)+'/configs/config.wtc')
            copyfile('./config/initrd.wtc',str(dest)+'/configs/initrd.wtc')
            # After copy, sync to disk
            if hasattr(os, 'sync'):
                sync = os.sync
            else:
                pass
                # todo: windows version's sync
                #import ctypes
                #libc = ctypes.CDLL("libc.so.6")
                #def sync():
                #    libc.sync()
            QMessageBox.about(self, "Write Finish", "Your Disk have been wrote!!!")
            self.close()

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
        howmany = 0
        filecontent = []
        for i in range(len(self.tableView.selectedIndexes())):
            howmany+=1
            index = self.tableView.selectedIndexes()[i]
            row_content = str(self.tableView.model().data(index))
            filecontent.append(row_content)
        ### todo: multiple lines could be selected, while we only want to use the first line.
        # Data Processing Routing goes from here.
        ### todo: judget the content
        if len(filecontent) == 0:
            QMessageBox.about(self, "At Least One Item", "At Least One Item!!!")
        else:
            ### todo: the local configuration file should be written starts from here.
            print filecontent

            #### Manually write our own configuration files, these files will be later copy into sd card
            # Write configuration file 1
            file = open("config/initrd.wtc","w")
            file.write("clientIP=%s\n" % filecontent[1])
            file.write("netmask=%s\n" % filecontent[2])
            file.write("routerIP=%s\n" % filecontent[3])
            file.write("nameserverIP=%s\n" % filecontent[4])
            file.write("config=local\nsetupPassword=783cc2d526d862eb68d68baa854985f4\r\nnetmedia=ethernet\r\n")
            file.close()
            # Write configuration file 1
            file = open("config/config.wtc","w")
            file.write("server=rdp:%s\n" % filecontent[5])
            file.write("User=CT:123456aB\n")
            file.write("graphic=abcdefg\n")
            file.close()

            # Write SD comes from here
            # PoP up the write content window
            self.dialog.show()

###################### main functionality ############################
if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow("./client.csv")
    main.resize(800,600)
    main.show()

    sys.exit(app.exec_())