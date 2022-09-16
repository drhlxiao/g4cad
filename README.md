# g4cad   - A freecad plugin which allows exporting CAD files to geant4 gdml files

People usually spend most of the time developing mass model when developing a Geant4-based Monte Carlo simulation package. For simple geometries, it is relatively easy to describe them using CGS models. 
However, this becomes almost impossible for complex geometries. 
G4cad is a workbench for FreeCAD, which is a general-purpose parametric 3D computer-aided design (CAD) modeler. Its features include

* Material management.  Users can define their own materials and set the predefined materials for different solids 
* Adding simple CGS models to existing CAD models
* Users can define the physical volume names for a solid
* Users can define tessellation tolerance for each individual solid
* Convert models to gdml files
* providing various tools for converting cad models to gdml files, like  measuring tools, tool to remove small parts

### Installation
1) Download g4cad https://github.com/drhlxiao/g4cad/archive/refs/heads/main.zip
2) Unzip the downloaded zip file
3) find the folder g4cad in unzipped folder, copy it to FreeCAD workbench directory (~/.FreeCAD/Mode on Linux)

![g4cad workbench](./tests/g4cad.png)
![converted model in g4](./tests/model_in_g4.png  )

