"""
Repository for publisher records.
"""

from typing import Optional, List
from smartlib.database.connection import DatabaseManager
from smartlib.publishers.models import Publisher

class PublisherRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, pub: Publisher) -> Publisher:
        sql = """
        INSERT INTO publishers (name, contact_email, phone, address, website, country)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(
            sql,
            (pub.name, pub.contact_email, pub.phone, pub.address, pub.website, pub.country)
        )
        self.db_manager.get_connection().commit()
        pub.publisher_id = cursor.lastrowid
        return pub

    def get_by_id(self, publisher_id: int) -> Optional[Publisher]:
        sql = """
        SELECT publisher_id, name, contact_email, phone, address, website, country, created_at
        FROM publishers WHERE publisher_id = ?;
        """
        row = self.db_manager.fetch_one(sql, (publisher_id,))
        return Publisher(**dict(row)) if row else None

    def get_by_name(self, name: str) -> Optional[Publisher]:
        sql = """
        SELECT publisher_id, name, contact_email, phone, address, website, country, created_at
        FROM publishers WHERE LOWER(name) = LOWER(?);
        """
        row = self.db_manager.fetch_one(sql, (name.strip(),))
        return Publisher(**dict(row)) if row else None

    def list_all(self) -> List[Publisher]:
        sql = """
        SELECT publisher_id, name, contact_email, phone, address, website, country, created_at
        FROM publishers ORDER BY name ASC;
        """
        rows = self.db_manager.fetch_all(sql)
        return [Publisher(**dict(r)) for r in rows]

    def count(self) -> int:
        row = self.db_manager.fetch_one("SELECT COUNT(*) as cnt FROM publishers;")
        return int(row["cnt"]) if row else 0
