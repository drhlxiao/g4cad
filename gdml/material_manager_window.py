#!/usr/bin/python
__author__ = 'Hualin Xiao'
__date__ = 'Sept. 10th, 2017'

import sys
from PySide.QtCore import *
from PySide.QtGui import *

from material_database import MaterialDatabase
import os.path
from utils import printf

#import MaterialDatabase


class MainWidget(QDialog):
    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.setGeometry(200, 200, 440, 680)
        self.setWindowTitle("Material database")
        self.layoutMain = QVBoxLayout(self)

        self.layoutDataBrowser = QHBoxLayout()
        self.buttonEditRecord = QPushButton('Edit')

        self.buttonNewRecord = QPushButton('Add new')
        self.textEdit = QTextEdit()
        self.textEdit.setGeometry(QRect(330, 50, 241, 511))

        # self.buttonNewRecord.clicked.connect(self.openAddRecordDialog)

        self.buttonDeleteRecord = QPushButton('Delete')
        self.layoutDataBrowser.addWidget(QLabel('User materials'))

        self.layoutDataBrowser.addWidget(self.buttonEditRecord)
        self.layoutDataBrowser.addWidget(self.buttonNewRecord)
        self.layoutDataBrowser.addWidget(self.buttonDeleteRecord)

        self.layoutMain.addLayout(self.layoutDataBrowser)

        self.listView = QListView()
        self.listView.clicked.connect(self.onListViewClick)

        self.buttonEditRecord.clicked.connect(self.editDatabaseFile)
        self.buttonDeleteRecord.clicked.connect(self.editDatabaseFile)
        self.buttonNewRecord.clicked.connect(self.editDatabaseFile)

        self.layoutMain.addWidget(self.listView)
        self.layoutMain.addWidget(self.textEdit)

        self.setLayout = self.layoutMain
        self.setDatabase()

    def editDatabaseFile(self):
        try:
            self.db.edit()
        except BaseException:
            printf("failed to open the material database file")
            pass

    def setDatabase(self):
        try:
            self.model = QStandardItemModel()
            self.db = MaterialDatabase()
            self.model.setHorizontalHeaderLabels(['Material', ''])
            names = []
            for mat in self.db.userMaterials:
                nameItem = QStandardItem(mat['name'])
                self.model.appendRow(nameItem)
            self.listView.setModel(self.model)

        except BaseException:
            pass

    def onListViewClick(self):

        index = self.listView.selectedIndexes()
        for item in index:
            mat = item.data()
            elements = self.db.getMaterial(mat)
            self.showMaterial(elements)

    def showMaterial(self, data):
        #matlist.append([name,frac_type, c['ref'], c['frac'],0, e['data']['density']])
        nrows = len(data)
        # print data[0]
        name, frac_type, comp, frac, z, density = data[0]
        self.textEdit.clear()
        cursor = QTextCursor(self.textEdit.document())
        cursor.insertHtml('<h3>{}</h3><br>'.format(name))
        cursor.insertHtml('<b>Density</b>: {} g/cm3<br>'.format(density))
        cursor.insertHtml('<b>Fraction:</b><br> ')

        for rowNb, row in enumerate(data):
            name, frac_type, comp, frac, z, density = row
            cursor.insertHtml('<b>{}</b> {}<br> '.format(comp, frac))

    @staticmethod
    def run(parent=None):
        dialog = MainWidget(parent)
        dialog.exec_()


def main():
    app = QApplication([])
    MainWidget.run()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
