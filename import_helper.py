import sys
from importlib import import_module, util
name = ''
# dynamic import  
def dynamic_import():
    """
    Imports the relevant module depending on the commandline arguments
    return: import module
    """
    global name
    try:
        maze_exists = util.find_spec('maze.' + sys.argv[2])
        if maze_exists:
            name = 'maze.' + sys.argv[2]
        else:
            name = 'maze.obstacles'
    except:
        name = 'maze.obstacles'
    return import_module(name)
