from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [
    Extension("utils", ["utils.pyx"]),
    Extension("G4Materials", ["G4Materials.pyx"]),
    Extension("GdmlExporter", ["GdmlExporter.pyx"]),
    Extension("GdmlImporter", ["GdmlImporter.pyx"]),
    Extension("GdmlInit", ["GdmlInit.pyx"]),
    Extension("GdmlSheet", ["GdmlSheet.pyx"]),
    Extension("GdmlWriter", ["GdmlWriter.pyx"]),
    Extension("LabelManager", ["LabelManager.pyx"]),
    Extension("MaterialDatabaseJSON", ["MaterialDatabaseJSON.pyx"]),
    Extension("MaterialDatabase", ["MaterialDatabase.pyx"]),
    Extension("MaterialDatabaseYmal", ["MaterialDatabaseYmal.pyx"]),
    Extension("MaterialExporter", ["MaterialExporter.pyx"]),
    Extension("MaterialManagerGui", ["MaterialManagerGui.pyx"]),
    Extension("MaterialSelectionDialog", ["MaterialSelectionDialog.pyx"]),
    Extension("MeasurementGui", ["MeasurementGui.pyx"]),
    Extension("utils", ["utils.pyx"]),
]
# Extension("G4Materials",["G4Materials.pyx"]),
# Extension("GdmlExporter",["GdmlExporter.pyx"]),
# Extension("GdmlImporter",["GdmlImporter.pyx"]),
# Extension("GdmlInit",["GdmlInit.pyx"]),
# Extension("GdmlSheet",["GdmlSheet.pyx"]),
# Extension("GdmlWriter",["GdmlWriter.pyx"]),
# Extension("LabelManager",["LabelManager.pyx"]),
# Extension("MaterialDatabaseJSON",["MaterialDatabaseJSON.pyx"]),
# Extension("MaterialDatabase",["MaterialDatabase.pyx"]),
# Extension("MaterialDatabaseYmal",["MaterialDatabaseYmal.pyx"]),
# Extension("MaterialExporter",["MaterialExporter.pyx"]),
# Extension("MaterialManagerGui",["MaterialManagerGui.pyx"]),
# Extension("MaterialSelectionDialog",["MaterialSelectionDialog.pyx"]),
# Extension("MeasurementGui",["MeasurementGui.pyx"])#,
# Extension("Elements",["Elements.pyx"])
# ]
setup(
    name="GDML",
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
