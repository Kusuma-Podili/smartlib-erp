"""CQL Evaluator translating AST to SQL queries and filter predicates."""

from typing import Tuple, List, Any
from .cql_parser import CqlNode, RelationNode, BooleanNode


class CqlEvaluator:
    """Translates CQL AST into parameterized SQL WHERE clauses."""

    INDEX_MAP = {
        "title": "books.title",
        "dc.title": "books.title",
        "author": "authors.name",
        "dc.creator": "authors.name",
        "isbn": "books.isbn",
        "subject": "categories.name",
        "dc.subject": "categories.name",
        "anywhere": "(books.title || ' ' || coalesce(books.description, '') || ' ' || coalesce(books.isbn, ''))"
    }

    def evaluate_to_sql(self, node: CqlNode) -> Tuple[str, List[Any]]:
        """Return (sql_where_clause, parameter_list)."""
        if node is None:
            return "1=1", []

        if isinstance(node, RelationNode):
            col = self.INDEX_MAP.get(node.index.lower(), "books.title")
            val = node.term
            rel = node.relation.lower()

            if rel in ["=", "all", "exact"]:
                return f"{col} LIKE ?", [f"%{val}%"]
            elif rel == "any":
                words = val.split()
                clauses = [f"{col} LIKE ?" for _ in words]
                return f"({' OR '.join(clauses)})", [f"%{w}%" for w in words]
            elif rel == "<":
                return f"{col} < ?", [val]
            elif rel == "<=":
                return f"{col} <= ?", [val]
            elif rel == ">":
                return f"{col} > ?", [val]
            elif rel == ">=":
                return f"{col} >= ?", [val]
            elif rel in ["<>", "/="]:
                return f"{col} NOT LIKE ?", [f"%{val}%"]
            return f"{col} LIKE ?", [f"%{val}%"]

        elif isinstance(node, BooleanNode):
            left_sql, left_params = self.evaluate_to_sql(node.left)
            right_sql, right_params = self.evaluate_to_sql(node.right)
            if node.operator == "AND":
                return f"({left_sql} AND {right_sql})", left_params + right_params
            elif node.operator == "OR":
                return f"({left_sql} OR {right_sql})", left_params + right_params
            elif node.operator == "NOT":
                return f"({left_sql} AND NOT ({right_sql}))", left_params + right_params

        return "1=1", []
