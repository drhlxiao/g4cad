# -*- coding: utf-8 -*-
"""

Created on Wed Jul 18 18:09:41 2018

@author: Hualin Xiao
"""

import FreeCAD
import Spreadsheet


class GdmlSheet:
    def __init__(self):
        self.doc = None
        self.sp = None
        self.row = 1

    def createNewSheet(self, name):
        if self.sp:
            self.sp.clearAll()
            return self.sp

        if FreeCAD.ActiveDocument:
            self.doc = FreeCAD.ActiveDocument
            self.sp = self.doc.getObject(name)
            if self.sp:
                self.sp.clearAll()
            else:
                self.sp = self.doc.addObject('Spreadsheet::Sheet', name)
            return self.sp
        else:
            return None

    def append(self, *args, **kwargs):
        if not self.sp:
            return False
        alphab = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i, arg in enumerate(args):
            self.sp.set('{}{}' .format(alphab[i], self.row), str(arg))

        self.row += 1

        return True
