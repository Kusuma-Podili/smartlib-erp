"""Serialized Patron ID / Card Code Generator: MEM-{YEAR}-{INDEX:04d}."""
import datetime
from typing import Optional
from smartlib.database.connection import DatabaseManager

class MemberIdGenerator:
    @staticmethod
    def generate_next_code(db_manager: Optional[DatabaseManager] = None) -> str:
        db = db_manager or DatabaseManager.get_instance()
        year = datetime.date.today().year
        row = db.fetch_one(
            "SELECT COUNT(*) as cnt FROM members WHERE member_code LIKE ?;",
            (f"MEM-{year}-%",)
        )
        idx = (int(row["cnt"]) if row else 0) + 1
        return f"MEM-{year}-{idx:04d}"
