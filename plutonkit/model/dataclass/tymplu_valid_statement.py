from dataclasses import dataclass


@dataclass
class TympluValidStatement:
    statement:str
    condition:str
    action:str
    key:str
    value:str
