# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sim.ui'
#
# Created: Fri Dec  8 12:15:16 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(548, 708)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(200, 670, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel
                                          | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtGui.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 521, 661))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.macro = QtGui.QPlainTextEdit(self.gridLayoutWidget)
        self.macro.setObjectName("macro")
        self.gridLayout.addWidget(self.macro, 5, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.g4exe = QtGui.QLineEdit(self.gridLayoutWidget)
        self.g4exe.setObjectName("g4exe")
        self.gridLayout.addWidget(self.g4exe, 3, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"),
                               Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"),
                               Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(
            QtGui.QApplication.translate("Dialog", "Dialog", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.macro.setPlainText(
            QtGui.QApplication.translate("Dialog", "/vis/mac", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setText(
            QtGui.QApplication.translate("Dialog", "~/freecad_gdml", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.label.setText(
            QtGui.QApplication.translate("Dialog", "Geant4 Marco:", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(
            QtGui.QApplication.translate("Dialog", "Executable program", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(
            QtGui.QApplication.translate("Dialog", "Work directory:", None,
                                         QtGui.QApplication.UnicodeUTF8))


class run():
    def __init__(self):
        self.d = QtGui.QWidget()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.d)
        self.d.show()
