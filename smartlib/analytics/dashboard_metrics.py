"""Real-time KPI metric aggregator for Administrator and Librarian dashboards."""
from typing import Dict, Any, Optional
from smartlib.database.connection import DatabaseManager

class DashboardMetrics:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def get_summary_kpis(self) -> Dict[str, Any]:
        """
        Compute all required dashboard metrics:
        - Total books, Total copies, Available copies, Issued copies
        - Total members, Active members, Expired memberships
        - Overdue books, Pending reservations
        - Total fines, Collected fines, Outstanding balance
        """
        # 1. Book & Copy metrics
        book_stats = self.db_manager.fetch_one("""
            SELECT 
                COUNT(*) as total_books,
                COALESCE(SUM(total_copies), 0) as total_copies,
                COALESCE(SUM(available_copies), 0) as available_copies,
                COALESCE(SUM(issued_copies), 0) as issued_copies,
                COALESCE(SUM(lost_copies), 0) as lost_copies,
                COALESCE(SUM(damaged_copies), 0) as damaged_copies
            FROM books;
        """)

        # 2. Member metrics
        member_stats = self.db_manager.fetch_one("""
            SELECT 
                COUNT(*) as total_members,
                SUM(CASE WHEN status = 'ACTIVE' THEN 1 ELSE 0 END) as active_members,
                SUM(CASE WHEN status = 'EXPIRED' THEN 1 ELSE 0 END) as expired_members,
                SUM(CASE WHEN status = 'SUSPENDED' THEN 1 ELSE 0 END) as suspended_members
            FROM members;
        """)

        # 3. Circulation metrics
        circ_stats = self.db_manager.fetch_one("""
            SELECT 
                COUNT(*) as active_loans,
                SUM(CASE WHEN due_date < DATE('now') THEN 1 ELSE 0 END) as overdue_books
            FROM borrowings
            WHERE status IN ('ACTIVE', 'OVERDUE');
        """)

        # 4. Reservation metrics
        reserve_stats = self.db_manager.fetch_one("""
            SELECT 
                COUNT(*) as pending_reservations
            FROM reservations
            WHERE status = 'PENDING';
        """)

        # 5. Financial fine metrics
        fine_stats = self.db_manager.fetch_one("""
            SELECT 
                COALESCE(SUM(amount), 0.0) as total_fines,
                COALESCE(SUM(paid_amount), 0.0) as collected_fines,
                COALESCE(SUM(balance_amount), 0.0) as outstanding_fines
            FROM fines;
        """)

        return {
            "total_books": int(book_stats["total_books"]) if book_stats else 0,
            "total_copies": int(book_stats["total_copies"]) if book_stats else 0,
            "available_copies": int(book_stats["available_copies"]) if book_stats else 0,
            "issued_copies": int(book_stats["issued_copies"]) if book_stats else 0,
            "lost_copies": int(book_stats["lost_copies"]) if book_stats else 0,
            "damaged_copies": int(book_stats["damaged_copies"]) if book_stats else 0,
            "total_members": int(member_stats["total_members"]) if member_stats else 0,
            "active_members": int(member_stats["active_members"] or 0) if member_stats else 0,
            "expired_members": int(member_stats["expired_members"] or 0) if member_stats else 0,
            "overdue_books": int(circ_stats["overdue_books"] or 0) if circ_stats else 0,
            "active_loans": int(circ_stats["active_loans"]) if circ_stats else 0,
            "pending_reservations": int(reserve_stats["pending_reservations"]) if reserve_stats else 0,
            "total_fines": float(fine_stats["total_fines"]) if fine_stats else 0.0,
            "collected_fines": float(fine_stats["collected_fines"]) if fine_stats else 0.0,
            "outstanding_fines": float(fine_stats["outstanding_fines"]) if fine_stats else 0.0
        }
