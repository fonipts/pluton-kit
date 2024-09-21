import re

from plutonkit.config.framework import VAR_TEMPLATE_EXEC

from .TemplateStruct import TemplateStruct


class TheTemplate:
    def __init__(self, content: str, args=None):
        self.args = args
        self.content = self.__wragle_data(content)

    def __command_details(self, name, contents, sub_content):

        lst = []
        first_count_space = 0
        for k, v in enumerate(contents):

            check_space = re.findall(r"^[\s]{0,}", v)
            space_count = len(check_space[0].split(" "))

            if k == 0:
                first_count_space = space_count
            regex = re.compile("^[\\s]{0,"+str(first_count_space)+"}")
            lst.append(regex.sub("", v))

        if name in VAR_TEMPLATE_EXEC:
            return VAR_TEMPLATE_EXEC[name]("\n".join(lst),sub_content)

        return ""

    def __wragle_data(self, content: str):
        find_value = re.findall(r"(\{\$)([a-zA-Z0-9_]{1,})(\})", content)
        if len(find_value) > 0:
            for val in find_value:
                content = content.replace("".join(val), self.args.get(val[1], ""))

        template_struct = TemplateStruct(content, self.args)

        for mv in template_struct.convert_template:
            sub_content = ""
            for sv in mv["component"]:
                sub_content += self.__command_details(sv["name"], sv["input"], sub_content)
            content = content.replace(mv["template"], sub_content)

        return content

    def get_content(self):
        return self.content
