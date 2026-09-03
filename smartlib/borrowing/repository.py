"""Persistence repository for active and historical circulation loans."""
from typing import Optional, List, Dict, Any, Tuple
from smartlib.database.connection import DatabaseManager
from smartlib.borrowing.models import BorrowingRecord

class BorrowingRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, rec: BorrowingRecord) -> BorrowingRecord:
        sql = """
        INSERT INTO borrowings (
            member_id, book_id, copy_id, issued_by_librarian_id,
            issue_date, due_date, renewal_count, max_renewals_allowed, status, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(
            sql,
            (
                rec.member_id, rec.book_id, rec.copy_id, rec.issued_by_librarian_id,
                rec.issue_date, rec.due_date, rec.renewal_count, rec.max_renewals_allowed,
                rec.status, rec.notes
            )
        )
        self.db_manager.get_connection().commit()
        rec.borrowing_id = cursor.lastrowid
        return rec

    def get_by_id(self, borrowing_id: int) -> Optional[BorrowingRecord]:
        sql = """
        SELECT br.*, b.title as book_title, b.isbn, c.copy_number, c.barcode,
               (m.first_name || ' ' || m.last_name) as member_name, m.member_code
        FROM borrowings br
        JOIN books b ON br.book_id = b.book_id
        JOIN book_copies c ON br.copy_id = c.copy_id
        JOIN members m ON br.member_id = m.member_id
        WHERE br.borrowing_id = ?;
        """
        row = self.db_manager.fetch_one(sql, (borrowing_id,))
        return BorrowingRecord(**dict(row)) if row else None

    def count_active_loans_by_member(self, member_id: int) -> int:
        sql = """
        SELECT COUNT(*) as cnt
        FROM borrowings
        WHERE member_id = ? AND status IN ('ACTIVE', 'OVERDUE');
        """
        row = self.db_manager.fetch_one(sql, (member_id,))
        return int(row["cnt"]) if row else 0

    def list_active_by_member(self, member_id: int) -> List[BorrowingRecord]:
        sql = """
        SELECT br.*, b.title as book_title, b.isbn, c.copy_number, c.barcode,
               (m.first_name || ' ' || m.last_name) as member_name, m.member_code
        FROM borrowings br
        JOIN books b ON br.book_id = b.book_id
        JOIN book_copies c ON br.copy_id = c.copy_id
        JOIN members m ON br.member_id = m.member_id
        WHERE br.member_id = ? AND br.status IN ('ACTIVE', 'OVERDUE')
        ORDER BY br.due_date ASC;
        """
        rows = self.db_manager.fetch_all(sql, (member_id,))
        return [BorrowingRecord(**dict(r)) for r in rows]

    def list_history_by_member(self, member_id: int) -> List[BorrowingRecord]:
        sql = """
        SELECT br.*, b.title as book_title, b.isbn, c.copy_number, c.barcode,
               (m.first_name || ' ' || m.last_name) as member_name, m.member_code
        FROM borrowings br
        JOIN books b ON br.book_id = b.book_id
        JOIN book_copies c ON br.copy_id = c.copy_id
        JOIN members m ON br.member_id = m.member_id
        WHERE br.member_id = ?
        ORDER BY br.borrowing_id DESC;
        """
        rows = self.db_manager.fetch_all(sql, (member_id,))
        return [BorrowingRecord(**dict(r)) for r in rows]

    def update_status(self, borrowing_id: int, status: str) -> None:
        self.db_manager.execute(
            "UPDATE borrowings SET status = ? WHERE borrowing_id = ?;",
            (status, borrowing_id)
        )
        self.db_manager.get_connection().commit()

    def update_due_date_and_renewals(self, borrowing_id: int, new_due_date: str, renewal_count: int) -> None:
        sql = """
        UPDATE borrowings 
        SET due_date = ?, renewal_count = ?, status = 'ACTIVE' 
        WHERE borrowing_id = ?;
        """
        self.db_manager.execute(sql, (new_due_date, renewal_count, borrowing_id))
        self.db_manager.get_connection().commit()

    def list_overdue_loans(self, as_of_date: str) -> List[BorrowingRecord]:
        sql = """
        SELECT br.*, b.title as book_title, b.isbn, c.copy_number, c.barcode,
               (m.first_name || ' ' || m.last_name) as member_name, m.member_code
        FROM borrowings br
        JOIN books b ON br.book_id = b.book_id
        JOIN book_copies c ON br.copy_id = c.copy_id
        JOIN members m ON br.member_id = m.member_id
        WHERE br.status IN ('ACTIVE', 'OVERDUE') AND br.due_date < ?
        ORDER BY br.due_date ASC;
        """
        rows = self.db_manager.fetch_all(sql, (as_of_date,))
        return [BorrowingRecord(**dict(r)) for r in rows]
