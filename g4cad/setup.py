import glob
from distutils.core import setup
from distutils.extension import Extension
import os
from Cython.Distutils import build_ext

py_files = glob.glob('source/*py')
modules = [os.path.splitext(os.path.basename(x))[0] for x in py_files]
ext_modules = []
excluded = ['InitGui', 'Elements']
for module, fname in zip(modules, py_files):
    if module not in excluded:
        ext_modules.append(Extension(module, [fname]))

setup(name='Gdml', cmdclass={'build_ext': build_ext}, ext_modules=ext_modules)
# python3 setup.py build_ext --inplace
