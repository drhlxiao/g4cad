# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 11:12:45 2017

@author: Hualin Xiao (hualin.xiao@psi.ch)
"""

from PySide import QtGui, QtCore
import FreeCAD
import FreeCADGui
import os
import ImportGui
import gdml_importer

import os.path

import gdml_exporter
import g4_materials

import re
import label_manager
from material_database import MaterialDatabase
from os.path import expanduser
import material_ui
import material_selection_window
import property_window
#import SimulationRunManager
boxID = 0
coneID = 0
sphereID = 0
cylID = 0
__dir__ = os.path.dirname(__file__)


# non icon comands
class ImportFile:

    def GetResources(self):
        return {
            'Pixmap': __dir__ + '/icons/import.svg',
            'MenuText': 'Import',
            'ToolTip': 'Import gdml files or other files'
        }

    def IsActive(self):
        return True

    def Activated(self):
        fname = QtGui.QFileDialog.getOpenFileName(directory=expanduser('~'))[0]
        if fname:
            # ImportGui.insert(fname,"Unnamed")
            gdml_importer.open(fname)
        else:
            FreeCAD.Console.PrintWarning('invalid filename')


# icon comands
class Export:

    def GetResources(self):
        return {
            'Pixmap': __dir__ + '/icons/export.svg',
            'MenuText': 'Export',
            'ToolTip': 'Export solids to gdml files'
        }

    def IsActive(self):
        # return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0
        return True

    def Activated(self):
        FreeCAD.Console.PrintMessage('Export objects to gdml files')
        #sel = FreeCADGui.Selection.getSelection()
        objects = FreeCAD.ActiveDocument.Objects

        sel = []
        for x in objects:
            if x.ViewObject.Visibility and x.isDerivedFrom("Part::Feature"):
                if all([p.ViewObject.Visibility for p in x.InListRecursive]):
                    # parents are also visible
                    sel.append(x)

        if not sel:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("No visible object in current document !")
            ret = msgBox.exec_()
            FreeCAD.Console.PrintWarning('No Active object!')
            return

        FreeCAD.Console.PrintMessage('Number of objects to be exported: %d' %
                                     len(sel))
        odir = QtGui.QFileDialog.getExistingDirectory(
            caption="Set output directory", directory=expanduser('~'))
        FreeCAD.Console.PrintMessage('exporting...')
        if odir:
            ex = gdml_exporter.GdmlExporter()
            ex.start(sel, odir)
        else:
            FreeCAD.Console.PrintMessage('Invalid output directory')


class MeshingToleranceManager:

    def GetResources(self):
        return {
            'Pixmap': __dir__ + '/icons/mesh.png',
            'MenuText': 'Set tessellation  tolerance ',
            'ToolTip': 'set tessellation tolerance'
        }

    def IsActive(self):
        return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        sel = FreeCADGui.Selection.getSelection()
        if not sel:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("No Active Object!")
            ret = msgBox.exec_()
            FreeCAD.Console.PrintWarning('No Active object!')
            return

        else:

            items = [
                '0.01', '0.1', '0.2', '0.5', '1', '2', '3', '4', '5', '10',
                '20', '50', '100', '200', '500', '1000'
            ]
            caption = ''
            if len(sel) == 1:
                caption = 'Tessellation tolerance for %s' % sel[0].Label
            else:
                caption = 'Tessellation  tolerance for the selected %d parts' % len(
                    sel)

            item, ok = QtGui.QInputDialog.getItem(None, caption,
                                                  "Tessellation tolerance:",
                                                  items, 0, False)
            if ok and item:
                for obj in sel:
                    label = obj.Label
                    pLabel = label_manager.LabelManager()
                    obj.Label = pLabel.updatePrecision(label, float(item))
                    FreeCAD.Console.PrintMessage('set: ' + label +
                                                 ' precision:' + item)

            return


class MaterialManager:

    def GetResources(self):
        return {
            'Pixmap': __dir__ + '/icons/database.svg',
            'MenuText': 'Material database',
            'ToolTip': 'Material database'
        }

    def IsActive(self):
        return True

    def Activated(self):
        material_manager_window.MainWidget.run()


class MaterialSetter:

    def GetResources(self):
        return {
            'Pixmap': __dir__ + '/icons/material.png',
            'MenuText': 'Set material',
            'ToolTip': 'set material'
        }

    def IsActive(self):
        return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        sel = FreeCADGui.Selection.getSelection()
        if not sel:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("No Active Object!")
            ret = msgBox.exec_()
            FreeCAD.Console.PrintWarning('No Active object!')
            return
        else:
            caption = ''
            if len(sel) == 1:
                caption = 'Set material for %s' % sel[0].Label
            else:
                caption = 'Set material for the selected %d parts' % len(sel)

            item, ok = material_selection_window.Dialog.run()
            FreeCAD.Console.PrintWarning('item, ok: ' + item + ' ' + str(ok))

            if item != "":
                for obj in sel:
                    label = obj.Label
                    pLabel = label_manager.LabelManager()
                    obj.Label = pLabel.updateMaterial(label, item.strip())
                    FreeCAD.Console.PrintMessage(label + ' material set to :' +
                                                 item + '\n')
            else:
                FreeCAD.Console.PrintWarning('Material not set\n')


class MeasurementTool:

    def GetResources(self):
        return {
            'Pixmap': __dir__ + '/icons/measure.png',
            'MenuText': 'Measure the dimensions  of the selected object',
            'ToolTip': 'Measure the dimensions of the selected object'
        }

    def IsActive(self):
        return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):

        sel = FreeCADGui.Selection.getSelection()
        if len(sel) != 1:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Select one part!")
            ret = msgBox.exec_()
            FreeCAD.Console.PrintWarning('select one part!')
            return
        else:
            if hasattr(sel[0], "Shape"):
                sol = sel[0].Shape
                name = sel[0].Label
                mass = 0

                boundBox = sol.BoundBox
                measurements = {
                    "name": name,
                    "vol": sol.Volume,
                    "wx": sol.CenterOfMass[0],
                    "wy": sol.CenterOfMass[1],
                    "wz": sol.CenterOfMass[2],
                    "cx": sol.Placement.Base[0],
                    "cy": sol.Placement.Base[1],
                    "cz": sol.Placement.Base[2],
                    "xLen": boundBox.XLength,
                    "yLen": boundBox.YLength,
                    "zLen": boundBox.ZLength,
                    "xmin": boundBox.XMin,
                    "xmax": boundBox.XMax,
                    "ymin": boundBox.YMin,
                    "ymax": boundBox.YMax,
                    "zmin": boundBox.ZMin,
                    "zmax": boundBox.ZMax,
                    'globalPlacement': sel[0].getGlobalPlacement()
                    # "mass": mass
                }
                property_window.MainWidget.run(measurements=measurements)

            elif hasattr(sel[0], "Mesh") or hasattr(sel[0], "Point"):
                FreeCAD.Console.PrintMessage(
                    "Can not measure mesh object or point!")
            else:
                FreeCAD.Console.PrintMessage(
                    "Measurement not available for the object!")


class PartVisibilityManager:

    def GetResources(self):
        return {
            'Pixmap': __dir__ + '/icons/hide.svg',
            'MenuText': 'Hide small parts',
            'ToolTip': 'Hide small parts'
        }

    def IsActive(self):
        doc = FreeCAD.ActiveDocument
        if doc:
            if len(doc.Objects) >= 1:
                return True

        return False

    def Activated(self):

        value, ok = QtGui.QInputDialog.getDouble(
            None, "Set the volume limit to be hidden", "Volume (mm3):")
        if not ok:
            return
        doc = FreeCAD.ActiveDocument
        objs = doc.Objects
        for ob in objs:
            try:
                sol = ob.Shape
                vol = sol.Volume
                if vol < value:
                    ob.ViewObject.Visibility = False
                    FreeCAD.Console.PrintMessage(ob.Label + ' volume: ' +
                                                 str(vol) + '\n')
            except Exception as e:
                FreeCAD.Console.PrintWarning(str(e))


class PartFilter:

    def GetResources(self):
        return {
            'Pixmap': __dir__ + '/icons/search.svg',
            'MenuText': 'Filter parts',
            'ToolTip': 'Filter parts'
        }

    def IsActive(self):
        doc = FreeCAD.ActiveDocument
        if doc:
            if len(doc.Objects) >= 1:
                return True

        return False

    def Activated(self):
        pattern, ok = QtGui.QInputDialog.getText(None, "Filter parts by name",
                                                 "Filter parts by name:")
        if not ok:
            return
        doc = FreeCAD.ActiveDocument
        objs = doc.Objects
        for ob in objs:
            try:
                label = ob.Label
                if pattern in label:
                    FreeCADGui.Selection.addSelection(ob)
                    FreeCAD.Console.PrintMessage('Found:' + ob.Label + '\n')
                    ob.ViewObject.Visibility = True
                else:
                    ob.ViewObject.Visibility = False
            except Exception as e:
                FreeCAD.Console.PrintWarning(str(e))


class PhysicalVolumeManager:

    def GetResources(self):
        return {
            'Pixmap': __dir__ + '/icons/setpv.svg',
            'MenuText': 'Set physical volume name',
            'ToolTip': 'Set physical volume name '
        }

    def IsActive(self):
        return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):

        sel = FreeCADGui.Selection.getSelection()
        if not sel:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("No Active Object!")
            ret = msgBox.exec_()
            FreeCAD.Console.PrintWarning('No Active object!')
            return
        else:
            name, ok = QtGui.QInputDialog.getText(None,
                                                  "Set physical volume name",
                                                  "Physical volume name:")
            if not ok:
                return
            elif name.strip():
                num_sel = len(sel)
                for i, obj in enumerate(sel):
                    label = obj.Label
                    pLabel = label_manager.LabelManager()
                    sd_name = name.strip()
                    if num_sel > 1:
                        sd_name = '{}_{}'.format(name.strip(), i)
                    obj.Label = pLabel.updatePhysicalVolume(label, sd_name)
                    FreeCAD.Console.PrintMessage(
                        'set {} as physical volume: {}\n'.format(
                            label, sd_name))
            else:
                FreeCAD.Console.PrintWarning('Invalid physical volume name\n')


class AddWorld:

    def GetResources(self):
        return {
            'Pixmap': __dir__ + '/icons/world.svg',
            'MenuText': 'Add world volume',
            'ToolTip': 'add world volume'
        }

    def IsActive(self):
        if FreeCAD.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        objs = FreeCAD.ActiveDocument.Objects
        for obj in objs:
            if obj.Name == '__world__':
                msgBox = QtGui.QMessageBox()
                msgBox.setText("The world volume already exists!")
                ret = msgBox.exec_()
                FreeCAD.Console.PrintWarning('world volume already exists!')
                return

        doc = FreeCAD.ActiveDocument
        doc.addObject("Part::Box", "__world__")
        world = doc.getObject("__world__")
        pLabel = label_manager.LabelManager()
        world.Label = pLabel.updateMaterial("World", "G4_AIR")
        world.Length = '10000 mm'
        world.Height = '10000 mm'
        world.Width = '10000 mm'
        world.ViewObject.DrawStyle = "Dotted"
        world.ViewObject.LineWidth = 1.0
        world.ViewObject.Transparency = 85
        world.ViewObject.Visibility = False
        world.Placement = FreeCAD.Placement(
            FreeCAD.Vector(-5000, -5000, -5000),
            FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 0),
            FreeCAD.Vector(0, 0, 0))
        doc.recompute()


class AddBox:

    def GetResources(self):
        return {
            'Pixmap': __dir__ + '/icons/cube.svg',
            'MenuText': 'Add a box',
            'ToolTip': 'add box volume'
        }

    def IsActive(self):
        if FreeCAD.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        doc = FreeCAD.ActiveDocument
        global boxID
        boxName = "Box_%d" % boxID
        doc.addObject("Part::Box", boxName)
        sbox = doc.getObject(boxName)
        sbox.Length = '100 mm'
        sbox.Height = '100 mm'
        sbox.Width = '100 mm'
        boxID = boxID + 1


class AddCylinder:

    def GetResources(self):
        return {
            'Pixmap': __dir__ + '/icons/cylinder.svg',
            'MenuText': 'Add a cylinder',
            'ToolTip': 'add a cylinder volume '
        }

    def IsActive(self):
        if FreeCAD.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        doc = FreeCAD.ActiveDocument
        global cylID
        name = "Cylinder_%d" % cylID
        mycyl = doc.addObject('Part::Cylinder', name)
        mycyl.Height = '50 mm'
        mycyl.Radius = '20 mm'
        cylID = cylID + 1


class AddSphere:

    def GetResources(self):
        return {
            'Pixmap': __dir__ + '/icons/sphere.svg',
            'MenuText': 'Add a sphere',
            'ToolTip': 'add a sphere volume '
        }

    def IsActive(self):
        if FreeCAD.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        doc = FreeCAD.ActiveDocument
        global sphereID
        name = "Sphere_%d" % sphereID
        mysphere = doc.addObject('Part::Sphere', name)
        mysphere.Radius = '50 mm'
        sphereID = sphereID + 1


class AddCone:

    def GetResources(self):
        return {
            'Pixmap': __dir__ + '/icons/cone.svg',
            'MenuText': 'Add a cone',
            'ToolTip': 'add a cone volume '
        }

    def IsActive(self):
        if FreeCAD.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        doc = FreeCAD.ActiveDocument
        global coneID
        name = "Cone_%d" % coneID
        mycone = doc.addObject('Part::Cone', name)
        mycone.Radius1 = '20 mm'
        mycone.Radius2 = '40 mm'
        mycone.Height = '60 mm'
        coneID = coneID + 1


if FreeCAD.GuiUp:
    FreeCAD.Gui.addCommand('export', Export())
    FreeCAD.Gui.addCommand('import', ImportFile())
    FreeCAD.Gui.addCommand('add_world', AddWorld())

    FreeCAD.Gui.addCommand('add_box', AddBox())
    FreeCAD.Gui.addCommand('add_cylinder', AddCylinder())
    FreeCAD.Gui.addCommand('add_sphere', AddSphere())
    FreeCAD.Gui.addCommand('add_cone', AddCone())

    FreeCAD.Gui.addCommand('set_material', MaterialSetter())
    FreeCAD.Gui.addCommand('set_tolerance', MeshingToleranceManager())
    FreeCAD.Gui.addCommand('set_physical_volume', PhysicalVolumeManager())

    FreeCAD.Gui.addCommand('hide_parts', PartVisibilityManager())
    FreeCAD.Gui.addCommand('filter_parts', PartFilter())
    FreeCAD.Gui.addCommand('show_measurements', MeasurementTool())
    FreeCAD.Gui.addCommand('manage_materials', MaterialManager())
    #FreeCAD.Gui.addCommand('run_sim', RunSim())
