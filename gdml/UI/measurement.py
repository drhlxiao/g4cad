# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'measurement.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_measurement(object):
    def setupUi(self, measurement):
        measurement.setObjectName("measurement")
        measurement.resize(439, 342)
        self.verticalLayout = QtWidgets.QVBoxLayout(measurement)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(measurement)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(measurement)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(measurement)
        self.buttonBox.accepted.connect(measurement.accept)
        self.buttonBox.rejected.connect(measurement.reject)
        QtCore.QMetaObject.connectSlotsByName(measurement)

    def retranslateUi(self, measurement):
        _translate = QtCore.QCoreApplication.translate
        measurement.setWindowTitle(_translate("measurement", "Dialog"))


class MainWindow(QtGui.QMainWindow):
    def __init__(self, ui_layout):
        QtGui.QMainWindow.__init__(self)
        self.ui = ui_layout
        ui_layout.setupUi(self)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = Ui_measurement()
    window = MainWindow(mw)
    window.show()
    sys.exit(app.exec_())
