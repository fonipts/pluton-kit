import os
import sys

from plutonkit.config import PYTHON_CMD


class PLCommand:
    def __init__(self):
        self.local_cli = {}

    def cli(self,name = None,description = None):
        def cli_real_decorator(function):

            def wrapper(*args,**kwargs):

                return function(*args,**kwargs)
            self.local_cli[name] = {
                "description":description,
                "func":function
                }
            return wrapper
        return cli_real_decorator

    def run(self):

        directory = os.getcwd()
        path = os.path.join(directory, f"{PYTHON_CMD}.py")

        if os.path.exists(path) is False:
            print(f"This file `{PYTHON_CMD}` must use in python cmd")
            sys.exit(0)
        if len(sys.argv) == 1:
            print("Please specify your command name")
            sys.exit(0)
        if sys.argv[1] not in self.local_cli:
            name_cli = sys.argv[1]
            print(f"Your command name `{name_cli}` does not exist your `{PYTHON_CMD}.py`")
            sys.exit(0)
        self.local_cli[sys.argv[1]]["func"](13,2)
