from dataclasses import dataclass


@dataclass
class FormatArgumentInput:
    name:str
    type:str
    question:str
    config:str
    option_name:str
