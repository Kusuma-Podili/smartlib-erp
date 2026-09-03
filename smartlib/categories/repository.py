"""
Repository for Category and classification hierarchies.
"""

from typing import Optional, List
from smartlib.database.connection import DatabaseManager
from smartlib.categories.models import Category

class CategoryRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, category: Category) -> Category:
        sql = """
        INSERT INTO categories (code, name, dewey_decimal_class, parent_category_id, description)
        VALUES (?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(
            sql,
            (category.code, category.name, category.dewey_decimal_class, category.parent_category_id, category.description)
        )
        self.db_manager.get_connection().commit()
        category.category_id = cursor.lastrowid
        return category

    def get_by_id(self, category_id: int) -> Optional[Category]:
        sql = """
        SELECT category_id, code, name, dewey_decimal_class, parent_category_id, description, created_at
        FROM categories WHERE category_id = ?;
        """
        row = self.db_manager.fetch_one(sql, (category_id,))
        return Category(**dict(row)) if row else None

    def get_by_code(self, code: str) -> Optional[Category]:
        sql = """
        SELECT category_id, code, name, dewey_decimal_class, parent_category_id, description, created_at
        FROM categories WHERE LOWER(code) = LOWER(?);
        """
        row = self.db_manager.fetch_one(sql, (code.strip(),))
        return Category(**dict(row)) if row else None

    def list_all(self) -> List[Category]:
        sql = """
        SELECT category_id, code, name, dewey_decimal_class, parent_category_id, description, created_at
        FROM categories ORDER BY code ASC;
        """
        rows = self.db_manager.fetch_all(sql)
        return [Category(**dict(r)) for r in rows]

    def count(self) -> int:
        row = self.db_manager.fetch_one("SELECT COUNT(*) as cnt FROM categories;")
        return int(row["cnt"]) if row else 0
