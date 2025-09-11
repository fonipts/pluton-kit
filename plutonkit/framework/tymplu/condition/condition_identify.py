import re
from typing import List

from plutonkit.helper.arguments import get_dict_value
from plutonkit.model.dataclass.tymplu_error_statement import (
    TympluErrorStatement,
)
from plutonkit.model.dataclass.tymplu_valid_statement import (
    TympluValidStatement,
)


class ConditionIdentify:
    def __init__(self, valids:List[TympluValidStatement], errors:List[TympluErrorStatement],arg):

        self.valids:List[TympluValidStatement] = valids
        self.errors:List[TympluErrorStatement] = errors
        self.arg = arg

    def action_equal(self,key,value):

        return self.data_format(key) == self.data_format(value)

    def action_not_equal(self,key,value):

        return self.data_format(key) != self.data_format(value)

    def action_greater(self,key,value):
        return self.data_format(key) > self.data_format(value)

    def action_greater_equal(self,key,value):
        return self.data_format(key) >= self.data_format(value)


    def action_less(self,key,value):
        return self.data_format(key) < self.data_format(value)

    def action_less_equal(self,key,value):
        return self.data_format(key) <= self.data_format(value)

    def data_format(self,value):
        value = str(value)
        is_int = re.match(r"^[0-9]+$",value)
        if is_int:
            return int(value)
        is_float = re.match(r"^[0-9]+$",value)
        if is_float:
            return float(value)
        if value in {"True"}:
            return True
        if value in {"False"}:
            return False
        if len(value)>1:
            if value[0] in {"'",'"'}:
                return value[1:len(value)-1]
        return value

    def validate(self):
        if len(self.errors)>0:
            return False

        valid_counter = 0
        for val in self.valids:
            method_name = f"action_{val.action.lower()}"
            if hasattr(self, method_name):
                key_state = get_dict_value(val.key.split("."), self.arg) or val.key
                value_state = get_dict_value(val.value.split("."), self.arg) or val.value
                if getattr(self, method_name)(key_state,value_state):
                    valid_counter +=1
        return valid_counter ==  len(self.valids)
