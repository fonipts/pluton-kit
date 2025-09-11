from typing import List

from plutonkit.framework.tymplu.ext.strings import (
    convert_unique_value, unique_value_generator,
)
from plutonkit.model.dataclass.tymplu_comment import TympluComment


class InterpreterComment:
    def __init__(self,tokens:List[TympluComment],content:str):
        self.tokens = tokens
        self.contents = content
        self.raw_contents = content
        self.replace_char = unique_value_generator()
    def convert(self):

        for val in self.tokens:
            self.raw_contents = self.raw_contents.replace(val.raw, self.replace_char,1)

        self.raw_contents = convert_unique_value(raw_contents=self.raw_contents, replace_char=self.replace_char)
    @property
    def content(self)->str:
        return self.raw_contents
