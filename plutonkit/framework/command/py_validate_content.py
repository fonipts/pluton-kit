import re


class PyValidateContent:
    def __init__(self,cmd_file):
        self.cmd_file = cmd_file
        self.content = ""
        with open(self.cmd_file, "r", encoding="utf-8") as fi:
            self.content = fi.read()

    def is_run_func_available(self):
        return re.search(r"def\s{1,}run\((.*?)\)\s{0,}:\n", self.content) is not None


    def get_class_import(self):
        glb = {}
        for valc in self.content.split("\n"):

            if valc:
                self._get_import(valc,glb)

        return glb

    def get_class_call(self):
        glb = {}
        for valc in self.content.split("\n"):
            if valc:
                self._get_call_class(valc,glb)

        return glb


    def _get_import(self,data_import,glb):
        match_anywhere = re.match(r"([\n\s]{0,}from[\s]{0,})(plutonkit)([\s]{0,}import[\s]{0,})[\(]{0,1}([a-zA-Z0-9\_\s\,]{1,})[\)]{0,1}\n{0,}", data_import)

        if match_anywhere:
            if len(match_anywhere.groups()) >=4:
                for vval in match_anywhere[4].strip().split(","):
                    if vval:
                        match_variable = re.match(r"([a-zA-Z0-9\_]+)\s{1,}(as|AS)\s{1,}([a-zA-Z0-9\_]+)", vval)
                        if match_variable:
                            if len(match_variable.groups()) >=3:
                                glb[str(match_variable[1])] = match_variable[3]
                        else:
                            glb[str(vval)] = vval

    def _get_call_class(self,data_class,glb):

        match_anywhere1 = re.match(r"[\n\s]{0,}([a-zA-Z0-9\_]+)[\s]{0,}=[\s]{0,}([a-zA-Z0-9\_]{1,})\((.*?)\)\n{0,}", data_class)
        if match_anywhere1:
            if len(match_anywhere1.groups()) >=3:
                glb[match_anywhere1[2]] = match_anywhere1[1]
