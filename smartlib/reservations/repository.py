"""Data repository for reservation hold queues."""
from typing import Optional, List
from smartlib.database.connection import DatabaseManager
from smartlib.reservations.models import Reservation

class ReservationRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, res: Reservation) -> Reservation:
        sql = """
        INSERT INTO reservations (book_id, member_id, queue_position, status, hold_expiry_date)
        VALUES (?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(
            sql,
            (res.book_id, res.member_id, res.queue_position, res.status, res.hold_expiry_date)
        )
        self.db_manager.get_connection().commit()
        res.reservation_id = cursor.lastrowid
        return res

    def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        sql = """
        SELECT r.*, b.title as book_title, b.isbn,
               (m.first_name || ' ' || m.last_name) as member_name, m.member_code
        FROM reservations r
        JOIN books b ON r.book_id = b.book_id
        JOIN members m ON r.member_id = m.member_id
        WHERE r.reservation_id = ?;
        """
        row = self.db_manager.fetch_one(sql, (reservation_id,))
        return Reservation(**dict(row)) if row else None

    def get_active_for_member_and_book(self, member_id: int, book_id: int) -> Optional[Reservation]:
        sql = """
        SELECT * FROM reservations
        WHERE member_id = ? AND book_id = ? AND status IN ('PENDING', 'READY_FOR_PICKUP');
        """
        row = self.db_manager.fetch_one(sql, (member_id, book_id))
        return Reservation(**dict(row)) if row else None

    def get_next_queue_position(self, book_id: int) -> int:
        row = self.db_manager.fetch_one(
            """
            SELECT COALESCE(MAX(queue_position), 0) as max_pos
            FROM reservations
            WHERE book_id = ? AND status = 'PENDING';
            """,
            (book_id,)
        )
        return (int(row["max_pos"]) if row else 0) + 1

    def list_pending_by_book(self, book_id: int) -> List[Reservation]:
        sql = """
        SELECT r.*, b.title as book_title, b.isbn,
               (m.first_name || ' ' || m.last_name) as member_name, m.member_code
        FROM reservations r
        JOIN books b ON r.book_id = b.book_id
        JOIN members m ON r.member_id = m.member_id
        WHERE r.book_id = ? AND r.status = 'PENDING'
        ORDER BY r.queue_position ASC, r.reservation_id ASC;
        """
        rows = self.db_manager.fetch_all(sql, (book_id,))
        return [Reservation(**dict(r)) for r in rows]

    def list_by_member(self, member_id: int) -> List[Reservation]:
        sql = """
        SELECT r.*, b.title as book_title, b.isbn,
               (m.first_name || ' ' || m.last_name) as member_name, m.member_code
        FROM reservations r
        JOIN books b ON r.book_id = b.book_id
        JOIN members m ON r.member_id = m.member_id
        WHERE r.member_id = ?
        ORDER BY r.reservation_id DESC;
        """
        rows = self.db_manager.fetch_all(sql, (member_id,))
        return [Reservation(**dict(r)) for r in rows]

    def update_status(self, reservation_id: int, status: str, hold_expiry_date: Optional[str] = None) -> None:
        if hold_expiry_date:
            sql = """
            UPDATE reservations 
            SET status = ?, hold_expiry_date = ?, available_since = CURRENT_TIMESTAMP 
            WHERE reservation_id = ?;
            """
            self.db_manager.execute(sql, (status, hold_expiry_date, reservation_id))
        else:
            sql = "UPDATE reservations SET status = ? WHERE reservation_id = ?;"
            self.db_manager.execute(sql, (status, reservation_id))
        self.db_manager.get_connection().commit()
