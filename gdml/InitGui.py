__title__ = "FreeCAD GDML converter"
__author__ = "Hualin Xiao (hualin.xiao@psi.ch) "
__url__ = "http://polar.psi.ch"
import FreeCAD
import FreeCADGui


class GDML(Workbench):

    MenuText = "GDML"
    ToolTip = "gdml workbench"
    Icon = """
    /* XPM */
static char *draf_xpm[] = {
"32 32 111 2 ",
"   c #35E00B0B1267",
".  c #3A3A0F0F1515",
"X  c #3E3E11101919",
"o  c #434D14841BFD",
"O  c #484716161D1C",
"+  c #454518181E1D",
"@  c #4B4B18171D1C",
"#  c #535319991F1E",
"$  c #474719182020",
"%  c #4BCA1DDD24E4",
"&  c #55AA191820CB",
"*  c #5A101C892492",
"=  c #63CA1DB625BF",
"-  c #6C6B1C9C26A6",
";  c #6C6B1E1D2827",
":  c #72721E1E2827",
">  c #7C3C1F1E29A9",
",  c #4D4C201F2727",
"<  c #52B925712BAB",
"1  c #55D529283030",
"2  c #5AC02E2E3535",
"3  c #5DDD32323938",
"4  c #6766207628D3",
"5  c #6D6D21212A2A",
"6  c #72C720CA2AD5",
"7  c #7D2620CA29D4",
"8  c #626136353C3C",
"9  c #62E238B73EBE",
"0  c #64B93AE540EB",
"q  c #68E83EBE44C4",
"w  c #6BEB43424A49",
"e  c #707046464C4C",
"r  c #717149494F4E",
"t  c #76594DBF53C5",
"y  c #7B7A57565C5C",
"u  c #84841E9E2B2B",
"i  c #8A8A1EEB2AC4",
"p  c #94931E9D2BAB",
"a  c #9C1A1F1E2C2C",
"s  c #A2A21F1F2D2D",
"d  c #8E8D20202727",
"f  c #8DB221212C75",
"g  c #93D2205F2B6A",
"h  c #9BF021762D82",
"j  c #96952423302F",
"k  c #A3A320ED2EFB",
"l  c #ABAB23BD2E61",
"z  c #AF2E21A130B0",
"x  c #B4E722553164",
"c  c #BD3C246433B3",
"v  c #BD672A803232",
"b  c #C36D24CF3535",
"n  c #C9C926A63737",
"m  c #C46E2C5734B5",
"M  c #CBCB2B6B3676",
"N  c #CFCF2E2E3838",
"B  c #D5BB29AA39ED",
"V  c #DA942A9F3AC6",
"C  c #E3E32D9B3DAB",
"Z  c #EA6A2DEE3F3F",
"A  c #EE5F2EA04040",
"S  c #F4C92F294233",
"D  c #F4F436364848",
"F  c #F5F53C3C4E4E",
"G  c #81005DDD62E2",
"H  c #828261E166E6",
"J  c #860565E56A6A",
"K  c #878768686CEC",
"L  c #8A096B6B7070",
"P  c #8E8E72717776",
"I  c #913B75CB7A24",
"U  c #941479F97CFC",
"Y  c #EDED44445555",
"T  c #D0D056566262",
"R  c #E3E372727E7E",
"E  c #EAEA72F27DFD",
"W  c #97177DFD8140",
"Q  c #99187F7F8404",
"!  c #F8F87A7A8686",
"~  c #989880808383",
"^  c #9B9B84848888",
"/  c #A0A08C368F39",
"(  c #A2E28ECE91D1",
")  c #ACD19B529DE6",
"_  c #B41AA370A673",
"`  c #BD3CAF2EB130",
"'  c #BEBEB1B1B3B3",
"]  c #F5F593939D9D",
"[  c #F9F996969F9F",
"{  c #C2C2B6B6B8B8",
"}  c #C5C5B9B9BBBB",
"|  c #C948BD3CBF3E",
" . c #CA09BEFEC100",
".. c #FCFCBEBEC4C4",
"X. c #CCCCC1C1C3C3",
"o. c #D4D4CBCBCCCC",
"O. c #DA0CD305D406",
"+. c #DFDFD8D8DADA",
"@. c #FCFCC5C5CACA",
"#. c #FCFCCECED3D3",
"$. c #E1E1DBDBDCDC",
"%. c #FDFDD6D6DADA",
"&. c #E5E5DFDFE0E0",
"*. c #E726E221E322",
"=. c #E9E9E4E4E5E5",
"-. c #EBEBE7E7E8E8",
";. c #EE6EEB6AEB6A",
":. c #F170EEAEEEAE",
">. c #F75DF55BF65C",
",. c #FA60F6C3F790",
"<. c #FFF5FFF4FFF4",
"<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.",
"<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.",
"<.<.<.<.<.<.<.<.<.<.<.>. .U 0 < o   X % 0 W  .<.<.<.<.<.<.<.<.<.",
"<.<.<.<.<.<.<.<.<.:.W o = j T R E S A V c g * , ) <.<.<.<.<.<.<.",
"<.<.<.<.<.<.<.<.) o u E @.,.%...] S S S S S S n = 9 *.<.<.<.<.<.",
"<.<.<.<.<.<.,.J & V ..#.E F S S S S S S S S S S S h % *.<.<.<.<.",
"<.<.<.<.<.<.H ; [ ! D S S Z x > ; ; 6 a V S S S S S k 2 ,.<.<.<.",
"<.<.<.<.<.) & Y ..F S S s O r ) {  .` L o f S S S S S - ) <.<.<.",
"<.<.<.<.;.o V S S S S > 3 +.<.<.<.<.<.<.;.w > S S S S b 2 <.<.<.",
"<.<.<.<.U i S S S S p q >.<.<.<.<.<.<.<.<.>.1 z S S S A . <.<.<.",
"<.<.<.>.O V S S S B $ -.<.<.<.<.<.<.<.<.<.<.O.O B S S c 2 <.<.<.",
"<.<.<.| = S S S S u W <.<.<.<.<.<.<.<.<.<.<.<._ O p p o  .<.<.<.",
"<.<.<.U p S S S S o &.<.<.<.<.<.<.<.<.<.<.<.<.<.o.Q ^ $.<.<.<.<.",
"<.<.<.9 b S S S V % <.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.",
"<.<.<.< B S S S x t <.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.",
"<.<.<.o C S S S z G <.<.<.<.<.<.<.*.I t t t t t t t J / =.<.<.<.",
"<.<.<.  Z S S S s L <.<.<.<.<.<.*.+ g x x x x x x x s i $ $.<.<.",
"<.<.<.o C S S S s G <.<.<.<.<.<.( i S S S S S S S S S S a H <.<.",
"<.<.<.< B S S S c e <.<.<.<.<.<.) 7 S S D S S D S S S S n 2 <.<.",
"<.<.<.9 c S S S V $ <.<.<.<.<.<.:.2 * 7 f f f f a S S S V < <.<.",
"<.<.<.U f S S S S O &.<.<.<.<.<.<.<.X._ / ^ ^ I * S S S B < <.<.",
"<.<.<. .= Z S S S i W <.<.<.<.<.<.<.<.<.<.<.<.O.* S S S B < <.<.",
"<.<.<.,.o n S S S V O =.<.<.<.<.<.<.<.<.<.<.<.O.& S S S B < <.<.",
"<.<.<.<.W > A S S S j 0 >.<.<.<.<.<.<.<.<.<.<.O.* S S S B < <.<.",
"<.<.<.<.:.o v S S S Z f 8 O.<.<.<.<.<.<.<.,._ 1 : S S S n 2 <.<.",
"<.<.<.<.<._ # B Z Z S S l @ w ( ' | ` ( t o 5 b S S S S l t <.<.",
"<.<.<.<.<.<.K = M Z S Z S Z x i 6 4 6 i l C S S S S A m # _ <.<.",
"<.<.<.<.<.<.,.J # m C Z S S S S S S S S S S S Z C N h o ~ <.<.<.",
"<.<.<.<.<.<.<.<.) o 7 m N C Z Z S S S Z Z C N m g @ q o.<.<.<.<.",
"<.<.<.<.<.<.<.<.<.;.I o 4 g l v m M m v l d 5 o y o.<.<.<.<.<.<.",
"<.<.<.<.<.<.<.<.<.<.<.>.} P 8 < o   o , q I ` >.<.<.<.<.<.<.<.<.",
"<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<.<."
};"""

    def Initialize(self):
        import plugin_init
        self.list = [
            "import", "export", "add_world", "add_box", "add_sphere",
            "add_cylinder", "add_cone", "set_material", "set_precision",
            "set_physical_volume", "hide_parts", "filter_parts",
            "show_measurements", "manage_materials"
        ]
        self.appendToolbar("GDML", self.list)
        self.appendMenu("GDML", self.list)

    def Activated(self):
        if not (FreeCAD.ActiveDocument):
            FreeCAD.newDocument()
        FreeCAD.Console.PrintMessage('GDML workbench loaded.. \n')
        return

    def Deactivated(self):
        return

    def ContextMenu(self, recipient):
        self.appendContextMenu(MenuText, self.list)

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(GDML)
App.addImportType("Geometry Description Markup Language(*.gdml)",
                  "GdmlImporter")
App.addExportType("Geometry Description Markup Language(*.gdml)",
                  "GdmlExporter")
