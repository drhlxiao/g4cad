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
import GdmlImporter

import os.path

import GdmlExporter 
import G4Materials

import re
import LabelManager
from MaterialDatabase import MaterialDatabase
from os.path import expanduser
import MaterialSelectionDialog
import MeasurementGui
#import SimulationRunManager 
boxID=0
coneID=0
sphereID=0
cylID=0
__dir__ = os.path.dirname(__file__)


# non icon comands
class ImportFile:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/import.svg',
                'MenuText': 'Import',
                'ToolTip': 'Import gdml files or other files'}

    def IsActive(self):
        return True

    def Activated(self):
        fname=QtGui.QFileDialog.getOpenFileName(directory=expanduser('~'))[0]
        if fname:
            #ImportGui.insert(fname,"Unnamed")
            GdmlImporter.open(fname)
        else:
            FreeCAD.Console.PrintWarning('invalid filename')

# icon comands
class Export:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/export.svg',
                'MenuText': 'Export',
                'ToolTip': 'Export solids to gdml files'}

    def IsActive(self):
        return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0


    def Activated(self):
        FreeCAD.Console.PrintMessage('export objects to gdml files')
        sel = FreeCADGui.Selection.getSelection() 
        if not sel:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("No Active Object!")
            ret = msgBox.exec_()
            FreeCAD.Console.PrintWarning('No Active object!')
            return 

        odir=QtGui.QFileDialog.getExistingDirectory(caption="Set output directory", directory=expanduser('~'))
        FreeCAD.Console.PrintMessage('exporting...')
        if odir:
            ex=GdmlExporter.GdmlExporter()
            ex.export(sel,odir)
        else:
            FreeCAD.Console.PrintMessage('Invalid output directory')


class SetPrecision:
    
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/mesh.svg',
                'MenuText': 'Set precision',
                'ToolTip': 'set precision'}

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

            items= ['0.01','0.1','0.2','0.5', '1','2', '3', '4', '5', '10', '20','50', '100', '200','500','1000']
            caption=''
            if len(sel)==1:
                caption='Tessellation tolerance for %s'%sel[0].Label
            else:
                caption='Tessellation  tolerance for the selected %d parts'%len(sel)

            item, ok = QtGui.QInputDialog.getItem(None,caption,
                "Tessellation tolerance:", items, 0, False)
            if ok and item:
                for obj in sel:
                    label=obj.Label
                    pLabel=LabelManager.LabelManager()
                    obj.Label=pLabel.updatePrecision(label,float(item))
                    FreeCAD.Console.PrintMessage('set: '+label+' precision:'+item)

            return 


import MaterialManagerGui

class ManageMaterials:

    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/database.svg',
                'MenuText': 'Material database',
                'ToolTip': 'Material database management'}

    def IsActive(self):
        return True
    def Activated(self):
        MaterialManagerGui.MainWidget.run()




class SetMaterial:
    
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/material.svg',
                'MenuText': 'Set material',
                'ToolTip': 'set material'}

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
            caption=''
            if len(sel)==1:
                caption='Set material for %s'%sel[0].Label
            else:
                caption='Set material for the selected %d parts'%len(sel)

            item,ok=MaterialSelectionDialog.setMaterialUI.run()
            FreeCAD.Console.PrintWarning('item, ok: '+item+' '+str(ok))

            if item <> "":
                for obj in sel:
                    label=obj.Label
                    pLabel=LabelManager.LabelManager()
                    obj.Label=pLabel.updateMaterial(label,item.strip())
                    FreeCAD.Console.PrintMessage(label+' material set to :'+item+'\n')
            else:
                FreeCAD.Console.PrintWarning('Material not set\n')




class ShowMeasurements:
    
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/measure.svg',
                'MenuText': 'Show dimensions',
                'ToolTip': 'Show dimensions'}

    def IsActive(self):
        return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0


    def Activated(self):

        sel = FreeCADGui.Selection.getSelection() 
        if len(sel)<>1:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Select one part!")
            ret = msgBox.exec_()
            FreeCAD.Console.PrintWarning('select one part!')
            return 
        else:
            try:
                if hasattr(sel[0],"Shape"):
                    sol=sel[0].Shape
                    name=sel[0].Label
                    mass=0

                    boundBox=sol.BoundBox
                    measurements={
                        "name":name,
                        "vol":sol.Volume,
                        "wx":sol.CenterOfMass[0],
                        "wy":sol.CenterOfMass[1],
                        "wz":sol.CenterOfMass[2],
                        "cx":sol.Placement.Base[0],
                        "cy":sol.Placement.Base[1],
                        "cz":sol.Placement.Base[2],
                        "xLen":boundBox.XLength,
                        "yLen":boundBox.YLength,
                        "zLen":boundBox.ZLength,
                        "xmin":boundBox.XMin,
                        "xmax":boundBox.XMax,
                        "ymin":boundBox.YMin,
                        "ymax":boundBox.YMax,
                        "zmin":boundBox.ZMin,
                        "zmax":boundBox.ZMax
                        #"mass": mass
                        }

                    MeasurementGui.MainWidget.run(measurements=measurements)


                elif hasattr(sel[0],"Mesh") or hasattr(sel[0],"Point"):
                    FreeCAD.Console.PrintMessage("Mesh or point selected")
                else:
                    FreeCAD.Console.PrintMessage("Unknown object")

            except:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("Failed to measure!")
                ret = msgBox.exec_()
                FreeCAD.Console.PrintWarning('failed to get the properties!')

class HideParts:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/hide.svg',
                'MenuText': 'Hide small parts',
                'ToolTip': 'Hide small parts'}

    def IsActive(self):
        doc=FreeCAD.ActiveDocument
        if doc:
            if len(doc.Objects)>=1:
                return True

        return False

    def Activated(self):

        value,ok= QtGui.QInputDialog.getDouble(None,"Set the volume limit to be hidden","Volume (mm3):")
        if not ok:
            return
        doc=FreeCAD.ActiveDocument
        objs=doc.Objects
        for ob in objs:
            try:
                sol=ob.Shape
                vol=sol.Volume
                if vol<value:
                    ob.ViewObject.Visibility=False
                    FreeCAD.Console.PrintMessage(ob.Label + ' volume: '+str(vol)+'\n')
            except:
                FreeCAD.Console.PrintMessage('Fail to check:'+ob.Label+'\n')



class SearchParts:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/search.svg',
                'MenuText': 'Search parts',
                'ToolTip': 'Search parts'}

    def IsActive(self):
        doc=FreeCAD.ActiveDocument
        if doc:
            if len(doc.Objects)>=1:
                return True

        return False

    def Activated(self):

        pattern,ok= QtGui.QInputDialog.getText(None,"Search parts by name","Search parts by name:")
        if not ok:
            return
        doc=FreeCAD.ActiveDocument
        objs=doc.Objects
        for ob in objs:
            try:
                label=ob.Label
                if pattern in label:
                    FreeCADGui.Selection.addSelection(ob)
                    FreeCAD.Console.PrintMessage('Found:'+ob.Label+'\n')
                    ob.ViewObject.Visibility=True
                else:
                    ob.ViewObject.Visibility=False
            except:
                pass


class SetPhysicalVolume:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/setpv.svg',
                'MenuText': 'Set physical volume',
                'ToolTip': 'Set physical volume '}

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
            name,ok= QtGui.QInputDialog.getText(None,"Set physical volume name","Physical volume name:")
            if not ok:
                return
            elif name.strip():
                num_sel=len(sel)
                for i,obj in enumerate(sel):
                    label=obj.Label
                    pLabel=LabelManager.LabelManager()
                    sd_name=name.strip()
                    if num_sel>1:
                        sd_name='{}_{}'.format(name.strip(),i)
                    obj.Label=pLabel.updatePhysicalVolume(label,sd_name)
                    FreeCAD.Console.PrintMessage('set {} as physical volume: {}\n'.format(label, sd_name))
            else:
                FreeCAD.Console.PrintWarning('Invalid physical volume name\n')








class AddWorld:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/world.svg',
                'MenuText': 'Add world volume',
                'ToolTip': 'add world volume'}
    def IsActive(self):
        if FreeCAD.ActiveDocument:
            return True
        else:
            return False
    def Activated(self):
        objs= FreeCAD.ActiveDocument.Objects
        for obj in objs:
            if obj.Name=='__world__':
                msgBox = QtGui.QMessageBox()
                msgBox.setText("The world volume already exists!")
                ret = msgBox.exec_()
                FreeCAD.Console.PrintWarning('world volume already exists!')
                return 

        doc=FreeCAD.ActiveDocument
        doc.addObject("Part::Box","__world__")
        world= doc.getObject("__world__") 
        pLabel=LabelManager.LabelManager()
        world.Label=pLabel.updateMaterial("World","G4_AIR")
        world.Length='10000 mm'
        world.Height='10000 mm'
        world.Width='10000 mm'
        world.ViewObject.DrawStyle="Dotted"
        world.ViewObject.LineWidth=1.0
        world.ViewObject.Transparency=85
        world.ViewObject.Visibility=False
        world.Placement=FreeCAD.Placement(FreeCAD.Vector(-5000,-5000,-5000), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0), FreeCAD.Vector(0,0,0))
        doc.recompute()



class AddBox:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/cube.svg',
                'MenuText': 'Add a box',
                'ToolTip': 'add box volume'}
    def IsActive(self):
        if FreeCAD.ActiveDocument:
            return True
        else:
            return False
    def Activated(self):
        doc=FreeCAD.ActiveDocument
        global boxID 
        boxName="Box_%d"%boxID
        doc.addObject("Part::Box",boxName)
        sbox= doc.getObject(boxName)
        sbox.Length='100 mm'
        sbox.Height='100 mm'
        sbox.Width='100 mm'
        boxID=boxID+1



class AddCylinder:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/cylinder.svg',
                'MenuText': 'Add a cylinder',
                'ToolTip': 'add a cylinder volume '}
    def IsActive(self):
        if FreeCAD.ActiveDocument:
            return True
        else:
            return False
    def Activated(self):
        doc=FreeCAD.ActiveDocument
        global cylID 
        name="Cylinder_%d"%cylID
        mycyl = doc.addObject('Part::Cylinder',name)
        mycyl.Height = '50 mm'
        mycyl.Radius = '20 mm'
        cylID=cylID+1


class AddSphere:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/sphere.svg',
                'MenuText': 'Add a sphere',
                'ToolTip': 'add a sphere volume '}
    def IsActive(self):
        if FreeCAD.ActiveDocument:
            return True
        else:
            return False
    def Activated(self):
        doc=FreeCAD.ActiveDocument
        global sphereID
        name="Sphere_%d"%sphereID
        mysphere= doc.addObject('Part::Sphere',name)
        mysphere.Radius = '50 mm'
        sphereID=sphereID+1


class AddCone:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/cone.svg',
                'MenuText': 'Add a cone',
                'ToolTip': 'add a cone volume '}
    def IsActive(self):
        if FreeCAD.ActiveDocument:
            return True
        else:
            return False
    def Activated(self):
        doc=FreeCAD.ActiveDocument
        global coneID
        name="Cone_%d"%coneID
        mycone= doc.addObject('Part::Cone',name)
        mycone.Radius1 = '20 mm'
        mycone.Radius2 = '40 mm'
        mycone.Height= '60 mm'
        coneID=coneID+1


#class RunSim:
#    def GetResources(self):
#        return {'Pixmap': __dir__ + '/icons/sim.png',
#                'MenuText': 'Run simulation',
#                'ToolTip': 'Run simulation'}
#    def IsActive(self):
#        if FreeCAD.ActiveDocument:
#            if FreeCAD.ActiveDocument.Objects:
#                return True
#
#        return False
#    def Activated(self):
#        SimulationRunManager.run()




if FreeCAD.GuiUp:
    FreeCAD.Gui.addCommand('export', Export())
    FreeCAD.Gui.addCommand('import', ImportFile())
    FreeCAD.Gui.addCommand('add_world', AddWorld())

    FreeCAD.Gui.addCommand('add_box', AddBox())
    FreeCAD.Gui.addCommand('add_cylinder', AddCylinder())
    FreeCAD.Gui.addCommand('add_sphere', AddSphere())
    FreeCAD.Gui.addCommand('add_cone', AddCone())

    FreeCAD.Gui.addCommand('set_material', SetMaterial())
    FreeCAD.Gui.addCommand('set_precision', SetPrecision())
    FreeCAD.Gui.addCommand('set_physical_volume', SetPhysicalVolume())

    FreeCAD.Gui.addCommand('hide_parts', HideParts())
    FreeCAD.Gui.addCommand('search_parts', SearchParts())
    FreeCAD.Gui.addCommand('show_measurements', ShowMeasurements())
    FreeCAD.Gui.addCommand('manage_materials', ManageMaterials())
    #FreeCAD.Gui.addCommand('run_sim', RunSim())
    

