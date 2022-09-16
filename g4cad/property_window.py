# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'properties.ui'
#
# Created: Fri May 17 22:06:32 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

import FreeCAD
from PySide import QtCore, QtGui


class MainWidget(QtGui.QDialog):
    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.setObjectName("Dialog")
        self.resize(454, 300)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget = QtGui.QTreeWidget(self)
        self.treeWidget.setObjectName("treeWidget")
        self.verticalLayout.addWidget(self.treeWidget)
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel
                                          | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"),
                               self.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"),
                               self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.setWindowTitle('Properties')
        self.treeWidget.headerItem().setText(0, 'Property')
        self.treeWidget.headerItem().setText(1, 'Value')

    def show_properties(self, m):
        root1 = QtGui.QTreeWidgetItem(self.treeWidget)
        root1.setText(0, "Name")
        root1.setText(1, m['name'])

        root2 = QtGui.QTreeWidgetItem(self.treeWidget)
        root2.setText(0, "Volume")
        root2.setText(1, str(m['vol']))

        root3 = QtGui.QTreeWidgetItem(self.treeWidget)
        root3.setText(0, "Center of mass")
        root3.setText(1, '[%.3f,%.3f,%.3f] mm' % (m['wx'], m['wy'], m['wz']))

        root4 = QtGui.QTreeWidgetItem(self.treeWidget)
        root4.setText(0, "Placement")
        root4.setText(1, '[%.3f,%.3f,%.3f] mm' % (m['cx'], m['cy'], m['cz']))

        root5 = QtGui.QTreeWidgetItem(self.treeWidget)
        root5.setText(0, "Geometric center")
        mean_x = (m['xmin'] + m['xmax']) / 2.
        mean_y = (m['ymin'] + m['ymax']) / 2.
        mean_z = (m['zmin'] + m['zmax']) / 2.
        root5.setText(1, '[%.3f,%.3f, %.3f] mm' % (mean_x, mean_y, mean_z))

        root6 = QtGui.QTreeWidgetItem(self.treeWidget)
        root6.setText(0, "BoundBox")
        root61 = QtGui.QTreeWidgetItem(root6)
        root61.setText(0, "Dimensions")
        root61.setText(
            1, '[%.3f,%.3f,%.3f] mm' % (m['xLen'], m['yLen'], m['zLen']))

        root62 = QtGui.QTreeWidgetItem(root6)
        root62.setText(0, "X range")
        root62.setText(1, '[%.3f,%.3f] mm' % (m['xmin'], m['xmax']))

        root63 = QtGui.QTreeWidgetItem(root6)
        root63.setText(0, "Y range")
        root63.setText(1, '[%.3f,%.3f] mm' % (m['ymin'], m['ymax']))

        root64 = QtGui.QTreeWidgetItem(root6)
        root64.setText(0, "Z range")
        root64.setText(1, '[%.3f,%.3f] mm' % (m['zmin'], m['zmax']))

        placement = m['globalPlacement']
        base = placement.Base
        root7 = QtGui.QTreeWidgetItem(self.treeWidget)
        root7.setText(0, "Global Placement")
        root71 = QtGui.QTreeWidgetItem(root7)
        root71.setText(0, "Base")
        root71.setText(1, '[%.3f,%.3f,%.3f] mm' % (base[0], base[1], base[2]))
        rot = placement.Rotation
        root72 = QtGui.QTreeWidgetItem(root7)
        root72.setText(0, "Rotation")
        root72.setText(1, '[%.3f,%.3f,%.3f] mm' % (rot[0], rot[1], rot[2]))

    @staticmethod
    def run(parent=None, measurements=None):
        dialog = MainWidget(parent)
        try:
            dialog.show_properties(measurements)
        except Exception as e:
            FreeCAD.Console.PrintWarning(str(e))
        dialog.exec_()


