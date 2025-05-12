import re
from copy import deepcopy

from plutonkit.framework.logic.ConditionSplit import ConditionSplit


class TemplateStructTags:
    def __init__(self, contents: str, args=None):
        self.args = args
        self.contents: list[str] = contents.split("\n")
        self.join_contents = ""
        self.template: list[str] = self.__find_template(self.contents)

        self.__verify_condition(self.template)

    def _clean_content(self,raw):
        return re.sub(r"^\{","",raw)

    def __find_template(self, contents: list[str]):
        templates = []
        rows = []
        raw_name = None
        raw_type = None
        row_count =1
        ref_row_count = 0
        for content in contents:
            raw_match = re.search(r"[\(][\s\n]{0,}@([a-z]{1,})[\s]{1,}([a-zA-Z0-9\_]{1,})([\s\n]{1,}[\{]{0,}|[\s\n\{]{1,})(.*?)[\s\n\}]{0,}[\s\n]{0,}[\)]",content)
            if raw_match:
                templates.append({
                    "name":raw_match[2],
                    "template":raw_match[0],
                    "type":raw_match[1],
                    "content": self._clean_content(raw_match[4]),
                    "start_row":row_count,
                    "end_row":row_count
                })
            else:
                if len(rows) > 0:
                    if re.match(r"[\s\n\}]{0,}[\)]{1}", content):

                        rows.append(content)
                        templates.append({
                            "name":raw_name,
                            "template":"\n".join(deepcopy(rows)),
                            "type":raw_type,
                            "content":self._clean_content( "\n".join(deepcopy(rows)[1:len(deepcopy(rows))-1]) ),
                            "start_row":ref_row_count,
                            "end_row":row_count
                        })
                        rows = []
                        raw_name = None
                        raw_type = None
                    else:
                        rows.append(content)

                raw_match1 = re.match(r"[\(][\s\n]{0,}@([a-z]{1,})[\s]{1,}([a-zA-Z0-9\_]{1,})([\s\n]{1,}[\{]{0,}|[\s\n\{]{1,})", content)
                if raw_match1:
                    raw_name = raw_match1[2]
                    raw_type = raw_match1[1]
                    ref_row_count = row_count
                    rows.append(content)
            row_count +=1

        return templates

    def __verify_condition(self,templates):

        raw_list = []


        ref_range_cond =  [ [x["start_row"],x["end_row"]] for x in templates if x["type"] == "condition"]
        counter = 0
        for template in templates:
            if template["type"] == "condition":
                if template["name"] == "if":
                    cond = ConditionSplit(template["content"] ,  self.args )

                    if cond.validCond() is False:
                        if counter+1 < len(ref_range_cond):
                            raw_list += list(range(template["start_row"],  ref_range_cond[counter+1][0]) )

                counter +=1

        raw_content = []

        for key,value in enumerate(self.contents):
            if key+1 not in tuple(raw_list):
                raw_content.append(value)

        self.contents = raw_content

    def get_content(self) -> str:
        return "\n".join(self.contents)
