# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 11:12:45 2017

@author: Hualin Xiao (hualin.xiao@psi.ch)
"""

import os
import sys
import json
import webbrowser
import elements


class MaterialDatabase(object):

    def __init__(self):
        self._data = None
        self._databaseFilename = ''
        self.loadDatabase()

    def getScriptDir(self):
        dn = os.path.dirname(os.path.realpath(__file__))
        return dn

    def edit(self):
        editor = os.getenv('EDITOR')
        if editor:
            os.system(editor + ' ' + self._databaseFilename)
        else:
            webbrowser.open(self._databaseFilename)

    def loadDatabase(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        dirs = [
            current_path,
            os.path.expanduser("~") + '/.FreeCAD', '{}/db'.format(current_path)
        ]
        for d in dirs:
            filename = '%s/user_materials.json' % d
            with open(filename) as f:
                self._data = json.load(f)
                if self._data:
                    self._databaseFilename = filename
                    return

    @property
    def userMaterials(self):
        return self._data

    def getMaterialList(self):
        try:
            matlist = [e['name'] for e in self._data]
            return matlist
        except BaseException:
            return []

    def getMaterial(self, name):
        matlist = []
        for e in self._data:
            if e['name'] == name:
                for c in e['data']['compositions']:
                    frac_type = 1
                    # mass fraction
                    if c['frac'] >= 1:
                        # composite
                        #
                        frac_type = 2
                    matlist.append([
                        name, frac_type, c['ref'], c['frac'], 0,
                        e['data']['density']
                    ])
        return matlist

    def getElements(self, reference):
        return elements.getElements(reference)

    def getIsotopes(self, reference):
        return elements.getIsotopes(reference)

    def getMaterialListbyNames(self, namelist):
        jlist = []
        for name in namelist:
            try:
                mat = self.getMaterial(name)
                js = dict()
                density = mat[0][5]
                ty = mat[0][1]
                comp = []
                for m in mat:
                    comp.append({'ref': m[2], 'frac': m[3]})
                js = {
                    "name": name,
                    "density": density,
                    "unit": "g/cm3",
                    "type": ty,
                    "compositions": comp
                }
                jlist.append(js)
            except BaseException:
                pass

        return jlist


if __name__ == "__main__":
    # test database
    db = MaterialDatabase()
    matlist = [
        "HPM1801", "BKG7G18", "PCB_FR4", "Al2O3", "Ti6Al4V", "F2G12",
        "Alu5A06", "PMMA"
    ]
    db.edit()
