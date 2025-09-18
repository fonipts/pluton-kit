import inspect
import os
import re

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

    def getcmd_arg_validated(self):
        arg_data = self.getcmd_arg()
        arg_list, _, ord_list = self.get_argument_details()
        if len(arg_data)>0:
            raw_list = []
            raw_dist = {}
            counter = 0
            for key,val in enumerate(arg_data):
                is_arg = len(arg_list)>key
                raw_value:any = val
                if re.match(r"^[0-9]\.+$",val):
                    raw_value = float(val)
                if re.match(r"^[0-9]+$",val):
                    raw_value = int(val)

                if is_arg:
                    raw_list.append(raw_value)
                else:

                    if len(ord_list)-1 >= key:
                        raw_dist[ord_list[key]] = raw_value
                    counter +=1

            return raw_list, raw_dist

        return [],{}
    def get_name_details(self):
        cmd_list = {}

        for key, value in self.list_func.items():
            cmd_list[key] = value['description']
        return cmd_list

    def validated_cmd_arg(self):
        arg_list, _ , ord_list = self.get_argument_details()
        cmd_arguments = self.getcmd_arg()

        if len(cmd_arguments) > len(ord_list):
            return False, "cmd arguments exceed in define value"

        if len(cmd_arguments) < len(arg_list):
            return False, "cmd arguments is lesser expected value"

        return True, ""

    def get_argument_details(self):
        index = self.get_index()
        arg_list = []
        arg_dict = []
        ord_list = []
        if index==0:
            return arg_list, arg_dict, ord_list
        if self.argv[index] in self.list_func:
            signature = inspect.signature(self.list_func[self.argv[index]]["func"])
            for name, param in signature.parameters.items():
                row_arg = {}
                ord_list.append(name)
                row_arg["name"] = name
                row_arg["kind"] = str(param.kind)
                row_arg["annotation"] = param.annotation
                is_object = False

                if param.default is not inspect.Signature.empty:
                    row_arg["default"] = param.default
                    is_object = True

                if is_object:
                    arg_dict.append(row_arg)
                else:
                    arg_list.append(row_arg)

        return arg_list, arg_dict, ord_list
