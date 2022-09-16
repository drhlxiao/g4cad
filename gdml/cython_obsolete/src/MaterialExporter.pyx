# -*- coding: utf-8 -*-
'''
Print all materials in the database to  a csv file
@author: Hualin Xiao
@date: Dec. 08, 2017
'''

import MaterialDatabase
import xlwt


def export_material():
    db=MaterialDatabase.MaterialDatabase()
    print 'available material:'
    mats=db.getMaterialList()
    bk=xlwt.Workbook()
    sheet=bk.add_sheet('materials')


    row=sheet.row(0)
    cols=['material','Type','Element','fraction', 'Z','density (g/cm3)']
    for nn, col in enumerate(cols):
        row.write(nn,col)
    
    nrow=1
    for mat_name in mats:
        print 'getting:', mat_name
        mat=db.getMaterial(mat_name)
        for n,ref in enumerate(mat):
            if n > 0:
                ref[0]=''
                ref[-1]=''
            row=sheet.row(nrow)
            nrow+=1
            for ncol,e in enumerate(ref):
                row.write(ncol,e)
            line=','.join(str(e) for e in ref)
            print line
    bk.save('db/user_materials_from_db.xls')





if __name__=="__main__":
    export_material()
