import sys
from PySide.QtCore import *
from PySide.QtGui import *
from material_database import MaterialDatabase


class Window(QWidget):
    def __init__(self):

        QWidget.__init__(self)

        self.treeView = QTreeView()
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)

        self.model = QStandardItemModel()
        self.db = MaterialDatabase()
        data = self.db.userMaterials
        self.addItems(data)
        self.treeView.setModel(self.model)

        self.model.setHorizontalHeaderLabels([self.tr("Object")])

        layout = QVBoxLayout()
        layout.addWidget(self.treeView)
        self.setLayout(layout)

    def addItems(self, data):

        for el in data:
            name = el['name']
            item = QStandardItem(name)
            self.model.appendRow(item)
            type_name = 'type: composition'
            if el['type'] == 1:
                type_name = 'type: fraction'
            # item.appendRow(type_name)
            #item.appendRow('density: %f'%el['density'])

    def openMenu(self, position):

        indexes = self.treeView.selectedIndexes()
        if len(indexes) > 0:

            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QMenu()
        if level == 0:
            menu.addAction(self.tr("Edit person"))
        elif level == 1:
            menu.addAction(self.tr("Edit object/container"))
        elif level == 2:
            menu.addAction(self.tr("Edit object"))

        menu.exec_(self.treeView.viewport().mapToGlobal(position))


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
