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
from plutonkit.framework.command.structure_command import StructureCommand

class Command:
    def __init__(self) -> None:
        self.index = 2

    def modifyArgvIndex(self,index):
        self.index = index
        return self

    def comment(self):
        return "Executing command using plutonkit"

    def execute(self):

        directory = os.getcwd()
        path = os.path.join(directory, PROJECT_COMMAND_FILE)
        if os.path.exists(path):
            is_file = os.path.isfile(path)
            if is_file:
                with open(path , "r", encoding="utf-8") as fi:
                    try:
                        read = fi.read()
                        content = load(str(read), Loader=Loader)

                        structureCommandCls = StructureCommand(content,directory)
                        get_errors = structureCommandCls.get_error()
                        if len(get_errors) == 0:
                            command_list = sys.argv[self.index::]
                            command_value = ":.:".join(command_list)
                            list_commands = structureCommandCls.get_list_commands()
                            if command_value in list_commands:
                                cmd_arg = list_commands[command_value]
                                for val in cmd_arg["command"]:
                                    val_clean = re.sub(r'\s{2,}', ' ', val)
                                    os.chdir(cmd_arg["chdir"])

                                    pip_run_command(val_clean.split(" "))
                                    exit(0)
                            else:
                                print("you are using an invalid command")
                                print("Please select the command below.")
                                for key,value in list_commands.items():
                                    print("  "," ".join(key.split(":.:"))," .... ",value.get("description","[no comment]") )
                            exit(0)
                        else:
                            for err in get_errors:
                                print(err)
                            exit(0)

                    except Exception as e:
                        print(e)
                        print("Invalid yaml file content")
                        exit(0)
        else:
            print("This command file `%s` is missing in the directory project"%(PROJECT_COMMAND_FILE))
            exit(0)
