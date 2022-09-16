# -*- coding: utf-8 -*-
"""

Created on Wed Jul 18 18:09:41 2018

@author: Hualin Xiao

"""


import FreeCAD
import Spreadsheet

class GdmlSheet:
    def __init__(self):
        self.doc=None
        self.sp=None
        self.row=1

    def createNewSheet(self,name):
        if self.sp:
            self.sp.clearAll()
            return self.sp
            
        if FreeCAD.ActiveDocument:
            self.doc=FreeCAD.ActiveDocument
            self.sp=self.doc.getObject(name)
            if self.sp:
                self.sp.clearAll()
            else:
                self.sp=self.doc.addObject('Spreadsheet::Sheet',name)
            return self.sp
        else:
            return None



    def append(self,name,value):
        if not self.sp:
            return False
        else:
            self.sp.set('A%d'%self.row,str(name))
            self.sp.set('B%d'%self.row,str(value))
            self.row+=1
            return True
    def append(self,a,b,c,d,e):
        if not self.sp:
            return False
        else:
            self.sp.set('A%d'%self.row,str(a))
            self.sp.set('B%d'%self.row,str(b))
            self.sp.set('C%d'%self.row,str(c))
            self.sp.set('D%d'%self.row,str(d))
            self.sp.set('E%d'%self.row,str(e))
            self.row+=1

    def append(self,a,b,c,d,e,f):
        if not self.sp:
            return False
        else:
            self.sp.set('A%d'%self.row,str(a))
            self.sp.set('B%d'%self.row,str(b))
            self.sp.set('C%d'%self.row,str(c))
            self.sp.set('D%d'%self.row,str(d))
            self.sp.set('E%d'%self.row,str(e))
            self.sp.set('F%d'%self.row,str(f))
            self.row+=1
            return True

        
        

        

