from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
files=["G4Materials.py",
"GdmlExporter.py",
"GdmlImporter.py",
"GdmlInit.py",
"GdmlSheet.py",
"GdmlWriter.py",
"HepUnit.py",
"InitGui.py",
"__init__.py",
"LabelManager.py",
"MaterialDatabaseGui.py",
"MaterialDatabase.py",
"MaterialExporter.py",
"MaterialManagerGui.py",
"MaterialSelectionDialog.py",
"SimDiag.py",
"SimManagerGui.py",
"sim.py",
"SimulationRunManager.py",
"utils.py"]
import os
ext_modules = [Extension(os.path.splitext(i)[0],  [i]) for i in files ]
setup(
    name = 'GdmlExporterAndWriter',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
