# -*- coding: utf-8 -*-
"""
Created on Fri Aug 1 11:12:45 2017

@author: Hualin Xiao (hualin.xiao@psi.ch)

Material database interface
"""

import G4Materials
import MaterialDatabase
from PySide import QtCore, QtGui


class SimpleListModel(QtCore.QAbstractListModel):

    def __init__(self, contents):
        super(SimpleListModel, self).__init__()
        self.contents = contents

    def rowCount(self, parent):
        return len(self.contents)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return str(self.contents[index.row()])



class setMaterialUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(setMaterialUI, self).__init__(parent)
        self.setWindowTitle("Material selector")
        self.resize(309, 391)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(309, 391))
        self.setMaximumSize(QtCore.QSize(309, 391))
      



        self.layoutWidget = QtGui.QWidget(self)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 25, 271, 341))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.search = QtGui.QLineEdit(self.layoutWidget)
        self.search.setObjectName("Search")
        self.search.setText("")
        self.search.setFocus()




        self.gridLayout.addWidget(self.search, 1, 0, 1, 2)
        self.label = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setText('Search')
        self.label_2.setText('Material')
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.listView = QtGui.QListView(self.layoutWidget)
        self.listView.setObjectName("listView")
        


        self.gridLayout.addWidget(self.listView, 3, 0, 1, 2)
        self.buttons = QtGui.QDialogButtonBox( QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.gridLayout.addWidget(self.buttons, 4, 0, 1, 2)


        self.listView.setSelectionMode(QtGui.QAbstractItemView.SelectionMode.SingleSelection)

        self.matlist=[]
        db=MaterialDatabase.MaterialDatabase()
        self.matlist.extend(db.getMaterialList())
        self.matlist.extend(G4Materials.materials)


        self.model = SimpleListModel(self.matlist)
        self.proxy = QtGui.QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.proxy.setDynamicSortFilter(True)
        #self.proxy.setFilterCaseSensitivity(QtCore.Qt.CaseInphysical)
        self.listView.setModel(self.proxy)


        #self.listView.clicked.connect(self.setResult)

        self.connect(self.search, QtCore.SIGNAL('textChanged(QString)'), 
                         self.proxy.setFilterFixedString)

        self.connect(self.search, QtCore.SIGNAL('textChanged(QString)'), 
                         self.forceSelection)

    @QtCore.Slot(str)
    def forceSelection(self, ignore):
        selection_model = self.listView.selectionModel()
        indexes = selection_model.selectedIndexes()

        if not indexes:
            index = self.proxy.index(0, 0)
            selection_model.select(index, QtGui.QItemSelectionModel.Select)
    

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def run(parent = None):
        dialog = setMaterialUI(parent)
        dialog.exec_()
        ans=dialog.getResult()
        
        return (ans,  QtGui.QDialog.Accepted)

    def getResult(self):
        indexes=self.listView.selectedIndexes()
        result=""
        for index in indexes:
            res=self.listView.model().itemData(index)
            result=res.values()[0]
        return result


import sys
from PySide import QtCore, QtGui
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    res,ok=setMaterialUI.run()
    print res
    app.exec_()
