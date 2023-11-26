
"""Module providing a function printing python version."""
import sys
from plutonkit.config.command import ACTIONS
from plutonkit.command.action.help import Help
from plutonkit.config import INTRODUCTION

def autoload():

    TEMPLATE = "%s\n" % (INTRODUCTION)
    print(TEMPLATE)
    try:
        ACTIONS['help'] = Help()
        ACTIONS[str(sys.argv[1])].execute()
    except Exception:
        print("Invalid argument, please type `help` to see available command ")
