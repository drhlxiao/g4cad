# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/main_test.ui'
#
# Created: Wed Apr 24 17:03:36 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtCore, QtGui
import Measurement


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(130, 80, 89, 25))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate(
            "MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate(
            "MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.assignWidgets()
        self.show()

    def assignWidgets(self):
        self.pushButton.clicked.connect(self.goPushed)

    def goPushed(self):
        print('calling measurement')
        measurements = {"Name": ('name', 'name'),
                        "Volume": ('sol.Volume', 'mm^3'),
                        "Weight Center": ('sol.CenterOfMass', 'mm'),
                        "Geometry Center": ('sol.Placement.Base', 'mm'),
                        "Bound Box": (('boundBox.XLength', 'boundBox.YLength', 'boundBox.ZLength'), 'mm'),
                        "X range": (('boundBox.XMin', 'boundBox.XMax'), 'mm'),
                        "Y range": (('boundBox.YMin', 'boundBox.YMax'), 'mm'),
                        "Z range": (('boundBox.ZMin', 'boundBox.ZMax'), 'mm')
                        }
        print(measurements)
        self.diaglog = Measurement.Ui_Measurement(self)
        self.diaglog.show_measurement(measurements)
        self.diaglog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)
