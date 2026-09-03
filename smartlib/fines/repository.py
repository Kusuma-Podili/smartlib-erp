"""Data access repository for fines."""
from typing import Optional, List
from smartlib.database.connection import DatabaseManager
from smartlib.fines.models import Fine

class FineRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, f: Fine) -> Fine:
        sql = """
        INSERT INTO fines (member_id, borrowing_id, fine_type, amount, paid_amount, balance_amount, status, reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(
            sql,
            (f.member_id, f.borrowing_id, f.fine_type, f.amount, f.paid_amount, f.balance_amount, f.status, f.reason)
        )
        self.db_manager.get_connection().commit()
        f.fine_id = cursor.lastrowid
        return f

    def get_by_id(self, fine_id: int) -> Optional[Fine]:
        sql = """
        SELECT f.*, (m.first_name || ' ' || m.last_name) as member_name, m.member_code, b.title as book_title
        FROM fines f
        JOIN members m ON f.member_id = m.member_id
        LEFT JOIN borrowings br ON f.borrowing_id = br.borrowing_id
        LEFT JOIN books b ON br.book_id = b.book_id
        WHERE f.fine_id = ?;
        """
        row = self.db_manager.fetch_one(sql, (fine_id,))
        return Fine(**dict(row)) if row else None

    def list_by_member(self, member_id: int) -> List[Fine]:
        sql = """
        SELECT f.*, (m.first_name || ' ' || m.last_name) as member_name, m.member_code, b.title as book_title
        FROM fines f
        JOIN members m ON f.member_id = m.member_id
        LEFT JOIN borrowings br ON f.borrowing_id = br.borrowing_id
        LEFT JOIN books b ON br.book_id = b.book_id
        WHERE f.member_id = ?
        ORDER BY f.fine_id DESC;
        """
        rows = self.db_manager.fetch_all(sql, (member_id,))
        return [Fine(**dict(r)) for r in rows]

    def update_balance_and_status(self, fine_id: int, paid_amount: float, balance_amount: float, status: str) -> None:
        sql = """
        UPDATE fines
        SET paid_amount = ?, balance_amount = ?, status = ?
        WHERE fine_id = ?;
        """
        self.db_manager.execute(sql, (paid_amount, balance_amount, status, fine_id))
        self.db_manager.get_connection().commit()

    def get_total_outstanding_by_member(self, member_id: int) -> float:
        row = self.db_manager.fetch_one(
            """
            SELECT COALESCE(SUM(balance_amount), 0.0) as total
            FROM fines
            WHERE member_id = ? AND status IN ('UNPAID', 'PARTIALLY_PAID');
            """,
            (member_id,)
        )
        return float(row["total"]) if row else 0.0
