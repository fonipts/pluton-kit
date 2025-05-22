import re

from plutonkit.config.framework import VAR_TEMPLATE_EXEC
from plutonkit.helper.format import (
    get_first_line_string_space, get_first_strings, get_str_if_empty,
)

from .TemplateStruct import TemplateStruct
from .TemplateStructTags import TemplateStructTags
from .TemplateCommentOut import TemplateCommentOut


class TheTemplate:
    def __init__(self, content: str, args=None,block=None):
        self.block = block
        self.args = args
        self.content = self.__wragle_data(content)

    def __set_value_in_tags(self,param):
        raw_bool = False
        if param["type"] == "block":
            raw_bool = True
            if param["name"] in self.block:
                call_func= self.block[ param["name"] ]["func"](self.args)
                return call_func, True


        if param["type"] == "condition":

            return "", True

        return "",raw_bool

    def __command_details(self, name, contents, sub_content):

        lst = []

        get_init_string = get_first_strings(contents)
        get_str_count = get_first_line_string_space(get_init_string["content"])

        for v in contents:
            if get_str_if_empty(v):
                lst.append("")
            else:
                regex = re.compile("^[\\s]{0,"+str(get_str_count)+"}")
                lst.append(regex.sub("", v))

        if name in VAR_TEMPLATE_EXEC:
            row_content =  VAR_TEMPLATE_EXEC[name]("\n".join(lst),sub_content)

            if name == "load":
                if row_content["is_valid_template"]:
                    temp_cls = TheTemplate(row_content["content"],self.args)
                    row_content = temp_cls.get_content()
                else:
                    row_content = row_content["content"]
            return row_content
        return ""

    def __wragle_data(self, content: str):

        template_comment_out = TemplateCommentOut(content)
        content = template_comment_out.get_remove_comment_content()

        find_value = re.findall(r"(\{\$)([a-zA-Z0-9_]{1,})(\})", content)
        if len(find_value) > 0:
            for val in find_value:
                content = content.replace("".join(val), self.args.get(val[1], ""))

        template_struct_block = TemplateStructTags(content, self.args)
        content = template_struct_block.get_content()
        for mv in template_struct_block.template:
            raw_content,raw_bool = self.__set_value_in_tags(mv)
            if raw_bool:
                content = content.replace(mv["template"], raw_content)

        template_struct = TemplateStruct(content, self.args)

        for mv in template_struct.convert_template:
            sub_content = ""
            for sv in mv["component"]:
                sub_content += self.__command_details(sv["name"], sv["input"], sub_content)
            content = content.replace(mv["template"], sub_content)

        return content

    def get_content(self):
        return self.content
