class Token:
    def __init__(self,type, raw,start_index,end_index):
        self.type = type
        self.raw = raw
        self.prep_raw = raw
        self.start_index = start_index
        self.end_index = end_index
