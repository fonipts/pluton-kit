from typing import List

from plutonkit.model.dataclass.tymplu_comment import TympluComment


class InterpreterComment:
    def __init__(self,tokens:List[TympluComment],content:str):
        self.tokens = tokens
        self.contents = content
        self.raw_contents = content
    def convert(self):
        for val in self.tokens:
            self.raw_contents = self.raw_contents.replace(val.raw, "")
    @property
    def content(self):
        return self.raw_contents
