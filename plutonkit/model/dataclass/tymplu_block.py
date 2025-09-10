from dataclasses import dataclass
from typing import List

from plutonkit.model.dataclass.tymplu_block_append import TympluBlockAppend


@dataclass
class TympluBlock:
    raw:str
    start_index:int
    end_index:int
    append:List[TympluBlockAppend]
