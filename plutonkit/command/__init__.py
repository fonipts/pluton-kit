"""Module providing a function printing python version."""

import os
import signal
import sys
import time

from plutonkit.command.action.help import Help
from plutonkit.config import INTRODUCTION, bcolors
from plutonkit.config.command import ACTIONS
from plutonkit.framework.exception.help_exception import HelpException
from plutonkit.framework.exception.validation_exception import (
    ValidationException,
)
from plutonkit.framework.exception.warning_exception import WarningException

# noqa: Our signal handler


def signal_handler():
    print("\nInvalid control +key or press control+z to exit")
    print("\nPlease try to select appropriate key selection")


def exit_handler():
    print("\nExiting....")
    sys.exit(0)


def autoload(type_cmd=None):

    signal.signal(signal.SIGINT, signal_handler)
    os.system('color')


    # noqa: Register the exit handler with `SIGTSTP` (Ctrl + Z)
    # windows does not support SIGTSTP
    if hasattr(signal, "SIGTSTP"):
        signal.signal(signal.SIGTSTP, exit_handler)

    print(f"{bcolors.HEADER}{INTRODUCTION}{bcolors.ENDC}\n")
    try:
        while 1:
            if type_cmd == "cmd":
                ACTIONS["cmd"].modify_argv_index(1).execute()
            else:
                if len(sys.argv)<2:
                    raise HelpException()
                if sys.argv[1] not in tuple(ACTIONS):
                    raise HelpException()
                basename = os.path.basename(sys.argv[1])

                ACTIONS["help"] = Help(sys.argv)
                ACTIONS[str(basename)].execute()

            time.sleep(30)
    except ValidationException as E:
        print(f"{bcolors.FAIL}Error: {E}{bcolors.ENDC}")
        for val in E.errors:
            print(f"    * {bcolors.FAIL}Error: {val}{bcolors.ENDC}")
    except WarningException as E:
        print(f"{bcolors.WARNING}Warning: {E}{bcolors.ENDC}")
    except HelpException:
        print(f"{bcolors.WARNING}Invalid argument, please type `help` to see available command{bcolors.ENDC}")
    except Exception as E:
        print(f"{bcolors.FAIL}Error:{E}{bcolors.ENDC}")

def load_command():
    autoload(type_cmd="cmd")
