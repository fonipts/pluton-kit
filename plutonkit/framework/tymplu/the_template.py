import re
from typing import List

from plutonkit.framework.tymplu.interpreter.interpreter_block import (
    InterpreterBlock,
)
from plutonkit.framework.tymplu.interpreter.interpreter_comment import (
    InterpreterComment,
)
from plutonkit.framework.tymplu.interpreter.interpreter_tags import (
    InterpreterTags,
)
from plutonkit.framework.tymplu.parser.lexer import Lexer
from plutonkit.framework.tymplu.parser.parser import Parser
from plutonkit.model.dataclass.tymplu_error_parse import TympluErrorParse


class TheTemplate:
    def __init__(self, content: str, args=None,block=None):
        self.raw_content = content
        self.block = block
        self.errors:List[TympluErrorParse] = []
        self.args = args
        self.content = self.__wragle_data(content)
    def convert_arg(self,content):
        find_value = re.findall(r"(\{\$)([a-zA-Z0-9_]{1,})(\})", content)
        if len(find_value) > 0:
            for val in find_value:
                content = content.replace("".join(val), self.args.get(val[1], ""))
        return content

    def _get_lex_parser(self, content)->Parser:
        lexr = Lexer(content)
        lexr.tokenize()
        parse = Parser(lexr.tokens, content)
        parse.parse()

        return parse

    def __wragle_data(self, content: str):

        parse_comment = self._get_lex_parser(content)

        temp_comment = InterpreterComment(parse_comment.parse_comment, content)
        temp_comment.convert()
        raw_content=temp_comment.content


        raw_content = self.convert_arg(raw_content)


        #lexr = Lexer(raw_content)
        #lexr.tokenize()
        #parse = Parser(lexr.tokens, raw_content)
        #parse.parse()

        parse_tag = self._get_lex_parser(raw_content)

        #print(parse.parse_tag,"::parse.parse_tag")
        #print(parse.parse_tag,":parse_tag:")
        temp_tags = InterpreterTags(parse_tag.parse_tag, raw_content,raw_content,self.args,self.block)
        temp_tags.convert()
        raw_content=temp_tags.content

        #print(parse.parse_block,":errors:")

        #lexr = Lexer(raw_content)
        #lexr.tokenize()
        #parse = Parser(lexr.tokens, raw_content)
        #parse.parse()

        parse_block = self._get_lex_parser(raw_content)

        temp_block = InterpreterBlock(parse_block.parse_block, raw_content,raw_content,self.args,TheTemplate)
        temp_block.convert()
        raw_content=temp_block.content

        self.errors = temp_block.errors+temp_tags.errors

        return raw_content
