"""
Data access repository for Author entities.
"""

from typing import Optional, List, Dict, Any
from smartlib.database.connection import DatabaseManager
from smartlib.authors.models import Author

class AuthorRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, author: Author) -> Author:
        sql = """
        INSERT INTO authors (name, biography, nationality, birth_year, death_year, website)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(
            sql,
            (author.name, author.biography, author.nationality, author.birth_year, author.death_year, author.website)
        )
        self.db_manager.get_connection().commit()
        author.author_id = cursor.lastrowid
        return author

    def get_by_id(self, author_id: int) -> Optional[Author]:
        sql = """
        SELECT author_id, name, biography, nationality, birth_year, death_year, website, created_at
        FROM authors WHERE author_id = ?;
        """
        row = self.db_manager.fetch_one(sql, (author_id,))
        return Author(**dict(row)) if row else None

    def get_by_name(self, name: str) -> Optional[Author]:
        sql = """
        SELECT author_id, name, biography, nationality, birth_year, death_year, website, created_at
        FROM authors WHERE LOWER(name) = LOWER(?);
        """
        row = self.db_manager.fetch_one(sql, (name.strip(),))
        return Author(**dict(row)) if row else None

    def list_all(self, search: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[Author]:
        clauses = []
        params = []
        if search:
            clauses.append("name LIKE ?")
            params.append(f"%{search.strip()}%")
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        sql = f"""
        SELECT author_id, name, biography, nationality, birth_year, death_year, website, created_at
        FROM authors
        {where}
        ORDER BY name ASC
        LIMIT ? OFFSET ?;
        """
        params.extend([limit, offset])
        rows = self.db_manager.fetch_all(sql, tuple(params))
        return [Author(**dict(r)) for r in rows]

    def count(self) -> int:
        row = self.db_manager.fetch_one("SELECT COUNT(*) as cnt FROM authors;")
        return int(row["cnt"]) if row else 0
