import os
import sys

from plutonkit.config import PYTHON_CMD
from plutonkit.framework.command.py_validate_arguments import (
    PyValidateArguments,
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

    def run(self):

        directory = os.getcwd()
        path = os.path.join(directory, f"{PYTHON_CMD}.py")

        validate_arg = PyValidateArguments(sys.argv,self.local_cli)
        getcmd_name = validate_arg.getcmd_name()

        if validate_arg.get_python_name_script():
            print("You are running in python script")

        if os.path.exists(path) is False:
            print(f"This file `{PYTHON_CMD}` must use in python cmd")
            sys.exit(0)
        if len(sys.argv) == 1:
            print("Please specify your command name")
            sys.exit(0)
        if getcmd_name not in self.local_cli:

            name_cli = sys.argv[1]
            print(f"Your command name `{name_cli}` does not exist your `{PYTHON_CMD}.py`")
            sys.exit(0)
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
        validate_arg.get_argument_details()
        args = ()
        ar_lst = tuple([2,4])
        args = ar_lst
        kwargs = {}
        self.local_cli[getcmd_name]["func"](*args,**kwargs)
