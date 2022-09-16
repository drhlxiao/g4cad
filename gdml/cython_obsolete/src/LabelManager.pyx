# -*- coding: utf-8 -*-
"""
Created on Fri Aug 1 11:12:45 2017

@author: Hualin Xiao (hualin.xiao@psi.ch)

Material database interface
"""

import ast
import re


def getSafeFilename(filename):
    return ''.join(ch for ch in filename if ch.isalnum())

class LabelManager:
    def __init__(self):
        self._material=''
        self._precision=0
        self._prefix=''
        self._physical_volume=''


    def parse(self,label):
        try:
            self._prefix=label.split('{')[0]
            data={}

            ret=re.findall(r"\{.*?\}",label)
            if ret:
                aux=ret[0]
                data=ast.literal_eval(aux)

            self._material=data.get('mat','')
            self._precision=data.get('tol',0)
            self._physical_volume=data.get('pv','')
        except:
            pass


    def getLabel(self,label):
        self.parse(label)
        return self._prefix
    def getFilenameFromLabel(self,label):
        self.parse(label)
        return  getSafeFilename(self._prefix)


    def getMaterial(self):
        return self._material
    def getPrecision(self):
        return self._precision
    def getPhysicalVolume(self):
        return self._physical_volume

    def setMaterial(self,mat):
        self._material=mat
    def setPrecision(self,pre):
        self._precision=pre

    def setPhysicalVolue(self,sd):
        self._physical_volume=sd

    def formatLabel(self):
        aux_info=''
        if self._material:
            aux_info+="'mat':'%s'"%self._material
        if self._precision>0:
            if aux_info<>'':
                aux_info+=','
            aux_info+="'tol':%f"%self._precision
        if self._physical_volume:
            if aux_info<>'':
                aux_info+=','
            aux_info+="'pv':'%s'"%self._physical_volume

        if not aux_info:
            return self._prefix
        else:
            return "%s{%s}"%(self._prefix,aux_info)

    def updateMaterial(self,label,mat):
        self.parse(label)
        self.setMaterial(mat)
        return self.formatLabel()

    def updatePhysicalVolume(self,label,sd):
        self.parse(label)
        self.setPhysicalVolue(sd)
        return self.formatLabel()

    def updatePrecision(self,label,pre):
        self.parse(label)
        self.setPrecision(pre)
        return self.formatLabel()

    def updateMatPcs(self,label,mat,pre):
        self.parse(label)
        self.setMaterial(mat)
        self.setPrecision(pre)
        return self.formatLabel()
        






if __name__=="__main__":

    pl=LabelManager()
    print pl.updatePhysicalVolume("HAS_sensor","sensor")
    print pl.updateMaterial("HAS_sensor{'pv':'sensor'}","G4_Si")
    print pl.updatePrecision("HAS_sensor",0.1)

