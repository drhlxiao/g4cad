# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'set_material.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

import g4_materials
import material_database
import sys
from PySide2 import QtCore, QtGui, QtWidgets


class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setObjectName("Dialog")
        self.resize(361, 442)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self)
        self.label.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.filterLineEdit = QtWidgets.QLineEdit(self)
        self.filterLineEdit.setObjectName("filterLineEdit")
        self.gridLayout.addWidget(self.filterLineEdit, 0, 1, 1, 3)
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 4)
        self.toolButton = QtWidgets.QToolButton(self)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 2, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(
            208,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.filterLineEdit.textChanged.connect(self.filterTextChanged)
        self.setWindowTitle("Dialog")
        self.label.setText('Filter')
        self.toolButton.setText('Database')

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.matList = []
        self.loadMaterials()

    def loadMaterials(self):
        db = material_database.MaterialDatabase()
        self.matList.extend(db.getMaterialList())
        self.matList.extend(g4_materials.materials)
        for mat in self.matList:
            self.listWidget.addItem(mat)

    def filterTextChanged(self):
        filterString = self.filterLineEdit.text()
        # self.listWidget.clear()
        numItems = self.listWidget.count()
        for i in range(numItems):
            hidden = filterString not in self.listWidget.item(i).text()
            self.listWidget.item(i).setHidden(hidden)

    def getResult(self):
        return self.listWidget.currentItem().text()

    @staticmethod
    def run(parent=None):
        dialog = Dialog(parent)
        dialog.exec_()
        ans = dialog.getResult()
        return (ans, QtWidgets.QDialog.Accepted)
