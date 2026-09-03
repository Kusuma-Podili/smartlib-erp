"""Data repository for physical book copy records."""
from typing import Optional, List
from smartlib.database.connection import DatabaseManager
from smartlib.copies.models import BookCopy

class CopyRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, copy: BookCopy) -> BookCopy:
        sql = """
        INSERT INTO book_copies (book_id, copy_number, barcode, condition, status, acquisition_cost, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(
            sql,
            (copy.book_id, copy.copy_number, copy.barcode, copy.condition, copy.status, copy.acquisition_cost, copy.notes)
        )
        self.db_manager.get_connection().commit()
        copy.copy_id = cursor.lastrowid
        return copy

    def get_by_id(self, copy_id: int) -> Optional[BookCopy]:
        sql = """
        SELECT c.*, b.title as book_title, b.isbn
        FROM book_copies c
        JOIN books b ON c.book_id = b.book_id
        WHERE c.copy_id = ?;
        """
        row = self.db_manager.fetch_one(sql, (copy_id,))
        return BookCopy(**dict(row)) if row else None

    def get_by_barcode(self, barcode: str) -> Optional[BookCopy]:
        sql = """
        SELECT c.*, b.title as book_title, b.isbn
        FROM book_copies c
        JOIN books b ON c.book_id = b.book_id
        WHERE c.barcode = ?;
        """
        row = self.db_manager.fetch_one(sql, (barcode.strip(),))
        return BookCopy(**dict(row)) if row else None

    def get_next_copy_index(self, book_id: int) -> int:
        row = self.db_manager.fetch_one(
            "SELECT COUNT(*) as cnt FROM book_copies WHERE book_id = ?;",
            (book_id,)
        )
        return (int(row["cnt"]) if row else 0) + 1

    def list_by_book_id(self, book_id: int) -> List[BookCopy]:
        sql = """
        SELECT c.*, b.title as book_title, b.isbn
        FROM book_copies c
        JOIN books b ON c.book_id = b.book_id
        WHERE c.book_id = ?
        ORDER BY c.copy_id ASC;
        """
        rows = self.db_manager.fetch_all(sql, (book_id,))
        return [BookCopy(**dict(r)) for r in rows]

    def find_available_copy_for_book(self, book_id: int) -> Optional[BookCopy]:
        sql = """
        SELECT c.*, b.title as book_title, b.isbn
        FROM book_copies c
        JOIN books b ON c.book_id = b.book_id
        WHERE c.book_id = ? AND c.status = 'AVAILABLE'
        ORDER BY c.copy_id ASC
        LIMIT 1;
        """
        row = self.db_manager.fetch_one(sql, (book_id,))
        return BookCopy(**dict(row)) if row else None

    def update_status_and_condition(self, copy_id: int, status: str, condition: Optional[str] = None) -> None:
        if condition:
            sql = """
            UPDATE book_copies 
            SET status = ?, condition = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE copy_id = ?;
            """
            self.db_manager.execute(sql, (status, condition, copy_id))
        else:
            sql = """
            UPDATE book_copies 
            SET status = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE copy_id = ?;
            """
            self.db_manager.execute(sql, (status, copy_id))
        self.db_manager.get_connection().commit()
