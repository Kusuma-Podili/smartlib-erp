"""Data repository for payment transactions."""
from typing import Optional, List
from smartlib.database.connection import DatabaseManager
from smartlib.payments.models import PaymentTransaction

class PaymentRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, p: PaymentTransaction) -> PaymentTransaction:
        sql = """
        INSERT INTO payments (fine_id, member_id, processed_by_librarian_id, amount, payment_method, receipt_number, transaction_reference, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(
            sql,
            (p.fine_id, p.member_id, p.processed_by_librarian_id, p.amount, p.payment_method, p.receipt_number, p.transaction_reference, p.notes)
        )
        self.db_manager.get_connection().commit()
        p.payment_id = cursor.lastrowid
        return p

    def list_by_member(self, member_id: int) -> List[PaymentTransaction]:
        sql = """
        SELECT * FROM payments WHERE member_id = ? ORDER BY payment_id DESC;
        """
        rows = self.db_manager.fetch_all(sql, (member_id,))
        return [PaymentTransaction(**dict(r)) for r in rows]
