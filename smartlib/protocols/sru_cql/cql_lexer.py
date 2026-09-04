"""Common Query Language (CQL) Lexical Analyzer."""

from enum import Enum, auto
from typing import List, Optional
from dataclasses import dataclass


class TokenType(Enum):
    TERM = auto()
    RELATION = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    PROX = auto()
    LPAREN = auto()
    RPAREN = auto()
    PREFIX = auto()
    EOF = auto()


@dataclass
class CqlToken:
    type: TokenType
    value: str
    position: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', pos={self.position})"


class CqlLexer:
    """Converts a CQL query string into a stream of tokens."""

    def __init__(self, query: str):
        self.query = query
        self.length = len(query)
        self.pos = 0

    def tokenize(self) -> List[CqlToken]:
        tokens = []
        while self.pos < self.length:
            c = self.query[self.pos]
            if c.isspace():
                self.pos += 1
                continue
            elif c == "(":
                tokens.append(CqlToken(TokenType.LPAREN, "(", self.pos))
                self.pos += 1
            elif c == ")":
                tokens.append(CqlToken(TokenType.RPAREN, ")", self.pos))
                self.pos += 1
            elif c == '"':
                start = self.pos
                self.pos += 1
                s = []
                while self.pos < self.length and self.query[self.pos] != '"':
                    s.append(self.query[self.pos])
                    self.pos += 1
                self.pos += 1  # closing quote
                tokens.append(CqlToken(TokenType.TERM, "".join(s), start))
            elif c in "=<>":
                start = self.pos
                rel = c
                self.pos += 1
                if self.pos < self.length and self.query[self.pos] in "=>":
                    rel += self.query[self.pos]
                    self.pos += 1
                tokens.append(CqlToken(TokenType.RELATION, rel, start))
            else:
                start = self.pos
                buf = []
                while self.pos < self.length and not self.query[self.pos].isspace() and self.query[self.pos] not in '()="<>':
                    buf.append(self.query[self.pos])
                    self.pos += 1
                word = "".join(buf)
                upper = word.upper()
                if upper == "AND":
                    tokens.append(CqlToken(TokenType.AND, word, start))
                elif upper == "OR":
                    tokens.append(CqlToken(TokenType.OR, word, start))
                elif upper == "NOT":
                    tokens.append(CqlToken(TokenType.NOT, word, start))
                elif upper == "PROX":
                    tokens.append(CqlToken(TokenType.PROX, word, start))
                elif word.lower() in ["all", "any", "exact", "within"]:
                    tokens.append(CqlToken(TokenType.RELATION, word, start))
                else:
                    tokens.append(CqlToken(TokenType.TERM, word, start))

        tokens.append(CqlToken(TokenType.EOF, "", self.pos))
        return tokens
