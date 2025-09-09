import re

from plutonkit.config.framework import VAR_TEMPLATE_EXEC
from plutonkit.framework.logic.tymplu.lexer import Lexer
from plutonkit.framework.logic.tymplu.parser import Parser
from plutonkit.helper.format import (
    get_first_line_string_space, get_first_strings, get_str_if_empty,
)

from ..logic.ConditionSplit import ConditionSplit


class TheTemplate:
    def __init__(self, content: str, args=None,block=None):
        self.raw_content = content
        self.block = block
        self.args = args
        self.content = self.__wragle_data(content)

    def __set_value_in_tags(self,param):
        raw_bool = False
        if param["type"] == "block":
            raw_bool = True
            if param["action"] in self.block:
                call_func= self.block[ param["action"] ]["func"](self.args)
                return call_func, True


        if param["type"] == "condition":

            return "", True

        if param["type"] == "content":

            return param["content"], True

        return "",raw_bool

    def __command_details(self, name, contents, sub_content) -> bool | dict[str, bool | str] | str :

        lst: list[str] = []

        get_init_string = get_first_strings(contents)
        get_str_count = get_first_line_string_space(get_init_string["content"])

        for v in contents:
            if get_str_if_empty(v):
                lst.append("")
            else:
                regex = re.compile("^[\\s]{0,"+str(get_str_count)+"}")
                lst.append(str(regex.sub("", v)))

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

    def __get_cond_valid_data(self,append_data,types:str):
        counter =0
        append_count = len(append_data)
        valid_cond = True
        valid_data = []
        end_index = 0
        start_index = 0
        while counter< append_count:
            row_data = append_data[counter]
            if row_data["type"] == "condition":
                valid_cond = False

                cond = ConditionSplit(row_data["content"],self.args)

                valid_cond = cond.validCond()
                if types == "tag" and valid_cond:
                    end_index = row_data["end_index"]
                    start_index = row_data["start_index"]

            elif row_data["type"] == "end":
                if types == "tag" and valid_cond:
                    valid_data.append({
                        "start_index":row_data["end_index"],
                        "end_index":start_index,
                        "raw":self.raw_content[start_index:row_data["end_index"]],
                        "type":"content",
                        "action":"content",
                        "content":self.raw_content[end_index:row_data["start_index"]]
                    })
                valid_cond = True
            else:
                if valid_cond:
                    valid_data.append(row_data)
            counter +=1
        return valid_data

    def __wragle_data(self, content: str):

        lexr = Lexer(content)
        lexr.tokenize()

        parse = Parser(lexr.tokens, content)
        parse.parse()

        for val in parse.parse_comment:
            content = content.replace(val['raw'], "")

        find_value = re.findall(r"(\{\$)([a-zA-Z0-9_]{1,})(\})", content)
        if len(find_value) > 0:
            for val in find_value:
                content = content.replace("".join(val), self.args.get(val[1], ""))


        parse_tag = self.__get_cond_valid_data(parse.parse_tag,"tag")

        for val in parse_tag:
            raw_content,raw_bool = self.__set_value_in_tags(val)
            if raw_bool:
                content = content.replace(val["raw"], raw_content)

        for val in parse.parse_block:
            sub_content = ""
            append_row = self.__get_cond_valid_data(val["append"],"block")


            for sv in append_row:
                sub_content += self.__command_details(sv["type"], sv["content"].split("\n"), sub_content)
            content = content.replace(val["raw"], sub_content)

        return content

    def get_content(self):
        return self.content
