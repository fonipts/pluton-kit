import os
import sys

from plutonkit.config import PYTHON_CMD, bcolors
from plutonkit.framework.exception.help_exception import HelpException
from plutonkit.framework.exception.validation_exception import (
    ValidationException,
)
from plutonkit.framework.exception.warning_exception import WarningException


def callback_scipt(func):
    def wrapper(*args, **kwargs):
        basename = os.path.basename(sys.argv[0])
        if basename in (f"{PYTHON_CMD}.py"):
            os.system('color')
            try:
                func(*args, **kwargs)
            except WarningException as E:
                print(f"{bcolors.WARNING}Warning: {E}{bcolors.ENDC}")
            except ValidationException as E:
                print(f"{bcolors.FAIL}Error: {E}{bcolors.ENDC}")
                for val in E.errors:
                    print(f"    * {bcolors.FAIL}Error: {val}{bcolors.ENDC}")
            except HelpException:
                print(f"{bcolors.WARNING}Invalid argument, please type `help` to see available command{bcolors.ENDC}")
            except Exception as E:
                print(f"{bcolors.FAIL}Error: {E}{bcolors.ENDC}")
        else:
            cmd_file = f"{PYTHON_CMD}.py"
            print(f"We are accessing `{cmd_file}`, in your local project.\n")
            func(*args, **kwargs)
    return wrapper
