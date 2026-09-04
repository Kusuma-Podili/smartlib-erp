"""CQL Recursive Descent Parser."""

from typing import List, Optional
from dataclasses import dataclass
from .cql_lexer import CqlLexer, CqlToken, TokenType


@dataclass
class CqlNode:
    pass


@dataclass
class RelationNode(CqlNode):
    index: str
    relation: str
    term: str

    def __repr__(self) -> str:
        return f"RelationNode({self.index} {self.relation} '{self.term}')"


@dataclass
class BooleanNode(CqlNode):
    operator: str
    left: CqlNode
    right: CqlNode

    def __repr__(self) -> str:
        return f"BooleanNode({self.operator} left={self.left}, right={self.right})"


class CqlParser:
    """Parses token stream into an Abstract Syntax Tree (AST)."""

    def __init__(self, tokens: List[CqlToken]):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> CqlToken:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else self.tokens[-1]

    def advance(self) -> CqlToken:
        tok = self.current()
        self.pos += 1
        return tok

    def parse(self) -> Optional[CqlNode]:
        if self.current().type == TokenType.EOF:
            return None
        return self._parse_boolean()

    def _parse_boolean(self) -> CqlNode:
        left = self._parse_primary()
        while self.current().type in [TokenType.AND, TokenType.OR, TokenType.NOT, TokenType.PROX]:
            op_tok = self.advance()
            right = self._parse_primary()
            left = BooleanNode(operator=op_tok.value.upper(), left=left, right=right)
        return left

    def _parse_primary(self) -> CqlNode:
        tok = self.current()
        if tok.type == TokenType.LPAREN:
            self.advance()
            node = self._parse_boolean()
            if self.current().type == TokenType.RPAREN:
                self.advance()
            return node

        # Term or Index Relation Term
        if tok.type == TokenType.TERM:
            first_term = self.advance().value
            if self.current().type == TokenType.RELATION:
                rel = self.advance().value
                term = self.advance().value if self.current().type == TokenType.TERM else ""
                return RelationNode(index=first_term, relation=rel, term=term)
            else:
                return RelationNode(index="anywhere", relation="=", term=first_term)

        return RelationNode(index="anywhere", relation="=", term="")
