import re
from glob import glob

from plutonkit.helper.template import convert_shortcode


class BlueprintFileSchema:
    def __init__(self, value, args, request_type) -> None:
        self.value = value
        self.args = args
        self.request_type = request_type

    def isObjFile(self):
        return "file" in self.value

    def get_save_files(self):
        value_mv_file = self.__clean_file_name(convert_shortcode(self.value.get("mv_file",""), self.args))
        value_file = self.__clean_file_name(convert_shortcode(self.value.get("file",""), self.args))
        list_mv_files = [value_mv_file]
        list_files = [value_file]
        if self.request_type == "git":
            list_mv_files = []
            list_files = []
            for name in glob(value_mv_file):
                list_mv_files.append(self.__clean_file_name(convert_shortcode(name, self.args)))
            for name in glob(value_file):
                list_files.append(self.__clean_file_name(convert_shortcode(name, self.args)))

        if "mv_file" in self.value:
            return list_mv_files
        return list_files

    def __clean_file_name(self, name):
        name = re.sub(r"^(/)", "", name)
        return name
