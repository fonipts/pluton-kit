import copy
import os
import re
from typing import List

from plutonkit.framework.request.validate_source import ValidateSource
from plutonkit.framework.tymplu.condition.condition_delimiter import (
    ConditionDelimiter,
)
from plutonkit.framework.tymplu.condition.condition_identify import (
    ConditionIdentify,
)
from plutonkit.helper.format import (
    get_first_line_string_space, get_first_strings, get_str_if_empty,
)
from plutonkit.model.dataclass.tymplu_block_append import TympluBlockAppend
from plutonkit.model.dataclass.tymplu_error_parse import TympluErrorParse
from plutonkit.model.dataclass.tymplu_tag import TympluTag


class InterpreterBlock:
    def __init__(self,tokens:List[TympluTag],content:str,copy_content:str,args=None,template=None):
        self.tokens:List[TympluTag] = tokens
        self.args = args
        self.contents = copy_content
        self.errors:List[TympluErrorParse] = []
        self.raw_contents = content
        self.template = template

    def type_empty(self,_:TympluBlockAppend,__:List[TympluBlockAppend]):

        return ""

    def type_load(self,node:TympluBlockAppend,_:List[TympluBlockAppend]):

        content = node.content
        valid_source = ValidateSource(content)
        data_content = ""
        is_valid_template = False

        if valid_source.arch_type == "local":
            directory = os.getcwd()
            try:
                path = os.path.join(directory, content.strip())
                base_name = os.path.splitext(path)
                if len(base_name) > 1:
                    if re.match(r"^(.tpl)", base_name[1]):
                        is_valid_template = True
                f_read = open(path, "r", encoding="utf-8")
                data_content = str(f_read.read())
                f_read.close()

                if is_valid_template:
                    temp_cls = self.template(data_content,self.args)
                    #row_content = temp_cls.content
                    return temp_cls.content
                return ""
            except Exception as e:
                print("Invalid source:",e)
        return ""

    def type_content(self,node:TympluBlockAppend,_:List[TympluBlockAppend]):

        return node.content

    def type_condition(self,node:TympluBlockAppend,tokens:List[TympluBlockAppend]):

        end_for = True
        raw_tokens = []
        for token in copy.deepcopy(tokens):
            if token.type in {"end","condition"}:
                end_for = False
            if end_for:
                tokens.pop(0)
                raw_tokens.append(token)

        cond = ConditionDelimiter(node.content)

        for err in cond.error_recording:
            self.errors.append(TympluErrorParse(type="condition",message=err.message,content=node.content,end_index=0,start_index=0))

        cond_valid = ConditionIdentify(cond.arg_list,cond.error_recording,self.args)
        if cond_valid.validate():

            return self.sub_convert(raw_tokens, "")
        return ""

    def convert(self):
        if len(self.tokens)>0:
            node = self.tokens[0]
            self.tokens.pop(0)
            content = self.sub_convert(node.append, "")
            self.raw_contents = self.raw_contents.replace(node.raw, content,1)
            self.convert()

    def sub_convert(self, tokens:List[TympluBlockAppend], sub_content:str):
        if len(tokens)>0:
            node = tokens[0]
            tokens.pop(0)

            method_name = f"type_{node.type.lower()}"
            if hasattr(self, method_name) is False:
                method_name = "type_empty"
                self.errors.append(TympluErrorParse(type="type",message=f"Tag `{node.type}` is invalid",content=node.content,end_index=0,start_index=0))


            get_init_string = get_first_strings(node.content.split("\n"))
            get_str_count = get_first_line_string_space(get_init_string["content"])

            lst: list[str] = []
            empty_counter = 0
            for v in node.content.split("\n"):
                if get_str_if_empty(v):
                    if empty_counter<2:
                        lst.append("")
                    empty_counter +=1
                else:
                    empty_counter = 0
                    regex = re.compile("^[\\s]{0,"+str(get_str_count)+"}")
                    lst.append(str(regex.sub("", v)))
            node.content =  "\n".join(lst)
            sub_content += getattr(self, method_name)(node,tokens)


            return self.sub_convert(tokens, sub_content)

        return sub_content

    @property
    def content(self):
        return self.raw_contents
