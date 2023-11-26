"""Module providing a function printing python version."""

import os
import re
import sys
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from plutonkit.helper.command import pip_run_command
from plutonkit.config import PROJECT_COMMAND_FILE

class Command:
    def __init__(self) -> None:
        pass

    def comment(self):
        return "Executing command using plutonkit"
    def execute(self):
        directory = os.getcwd()
        path = os.path.join(directory, PROJECT_COMMAND_FILE)
        if os.path.exists(path):
            is_file = os.path.isfile(path)
            if is_file:
                with open(path , 'r', encoding="utf-8") as fi:
                    try:
                        read = fi.read()
                        content = load(str(read), Loader=Loader)

                        content_script = content['script']
                        try:
                            command_value = sys.argv[2]
                            if command_value not in content_script:
                                print("Invalid command variable")
                                return

                            try :
                                for val in content_script[command_value]['command']:
                                    os.chdir(directory)
                                    val_clean = re.sub(r'\s{2,}', ' ', val)
                                    pip_run_command(val_clean.split(" "))
                            except Exception as e2:
                                print(e2)
                        except Exception:
                            print("Please specify your command like `plutonkit command start`")
                    except Exception:
                        print("Invalid yaml file content")
        else:
            print("This command file `%s` is missing in the directory project"%(PROJECT_COMMAND_FILE))
