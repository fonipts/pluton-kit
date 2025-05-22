import re

class TemplateCommentOut:
    def __init__(self, contents: str):

        self.contents: list[str] = contents.split("\n")
        self.join_contents = ""
        self.templates: list[str] = self.__find_template(self.contents)


    def _clean_content(self,raw):
        return re.sub(r"^\{","",raw)

    def __find_template(self, contents: list[str]):
        templates = []
        rows_content = []
        row_count =1
        ref_row_count = 0
        is_open_comment = False
        for content in contents:
            raw_match = re.match(r"([\(])[\s\n]{0,}#[\s\n]{0,}[\(]{0}(.*?)[\)]{0}[\s\n]{0,}#[\s\n]{0,}([\)])",content)
            if raw_match:
                templates.append({
                            "type":"whole_comment",
                            "template":raw_match[0],
                            "start_row":row_count,
                            "end_row":row_count
                        })
            else:
                if is_open_comment is False:
                    raw_match1 = re.match(r"([\(][\s]{0,}#[\s\n]{0,})",content)
                    if raw_match1:
                        ref_row_count = row_count
                        is_open_comment = True
                        split_sign = raw_match1[1]
                        splt_msg = split_sign.join(  content.split(raw_match1[1])[1:] )
                        rows_content.append(f"{split_sign}{splt_msg}")
                else:
                    raw_match2 = re.search(r"([\s\n]{0,}#[\s]{0,}[\)])",content)
                    if raw_match2:
                        is_open_comment = False

                        split_sign = raw_match2[1]
                        splt_msg = split_sign.join(  content.split( split_sign )[:1] )
                        rows_content.append(f"{splt_msg}{split_sign}")
                        templates.append({
                            "type":"whole_comment",
                            "template":"\n".join(rows_content),
                            "start_row":ref_row_count,
                            "end_row":row_count
                        })
                        rows_content = []
                    else:
                        rows_content.append(content)

            raw_match3 = re.search(r"([\(][\s\n]{0,}#[\s\n]{0,}[\)])", content)

            if raw_match3:
                split_sign = raw_match3[1]
                splt_msg = split_sign.join(  content.split(raw_match3[1])[1:] )
                templates.append({

                            "template":f"{split_sign}{splt_msg}",
                            "type":"single_comment",
                            "start_row":row_count,
                            "end_row":row_count
                        })
            row_count +=1

        return templates


    def get_remove_comment_content(self) -> str:
        ref_content = "\n".join(self.contents)
        for template in self.templates:
            ref_content = ref_content.replace(template["template"],"")
        return ref_content
