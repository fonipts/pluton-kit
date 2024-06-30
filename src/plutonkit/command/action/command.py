"""Module providing a function printing python version."""

import os
import sys

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from plutonkit.config import PROJECT_COMMAND_FILE
from plutonkit.framework.command.structure_command import StructureCommand
from plutonkit.helper.command import clean_command_split, pip_run_command


class Command:
    def __init__(self) -> None:
        self.index = 2

    def modify_argv_index(self, index):
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
                with open(path, "r", encoding="utf-8") as fi:
                    try:
                        read = fi.read()
                        content = load(str(read), Loader=Loader)

                    except Exception as e:
                        print(e)
                        print("Invalid yaml file content")
                        sys.exit(0)

                    structure_command_cls = StructureCommand(content, directory)
                    get_errors = structure_command_cls.get_error()
                    if len(get_errors) == 0:
                        command_list = sys.argv[self.index : :]
                        command_value = ":.:".join(command_list)
                        list_commands = structure_command_cls.get_list_commands()
                        if command_value in list_commands:
                            cmd_arg = list_commands[command_value]
                            for val in cmd_arg["command"]:
                                os.chdir(cmd_arg["chdir"])
                                pip_run_command(clean_command_split(val))
                                sys.exit(0)
                        else:
                            print("you are using an invalid command")
                            print("Please select the command below.")
                            for key, value in list_commands.items():
                                print(
                                    "  ",
                                    " ".join(key.split(":.:")),
                                    " .... ",
                                    value.get("description", "[no comment]"),
                                )
                        sys.exit(0)
                    else:
                        for err in get_errors:
                            print(err)
                        sys.exit(0)
        else:
            print(
                "This command file `%s` is missing in the directory project"
                % (PROJECT_COMMAND_FILE)
            )
            sys.exit(0)
