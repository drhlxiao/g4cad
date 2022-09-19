[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7085915.svg)](https://doi.org/10.5281/zenodo.7085915)
# G4CAD   - A FreeCAD workbench for converting CAD files to GDML 

Physicists usually spend most of the time developing mass model when developing a Geant4-based Monte Carlo simulation package. For simple geometries, it is relatively easy to describe them using CGS models. 
However, this becomes almost impossible for complex geometries. 
G4cad is a free, open source workbench for FreeCAD. Its features include

* Material management.  Users can define their own materials and set the predefined materials for different solids 
* Adding simple CGS models to existing CAD models
* Users can define the physical volume names for a solid
* Users can define tessellation tolerance for each individual solid
* Convert models to gdml files
* providing various tools useful for converting CAD models to gdml, like  measuring tools, tool to remove small parts

We also developed a web version, which can be found at the link http://polar.psi.ch/cadmc/

### Requirements
 Tested with FreeCAD 0.19, on both Ubuntu and Windows，  should also work with Freecad v0.16, v0.17 and v0.18



### Installation
1) Download g4cad https://github.com/drhlxiao/g4cad/archive/refs/heads/main.zip
2) Unzip the downloaded zip file
3) find the folder g4cad in unzipped folder, copy it to FreeCAD workbench directory (~/.FreeCAD/Mod on Linux, and <FREECAD_INSTALLATION_PATH>/Mod on windows)



### Typical Workflow
1) Activate the workbench "g4cad" in FreeCAD (view->Workbench->g4cad)
2) Open the step file to be converted 
3) click the icon "add world volume" in the toolbar to add a world volume 
4) Select a solid, set material
5) If the material you want is not in the list, open the user_materials.json with a text editor, add the information of the material
6) Select the solids to be exported
7) click the icon "Export solids to gdml files" to generate gdml files
8) If everything goes well, the gdml files are written to gdml/ in the specified folder and a log file can also be found in the folder.  
9) Reading gdml files in Geant4

Here is a code snippet 
```cpp
G4VPhysicalVolume* DetectorConstruction::Construct(){
G4String worldGdmlFilename="<GMLD_OUTPUT_PATH>/gdml/World.gdml"
G4GDMLParser parser;
parser.Read(worldGdmlFilename);
G4VPhysicalVolume *world= parser.GetWorldVolume();     
//other code 
  return world;
}
 ```


### Cite this work
If you use g4cad in your work, please use the following citation,
```sh
@software{g4cad,
  author       = {Hualin Xiao, Wojtek Hajdas},
  title        = {{g4cad - A freecad workbench for converting CAD 
                   files to gdml}},
  month        = sep,
  year         = 2022,
  publisher    = {Zenodo},
  version      = {v1.0},
  doi          = {10.5281/zenodo.7085915},
  url          = {https://doi.org/10.5281/zenodo.7085915}
}
```
## Maintanance and services

Maintainance and extended services related this software can be provide by [SE2S Ltd.](https://www.se2s.ch/).

SE2S Ltd. is a Swiss based tech-SME with over 30 years of experience in radiation qualification, particle detection and data analysis. Its founders gathered profound expertise in radiation qualification and testing, electronics design, hardware and software development, and data evaluation for applications in aerospace. Founded in 2020, SE2S GmbH offers next generation services and products in the following three fields:
- radiation detection systems
- Radiation analysis software and services
- Radiation qualification and testing services
For more details, please visit SE2S website: [https://www.se2s.ch/](https://www.se2s.ch/)

### Screenshots
 * g4cad Workbench
![g4cad workbench](./tests/g4cad.png)
 *  view of the exported model in geant4
![converted model in g4](./tests/model_in_g4.png  )

