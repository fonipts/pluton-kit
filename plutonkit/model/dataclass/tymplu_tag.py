from dataclasses import dataclass


@dataclass
class TympluTag:
    raw:str
    content:str
    action:str
    type:str
    start_index:int
    end_index:int
