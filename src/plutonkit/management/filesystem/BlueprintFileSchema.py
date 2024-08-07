import re

from plutonkit.helper.template import convert_shortcode


class BlueprintFileSchema:
    def __init__(self,value,args) -> None:
        self.value = value
        self.args = args

    def isObjFile(self):
        return "file" in self.value
    def get_save_files(self):
        if "mv_file" in self.value:
            return [
                self.__clean_file_name(convert_shortcode(self.value["mv_file"], self.args))
                ]
        return [
            self.__clean_file_name(convert_shortcode(self.value["file"], self.args))
            ]

    def __clean_file_name(self, name):
        name = re.sub(r"^(/)","",name)
        return name
