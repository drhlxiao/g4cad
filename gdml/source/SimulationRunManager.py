# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simdiag.ui'
#
# Created: Fri Dec  8 14:14:54 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

import sys

import gdml_exporter

import FreeCAD
import FreeCADGui

from PySide import QtCore, QtGui
import utils
import ImportGui

import subprocess

env = "source /opt/geant4/geant4.10.01-install/bin/geant4.sh;"
macroTemplate = '''
/analysis/bookHist true
/analysis/bookTree true
/analysis/storeTrack true
/analysis/addSD sensor

/run/initialize
/vis/scene/create
#/vis/open OGLSQt
/vis/open VRML2FILE
/vis/viewer/set/autoRefresh false
/vis/verbose errors
/vis/drawVolume
/vis/viewer/set/viewpointThetaPhi 40 40.
# Draw coordinate axes:
/vis/scene/add/axes 0 0 0 10 mm
# Draw smooth trajectories at end of event, showing trajectory points
# as markers 2 pixels wide:
/vis/scene/add/trajectories smooth
/vis/modeling/trajectories/create/drawByCharge
# Draw hits at end of event:
/vis/scene/add/hits
/vis/modeling/trajectories/create/drawByParticleID
/vis/modeling/trajectories/drawByParticleID-0/default/setDrawStepPts true
/vis/scene/endOfEventAction accumulate 100
/vis/viewer/set/autoRefresh true
/vis/verbose warnings



/gps/particle   e-
/gps/energy 1 MeV
#/gps/pos/type Beam
#/gps/pos/shape Circle
#/gps/pos/centre 0 0 0 mm
#x, z,y
/gps/position 0. 0 100 mm
/gps/direction 0 0 -1

#/gps/pos/sigma_x 1 mm
#/gps/pos/sigma_y 1 mm
#/gps/pos/rot1 1 0 0
#/gps/pos/rot2 0 0 -1
#/gps/ang/type iso

/run/beamOn 100
'''
defaultWorkdir = '~/freecad_sim'
exePattern = 'g4Dose -gdml %s  -m %s '
macro_fname = 'test.mac'


def printf(msg):
    print(msg)
    FreeCAD.Console.PrintMessage(msg + '\n')


class setSimulationRunUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(setSimulationRunUI, self).__init__(parent)

        self.setWindowTitle("Simulation run configuration")
        self.gridLayoutWidget = QtGui.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 521, 661))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.macro = QtGui.QPlainTextEdit(self.gridLayoutWidget)
        self.macro.setObjectName("macro")
        self.gridLayout.addWidget(self.macro, 5, 0, 1, 1)
        self.workdir = QtGui.QLineEdit(self.gridLayoutWidget)
        self.workdir.setObjectName("workdir")
        self.gridLayout.addWidget(self.workdir, 1, 0, 1, 1)
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

        # QtCore.QMetaObject.connectSlotsByName(self)

        self.macro.setPlainText(
            QtGui.QApplication.translate("Dialog", macroTemplate, None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.workdir.setText(
            QtGui.QApplication.translate("Dialog", defaultWorkdir, None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.label.setText(
            QtGui.QApplication.translate("Dialog", "Geant4 Marco:", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.g4exe.setText(exePattern)
        self.label_3.setText(
            QtGui.QApplication.translate("Dialog", "Executable program", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(
            QtGui.QApplication.translate("Dialog", "Work directory:", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.buttonBox = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok,
            QtCore.Qt.Horizontal, self)
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 1)
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.start)
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        self.connect(self.workdir, QtCore.SIGNAL("textChanged(QString)"),
                     self.loadMacro)
        # static method to create the dialog and return (date, time, accepted)

    @QtCore.Slot(str)
    def loadMacro(self):
        filename = self.workdir.text() + '/' + macro_fname
        try:
            with open(filename) as f:
                macros = f.readlines()
                self.macro.setPlainText(macros)
        except Exception as e:
            FreeCAD.Console.PrintWarning(str(e))

    def write_macro(self):
        wdir = self.workdir.text()
        utils.mkdir(wdir)
        filename = wdir + '/' + macro_fname
        printf("writing " + filename)
        try:
            f = open(filename, 'w')
            print self.macro.toPlainText()
            f.write(self.macro.toPlainText())
            f.close()
        except Exception as e:
            FreeCAD.Console.PrintWarning(str(e))
        return filename

    @QtCore.Slot()
    def start(self):
        g4mac = self.write_macro()

        wdir = self.workdir.text()
        gdmlFile = wdir + '/World.gdml'
        printf('writing:' + gdmlFile)
        allobjs = None
        allobjs = FreeCAD.ActiveDocument.Objects
        root = wdir + '/test.root'
        if not allobjs:
            printf("Can not start simulation. No objects...\n")
            return

        if allobjs:
            printf("Exporting gdml file...\n")
            ex = gdml_exporter.GdmlExporter()
            ex.exportToSingleFile(allobjs, gdmlFile)

            cmdPattern = self.g4exe.text()
            cmd = env + "\n g4Dose -gdml %s -m %s -o %s" % (
                gdmlFile.strip(), g4mac.strip(), root.strip())
            printf(cmd)
            subprocess.call(cmd, shell=True)

    @staticmethod
    def run(parent=None):

        dialog = setSimulationRunUI(parent)
        dialog.loadMacro()
        dialog.exec_()
        return (QtGui.QDialog.Accepted)


def run():
    r = setSimulationRunUI.run()


def main():
    app = QtGui.QApplication(sys.argv)
    ok = setSimulationRunUI.run()
    app.exec_()


if __name__ == "__main__":
    main()
