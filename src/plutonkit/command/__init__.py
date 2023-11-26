
from plutonkit.config import INTRODUCTION
from plutonkit.config.command import ACTIONS
from plutonkit.command.action.help import Help

import sys

def autoload():

    TEMPLATE = "%s\n" % (INTRODUCTION)
    print(TEMPLATE)
    try:
        ACTIONS['help'] = Help()
        ACTIONS[str(sys.argv[1])].execute()
    except Exception as e:
        print("Invalid argument, please type `help` to see available command ")

