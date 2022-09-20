__title__ = "FreeCAD geant4 mass model creator G4CAD"
__author__ = "Hualin Xiao (hualin.xiao@psi.ch) "
__url__ = ""
import FreeCAD
import FreeCADGui

class G4CAD(Workbench):

    MenuText = "G4CAD"
    ToolTip = "G4CAD - a Geant4 mass model creator"
    Icon = """
/* XPM */
static char *e989dec9477c492c8c341340245304b99otIH7s4cf3mqL2D[] = {
/* columns rows colors chars-per-pixel */
"32 32 55 1 ",
"  c #209CEE",
". c #259EEE",
"X c #289FEE",
"o c #29A0EE",
"O c #2DA2EF",
"+ c #31A3EF",
"@ c #36A5EF",
"# c #3DA9F0",
"$ c #46ADF1",
"% c #53B2F2",
"& c #57B4F2",
"* c #5BB6F2",
"= c #63BAF3",
"- c #68BCF3",
"; c #6DBEF4",
": c #72C1F4",
"> c #76C2F4",
", c #78C3F5",
"< c #79C3F5",
"1 c #83C8F5",
"2 c #84C8F5",
"3 c #8BCBF6",
"4 c #8ECDF6",
"5 c #91CEF6",
"6 c #93CFF7",
"7 c #99D1F7",
"8 c #9BD2F7",
"9 c #9ED4F7",
"0 c #A0D5F7",
"q c #A4D6F8",
"w c #A6D7F8",
"e c #A8D8F8",
"r c #B1DCF9",
"t c #B4DEF9",
"y c #B8DFF9",
"u c #BBE1F9",
"i c #BDE2FA",
"p c #C6E5FA",
"a c #C8E7FB",
"s c #CEE9FB",
"d c #D2EBFB",
"f c #D4ECFC",
"g c #D9EEFC",
"h c #DBEFFC",
"j c #DEF0FC",
"k c #E3F3FD",
"l c #E4F3FD",
"z c #EAF6FD",
"x c #EDF7FD",
"c c #EFF8FE",
"v c #F1F9FE",
"b c #F4FAFE",
"n c #F8FBFE",
"m c #F8FCFE",
"M c #FDFEFF",
/* pixels */
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"              #<42&             ",
"            oqMMMMMf#           ",
"            iMMMzmMMjo          ",
"           <MMt+ XeMM3          ",
"           lMf.   ovMk          ",
"          *MM;     0Mm          ",
"          5MMO     O4-          ",
"          iMk                   ",
"          gMp                   ",
"          xMy                   ",
"          bMr   1uii0#          ",
"          bMt   bMMMMf          ",
"          zMi   :qecMn          ",
"          gMd      9Mm          ",
"          iMz      8Mm          ",
"          8MM@     8Mm          ",
"          =MM<     0Mb          ",
"          ovMf     aMg          ",
"           5MMq.  >MM9          ",
"           XfMMvslMMx@          ",
"            @pMMMMMh$           ",
"              %384*             ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                "
};
"""
    def Initialize(self):
        import g4cad_init
        self.list = [
            "import", "export", "add_world", "add_box", "add_sphere",
            "add_cylinder", "add_cone", "set_material", "set_tolerance",
            "set_physical_volume", "hide_parts", "filter_parts",
            "show_measurements", "manage_materials"
        ]
        self.appendToolbar("G4CAD", self.list)
        self.appendMenu("G4CAD", self.list)

    def Activated(self):
        if not (FreeCAD.ActiveDocument):
            FreeCAD.newDocument()
        FreeCAD.Console.PrintMessage('G4CAD workbench loaded.. \n')
        return

    def Deactivated(self):
        return

    def ContextMenu(self, recipient):
        self.appendContextMenu(MenuText, self.list)

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(G4CAD)
App.addImportType("Geometry Description Markup Language(*.gdml)",
                  "GdmlImporter")
App.addExportType("Geometry Description Markup Language(*.gdml)",
                  "GdmlExporter")
