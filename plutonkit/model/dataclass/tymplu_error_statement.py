from dataclasses import dataclass


@dataclass
class TympluErrorStatement:
    type:str
    message:str
