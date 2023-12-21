
"""Module providing a function printing python version."""
import sys
from plutonkit.config.command import ACTIONS
from plutonkit.command.action.help import Help
from plutonkit.config import INTRODUCTION

import signal
import time

# Our signal handler
def signal_handler(signum, frame):
    print('\nInvalid control +key or press control+z to exit')
    print('\nPlease try to select appropriate key selection')

def exit_handler(signum, frame):
    print('\nExiting....')
    exit(0)

def autoload():

    signal.signal(signal.SIGINT, signal_handler)

# Register the exit handler with `SIGTSTP` (Ctrl + Z)
    signal.signal(signal.SIGTSTP, exit_handler)

    TEMPLATE = "%s\n" % (INTRODUCTION)
    print(TEMPLATE)
    try:
        while 1:
            ACTIONS['help'] = Help()
            ACTIONS[str(sys.argv[1])].execute()
            time.sleep(30)
    except Exception:
        print("Invalid argument, please type `help` to see available command ")
