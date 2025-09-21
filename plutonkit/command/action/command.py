import importlib
import os
import sys

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from plutonkit.config import PROJECT_COMMAND_FILE, PYTHON_CMD, bcolors
from plutonkit.framework.command.py_validate_content import PyValidateContent
from plutonkit.framework.command.structure_command import StructureCommand
from plutonkit.framework.exception.cmd_validation_exception import (
    CmdValidationException,
)
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
            self.command_start_python(list_commands, directory)


    def command_start_python(self, list_commands, directory):
        cmd_file = f"{PYTHON_CMD}.py"
        path = os.path.join(directory, cmd_file)

        if os.path.isfile(path):
            py_file_class = PyValidateContent(path)
            var_class_import = py_file_class.get_class_import()
            var_class_call = py_file_class.get_class_call()

            if var_class_import.get("Command",None) is None:
                raise WarningException(f"In your `{cmd_file}`, please import `Command` in using command")

            if var_class_import["Command"] not in var_class_call:
                raise WarningException(f"In your `{cmd_file}`, Invalid in retrieving you command details")

            try:
                sys.path.append( directory )
                mod = importlib.import_module(PYTHON_CMD)
                if not hasattr(mod,"run"):
                    command_class = getattr(mod, var_class_call[ var_class_import["Command"] ])
                    command_class.run()
                else:
                    mod.run()
            except CmdValidationException as e:
                print(e)
                self.post_list_command(list_commands)
                print("\n")
                print(f"{bcolors.WARNING}{e}{bcolors.ENDC}")
        else:
            self.post_list_command(list_commands)
        sys.exit(0)

    def post_list_command(self, list_commands):
        print("you are using an invalid command")
        print(f"{bcolors.OKBLUE}Please select the command below.{bcolors.ENDC}")
        for key, value in list_commands.items():
            print("  ",
                " ".join(key.split(":.:")),
                 " .... ",
                convertVarToTemplate(value.get("description", "[no comment]")),
                )
