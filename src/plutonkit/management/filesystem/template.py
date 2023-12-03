import re

class Template:
    def __init__(self,content,filename) -> None:
        self.content = content
        self.filename = filename
    def setVariable(self,argument = {}):
        results = re.findall(r"(\(\{[\s]{0,}[a-zA-Z\_]{1,}[\s]{0,}\}\))",self.content)

        for val in results:
            key_re = val.replace("({","" ).replace("})","" )
            ref_value  = argument.get(key_re,"")
            self.content = self.content.replace(val,ref_value)
    def getContent(self):
        return  self.content
