# -*- coding: utf8 -*-
# part of the code taken from  https://github.com/KeithSloan/FreeCAD_GDML

import math
import re
import sys
import os
import PartGui
import FreeCAD
import Part
printverbose = False


if FreeCAD.GuiUp:
    import FreeCADGui
    gui = True
else:
    if printverbose:
        print("FreeCAD Gui not present.")
    gui = False


if open.__module__ == '__builtin__':
    pythonopen = open  # to distinguish python built-in open function from the one declared here


def open(filename):
    "called when freecad opens a file."
    global doc
    global pathName
    docname = os.path.splitext(os.path.basename(filename))[0]
    doc = FreeCAD.newDocument(docname)
    if filename.lower().endswith('.gdml'):
        processGDML(filename)
    return doc


def insert(filename, docname):
    "called when freecad imports a file"
    global doc
    global pathName
    groupname = os.path.splitext(os.path.basename(filename))[0]
    try:
        doc = FreeCAD.getDocument(docname)
    except NameError:
        doc = FreeCAD.newDocument(docname)
    if filename.lower().endswith('.gdml'):
        processGDML(filename)


class switch(object):
    value = None

    def __new__(class_, value):
        class_.value = value
        return True


def case(*args):
    return any((arg == switch.value for arg in args))


def myVector(x, y, z):
    base = FreeCAD.Vector(float(eval(x)), float(eval(y)), float(eval(z)))
    return base


def createBox(solid, volref, pos, rot):
    printf("CreateBox : ")
    printf(solid.attrib)
    mycube = doc.addObject('Part::Box',
                           volref.get('ref') + '_' + solid.get('name') + '_')
    mycube.Length = solid.get('x')
    mycube.Width = solid.get('y')
    mycube.Height = solid.get('z')
    printf("Position : ")
    #printf( pos.attrib)
    base = None
    if pos:
        base = myVector(pos.get('x'), pos.get('y'), pos.get('z'))
    else:
        base = FreeCAD.Vector(0, 0, 0)

    if rot:
        printf("Rotation : ")
        printf(rot.attrib)

    axis = FreeCAD.Vector(0, 0, 1)
    angle = 0
    place = FreeCAD.Placement(base, axis, angle)
    mycube.Placement = place
    print(mycube.Placement.Rotation)
    mycube.ViewObject.DisplayMode = 'Wireframe'


def makeCylinder(solid, r):
    mycyl = doc.addObject('Part::Cylinder', solid.get('name') + '_')
    mycyl.Height = solid.get('z')
    mycyl.Radius = r
    if solid.get('aunit' == 'rad'):
        mycyl.Angle = 180 * float(solid.get('deltaphi')) / math.pi
    if solid.get('aunit' == 'degrees'):
        mycyl.Angle = solid.get('deltaphi')
    return mycyl


def createTube(solid, volref, pos, rot):
    printf("CreateTube : ")
    print(solid.attrib)
    rmin = solid.get('rmin')
    rmax = solid.get('rmax')
    if (rmin is None or rmin == 0):
        mytube = makeCylinder(solid, rmax)
    else:
        mytube = doc.addObject('Part::Cut', 'Tube_' + solid.get('name') + '_')
        mytube.Base = makeCylinder(solid, rmax)
        mytube.Tool = makeCylinder(solid, rmin)

    print("Position : ")
    base = None
    if pos:
        print(pos.attrib)
        base = myVector(pos.get('x'), pos.get('y'), pos.get('z'))
    else:
        base = FreeCAD.Vector(0, 0, 0)

    if rot:
        print("Rotation : ")
        print(rot.attrib)
    axis = FreeCAD.Vector(0, 0, 1)
    angle = 0
    place = FreeCAD.Placement(base, axis, angle)
    mytube.Placement = place
    print(mytube.Placement.Rotation)


def createCone(solid, volref, pos, rot):
    printf("Cone is not implemented ")
    print(solid.attrib)


def createSolid(solid, volref, pos, rot):

    while switch(solid.tag):
        if case('box'):
            printf("Create box\n")
            createBox(solid, volref, pos, rot)
            break
        if case('tube'):
            printf("Create tube\n")
            createTube(solid, volref, pos, rot)
            break
        if case('cone'):
            printf("Create cone\n")
            createCone(solid, volref, pos, rot)
            break
        printf("Solid : " + solid.tag + " Not yet supported")
        break


def getRef(ptr):
    ref = ptr.get('ref')
    print("ref : " + ref)
    return ref


def parseObject(root, ptr):
    print(ptr.tag)
    print(ptr.attrib)
    if ptr.tag in ["subtraction", "union", "intersection"]:
        print("Boolean : " + ptr.tag)
        base = ptr.find('first')
        name = getRef(base)
        base = root.find("solids/*[@name='%s']" % name)
        parseObject(root, base)
        tool = ptr.find('second')
        name = getRef(tool)
        tool = root.find("solids/*[@name='%s']" % name)
        parseObject(root, tool)


def getVolSolid(root, name):
    print("Get Volume Solid")
    vol = root.find("structure/volume[@name='%s']" % name)
    sr = vol.find("solidref")
    print(sr.attrib)
    name = getRef(sr)
    solid = root.find("solids/*[@name='%s']" % name)
    return solid


def parsePhysVol(root, ptr):
    printf("ParsePhyVol")
    pos = ptr.find("positionref")
    if pos is not None:
        name = getRef(pos)
        pos = root.find("define/position[@name='%s']" % name)
        printf(pos.attrib)
    else:
        pos = ptr.find("position")
    rot = ptr.find("rotationref")
    if rot is not None:
        name = getRef(rot)
        rot = root.find("define/rotation[@name='%s']" % name)
    else:
        rot = ptr.find("rotation")
    volref = ptr.find("volumeref")
    name = getRef(volref)
    solid = getVolSolid(root, name)
    # if ((pos is not None) and (rot is not None)) :
    createSolid(solid, volref, pos, rot)
    # else:
    #    printf("not to create solid")

    parseVolume(root, name)


# ParseVolume
def parseVolume(root, name):
    printf("ParseVolume : " + name)
    vol = root.find("structure/volume[@name='%s']" % name)
    printf(vol.attrib)
    for pv in vol.findall('physvol'):
        parsePhysVol(root, pv)


def processGDML(filename):
    FreeCAD.Console.PrintMessage('Import GDML file : ' + filename + '\n')
    if printverbose:
        printf('ImportGDML Version 0.1')

    import xml.etree.ElementTree as ET
    tree = ET.parse(filename)
    root = tree.getroot()
    if printverbose:
        printf('Parsing gdml ...\n')

    for setup in root.find('setup'):
        setup.attrib
        FreeCAD.Console.PrintMessage(setup.attrib)
        ref = getRef(setup)
        parseVolume(root, ref)

    doc.recompute()
    if printverbose:
        printf('End ImportGDML')
    FreeCAD.Console.PrintMessage('End processing GDML file\n')


def printf(msg):
    FreeCAD.Console.PrintMessage(str(msg) + '\n')
    if printverbose:
        print(str(msg) + '\n')
