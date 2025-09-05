from plutonkit.model.enum.token_type import TokenType


class Token:
    def __init__(self,types:TokenType, raw:str,start_index:int,end_index:int):
        self.type = types
        self.raw = raw.strip()
        self.prep_raw = raw.strip()
        self.start_index = start_index
        self.end_index = end_index
