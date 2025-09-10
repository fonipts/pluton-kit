import re
from typing import List

from plutonkit.model.dataclass.tymplu_block import TympluBlock
from plutonkit.model.dataclass.tymplu_block_append import TympluBlockAppend
from plutonkit.model.dataclass.tymplu_comment import TympluComment
from plutonkit.model.dataclass.tymplu_tag import TympluTag
from plutonkit.model.dto.token import Token


class Parser:
    def __init__(self, tokens:List[Token],code:str):
        self.tokens:List[Token] = tokens
        self.code = code
        self.parse_block:List[TympluBlock] = []
        self.parse_tag:List[TympluTag] = []
        self.parse_comment:List[TympluComment] = []

        self.remove_comment = []

    def parse(self):
        for node in self.tokens:
            method_name = f"visit_{node.type.name.lower()}"
            if hasattr(self, method_name) and method_name =="visit_comments":
                getattr(self, method_name)(node)

        for node in self.tokens:
            method_name = f"visit_{node.type.name.lower()}"
            if hasattr(self, method_name) and method_name !="visit_comments":
                for vv in self.remove_comment:
                    node.prep_raw = node.prep_raw.replace(vv,"")

                getattr(self, method_name)(node)

    def visit_blocks(self, node:Token):
        raw = node.prep_raw[2:len(node.prep_raw)-2]

        row = 0
        rows_count = 0
        row_name = ""
        row_content = ""
        append_row = []
        for rr in raw.split("\n"):
            start_value = re.findall(r"@([a-zA-Z0-9_]{1,})[\t\s]{0,}([\{\}]{0,})", rr)

            rr_val = rr
            if start_value:

                rr_val = ""
                row_name = start_value[0][0]

            if row_name !="":
                findall_open = len(re.findall(r"{", rr))
                findall_close = len(re.findall(r"}", rr))
                if findall_open > 0:
                    rows_count += findall_open
                if findall_close > 0:
                    rows_count -= findall_close
                if rows_count>0:
                    row_content +=rr_val+"\n"
                if rows_count==0 :
                    append_row.append(TympluBlockAppend(type=row_name,
                        content=row_content))

                    row_content = ""
                    row_name = ""
            row +=1
        self.parse_block.append(TympluBlock(
                    raw=node.raw,
                    start_index=node.start_index,
                    end_index=node.end_index,
                    append=append_row
        )
    )


    def visit_tags(self, node:Token):
        raw = node.prep_raw[1:len(node.prep_raw)-1]
        raw_match = re.match(r"[\s\n]{0,}@([a-z]{1,})[\s]{1,}([a-zA-Z0-9\_]{1,})", raw)
        content = ""
        split_a1 = raw.split("{")
        if len(split_a1)>1:
            content =split_a1[1].split("}")[0]

        if raw_match:
            self.parse_tag.append(TympluTag(
                raw=node.raw,
                content=content,
                action=raw_match[2],
                type=raw_match[1],
                start_index=node.start_index,
                end_index=node.end_index
            ))

    def visit_comments(self, node:Token):

        raw_match3 = re.search(r"([\(][\s\n]{0,}#[\s\n]{0,}[\)])", node.raw)
        if raw_match3:
            rown = "".join(self.code[node.start_index:].split(raw_match3[0])[1:])
            rown = rown.split("\n")

            if len(rown)>0:

                self.parse_comment.append(TympluComment(
                    raw=raw_match3[0]+rown[0],
                    content=rown[0].lstrip(),
                    start_index=node.start_index,
                    end_index=node.start_index + len(rown[0].lstrip())
                ))
                self.remove_comment.append(raw_match3[0]+rown[0])
        else:
            raw_match_start = re.search(r"^([\(][\s\n]{0,}#[\s\n]{0,})",node.raw)
            raw_match_end = re.search(r"([\s\n]{0,}#[\s\n]{0,}[\)])$",node.raw)
            if raw_match_start and raw_match_end:
                new_text = re.sub(r"^([\(][\s\n]{0,}#[\s\n]{0,})", "", node.raw, flags=re.IGNORECASE)
                new_text = re.sub(r"([\s\n]{0,}#[\s\n]{0,}[\)])$", "", new_text, flags=re.IGNORECASE)

                self.parse_comment.append(TympluComment(
                    raw=node.raw,
                    content=new_text,
                    start_index=node.start_index,
                    end_index=node.end_index
                ))
                node.raw = ""
                self.remove_comment.append(node.raw)
