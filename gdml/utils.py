
import os
def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def show_message(msg, type='msg'):
    try:
        import FreeCAD
        if type == 'msg':
            FreeCAD.Console.PrintMessage(msg)
        else:
            FreeCAD.Console.PrintWarning(msg)
    except BaseException:
        print(msg)
def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def get_current_path():
    return os.path.dirname(os.path.realpath(__file__))
