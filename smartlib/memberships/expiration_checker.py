"""Automated scanner identifying expired memberships and updating patron records."""
import datetime
from typing import List, Optional
from smartlib.database.connection import DatabaseManager
from smartlib.constants import MembershipStatus
from smartlib.audit.audit_service import AuditService

class MembershipExpirationChecker:
    def __init__(self, db_manager: Optional[DatabaseManager] = None, audit_svc: Optional[AuditService] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()
        self.audit_svc = audit_svc or AuditService()

    def scan_and_expire(self, as_of_date: Optional[str] = None) -> List[int]:
        """Scan for active memberships past expiry date and transition to EXPIRED."""
        target_date = as_of_date or datetime.date.today().strftime("%Y-%m-%d")
        sql = """
        SELECT member_id, member_code, expiry_date
        FROM members
        WHERE status = 'ACTIVE' AND expiry_date < ?;
        """
        rows = self.db_manager.fetch_all(sql, (target_date,))
        expired_ids = []
        for r in rows:
            mid = r["member_id"]
            self.db_manager.execute(
                "UPDATE members SET status = 'EXPIRED' WHERE member_id = ?;",
                (mid,)
            )
            expired_ids.append(mid)
            self.audit_svc.log(
                action="MEMBERSHIP_EXPIRED",
                entity_type="Member",
                entity_id=mid,
                description=f"Patron {r['member_code']} membership expired on {r['expiry_date']}."
            )
        self.db_manager.get_connection().commit()
        return expired_ids
