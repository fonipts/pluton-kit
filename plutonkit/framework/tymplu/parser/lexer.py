import re
from typing import List

from plutonkit.model.dto.token import Token
from plutonkit.model.enum.token_type import TokenType


class Lexer:
    def __init__(self,code:str):
        self.code = code
        self.index = 0
        self.row=0
        self.col=0
        self.tokens: List[Token] = []

    def tokenize(self):
        while self.index <len(self.code):

            if self.code[self.index] == "(" :
                self.strip_syntax()
            else:
                self.index +=1

    def strip_syntax(self):
        start_index = self.index
        end_index = self.index
        self.index +=1
        open_case = 1

        valid = True
        while self.index <len(self.code) and valid:
            quote_char = self.code[self.index]

            if quote_char == "(":

                open_case +=1
            if quote_char == ")":

                open_case -=1
            self.index +=1
            if open_case <= 0:
                valid = False

        end_index = self.index
        codeStr = "".join(self.code[start_index:end_index])

        raw_match1 = re.search(r"[\(][\s\n]{0,}#", codeStr)
        if raw_match1:
            self.tokens.append(Token(TokenType.COMMENTS,codeStr,start_index,end_index))
        raw_match2 = re.search(r"[\(][\s\n]{0,}@([a-zA-Z0-9_]{1,})[\s\n]{1,}([a-zA-Z0-9_]{1,})", codeStr)
        if raw_match2:
            self.tokens.append(Token(TokenType.TAGS,codeStr,start_index,end_index))
        raw_match3 = re.search(r"^[\(][\s\n]{0,}[\{][\s\n]{0,}@([a-zA-Z0-9_]{1,})", codeStr)
        raw_match3a = re.search(r"[\s\n]{0,}[\}][\s\n]{0,}[\)]$", codeStr)
        if raw_match3 and raw_match3a:
            self.tokens.append(Token(TokenType.BLOCKS,codeStr,start_index,end_index))
