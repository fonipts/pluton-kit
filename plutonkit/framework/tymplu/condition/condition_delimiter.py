import re
from typing import List

from plutonkit.model.dataclass.tymplu_error_statement import (
    TympluErrorStatement,
)
from plutonkit.model.dataclass.tymplu_valid_statement import (
    TympluValidStatement,
)


class ConditionDelimiter:
    def __init__(self, cond: str):
        self.action = {
            "==":"equal",
            ">":"greater",
            ">=":"greater_equal",
            "<":"less",
            "<=":"less_equal",
            "!=":"not_equal"
        }
        self.cond: str = cond.strip()

        self.arg_list:List[TympluValidStatement] = []
        self.error_recording:List[TympluErrorStatement] = []
        self.__bootload()

    def validate_cond(self,cond):
        find_value = re.findall(r"(.*?)\s{0,}([=]{2}|!\=|<\=|>\=|<|>)", cond.strip())
        if len(find_value) == 1:

            raw_key = find_value[0][0]
            raw_cond = find_value[0][1]
            raw_value = ""
            value_split = cond.split(raw_cond)

            if len(value_split) > 0:
                raw_value = value_split[1].strip()

            else:
                self.error_recording.append(TympluErrorStatement(type="condition",message="No value found in statement"))

            if raw_cond in self.action:
                self.arg_list.append( TympluValidStatement(statement=cond,
                    condition=raw_cond,
                    key=raw_key,
                    action=self.action[raw_cond],
                    value=raw_value) )
            else:
                self.error_recording.append(TympluErrorStatement(type="condition",message="Condition is not allowed "))
        else:
            self.error_recording.append(TympluErrorStatement(type="newline",message="No delimiter like && and || found in the statement"))

    def __bootload(self):
        last_char = ""
        last_delimiter = ""
        is_open_qoute = False
        qoute_counter = 0
        for k,v in enumerate(self.cond):
            if k>0:
                last_char = self.cond[k-1]
            if v in ['"',"'"]:
                qoute_counter+=1
                is_open_qoute = (qoute_counter%2)==1

            if v in ["|","&"]:
                if is_open_qoute is False:

                    if last_char == v:
                        last_delimiter = last_char + v
                        split_str = self.cond.split(last_delimiter)

                        self.validate_cond(  split_str[len(self.arg_list)-1] )

        if is_open_qoute is False:

            if last_delimiter != "":
                split_str = self.cond.split(last_delimiter)

                self.validate_cond(  split_str[len(self.arg_list)-1] )
            else:
                self.validate_cond(self.cond)
        if len(self.arg_list) ==0:
            self.error_recording.append(TympluErrorStatement(type="condition",message="no valid condition found"))
