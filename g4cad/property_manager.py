# -*- coding: utf-8 -*-
"""
Created on Fri Sept 19 11:12:45 2022

@author: Hualin Xiao (hualin.xiao@se2s.ch)

Material database interface
"""

import FreeCAD


class PropertyManager:
    default_tollerance = 0.1
    default_material = 'G4_Al'

    @classmethod
    def updatePropertyString(self, obj, prop, new_value):
        try:
            setattr(obj, prop, new_value)
            return
        except AttributeError:
            pass
        try:
            obj.addProperty("App::PropertyString", prop)
            setattr(obj, prop, new_value)
        except Exception as e:
            FreeCAD.Console.PrintWarning(str(e))

    @classmethod
    def updatePropertyFloat(self, obj, prop, new_value):
        try:
            new_value = float(new_value)
        except TypeError:
            FreeCAD.Console.PrintWarning('Failed to change the property ' +
                                         pro + '! Invalid value:' + toll)
            return
        try:
            setattr(obj, prop, new_value)
            return
        except AttributeError:
            pass

        try:
            obj.addProperty("App::PropertyFloat", prop)
            setattr(obj, prop, new_value)
        except Exception as e:
            FreeCAD.Console.PrintWarning(str(e))

    @classmethod
    def getProperty(self, obj, prop, _id=0):
        try:
            return getattr(obj, prop)
        except AttributeError:
            if prop == 'Material':
                return PropertyManager.default_material
            elif prop == 'Tolerance':
                return PropertyManager.default_tollerance
            elif prop == 'Physical_Volume':
                return '__phys_%d' % _id
