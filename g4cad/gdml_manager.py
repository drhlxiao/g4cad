# -*- coding: utf-8 -*-
"""
Created on May 16 11:12:45 2017
@author: Hualin Xiao
@email:  hualin.xiao@psi.ch

"""

import math

import numpy as np
import g4_materials
import material_database
import FreeCAD
import time


class GdmlManager(object):

    def __init__(self):
        self.define = ['define', {}, []]  # name, data, children
        self.materials = ['materials', {}, []]
        self.solids = ['solids', {}, []]
        self.structure = ['structure', {}, []]
        self.__isotops = []
        self.__elements = []
        self.__materials = []

        self.created_materials = []
        self.created_elements = []

        self.world_sphere_min_halfx = 100
        self.max_world_r = 0
        self.world_volume_name = ''
        self.db = material_database.MaterialDatabase()

        self.document = [
            'gdml', {
                'xmlns:gdml':
                "http://cern.ch/2001/Schemas/GDML",
                'xmlns:xsi':
                "http://www.w3.org/2001/XMLSchema-instance",
                'xsi:noNamespaceSchemaLocation':
                "http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd"
            }, [self.define, self.materials, self.solids, self.structure]
        ]
        self.list_float_elem = ["x", "y", "z", "rmin", "rmax"]

        self.addDefaultValues()

    def addDefaultValues(self):
        self.addConstant('HALFPI', "pi/2")
        self.addConstant('PI', "1.0*pi")
        self.addConstant('TWOPI', "2.0*pi")
        self.addPosition('center', 0, 0, 0, "mm")
        self.addRotation('identity', 0, 0, 0, unit='deg')
        self.addMaterial("Galaxy", "H", 1, 1.0, 1e-25, unit="g/cm3")

    def processMaterial(self, mat):
        if mat in g4_materials.materials:
            self.freecadPrint('Default material: ' + mat)
        else:
            self.freecadPrint('Loading material ' + mat +
                              ' from database')
            self.addDatabaseMaterial(mat)

    def adddMaterial(self, name, density, componds, density_unit="g/cm3"):
        # componds

        elements = ['D', {'value': density, 'unit': density_unit}, []]
        elements.append(componds)

        self.materials[2].append(['material', {'name': name}, elements])

    def evaluateConstants(self):
        for element in self.define[2]:
            if element[0] == "constant":
                globals()[element[1]['name']] = eval(element[1]['value'])

    def addPolyhedraSolid(self, solid_name, faces):
        self.solids[2].append(['tessellated', {'name': solid_name}, faces])

    def addTesselatedSolid(self, name, triangles):
        nv = 0
        faces = []
        self.world_sphere_min_halfx = 100

        for v in triangles[0]:
            x = v[0]
            y = v[1]
            z = v[2]
            distance = math.sqrt(x * x + y * y + z * z)
            if distance > self.world_sphere_min_halfx:
                self.world_sphere_min_halfx = distance

            if distance > self.max_world_r:
                self.max_world_r = distance

            vertex_name = "__v_%s_%05d" % (name, nv)
            self.addPosition(vertex_name, x, y, z, "mm")
            nv += 1
        for tri in triangles[1]:
            face = []
            v1 = tri[0]
            vn1 = "__v_%s_%05d" % (name, v1)
            v2 = tri[1]
            vn2 = "__v_%s_%05d" % (name, v2)
            v3 = tri[2]
            vn3 = "__v_%s_%05d" % (name, v3)
            faces.append([
                'triangular', {
                    'vertex1': vn1,
                    'vertex2': vn2,
                    'vertex3': vn3,
                    'type': 'ABSOLUTE'
                }, []
            ])

        solid_name = '_sol_%s' % name
        self.solids[2].append(['tessellated', {'name': solid_name}, faces])
        return solid_name

    def getPartsMaxR(self):
        return self.max_world_r

    def addPosition(self, name, x, y, z, unit="cm"):
        self.define[2].append([
            'position', {
                'name': name,
                'x': x,
                'y': y,
                'z': z,
                'unit': unit
            }, []
        ])

    def addConstant(self, name, value):
        self.define[2].append(['constant', {'name': name, 'value': value}, []])

    def computeGDMLRotationAngleFromAxis(self, xaxis, yaxis, zaxis):

        xaxis0 = np.array([1., 0., 0.])
        yaxis0 = np.array([0., 1., 0.])
        zaxis0 = np.array([0., 0., 1.])
        # print "axis",xaxis,yaxis,zaxis
        xaxis3 = xaxis
        zaxis2 = zaxis
        yaxis3 = yaxis

        sin_ay = -np.dot(zaxis2, xaxis0)
        cos_ay = 0.
        phi = 0.
        cphi = 1.
        sphi = 0.
        if (abs(sin_ay) < 1.):
            phi = math.atan2(zaxis2[1], zaxis2[2])
            cphi = np.cos(phi)
            sphi = np.sin(phi)
            if (abs(cphi) > 0.00001):
                cos_ay = zaxis2[2] / cphi
            else:
                cos_ay = zaxis2[1] / sphi
        angle_y = math.atan2(sin_ay, cos_ay)
        xaxis2 = np.array([cos_ay, sin_ay * sphi, sin_ay * cphi])
        yaxis2 = np.array([0, cphi, -sphi])
        cos_az = np.dot(yaxis3, yaxis2)
        sin_az = -np.dot(yaxis3, zaxis2)
        angle_z = math.atan2(sin_az, cos_az)
        angle_x = phi
        return [angle_x, angle_y, angle_z]

    def addRotation(self, name, x, y, z, unit='deg'):
        self.define[2].append([
            'rotation', {
                'name': name,
                'x': x,
                'y': y,
                'z': z,
                'unit': unit
            }, []
        ])

    def addMaterialList(self, material_list):
        for key in material_list:
            mat_list = []
            mat_list.append(material_list[key])
            self.materials[2].append(mat_list)

    def addMaterial(self, name, formula, Z, atom, D, unit="g/cm3"):
        if name not in self.__materials:
            self.materials[2].append([
                'material', {
                    'name': name,
                    'Z': Z,
                    "formula": formula
                },
                [['D', {
                    'value': D,
                    'unit': unit
                }, []], ['atom', {
                    'value': atom
                }, []]]
            ])
            self.__materials.append(name)

    def material(self, name, formula, Z, atom, D, unit="g/cm3"):
        self.addMaterial(name, formula, Z, atom, D)
        return {'formula': formula, 'name': name, 'Z': Z, 'a': atom, 'D': D}

    def addMixture(self, name, rho, elems, unit="g/cm3"):
        subel = [['D', {'value': rho, 'unit': unit}, []]]
        for el in elems.keys():
            subel.append(['fraction', {'n': elems[el], 'ref': el}, []])
        self.materials[2].append(['material', {'name': name}, subel])

    def addComposite(self, name, rho, elems, unit="g/cm3"):
        subel = [['D', {'value': rho, 'unit': unit}, []]]
        for el in elems.keys():
            subel.append(['composite', {'n': elems[el], 'ref': el}, []])

        self.materials[2].append(['material', {'name': name}, subel])

    def addElement(self, name, symb, z, a):
        if name not in self.__elements:
            self.materials[2].append([
                'element', {
                    'name': name,
                    'formula': symb,
                    'Z': z
                }, [['atom', {
                    'value': a
                }, []]]
            ])
            self.__elements.append(name)

    def element(self, symb, name, z, a):
        self.addElement(name, symb, z, a)
        return {'formula': symb, 'name': name, 'Z': z, 'a': a}

    def addIsotope(self, name, Z, N, a):
        if name not in self.__isotops:
            self.materials[2].append([
                'isotope', {
                    'name': name,
                    'N': N,
                    'Z': Z
                }, [['atom', {
                    'value': a,
                    "type": "A"
                }, []]]
            ])
            self.__isotops.append(name)

    def addElements(self, name, isotopedict):
        if len(isotopedict) < 1:
            return False
        isotopes = []
        for reference, fraction in isotopedict.items():
            isotopes.append(
                ['fraction', {
                    'ref': reference,
                    'n': fraction
                }, []])
        self.materials[2].append(['element', {'name': name}, isotopes])

    def addDatabaseElement(self, elementName):
        if not self.db:
            return
        dbresults = self.db.getElements(elementName)
        isotopedict = dict()
        if not dbresults:
            return
        for item in dbresults:
            name, fraction, reference = item
            isotopedict[reference] = fraction
            self.addDatabaseIsotope(reference)
        self.addElements(elementName, isotopedict)

    def addDatabaseIsotope(self, reference):
        if not self.db:
            return
        iso = self.db.getIsotopes(reference)
        for row in iso:
            name, Z, A, mass, abundance = row
            self.addIsotope(name, Z, A, mass)

    def addDatabaseMaterial(self, mat_name):
        if not self.db:
            return
        iso = self.db.getMaterial(mat_name)
        if not iso:
            self.freecadPrint("No information for the material: " + mat_name)
            return
        name, frac_type, element_ref, fraction, Z, density = iso[0]
        if len(iso) == 1:
            if frac_type == 0 and Z > 0:
                self.addMaterial(name, '_' + name, Z, fraction, density)
                return
        if frac_type == 0:
            return

        elems = dict()

        for row in iso:
            name, frac_type, element_ref, fraction, Z, density = row
            if fraction > 0 and density > 0:
                if self.db.getElements(element_ref):
                    self.addDatabaseElement(element_ref)
                elif frac_type != 2:
                    self.addDatabaseMaterial(element_ref)
                elems[element_ref] = fraction

        if not elems:
            return
        if frac_type == 1:
            self.addMixture(name, density, elems)
        elif frac_type == 2:
            self.addComposite(name, density, elems)

    def removeAllMaterialsAndElements(self):
        for el in self.materials[2]:
            self.materials[2].remove(el)
        self.materials[2] = []

    def resetAll(self):
        for elem in self.document[2]:
            for i in range(len(elem[2])):
                del elem[2][-1]
        del self.document[2][-1]

    def addWorld(self, name='world', x=10000, y=1000, z=10000):
        self.addBox(name, x, y, z, "mm")
        return name

    def createWorldVolume(self,
                          x=10000,
                          y=10000,
                          z=10000,
                          world_mat='G4_Galactic'):
        if self.world_volume_name == "":
            solid_world = self.addWorld('__box_world__', x, y, z)
            self.world_volume_name = self.addVolume('world',
                                                    solid_world,
                                                    world_mat,
                                                    daughters=[])

        return self.world_volume_name

    def addBox(self, name, dx, dy, dz, lunit="cm"):
        self.solids[2].append([
            'box', {
                'name': name,
                'x': dx,
                'y': dy,
                'z': dz,
                'lunit': lunit
            }, []
        ])

    def box(self, name, dx, dy, dz, lunit="cm"):
        self.addBox(name, dx, dy, dz, lunit)
        return [dx, dy, dz]

    def addSphere(self,
                  name,
                  rmin,
                  rmax,
                  startphi,
                  deltaphi,
                  starttheta,
                  deltatheta,
                  lunit="cm",
                  aunit="deg"):
        self.solids[2].append([
            'sphere', {
                'name': name,
                'rmin': rmin,
                'rmax': rmax,
                'startphi': startphi,
                'deltaphi': deltaphi,
                'starttheta': starttheta,
                'deltatheta': deltatheta,
                'aunit': aunit,
                'lunit': lunit
            }, []
        ])

    def addCone(self,
                name,
                z,
                rmin1,
                rmin2,
                rmax1,
                rmax2,
                sphi,
                dphi,
                lunit="cm",
                aunit="deg"):
        self.solids[2].append([
            'cone', {
                'name': name,
                'z': z,
                'rmin1': rmin1,
                'rmin2': rmin2,
                'rmax1': rmax1,
                'rmax2': rmax2,
                'startphi': sphi,
                'deltaphi': dphi,
                'aunit': aunit,
                'lunit': lunit
            }, []
        ])

    def cone(self,
             name,
             rmin1,
             rmax1,
             rmin2,
             rmax2,
             z,
             sphi,
             dphi,
             lunit="cm",
             aunit="deg"):
        self.addCone(name, z, rmin1, rmin2, rmax1, rmax2, sphi, dphi, lunit,
                     aunit)
        return [rmin1, rmin2, rmax1, rmax2, sphi, dphi]

    def addPara(self, name, x, y, z, alpha, theta, phi):
        self.solids[2].append([
            'para', {
                'name': name,
                'x': x,
                'y': y,
                'z': z,
                'alpha': alpha,
                'theta': theta,
                'phi': phi
            }, []
        ])

    def addTrap(self, name, z, theta, phi, y1, x1, x2, alpha1, y2, x3, x4,
                alpha2):
        self.solids[2].append([
            'trap', {
                'name': name,
                'z': z,
                'theta': theta,
                'phi': phi,
                'x1': x1,
                'x2': x2,
                'x3': x3,
                'x4': x4,
                'y1': y1,
                'y2': y2,
                'alpha1': alpha1,
                'alpha2': alpha2
            }, []
        ])

    def addTrd(self, name, x1, x2, y1, y2, z):
        self.solids[2].append([
            'trd', {
                'name': name,
                'x1': x1,
                'x2': x2,
                'y1': y1,
                'y2': y2,
                'z': z
            }, []
        ])

    def addTube(self,
                name,
                rmin,
                rmax,
                z,
                startphi,
                deltaphi,
                lunit="cm",
                aunit="deg"):
        self.solids[2].append([
            'tube', {
                'name': name,
                'rmin': rmin,
                'rmax': rmax,
                'z': z,
                'startphi': startphi,
                'deltaphi': deltaphi,
                "aunit": aunit,
                "lunit": lunit
            }, []
        ])

    def tube(self,
             name,
             rmin,
             rmax,
             z,
             startphi,
             deltaphi,
             lunit="cm",
             aunit="deg"):
        self.addTube(name, rmin, rmax, z, startphi, deltaphi, lunit, aunit)
        return [rmin, rmax, z, startphi, deltaphi]

    def addPolycone(self, name, startphi, deltaphi, zplanes):
        zpls = []
        for zplane in zplanes:
            zpls.append([
                'zplane', {
                    'z': zplane[0],
                    'rmin': zplane[1],
                    'rmax': zplane[2]
                }, []
            ])
        self.solids[2].append([
            'polycone', {
                'name': name,
                'startphi': startphi,
                'deltaphi': deltaphi
            }, zpls
        ])

    def addTorus(self, name, r, rmin, rmax, startphi, deltaphi):
        self.solids[2].append([
            'torus', {
                'name': name,
                'rtor': r,
                'rmin': rmin,
                'rmax': rmax,
                'startphi': startphi,
                'deltaphi': deltaphi
            }, []
        ])

    def addPolyhedra(self, name, startphi, totalphi, numsides, zplanes):
        zpls = []
        for zplane in zplanes:
            zpls.append([
                'zplane', {
                    'z': zplane[0],
                    'rmin': zplane[1],
                    'rmax': zplane[2]
                }, []
            ])
        self.solids[2].append([
            'polyhedra', {
                'name': name,
                'startphi': startphi,
                'totalphi': totalphi,
                'numsides': numsides
            }, zpls
        ])

    def addEltube(self, name, x, y, z):
        self.solids[2].append(
            ['eltube', {
                'name': name,
                'x': x,
                'y': y,
                'z': z
            }, []])

    def addHype(self, name, rmin, rmax, inst, outst, z):
        self.solids[2].append([
            'hype', {
                'name': name,
                'rmin': rmin,
                'rmax': rmax,
                'inst': inst,
                'outst': outst,
                'z': z
            }, []
        ])

    def addXtru(self,
                name,
                xy_polygon,
                z_pos_vec,
                x_offset_vec,
                y_offset_vec,
                scaling_vec,
                unit="cm"):
        polygon_vertices = []
        for vertex in xy_polygon:
            polygon_vertices.append(
                ['twoDimVertex', {
                    'x': vertex[0],
                    'y': vertex[1]
                }, []])
        z_sections = []
        for i in range(len(z_pos_vec)):
            z = z_pos_vec[i]
            x_off = x_offset_vec[i]
            y_off = y_offset_vec[i]
            scaling = scaling_vec[i]
            z_sections.append([
                'section', {
                    'zOrder': i + 1,
                    'zPosition': z,
                    'xOffset': x_off,
                    'yOffset': y_off,
                    'scalingFactor': scaling
                }, []
            ])
        self.solids[2].append([
            'xtru', {
                'name': name,
                'lunit': unit
            }, polygon_vertices + z_sections
        ])

    def addPos(self, subels, type, name, v, unit="m"):
        if v[0] != 0.0 or v[1] != 0.0 or v[2] != 0.0:
            subels.append([
                type, {
                    'name': name,
                    'x': v[0],
                    'y': v[1],
                    'z': v[2],
                    'unit': unit
                }, []
            ])

    def addRot(self, subels, type, name, v, unit="deg"):
        if v[0] != 0.0 or v[1] != 0.0 or v[2] != 0.0:
            subels.append([
                type, {
                    'name': name,
                    'x': v[0],
                    'y': v[1],
                    'z': v[2],
                    'unit': unit
                }, []
            ])

    def addBoolean(self,
                   type_boolean,
                   name,
                   first_name,
                   second_name,
                   translation,
                   rotation,
                   lunit="cm",
                   aunit="deg"):
        subels = [['first', {
            'ref': first_name
        }, []], ['second', {
            'ref': second_name
        }, []]]
        self.addPos(subels, 'position', 'bool_pos_' + name, translation, lunit)
        self.addRot(subels, 'rotation', 'bool_rot_' + name, rotation, aunit)
        self.solids[2].append([type_boolean, {'name': name}, subels])

    def union(self, name, first, second, pos, rot):
        self.addBoolean("union", name, first, second, pos, rot)
        return [name, first, second, pos, rot]

    def subtraction(self, name, first, second, pos, rot):
        self.addBoolean("subtraction", name, first, second, pos, rot)
        return [name, first, second, pos, rot]

    def intersection(self, name, first, second, pos, rot):
        self.addBoolean("intersection", name, first, second, pos, rot)
        return [name, first, second, pos, rot]

    def moveFrontLast(self):
        if len(self.structure[2]) > 1:
            new_structure = self.structure[2][1:]
            new_structure.append(self.structure[2][0])
            self.structure[2] = new_structure

    def addVolume(self, volume, solid, material, daughters):
        subels = [['materialref', {
            'ref': material
        }, []], ['solidref', {
            'ref': solid
        }, []]]
        for child in daughters:
            subsubels = [['volumeref', {
                'ref': child[0]
            }, []], ['positionref', {
                'ref': child[1]
            }, []]]
            if child[2] != '':
                subsubels.append(['rotationref', {'ref': child[2]}, []])

            phys_vol_name = child[0]
            if len(child) >= 4:
                phys_vol_name = child[3]
            subels.append(['physvol', {'name': phys_vol_name}, subsubels])

        self.structure[2].append(['volume', {'name': volume}, subels])
        return volume

    def addPhysVolume(self,
                      mother_name,
                      log_vol_name,
                      phys_vol_name,
                      position_name,
                      rot_name=None):

        mother_vol = self.getLogicalVolume(mother_name)

        phys_vol_elem = [
            "physvol", {},
            [["volumeref", {
                "ref": log_vol_name
            }, []], ["positionref", {
                "ref": position_name
            }, []]]
        ]
        if (phys_vol_name is not None):
            phys_vol_elem[1]['name'] = phys_vol_name
        if (rot_name is not None):
            phys_vol_elem[2].append(["rotationref", {"ref": rot_name}, []])
        mother_vol[2].append(phys_vol_elem)

    '''
    def includePhysVolume(self, mother_name,phys_vol_name, file_name, position_name,rot_name=None):
        mother_vol=self.getLogicalVolume(mother_name)
        phys_vol_elem=["physvol",{},[["file",{"name":file_name},[]],
                                    ["positionref",{"ref":position_name},[]]]]
        if (phys_vol_name is not None):
            phys_vol_elem[1]['name']= phys_vol_name
        if (rot_name is not None):
            phys_vol_elem[2].append( ["rotationref",{"ref":rot_name},[]])
        mother_vol[2].append(phys_vol_elem)
    '''

    def includePhysVolume(self, mother_name, phys_vol_name, file_name, pos,
                          rot):

        position_name = "center"
        rot_name = "identity"

        if pos:
            position_name = pos['name']
            self.addPosition(position_name, pos['x'], pos['y'], pos['z'],
                             pos['unit'])
        if rot:
            rot_name = rot['name']
            self.addRotation(rot_name, rot['x'], rot['y'], rot['z'],
                             rot['unit'])

        mother_vol = self.getLogicalVolume(mother_name)
        phys_vol_elem = [
            "physvol", {},
            [["file", {
                "name": file_name
            }, []], ["positionref", {
                "ref": position_name
            }, []]]
        ]
        if (phys_vol_name is not None):
            phys_vol_elem[1]['name'] = phys_vol_name
        if (rot_name is not None):
            phys_vol_elem[2].append(["rotationref", {"ref": rot_name}, []])
        mother_vol[2].append(phys_vol_elem)

    def insertVolume(self, volume, solid, material, daughters, index=0):
        # print volume, solid, material, daughters
        subels = [['materialref', {
            'ref': material
        }, []], ['solidref', {
            'ref': solid
        }, []]]
        for child in daughters:
            subsubels = [['volumeref', {
                'ref': child[0]
            }, []], ['positionref', {
                'ref': child[1]
            }, []]]
            if child[2] != '':
                subsubels.append(['rotationref', {'ref': child[2]}, []])

            phys_vol_name = child[0]
            if len(child) >= 4:
                phys_vol_name = child[3]
            subels.append(['physvol', {'name': phys_vol_name}, subsubels])

        self.structure[2].insert(index, ['volume', {'name': volume}, subels])

    def logvolume(self, name, solid, medium):
        self.last_volume = [name, solid, medium]
        self.daugthers = []
        return [name, solid, medium]

    def physvolume(self, lv_ref, pos_ref, rot_ref, phys_name):

        self.daugthers += [[lv_ref, pos_ref, rot_ref, phys_name]]

    def processVolume(self):
        volume = self.last_volume[0]
        solid = self.last_volume[1]
        material = self.last_volume[2]
        daughters = self.daugthers
        self.addVolume(volume, solid, material, daughters)

    def addSetup(self, name, version, world):
        world_name = '__setup__%s' % name
        self.document[2].append([
            'setup', {
                'name': world_name,
                'version': version
            }, [['world', {
                'ref': world
            }, []]]
        ])
        return world_name

    def writeFile(self, file_name):
        gdml_file = open(file_name, 'w')

        offset = ''

        def writeElement(elem, offset):
            offset = offset + '  '
            gdml_file.write(offset + '<%s' % (elem[0]))
            ordered_keys = []
            try:
                ordered_keys = np.sort(elem[1].keys())
            except BaseException:
                ordered_keys = elem[1].keys()
            for attr in ordered_keys:
                if attr in self.list_float_elem:
                    gdml_file.write(' %s="%.6e"' %
                                    (attr, float(elem[1][attr])))
                else:
                    gdml_file.write(' %s="%s"' % (attr, elem[1][attr]))
            # if elem[2].__len__() > 0:
            if len(elem[2]) > 0:
                gdml_file.write('>\n')
                for subel in elem[2]:
                    writeElement(subel, offset)

                gdml_file.write(offset + '</%s>\n' % (elem[0]))
            else:
                gdml_file.write('/>\n')

        gdml_file.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
        creator_info = '''<!--  Created by Freecad g4cad workbench (https://github.com/drhlxiao/g4cad) at  %s.-->\n    ''' % time.strftime(
            '%c')
        gdml_file.write(creator_info)
        writeElement(self.document, '')
        gdml_file.write(creator_info)
        gdml_file.close()

    def getXmlElement(self, mother_elem, type, element_name=None):
        for ele in mother_elem[2]:
            if ele[0] == type:
                if element_name is not None:
                    if ele[1]['name'] == element_name:
                        return ele
                else:
                    return ele
        return None

    def removeElement(self, mother_elem, type, element_name):
        i = 0
        for ele in mother_elem[2]:
            if ele[0] == type and 'name' in ele[1]:
                if ele[1]['name'] == element_name:
                    del mother_elem[2][i]
                    return True
            i += 1
        return False

    def getAttributeValue(self, element, attr_name, default=None):
        if attr_name in element[1]:
            return element[1][attr_name]
        return default

    def setAttributeValue(self, element, attr_name, attr_val):
        if attr_name in element[1]:
            element[1][attr_name] = attr_val

    def addAttribute(self, element, attr_name, attr_val):
        if attr_name not in element[1]:
            element[1][attr_name] = attr_val

    def getPosition(self, name):
        posElem = self.getXmlElement(self.define, 'position', name)
        if (posElem is not None):
            unit = eval(self.getAttributeValue(posElem, 'unit', 'mm'))
            x = eval(self.getAttributeValue(posElem, 'x', 0.)) * unit
            y = eval(self.getAttributeValue(posElem, 'y', 0.)) * unit
            z = eval(self.getAttributeValue(posElem, 'z', 0.)) * unit
            return np.array([x, y, z])
        return None

    def getRotation(self, name):
        rotElem = self.getXmlElement(self.define, 'rotation', name)
        if (rotElem is not None):
            unit = eval(self.getAttributeValue(rotElem, 'unit', 'deg'))
            x = float(self.getAttributeValue(rotElem, 'x', 0.)) * unit
            y = float(self.getAttributeValue(rotElem, 'y', 0.)) * unit
            z = float(self.getAttributeValue(rotElem, 'z', 0.)) * unit
            return np.array([x, y, z])
        return None

    def removePosition(self, name):
        return self.removeElement(self.define, 'position', name)

    def removeRotation(self, name):
        return self.removeElement(self.define, 'rotation', name)

    def changePosition(self, name, pos):
        posElem = self.getXmlElement(self.define, 'position', name)
        if (posElem is not None):
            unit = eval(self.getAttributeValue(posElem, 'unit', 'mm'))
            posElem[1]['x'] = pos[0] / unit
            posElem[1]['y'] = pos[1] / unit
            posElem[1]['z'] = pos[2] / unit

    def changeRotation(self, name, rot):
        rotElem = self.getXmlElement(self.define, 'rotation', name)
        if (rotElem is not None):
            unit = eval(self.getAttributeValue(rotElem, 'unit', 'deg'))
            rotElem[1]['x'] = rot[0] / unit
            rot[1]['y'] = rot[1] / unit
            rot[1]['z'] = rot[2] / unit

    def translatePosition(self, name, trans):
        pos = self.getPosition(name)
        if (pos is not None):
            self.changePosition(name, pos + trans)

    def removeVolume(self, name):
        list_to_remove = []
        for vol in self.structure[2]:
            name_vol = self.getAttributeValue(vol, "name")
            if name == name_vol:
                list_to_remove += [vol]
            phys_list_to_remove = []
            for elem in vol[2]:
                if elem[0] == "physvol":
                    name_phys_vol = self.getAttributeValue(elem, "name")
                    if name_phys_vol is None:
                        for subelem in elem[2]:
                            if subelem[0] == 'volumeref':
                                name_phys_vol = self.getAttributeValue(
                                    subelem,
                                    'ref',
                                )
                    if name_phys_vol == name:
                        phys_list_to_remove += [elem]
            for phys_vol in phys_list_to_remove:
                vol[2].remove(phys_vol)
        for vol in list_to_remove:
            self.structure[2].remove(vol)

    def removeVolumeAndRelatives(self, name):
        self.removeRotationVolume(name)
        self.removePositionVolume(name)
        self.removeSolidOfPhysVolume(name)
        list_to_remove = []
        for vol in self.structure[2]:
            name_vol = self.getAttributeValue(vol, "name")
            if name == name_vol:
                list_to_remove += [vol]
            phys_list_to_remove = []
            for elem in vol[2]:
                if elem[0] == "physvol":
                    name_phys_vol = self.getAttributeValue(elem, "name")
                    name_log_vol = None
                    for subelem in elem[2]:
                        if subelem[0] == 'volumeref':
                            name_log_vol = self.getAttributeValue(
                                subelem,
                                'ref',
                            )
                    if (name_phys_vol is None):
                        name_phys_vol = name_log_vol
                    if name_phys_vol == name:
                        phys_list_to_remove += [elem]
                        log_vol = self.getLogicalVolume(name_log_vol)
                        if log_vol not in list_to_remove:
                            list_to_remove += [log_vol]

            for phys_vol in phys_list_to_remove:
                vol[2].remove(phys_vol)
        for vol in list_to_remove:
            if vol in self.structure[2]:
                self.structure[2].remove(vol)
        self.removeRotationVolume(name)

    def getListPhysVolumeNamesInG4(self):
        list_vol_name = []
        for vol in self.structure[2]:
            for elem in vol[2]:
                if elem[0] == "physvol":
                    name_phys_vol = self.getAttributeValue(elem, "name")
                    if name_phys_vol is None:
                        for subelem in elem[2]:
                            if subelem[0] == 'volumeref':
                                name_phys_vol = self.getAttributeValue(
                                    subelem, 'ref') + "_PV"
                    list_vol_name += [name_phys_vol]
        return list_vol_name

    def getListPhysVolumeNames(self):
        list_vol_name = []
        for vol in self.structure[2]:
            for elem in vol[2]:
                if elem[0] == "physvol":
                    name_phys_vol = self.getAttributeValue(elem, "name")
                    if name_phys_vol is None:
                        for subelem in elem[2]:
                            if subelem[0] == 'volumeref':
                                name_phys_vol = self.getAttributeValue(
                                    subelem, 'ref')
                    list_vol_name += [name_phys_vol]
        return list_vol_name

    def getNamePositionVolume(self, name_vol):
        for vol in self.structure[2]:
            for elem in vol[2]:
                if elem[0] == "physvol":
                    name_phys_vol = self.getAttributeValue(elem, "name", None)
                    pname = None
                    for subelem in elem[2]:
                        if subelem[0] == 'volumeref' and name_phys_vol is None:
                            name_phys_vol = self.getAttributeValue(
                                subelem, 'ref')
                        if subelem[0] == 'positionref':
                            pname = self.getAttributeValue(subelem, 'ref')
                    if name_phys_vol == name_vol and pname is not None:
                        return pname
        return None

    def changePositionVolume(self, name, pos):
        name_pos = self.getNamePositionVolume(name)
        if (name_pos is not None):
            self.changePosition(name_pos, pos)

    def getPositionVolume(self, name):
        name_pos = self.getNamePositionVolume(name)

        if (name_pos is not None):
            return self.getPosition(name_pos)
        else:
            pos = None
            for vol in self.structure[2]:
                for elem in vol[2]:
                    if elem[0] == "physvol":
                        name_phys_vol = self.getAttributeValue(
                            elem, "name", None)
                        pos = None
                        for subelem in elem[2]:
                            if subelem[
                                    0] == 'volumeref' and name_phys_vol is None:
                                name_phys_vol = self.getAttributeValue(
                                    subelem, 'ref')
                            if subelem[0] == 'position':
                                unit = eval(
                                    self.getAttributeValue(
                                        subelem, 'unit', 'mm'))
                                x = eval(
                                    self.getAttributeValue(subelem, 'x',
                                                           0.)) * unit
                                y = eval(
                                    self.getAttributeValue(subelem, 'y',
                                                           0.)) * unit
                                z = eval(
                                    self.getAttributeValue(subelem, 'z',
                                                           0.)) * unit
                                pos = np.array([x, y, z])

                        if name_phys_vol == name and pos is not None:
                            return pos

        return None

    def removePositionVolume(self, name):
        name_pos = self.getNamePositionVolume(name)
        if name_pos is not None:
            return self.removePosition(name_pos)
        return False

    def getRotationVolume(self, name):
        name_rot = None
        for vol in self.structure[2]:
            for elem in vol[2]:
                if elem[0] == "physvol":
                    name_phys_vol = self.getAttributeValue(elem, "name")
                    rname = None
                    for subelem in elem[2]:
                        if subelem[0] == 'volumeref' and name_phys_vol is None:
                            name_phys_vol = self.getAttributeValue(
                                subelem, 'ref')
                        if subelem[0] == 'rotationref':
                            rname = self.getAttributeValue(subelem, 'ref')
                    if name_phys_vol == name and rname is not None:
                        name_rot = rname
        if name_rot is not None:
            return self.getRotation(name_rot)
        return None

    def removeRotationVolume(self, name):
        name_rot = None
        for vol in self.structure[2]:
            for elem in vol[2]:
                if elem[0] == "physvol":
                    name_phys_vol = self.getAttributeValue(elem, "name")
                    rname = None
                    for subelem in elem[2]:
                        if subelem[0] == 'volumeref' and name_phys_vol is None:
                            name_phys_vol = self.getAttributeValue(
                                subelem, 'ref')
                        if subelem[0] == 'rotationref':
                            rname = self.getAttributeValue(subelem, 'ref')
                    if name_phys_vol == name and rname is not None:
                        name_rot = rname
        if name_rot is not None:
            return self.removeRotation(name_rot)
        return False

    def getLogicalVolumeName(self, phys_vol_name):
        for vol in self.structure[2]:
            for elem in vol[2]:
                if elem[0] == "physvol":
                    name_phys_vol = self.getAttributeValue(elem, "name")
                    log_name = None
                    for subelem in elem[2]:
                        if subelem[0] == 'volumeref':
                            log_name = self.getAttributeValue(subelem, 'ref')
                    if name_phys_vol is None:
                        name_phys_vol = log_name
                    if name_phys_vol == phys_vol_name:
                        return log_name
        return None

    def removeSolid(self, solid_name):
        i = 0
        for vol in self.solids[2]:
            name = self.getAttributeValue(vol, "name")
            if name == solid_name:
                del self.solids[2][i]
                return True
            i += 1
        return False

    def getLogicalVolume(self, vol_name):
        for vol in self.structure[2]:
            name = self.getAttributeValue(vol, "name")
            if name == vol_name:
                return vol
        return None

    def getSolid(self, solid_name):
        for vol in self.solids[2]:
            name = self.getAttributeValue(vol, "name")
            if name == solid_name:
                return vol
        return None

    def getSolidOfPhysVolume(self, phys_vol_name):
        """
        get solid physical name
        """
        logical_volume_name = self.getLogicalVolumeName(phys_vol_name)
        if logical_volume_name is not None:
            solid_name = None
            for vol in self.structure[2]:
                name = self.getAttributeValue(vol, "name")
                if name == logical_volume_name and solid_name is None:
                    for elem in vol[2]:
                        if elem[0] == "solidref":
                            solid_name = self.getAttributeValue(elem, "ref")
            if solid_name is not None:
                return self.getSolid(solid_name)

    def removeSolidOfPhysVolume(self, phys_vol_name):
        logical_volume_name = self.getLogicalVolumeName(phys_vol_name)
        if logical_volume_name is not None:
            solid_name = None
            for vol in self.structure[2]:
                name = self.getAttributeValue(vol, "name")
                if name == logical_volume_name and solid_name is None:
                    for elem in vol[2]:
                        if elem[0] == "solidref":
                            solid_name = self.getAttributeValue(elem, "ref")
            if solid_name is not None:
                return self.removeSolid(solid_name)
        return False

    def setMaterialOfPhysVolume(self, phys_vol_name, material_name):
        logical_volume_name = self.getLogicalVolumeName(phys_vol_name)

        if logical_volume_name is not None:
            volElem = self.getXmlElement(self.structure, 'volume',
                                         logical_volume_name)
            for subelem in volElem[2]:
                if subelem[0] == 'materialref':
                    subelem[1]['ref'] = material_name
                    return True
        return False

    def getMaterialDensity(self, mat_name):
        mat_elem = self.getXmlElement(self.materials, "material", mat_name)
        if mat_elem is not None:
            dens_elem = self.getXmlElement(mat_elem, "D")
            unit = eval(self.getAttributeValue(dens_elem, "unit", "g/cm3"))
            density = float(dens_elem[1]["value"]) * unit
            return density
        return None

    def freecadPrint(self, msg):
        FreeCAD.Console.PrintMessage(msg + '\n')
