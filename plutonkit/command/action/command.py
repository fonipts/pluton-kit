import importlib
import os
import sys

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from plutonkit.config import PROJECT_COMMAND_FILE, PYTHON_CMD
from plutonkit.framework.command.py_validate_content import PyValidateContent
from plutonkit.framework.command.structure_command import StructureCommand
from plutonkit.framework.exception.validation_exception import (
    ValidationException,
)
from plutonkit.framework.exception.warning_exception import WarningException
from plutonkit.helper.command import clean_command_split, pip_run_command
from plutonkit.helper.environment import (
    convertVarToTemplate, setEnvironmentVariable,
)


class Command:
    def __init__(self, argv) -> None:
        self.index = 2
        self.argv = argv

    def modify_argv_index(self, index):
        self.index = index
        return self

    def comment(self):
        return "Executing command using plutonkit"

    def execute(self):

        directory = os.getcwd()
        path = os.path.join(directory, PROJECT_COMMAND_FILE)

        if os.path.exists(path) is False:
            raise ValidationException(f"This command file `{PROJECT_COMMAND_FILE}` is missing in the directory project")

        if os.path.isfile(path) is False:
            raise ValidationException(f"This file `{PROJECT_COMMAND_FILE}` is invalid")

        with open(path, "r", encoding="utf-8") as fi:

            read = fi.read()
            content = load(str(read), Loader=Loader)

        self.command_start(content, directory)

    def command_start(self, content, directory):
        structure_command_cls = StructureCommand(content, directory)
        setEnvironmentVariable(content.get("env",{}))
        get_errors = structure_command_cls.get_error()
        if len(get_errors) > 0:
            raise ValidationException("Invalid yaml file content",errors=get_errors)

        command_list = self.argv[self.index::]
        command_value = ":.:".join(command_list)
        list_commands = structure_command_cls.get_list_commands()

        if command_value in list_commands:
            cmd_arg = list_commands[command_value]
            is_exec_running = len(cmd_arg["command"])>0
            while is_exec_running:
                try:
                    os.chdir(cmd_arg["chdir"])
                    pip_run_command(clean_command_split(cmd_arg["command"][0]))
                except Exception as E:
                    print(E)
                cmd_arg["command"].pop(0)
                is_exec_running = len(cmd_arg["command"])>0
            sys.exit(0)
        else:
            cmd_file = f"{PYTHON_CMD}.py"

            path = os.path.join(directory, cmd_file)

            if os.path.isfile(path):
                py_file_class = PyValidateContent(path)

                if py_file_class.is_run_func_available() is False:
                    raise WarningException("In your `{cmd_file}`, please add `run` function name in order to execute the cmd command")

                sys.path.append( directory )
                mod = importlib.import_module(PYTHON_CMD)
                mod.run()
            else:
                print("you are using an invalid command")
                print("Please select the command below.")
                for key, value in list_commands.items():
                    print("  ",
                        " ".join(key.split(":.:")),
                        " .... ",
                        convertVarToTemplate(value.get("description", "[no comment]")),
                        )
        sys.exit(0)
