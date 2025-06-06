from plutonkit.helper.template import convert_template


class PLTemplate:
    def __init__(self,content:str):
        self.content:str = content
    def render(self,arg):
        return convert_template(self.content,arg,None)
