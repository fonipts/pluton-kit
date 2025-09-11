from typing import List

from plutonkit.framework.tymplu.condition.condition_delimiter import (
    ConditionDelimiter,
)
from plutonkit.framework.tymplu.condition.condition_identify import (
    ConditionIdentify,
)
from plutonkit.framework.tymplu.ext.strings import (
    convert_unique_value, unique_value_generator,
)
from plutonkit.model.dataclass.tymplu_error_parse import TympluErrorParse
from plutonkit.model.dataclass.tymplu_tag import TympluTag


class InterpreterTags:
    def __init__(self,tokens:List[TympluTag],content:str,copy_content:str,args=None,block=None):
        self.tokens:List[TympluTag] = tokens
        self.block=block
        self.contents = copy_content
        self.args = args
        self.errors:List[TympluErrorParse] = []
        self.raw_contents:str = content
        self.last_condition_statement = ""
        self.replace_char = unique_value_generator()

    def type_empty(self,node:TympluTag):
        self.raw_contents = self.raw_contents.replace(node.raw, self.replace_char,1)

    def type_block(self,node:TympluTag):


        if node.action in self.block:
            call_func= self.block[ node.action ]["func"](self.args)
            self.raw_contents = self.raw_contents.replace(node.raw, call_func,1)
        else:
            self.raw_contents = self.raw_contents.replace(node.raw, self.replace_char,1)

    def type_each(self,node:TympluTag):
        if node.action== "for":
            pass
    def type_condition(self,node:TympluTag):

        valid_cond = False
        if node.action== "if":
            cond = ConditionDelimiter(node.content)

            for err in cond.error_recording:
                self.errors.append(TympluErrorParse(type="condition",
                    message=err.message,content=node.content,end_index=0,start_index=0))

            cond_valid = ConditionIdentify(cond.arg_list,cond.error_recording,self.args)
            valid_cond = cond_valid.validate()

            if self.last_condition_statement !="valid":
                self.last_condition_statement = node.action

            if valid_cond:
                self.last_condition_statement = "valid"

        if node.action== "else":
            valid_cond = self.last_condition_statement == "if"
            self.last_condition_statement = ""

        next_token = self._get_next_token(node)

        if valid_cond:
            self.raw_contents = self.raw_contents.replace(node.raw, self.replace_char)
        else:
            if next_token is None:
                self.raw_contents = self.raw_contents.replace(node.raw+self.contents[node.end_index:], self.replace_char,1)
            else:
                self.raw_contents = self.raw_contents.replace(node.raw+self.contents[node.end_index:next_token.start_index], self.replace_char,1)

    def _get_next_token(self,node):
        get_node = None
        if len(self.tokens)>0:
            next_token = self.tokens[0]
            self.tokens.pop(0)
            if next_token.type.lower() == "end":
                self.raw_contents = self.raw_contents.replace(next_token.raw, self.replace_char,1)
                if node.action == next_token.action:
                    get_node = next_token
                else:
                    self.errors.append(TympluErrorParse(type="end",message=f"Missing @(end {node.action} {node.type}) at end of {node.type}",
                        content=node.raw,end_index=node.end_index,start_index=node.start_index))
            else:
                self.raw_contents = self.raw_contents.replace(next_token.raw, self.replace_char,1)
                self.errors.append(TympluErrorParse(type="end",message=f"Missing @(end {node.action} {node.type}) at end of {node.type}",
                    content=node.raw,end_index=node.end_index,start_index=node.start_index))
        else:
            self.errors.append(TympluErrorParse(type="end",message=f"Missing @(end {node.action} {node.type}) at end of {node.type}",
                content=node.raw,end_index=node.end_index,start_index=node.start_index))
        return get_node
    def convert(self):

        if len(self.tokens)>0:
            node = self.tokens[0]
            self.tokens.pop(0)
            method_name = f"type_{node.type.lower()}"
            if hasattr(self, method_name) is False:
                method_name = "type_empty"
                self.errors.append(TympluErrorParse(type="type",message=f"Tag `{node.type}` is invalid",
                    content=node.raw,end_index=node.end_index,start_index=node.start_index))
            if self.raw_contents.find(node.raw) == -1:
                method_name = "type_empty"

            getattr(self, method_name)(node)
            self.convert()

    @property
    def content(self)->str:
        self.raw_contents = convert_unique_value(raw_contents=self.raw_contents, replace_char=self.replace_char)
        return self.raw_contents
