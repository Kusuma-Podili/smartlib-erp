"""Data repository for return transactions."""
from typing import Optional, List
from smartlib.database.connection import DatabaseManager
from smartlib.returns.models import ReturnRecord

class ReturnRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, rec: ReturnRecord) -> ReturnRecord:
        sql = """
        INSERT INTO returns (borrowing_id, returned_date, received_by_librarian_id, overdue_days, fine_amount, condition_on_return, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(
            sql,
            (rec.borrowing_id, rec.returned_date, rec.received_by_librarian_id, rec.overdue_days, rec.fine_amount, rec.condition_on_return, rec.notes)
        )
        self.db_manager.get_connection().commit()
        rec.return_id = cursor.lastrowid
        return rec

    def get_by_borrowing_id(self, borrowing_id: int) -> Optional[ReturnRecord]:
        sql = """
        SELECT return_id, borrowing_id, returned_date, received_by_librarian_id, overdue_days, fine_amount, condition_on_return, notes, created_at
        FROM returns WHERE borrowing_id = ?;
        """
        row = self.db_manager.fetch_one(sql, (borrowing_id,))
        return ReturnRecord(**dict(row)) if row else None
