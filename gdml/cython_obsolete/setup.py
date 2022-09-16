from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
ext_modules = cythonize("src/*.pyx")
# [
#        Extension("GDML.*",["GDML/*.pyx"]),
#        #Extension("Elements",["GDML/Elements.pyx"])
#        ]
setup(
    name="GDML",
    #cmdclass = {'build_ext': build_ext},
    ext_modules=ext_modules
)
