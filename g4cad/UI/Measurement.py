# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Measurement.ui'
#
# Created: Wed Apr 24 16:32:58 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui


class Ui_Measurement(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Ui_Measurement, self).__init__()
        self.setupUi(self)

    def setupUi(self, P):
        P.setObjectName("P")
        P.resize(562, 349)
        self.verticalLayout = QtGui.QVBoxLayout(P)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtGui.QTableWidget(P)
        self.tableWidget.setObjectName("tableWidget")
        # self.tableWidget.setRowCount(0)

        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(('Property', 'Value'))
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(P)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(P)
        QtCore.QObject.connect(
            self.buttonBox, QtCore.SIGNAL("accepted()"), P.accept)
        QtCore.QObject.connect(
            self.buttonBox, QtCore.SIGNAL("rejected()"), P.reject)
        QtCore.QMetaObject.connectSlotsByName(P)

    def retranslateUi(self, P):
        P.setWindowTitle(QtGui.QApplication.translate(
            "P", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

    def show_measurement(self, m):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(8)
        row = 0
        for key, val in m.items():
            value = str(val[0])+' '+str(val[1])
            self.tableWidget.setItem(row, 0, QtGui.QTableWidgetItem(key))
            self.tableWidget.setItem(row, 1, QtGui.QTableWidgetItem(value))
            row += 1
