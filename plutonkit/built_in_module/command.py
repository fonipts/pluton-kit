import os
import sys

from plutonkit.config import PYTHON_CMD
from plutonkit.framework.command.py_validate_arguments import (
    PyValidateArguments,
)
from plutonkit.framework.decorator.builtin_cmd import callback_script
from plutonkit.framework.exception.validation_exception import (
    ValidationException,
)


class PLCommand:
    def __init__(self):
        self.local_cli = {}

    def cli(self,name = None,description = None):
        def cli_real_decorator(function):

            def wrapper(*args,**kwargs):

                return function(*args,**kwargs)
            final_name = name is None and function.__name__ or name
            self.local_cli[final_name] = {
                "description":description,
                "func":function
                }
            return wrapper
        return cli_real_decorator

    @callback_script
    def run(self):

        directory = os.getcwd()
        path = os.path.join(directory, f"{PYTHON_CMD}.py")

        validate_arg = PyValidateArguments(sys.argv,self.local_cli)
        getcmd_name = validate_arg.getcmd_name()

        if validate_arg.get_python_name_script():
            print("You are running a python script")

        if os.path.exists(path) is False:
            raise ValidationException("This file `{PYTHON_CMD}` must use in python cmd")
        if len(sys.argv) == 1:
            raise ValidationException("Please specify your command name")
        if getcmd_name not in self.local_cli:
            raise ValidationException(f"Your command name `{getcmd_name}` does not exist your `{PYTHON_CMD}.py`")
        #
        #signature = inspect.signature(self.local_cli[sys.argv[1]]["func"])
        #for name, param in signature.parameters.items():
        #    print(f"Name: {name}")
        #    print(f"Kind: {param.kind}")
        #    print(f"Default: {param.default}")
        #    print("-" * 20)
        #    print(f"  Type annotation: {param.annotation}")
        #    if param.annotation is inspect._empty:
        #        print("  No type hint provided")

        #    arg_list, arg_dict, ord_list = validate_arg.get_argument_details()

        #    print(cmd_arg_list,":cmd_arguments")
        #    print(arg_list,":arg_list")
        #    print(arg_dict,":arg_dict")
        #    print(ord_list,":ord_list")
        valid_cmd,mes_cmd=validate_arg.validated_cmd_arg()
        if valid_cmd is False:
            raise ValidationException(mes_cmd)

        cmd_arg_list, cmd_arg_dict = validate_arg.getcmd_arg_validated()
        args = tuple(cmd_arg_list)
        kwargs = cmd_arg_dict
        self.local_cli[getcmd_name]["func"](*args,**kwargs)
