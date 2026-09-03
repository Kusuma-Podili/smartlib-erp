"""Serialized Cashier Desk Receipt Generator: REC-{YEAR}-{INDEX:05d}."""
import datetime
from typing import Optional
from smartlib.database.connection import DatabaseManager

class ReceiptGenerator:
    @staticmethod
    def generate_receipt_number(db_manager: Optional[DatabaseManager] = None) -> str:
        db = db_manager or DatabaseManager.get_instance()
        year = datetime.date.today().year
        row = db.fetch_one(
            "SELECT COUNT(*) as cnt FROM payments WHERE receipt_number LIKE ?;",
            (f"REC-{year}-%",)
        )
        idx = (int(row["cnt"]) if row else 0) + 1
        return f"REC-{year}-{idx:05d}"
