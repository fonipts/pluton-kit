from dataclasses import dataclass


@dataclass
class TympluComment:
    raw:str
    content:str
    start_index:int
    end_index:int
