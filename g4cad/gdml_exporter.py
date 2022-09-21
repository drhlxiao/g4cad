# -*- coding: utf-8 -*-
"""
Created on May 16 11:12:45 2017
@author: Hualin Xiao
@email:  hualin.xiao@psi.ch

FreeCAD G4CAD workbench

"""

import os
import sys
import re
import ImportGui
import FreeCAD
import FreeCADGui

import gdml_sheet
from gdml_manager import GdmlManager
from property_manager import PropertyManager


def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


class GdmlExporter:

    def __init__(self):
        self.min_volume = 0
        self.logfile = None
        self.shape_counter = 0
        self.worker = None
    def setWorker(self,worker):
        self.worker=worker

    def getPlacementBase(self, ob):
        try:
            return ob.Placement.Base
        except Exception as e:
            FreeCAD.Console.PrintWarning(str(e))
            return []

    def getEulerAngle(self, ob):
        '''debug and test needed'''
        try:
            rot = ob.Placement.Rotation
            angles = FreeCAD.Base.Rotation(rot).toEuler()
            # yaw pitch roll, z, y,x
            return FreeCAD.Vector(angles)
        except Exception as e:
            FreeCAD.Console.PrintWarning(str(e))
            return FreeCAD.Vector()

    def checkPlacement(self, ob, x, y, z):
        b = FreeCAD.Vector(x, y, z)
        zero = FreeCAD.Vector(0, 0, 0)
        dispalacement = None
        rot = None
        displacement = ob.Placement.Base - b
        rot = self.getEulerAngle(ob)
        if (ob.Placement.Base - b).Length < 1e-6:
            displacement = None
        if (rot - zero).Length < 1e-3:
            rot = None

        return displacement, rot

    def meshing(self, mesh, gd, solid_name):
        n = 0
        for vec in mesh[0]:
            vertex_name = '__v_' + solid_name + '_%05d' % n
            gd.addPosition(vertex_name, vec.x, vec.y, vec.z, "mm")
            n += 1

        faces = []
        for tri in mesh[1]:
            face = []
            v1 = tri[0]
            vn1 = "__v_%s_%05d" % (solid_name, v1)
            v2 = tri[1]
            vn2 = "__v_%s_%05d" % (solid_name, v2)
            v3 = tri[2]
            vn3 = "__v_%s_%05d" % (solid_name, v3)
            faces.append([
                'triangular', {
                    'vertex1': vn1,
                    'vertex2': vn2,
                    'vertex3': vn3,
                    'type': 'ABSOLUTE'
                }, []
            ])
        gd.addPolyhedraSolid(solid_name, faces)

    def meshShape(self, ob, gd, solid_name):

        toll=PropertyManager.getProperty(ob, 'Tolerance')

        mesh = ob.Shape.tessellate(toll)
        self.meshing(mesh, gd, solid_name)


    def processObject(self, gd, ob, create_solid_only=False):
        world_volume = gd.createWorldVolume()
        solid_name = '__sol_%d_' % self.shape_counter
        volume_name = '__vol__%d_' % self.shape_counter
        position_name = '__pos__%d_' % self.shape_counter
        rotation_name = '__rot__%d_' % self.shape_counter


        phys_name = PropertyManager.getProperty(ob,'Physical_Volume', self.shape_counter)
        material_name = PropertyManager.getProperty(ob, 'Material')

        self.shape_counter += 1
        displacement = None
        rot = None
        is_CSG = True

        if ob.TypeId == "Part::Sphere":
            #self.info("Sphere Radius : " + str(ob.Radius))
            rmax = ob.Radius
            gd.addSphere(solid_name, 0, rmax, 0, 360, 0, 180, "mm", "deg")
            displacement, rot = self.checkPlacement(ob, 0, 0, 0)

        elif ob.TypeId == "Part::Box":
            #self.info("cube : (" + str(ob.Length) + "," +
            #                  str(ob.Width) + "," + str(ob.Height) + ")")
            displacement, rot = self.checkPlacement(ob, -ob.Length / 2,
                                                    -ob.Width / 2,
                                                    -ob.Height / 2)
            gd.addBox(solid_name, ob.Length, ob.Width, ob.Height, "mm")

        elif ob.TypeId == "Part::Cylinder":
            #self.info("cylinder : Height " + str(ob.Height) +
            #                  " Radius " + str(ob.Radius))
            displacement, rot = self.checkPlacement(ob, 0, 0, -ob.Height / 2)
            gd.addTube(solid_name, 0, ob.Radius, ob.Height, 0, 360, "mm",
                       "deg")
        elif ob.TypeId == "Part::Cone":
            #self.info("cone : Height " + str(ob.Height) + " Radius1 " +
            #                  str(ob.Radius1) + " Radius2 " + str(ob.Radius2))
            displacement, rot = self.checkPlacement(ob, 0, 0, -ob.Height / 2)
            gd.addCone(solid_name, ob.Height, 0, 0, ob.Radius1, ob.Radius2, 0,
                       360, "mm", "deg")

        elif ob.TypeId == "Part::Torus":
            #self.info("Torus")
            if ob.Angle3 == 360.00:
                displacement, rot = self.checkPlacement(ob, 0, 0, 0)
                gd.addTorus(solid_name, ob.Radius1, 0, ob.Radius2, 0, 360)
            else:  # Cannot convert to rotate extrude so best effort is polyhedron
                self.meshShape(ob, gd, solid_name)
        elif ob.isDerivedFrom('Part::Feature'):
            #self.info("Part::Feature")
            displacement, rot = self.checkPlacement(ob, 0, 0, 0)
            is_CSG = False
            self.meshShape(ob, gd, solid_name)
        try:
            boundBox = ob.Shape.BoundBox
        except AttributeError:
            boundBox = None

        pos_in_world = {}
        rot_in_world = {}
        # position and rotation have to be defined in world for a non-mesh
        # object

        if displacement:
            gd.addPosition(position_name, displacement.x, displacement.y,
                           displacement.z, "mm")
            if is_CSG:
                pos_in_world = {
                    'name': position_name,
                    'x': displacement.x,
                    'y': displacement.y,
                    'z': displacement.z,
                    'unit': 'mm'
                }
        else:
            position_name = 'center'

        if rot:
            gd.addRotation(rotation_name, rot.x, rot.y, rot.z, 'deg')
            if is_CSG:
                rot_in_world = {
                    'name': rotation_name,
                    'x': rot.x,
                    'y': rot.y,
                    'z': rot.z,
                    'unit': 'deg'
                }
        else:
            rotation_name = 'identity'

        if not create_solid_only:
            gd.addVolume(volume_name, solid_name, material_name, [])
            gd.addPhysVolume(world_volume, volume_name, phys_name,
                             position_name, rotation_name)

        return solid_name, volume_name, phys_name, material_name, pos_in_world, rot_in_world, boundBox


    def start(self, exportlist, output, multi_files=True):
        logdir = output
        if not multi_files:
            logdir = os.path.dirname(output)
        self.initLog(logdir)
        self.info('Writing gdml...\n')

        if multi_files:
            odir = os.path.normpath(output) + '/gdml'
            if not os.path.exists(odir):
                os.makedirs(odir)
            file_list, phys_name_list, pos_list, rot_list = self.exportSubShapes(
                exportlist, odir)
            self.mergeGDML(file_list, phys_name_list, pos_list, rot_list, odir)
        else:
            self.exportToSingleFile(exportlist, output)
        self.info('done!\n')

    def checkWorld(self, gd):
        for i in FreeCAD.ActiveDocument.Objects:
            if i.Name == "__world__" and i.TypeId == "Part::Box":
                mat = PropertyManager.getProperty(i, 'Material')
                x = i.Length
                y = i.Width
                z = i.Height
                self.info("creating world...")
                self.info("size:(%f,%f,%f)" % (x, y, z))
                self.info("material:" + mat)
                gd.createWorldVolume(x, y, z, mat)

    def initLog(self, odir):
        logfilename = '%s/g4cad.log' % odir
        self.logfile = open(logfilename, 'w')

    def exportToSingleFile(self, exportlist, fname):
        gdml = GdmlManager()
        self.checkWorld(gdml)
        world_volume_name = gdml.createWorldVolume()
        self.info("world:" + world_volume_name)
        sheet = gdml_sheet.GdmlSheet()
        sheet.createNewSheet("log")
        sheet.append('No.', 'Part', 'solid', 'logical volume',
                     'physical volume', 'material', 'center x', 'center y',
                     'center z', 'length x', 'length y', 'length z')
        materials = []
        for num, i in enumerate(exportlist):

            if i.TypeId == 'Spreadsheet::Sheet':
                continue

            if i.Name == "__world__" and i.TypeId == "Part::Box":
                continue
            ulabel = i.Label
            self.info("Exporting %s \n..."%ulabel)
            label = get_valid_filename(ulabel)
            name = i.Name
            solid, vol, phys, mat, world_pos, world_rot, boundBox = self.processObject(
                gdml, i)
            if mat not in materials:
                gdml.processMaterial(mat)
                materials.append(mat)

            center_x = ''
            center_y = ''
            center_z = ''
            length_x = ''
            length_y = ''
            length_z = ''
            if boundBox:
                center_x = (boundBox.XMin + boundBox.XMax) / 2
                center_y = (boundBox.YMin + boundBox.YMax) / 2
                center_z = (boundBox.ZMin + boundBox.ZMax) / 2
                length_x = boundBox.XLength
                length_y = boundBox.YLength
                length_z = boundBox.ZLength

            sheet.append(num, label, solid, vol, phys, mat, center_x, center_y,
                         center_z, length_x, length_y, length_z)

        gdml.moveFrontLast()
        gdml.addSetup('world', '1.0', world_volume_name)
        gdml.writeFile(fname)



    def exportSubShapes(self, exportlist, odir):
        self.info('Converting parts to gdml files\n')
        gdml_files = []
        phys_name_list = []
        pos_world_list = []
        rot_world_list = []

        if not os.path.exists(odir):
            os.makedirs(odir)

        sheet = gdml_sheet.GdmlSheet()
        sheet.createNewSheet("gdml_log")
        sheet.append("Part", "GDML file", 'solid', 'logical volume',
                     'physical volume', 'material', 'center x', 'center y',
                     'center z', 'length x', 'length y', 'length z')

        for n, i in enumerate(exportlist):
            if i.TypeId == 'Spreadsheet::Sheet':
                continue


            ulabel = i.Label
            ascii_label = get_valid_filename(ulabel)
            fname=os.path.join(odir, "%s_%d.gdml" % (ascii_label, n))

            self.info('Exporting %s -> %s \n' % (ascii_label, fname))

            if i.Name == "__world__" and i.TypeId == "Part::Box":
                continue

            phys_name=PropertyManager.getProperty(i,'Physical_Volume',n)

            phys_name_list.append(phys_name)

            gdml_files.append(fname)

            gdml = GdmlManager()
            self.checkWorld(gdml)

            world_volume_name = gdml.createWorldVolume()
            sol, vol, phys, mat, world_pos, world_rot, boundBox = self.processObject(
                gdml, i)

            pos_world_list.append(world_pos)
            rot_world_list.append(world_rot)

            gdml.processMaterial(mat)

            center_x = ''
            center_y = ''
            center_z = ''
            length_x = ''
            length_y = ''
            length_z = ''
            if boundBox:
                center_x = (boundBox.XMin + boundBox.XMax) / 2
                center_y = (boundBox.YMin + boundBox.YMax) / 2
                center_z = (boundBox.ZMin + boundBox.ZMax) / 2
                length_x = boundBox.XLength
                length_y = boundBox.YLength
                length_z = boundBox.ZLength

            sheet.append((ascii_label), os.path.basename(fname),
                         sol, vol, phys, mat, center_x, center_y, center_z,
                         length_x, length_y, length_z)

            gdml.moveFrontLast()
            gdml.addSetup('world', '0.0', vol)
            gdml.writeFile(fname)
            sheet.recompute()
        return gdml_files, phys_name_list, pos_world_list, rot_world_list

    def mergeGDML(self, file_list, phys_name_list, pos_world_list,
                  rot_world_list, odir):
        # write World.gdml
        self.info('Writing World volume...\n')

        if len(file_list) > 1:
            gdml = GdmlManager()
            self.checkWorld(gdml)
            world_volume_name = gdml.createWorldVolume()
            fname_out = '%s/World.gdml' % (odir)
            for gdml_fname, phys_vol_name, pos, rot in zip(
                    file_list, phys_name_list, pos_world_list, rot_world_list):
                part_file_name = 'gdml/' + os.path.basename(gdml_fname)
                gdml.includePhysVolume(world_volume_name, phys_vol_name,
                                       part_file_name, pos, rot)
            gdml.addSetup('world', '1.0', world_volume_name)
            gdml.writeFile(fname_out)

    def setMinimalVolume(self, minvol):
        self.min_volume = minvol

    def info(self, msg):
        msg += "\n"
        if self.worker:
            self.worker.info(msg)

        if self.logfile:
            self.logfile.write(msg)


def export(exportList, output_filename):
    ex = GdmlExporter()
    ex.start(exportList, output_filename, False)
