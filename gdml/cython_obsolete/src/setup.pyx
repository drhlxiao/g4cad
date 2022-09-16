from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [
        Extension("utils",["utils.py"]),
        Extension("G4Materials",["G4Materials.py"]),
        Extension("GdmlExporter",["GdmlExporter.py"]),
        Extension("GdmlImporter",["GdmlImporter.py"]),
        Extension("GdmlInit",["GdmlInit.py"]),
        Extension("GdmlSheet",["GdmlSheet.py"]),
        Extension("GdmlWriter",["GdmlWriter.py"]),
        Extension("LabelManager",["LabelManager.py"]),
        Extension("MaterialDatabaseJSON",["MaterialDatabaseJSON.py"]),
        Extension("MaterialDatabase",["MaterialDatabase.py"]),
        Extension("MaterialDatabaseYmal",["MaterialDatabaseYmal.py"]),
        Extension("MaterialExporter",["MaterialExporter.py"]),
        Extension("MaterialManagerGui",["MaterialManagerGui.py"]),
        Extension("MaterialSelectionDialog",["MaterialSelectionDialog.py"]),
        Extension("MeasurementGui",["MeasurementGui.py"])#,
        #Extension("Elements",["Elements.py"])
        ]
setup(
        name = "DML",
        cmdclass = {'build_ext': build_ext},
        ext_modules = ext_modules
        )
