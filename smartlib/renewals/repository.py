"""Data repository for renewal audit entries."""
from typing import Optional, List
from smartlib.database.connection import DatabaseManager
from smartlib.renewals.models import RenewalRecord

class RenewalRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, rec: RenewalRecord) -> RenewalRecord:
        sql = """
        INSERT INTO renewals (borrowing_id, requested_by_member_id, approved_by_librarian_id, previous_due_date, new_due_date)
        VALUES (?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(
            sql,
            (rec.borrowing_id, rec.requested_by_member_id, rec.approved_by_librarian_id, rec.previous_due_date, rec.new_due_date)
        )
        self.db_manager.get_connection().commit()
        rec.renewal_id = cursor.lastrowid
        return rec
