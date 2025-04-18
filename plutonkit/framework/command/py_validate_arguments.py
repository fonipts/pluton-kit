import inspect
import os

from plutonkit.config import PYTHON_CMD


class PyValidateArguments:
    def __init__(self,argv,list_func):
        self.argv = argv
        self.list_func = list_func

    def get_python_name_script(self):
        basename = os.path.basename(self.argv[0])

        return basename == f"{PYTHON_CMD}.py"

    def get_index(self):
        basename = os.path.basename(self.argv[0])

        if basename == "plutonkit":
            if len(self.argv) >=3:
                return 2
        if basename in ("plkcmd",f"{PYTHON_CMD}.py"):
            if len(self.argv) >=2:
                return 1

        return 0

    def getcmd_name(self):
        index = self.get_index()

        if index>0:

            return self.argv[index]


        return ""

    def getcmd_arg(self):
        index = self.get_index()

        if index+1>0:

            return self.argv[index+1::]


        return []

    def get_argument_details(self):
        index = self.get_index()
        arg_list = []
        if index==0:
            return arg_list
        if self.argv[index] in self.list_func:
            signature = inspect.signature(self.list_func[self.argv[index]]["func"])
            for name, param in signature.parameters.items():
                row_arg = {}
                row_arg["name"] = name
                row_arg["kind"] = param.kind
                #print(f"Name: {name}")
                #print(f"Kind: {param.kind}")
                #print(f"Default: {param.default}")
                #print("-" * 20)
                #print(f"  Type annotation: {param.annotation}")
                #if param.annotation is inspect._empty:
                #    print("  No type hint provided")
                arg_list.append(row_arg)
        return arg_list
