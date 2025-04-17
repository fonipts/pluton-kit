import re
class PyValidateContent:
    def __init__(self,cmd_file):
        self.cmd_file = cmd_file
        self.content = ""
        with open(self.cmd_file, "r", encoding="utf-8") as fi:
            self.content = fi.read()

    def is_run_func_available(self):
        return re.search(r"def\s{1,}run\(\s{0,}\)\s{0,}:\n", self.content) is not None
