"""Historical circulation trends, genre popularity, and patron activity analytics."""
from typing import List, Dict, Any, Optional
from smartlib.database.connection import DatabaseManager

class TrendsAnalyzer:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def get_popular_books(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Rank most frequently borrowed books."""
        sql = """
        SELECT b.book_id, b.title, b.isbn, a.name as author_name, COUNT(br.borrowing_id) as borrow_count
        FROM books b
        JOIN borrowings br ON b.book_id = br.book_id
        LEFT JOIN authors a ON b.author_id = a.author_id
        GROUP BY b.book_id
        ORDER BY borrow_count DESC
        LIMIT ?;
        """
        rows = self.db_manager.fetch_all(sql, (limit,))
        return [dict(r) for r in rows]

    def get_popular_categories(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Rank most frequently circulated categories."""
        sql = """
        SELECT c.category_id, c.code, c.name, COUNT(br.borrowing_id) as borrow_count
        FROM categories c
        JOIN books b ON c.category_id = b.category_id
        JOIN borrowings br ON b.book_id = br.book_id
        GROUP BY c.category_id
        ORDER BY borrow_count DESC
        LIMIT ?;
        """
        rows = self.db_manager.fetch_all(sql, (limit,))
        return [dict(r) for r in rows]

    def get_monthly_circulation_trends(self) -> List[Dict[str, Any]]:
        """Monthly borrowing vs return counts."""
        sql = """
        SELECT strftime('%Y-%m', issue_date) as month, COUNT(*) as issues_count
        FROM borrowings
        GROUP BY month
        ORDER BY month ASC;
        """
        rows = self.db_manager.fetch_all(sql)
        return [dict(r) for r in rows]
