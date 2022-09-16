# -*- coding: utf-8 -*-
"""
Created on May 16 11:12:45 2017
@author: Hualin Xiao
@email:  hualin.xiao@psi.ch


FreeCAD GDML workbench


To do list:
       optimize the geometry:
      * increase precision for physical volumes
      * merge parts with the same material to reduce overlaps
      * FreeCAD plugin
      * editing models with freecad



"""

import sys
import FreeCAD
import FreeCADGui 
import os
import ImportGui
from GdmlWriter import *
#import material
import re
import LabelManager
import GdmlSheet
import utils



class GdmlExporter:
    def __init__(self):
        self.min_volume=0
        self.precision=0.1
        self.logfile=None
        self.shape_counter=0
        self.default_material="G4_Al"

        


    def getPlacementBase(self,ob):
        try:
            return ob.Placement.Base
        except:
            return []

    def getEulerAngle(self,ob):
        '''debug and test needed'''
        try:
            rot=ob.Placement.Rotation
            angles=FreeCAD.Base.Rotation(rot).toEuler()
            # yaw pitch roll, z, y,x
            return FreeCAD.Vector(angles)
        except:
            return FreeCAD.Vector()

    def checkPlacement(self,ob,x,y,z):
        b = FreeCAD.Vector(x,y,z)
        zero=FreeCAD.Vector(0,0,0)
        dispalacement=None
        rot=None
        displacement=ob.Placement.Base-b
        rot=self.getEulerAngle(ob)
        if (ob.Placement.Base - b).Length < 1e-6:
            displacement=None
        if (rot-zero).Length<1e-3:
            rot=None

        return displacement,rot

    def meshing(self, mesh, gd, solid_name):
        n=0
        for vec in mesh[0]:
            vertex_name='__v_'+solid_name+'_%05d'%n
            gd.addPosition(vertex_name, vec.x,vec.y,vec.z,"mm")
            n+=1

        faces=[]
        for tri in mesh[1]:
            face=[]
            v1= tri[0]
            vn1="__v_%s_%05d"%(solid_name,v1)
            v2= tri[1]
            vn2="__v_%s_%05d"%(solid_name,v2)
            v3= tri[2]
            vn3="__v_%s_%05d"%(solid_name,v3)
            faces.append(['triangular',{'vertex1':vn1,'vertex2':vn2,'vertex3':vn3,'type':'ABSOLUTE'}, []])
        gd.addPolyhedraSolid(solid_name,faces)




    def meshShape(self, ob,gd, solid_name):
        pcs=self.getPrecision(ob)
        #self.printf('%s precision:%f\n'%(ob.Label,pcs))
        mesh=ob.Shape.tessellate(pcs)
        self.meshing(mesh, gd, solid_name)

    def getMaterial(self,label):
        pLabel=LabelManager.LabelManager()
        pLabel.parse(label)
        mat=pLabel.getMaterial()
        if mat=="":
            mat=self.default_material
        return mat

    def checkPhysicalVolume(self, label):
        pLabel=LabelManager.LabelManager()
        pLabel.parse(label)
        return pLabel.getPhysicalVolume()

    

        

    def getPrecision(self,ob):
        pLabel=LabelManager.LabelManager()
        pLabel.parse(ob.Label)
        label_precision=pLabel.getPrecision()
        if label_precision>0:
            return label_precision
        else:
            return self.precision




    def processObject(self,gd,ob, create_solid_only=False):
        world_volume=gd.createWorldVolume()
        solid_name='__sol_%d_'%self.shape_counter
        volume_name='__vol__%d_'%self.shape_counter
        position_name='__pos__%d_'%self.shape_counter
        rotation_name='__rot__%d_'%self.shape_counter
        


        phys_name='__phys_%d_'%self.shape_counter
        physical_volume=self.checkPhysicalVolume(ob.Label)
        if physical_volume:
            phys_name=physical_volume

        material_name=self.getMaterial(ob.Label)
        self.shape_counter+=1
        displacement=None
        rot=None
        is_CSG=True

        if ob.TypeId == "Part::Sphere" :
            self.printf( "Sphere Radius : "+str(ob.Radius))
            rmax=ob.Radius
            #csg.write("sphere($fn = 0, "+fafs+", r = "+str(ob.Radius)+");\n")
            gd.addSphere(solid_name, 0, rmax, 0, 360, 0, 180,"mm","deg")
            displacement,rot=self.checkPlacement(ob,0,0,0)
               
        elif ob.TypeId == "Part::Box" :
            self.printf( "cube : ("+ str(ob.Length)+","+str(ob.Width)+","+str(ob.Height)+")")
            displacement,rot= self.checkPlacement(ob,-ob.Length/2,-ob.Width/2,-ob.Height/2)        
            gd.addBox(solid_name, ob.Length, ob.Width, ob.Height,"mm")

        elif ob.TypeId == "Part::Cylinder" :
            self.printf( "cylinder : Height "+str(ob.Height)+ " Radius "+str(ob.Radius) )
            displacement,rot= self.checkPlacement(ob,0,0,-ob.Height/2)
            gd.addTube(solid_name, 0, ob.Radius, ob.Height, 0, 360,"mm","deg")
            #def addTube(self, name, rmin, rmax, z, startphi, deltaphi,lunit="cm",aunit="deg"):
                
        elif ob.TypeId == "Part::Cone" :
            self.printf( "cone : Height "+str(ob.Height)+ " Radius1 "+str(ob.Radius1)+" Radius2 "+str(ob.Radius2))
            displacement,rot= self.checkPlacement(ob,0,0,-ob.Height/2)
            gd.addCone(solid_name, ob.Height, 0, 0, ob.Radius1, ob.Radius2, 0, 360,"mm","deg")

        elif ob.TypeId == "Part::Torus" :
            self.printf( "Torus")
            if ob.Angle3 == 360.00 :
                displacement,rot=self.checkPlacement(ob,0,0,0)
                gd.addTorus(solid_name, ob.Radius1,0, ob.Radius2, 0, 360)
            else : # Cannot convert to rotate extrude so best effort is polyhedron
                self.meshShape(ob,gd, solid_name)
        #the following lines of still needs to be debuged
            commented='''
        elif ob.TypeId == "Part::Cut" :
            print "Cut"
            sol0,vol0,phy0=self.processObject(gd,ob.Base,True)
            sol1,vol1,phy1=self.processObject(gd,ob.Tool,True)
            relative_pos=[0,0,0]
            relative_rot=[0,0,0]
            gd.subtraction(solid_name,sol0, sol1,relative_pos, relative_rot)

        elif ob.TypeId == "Part::Fuse" :
            print "union"
            sol0,vol0,phy0=self.processObject(gd,ob.Base,True)
            sol1,vol1,phy1=self.processObject(gd,ob.Tool,True)
            relative_pos=[0,0,0]
            relative_rot=[0,0,0]
            gd.union(solid_name,sol0, sol1,relative_pos, relative_rot)

        elif ob.TypeId == "Part::Common" :
            sol0,vol0,phy0=self.processObject(gd,ob.Base,True)
            sol1,vol1,phy1=self.processObject(gd,ob.Tool,True)
            relative_pos=[0,0,0]
            relative_rot=[0,0,0]
            gd.intersection(solid_name,sol0, sol1,relative_pos, relative_rot)
            '''
        elif ob.isDerivedFrom('Part::Feature') :
            self.printf( "Part::Feature")
            displacement,rot= self.checkPlacement(ob,0,0,0)
            is_CSG=False
            self.meshShape(ob,gd,solid_name)


        
        pos_in_world={}
        rot_in_world={}
        #position and rotation have to be defined in world for a non-mesh object


        if displacement:
            gd.addPosition(position_name, displacement.x, displacement.y, displacement.z,"mm")
            if is_CSG:
                pos_in_world={
                        'name':position_name,
                        'x':displacement.x,
                        'y':displacement.y,
                        'z':displacement.z,
                        'unit':'mm'
                        }
        else:
            position_name='center'

        if rot:
            gd.addRotation(rotation_name, rot.x, rot.y, rot.z,'deg')
            if is_CSG:
                rot_in_world={
                        'name':rotation_name,
                        'x':rot.x,
                        'y':rot.y,
                        'z':rot.z,
                        'unit':'deg'
                        }
        else:
            rotation_name='identity'

        if not create_solid_only:
            gd.addVolume(volume_name, solid_name, material_name, [])
            gd.addPhysVolume(world_volume,volume_name, phys_name, position_name,rotation_name)

        return solid_name,volume_name,phys_name,material_name,pos_in_world,rot_in_world


    def setPrecision(value):
        self.precision=value
    def export(self,exportlist,output, multi_files=True):
     
        logdir=output
        if multi_files==False:
            logdir=os.path.dirname(output)
        self.initLog(logdir)
        self.printf('Writing gdml...\n')
     

        if multi_files:
            odir=os.path.normpath(output)+'/gdml'
            utils.mkdir(odir)
            file_list,phys_name_list, pos_list, rot_list =self.exportSubShapes(exportlist,odir)
            self.mergeGDML(file_list,phys_name_list,pos_list, rot_list,odir)
        else:
            self.exportToSingleFile(exportlist, output)
        self.printf('done!\n')

    def checkWorld(self, gd):
        for i in FreeCAD.ActiveDocument.Objects:
            if i.Name=="__world__" and i.TypeId=="Part::Box":
                mat=self.getMaterial(i.Label)
                x=i.Length
                y=i.Width
                z=i.Height
                self.printf("creating world...")
                self.printf("size:(%f,%f,%f)"%(x,y,z))
                self.printf("material:"+mat)
                gd.createWorldVolume(x,y,z,mat)

    def initLog(self,odir):
        logfilename='%s/cad2gdml.log'%odir
        self.logfile=open(logfilename,'w')

    

    def exportToSingleFile(self,exportlist, fname):
        gdml=GdmlWriter()
        self.checkWorld(gdml)
        world_volume_name=gdml.createWorldVolume()
        self.printf("world:"+world_volume_name)
        sheet=GdmlSheet.GdmlSheet()
        sheet.createNewSheet("log")
        sheet.append('No.','Part','solid','logical volume','physical volume','material')
        materials=[]
        for num, i in enumerate(exportlist):
            if i.TypeId=='Spreadsheet::Sheet':
                continue

            if i.Name=="__world__" and i.TypeId=="Part::Box":
                continue
            
            #volume=i.Shape.Volume
            ulabel=i.Label
            label=ulabel.encode('ascii','ignore')
            name=i.Name
            #print 'volume: %s -- %s: %f'%(label,name,volume)

            solid,vol,phys,mat,world_pos,world_rot=self.processObject(gdml,i)
            if mat not in materials:
                gdml.processMaterial(mat)
                materials.append(mat)

            sheet.append(num,label,solid,vol,phys,mat)

        gdml.moveFrontLast()
        gdml.addSetup('world', '1.0', world_volume_name)
        gdml.writeFile(fname)


    def getPhysVolumeName(self,n, ulabel):
        phys_name="_phys_%d"%n
        #default phys volume name in the world.gdml
        physical_volume=self.checkPhysicalVolume(ulabel)
        if physical_volume:
            phys_name=physical_volume
            #extract from the label
        return phys_name



    def exportSubShapes(self,exportlist,odir):
        self.printf( 'Converting parts to gdml files\n')
        gdml_files=[]
        phys_name_list=[]
        pos_world_list=[]
        rot_world_list=[]


        utils.mkdir(odir)
        sheet=GdmlSheet.GdmlSheet()
        sheet.createNewSheet("gdml_log")
        sheet.append("Part","GDML file",'solid','logical volume','physical volume','material')

        
        for n, i in enumerate(exportlist):
            if i.TypeId=='Spreadsheet::Sheet':
                continue
            pLabel=LabelManager.LabelManager()
            ulabel=i.Label
            ascii_label=ulabel.encode('ascii','ignore')
            fname=odir+"/%s_%d.gdml"%(pLabel.getFilenameFromLabel(ascii_label),n)

            self.printf('%s -> %s \n'%(ascii_label,fname))

            if i.Name=="__world__" and i.TypeId=="Part::Box":
                continue

            phys_name=self.getPhysVolumeName(n,ulabel)
            phys_name_list.append(phys_name)

            gdml_files.append(fname)

            gdml=GdmlWriter()
            self.checkWorld(gdml)

            world_volume_name=gdml.createWorldVolume()
            sol,vol,phys,mat,world_pos,world_rot=self.processObject(gdml,i)

            pos_world_list.append(world_pos)
            rot_world_list.append(world_rot)
            

            gdml.processMaterial(mat)

            sheet.append(pLabel.getLabel(ascii_label),
                    os.path.basename(fname),sol,vol,phys,mat)

            gdml.moveFrontLast()
            gdml.addSetup('world', '0.0', vol )
            gdml.writeFile(fname)
        return gdml_files, phys_name_list,pos_world_list,rot_world_list


    def mergeGDML(self,file_list,phys_name_list,pos_world_list, rot_world_list,odir):
        #write World.gdml
        self.printf('wring world gdml\n')

        if len(file_list)> 1:
            gdml=GdmlWriter()
            self.checkWorld(gdml)
            world_volume_name=gdml.createWorldVolume()
            fname_out='%s/World.gdml'%(odir)
            for gdml_fname, phys_vol_name, pos, rot in zip(file_list,phys_name_list,pos_world_list,rot_world_list):
                part_file_name='gdml/'+os.path.basename(gdml_fname)
                gdml.includePhysVolume(world_volume_name, phys_vol_name,part_file_name,pos,rot)
            gdml.addSetup('world', '1.0', world_volume_name)
            gdml.writeFile(fname_out)
    def setMinimalVolume(self, minvol):
        self.min_volume=minvol

    def printf(self,msg):
        msg+="\n"
        FreeCAD.Console.PrintMessage(msg)
        if self.logfile:
            self.logfile.write(msg)




def export(exportList,output_filename):
    ex=GdmlExporter()
    ex.export(exportList,output_filename,False)


