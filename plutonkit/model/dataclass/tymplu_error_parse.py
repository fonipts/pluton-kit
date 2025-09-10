from dataclasses import dataclass


@dataclass
class TympluErrorParse:
    type:str
    content:str
    message:str
    start_index:int
    end_index:int
