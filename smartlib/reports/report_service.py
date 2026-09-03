"""Comprehensive report generation engine."""
from typing import Optional, Dict, Any, List
from smartlib.database.connection import DatabaseManager
from smartlib.reports.exporters import ReportExporter

class ReportService:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def generate_books_inventory_report(self) -> Dict[str, Any]:
        sql = """
        SELECT b.isbn, b.title, a.name as author, c.name as category,
               b.shelf_number, b.total_copies, b.available_copies, b.issued_copies, b.price
        FROM books b
        LEFT JOIN authors a ON b.author_id = a.author_id
        LEFT JOIN categories c ON b.category_id = c.category_id
        ORDER BY b.title ASC;
        """
        rows = self.db_manager.fetch_all(sql)
        headers = ["ISBN", "Title", "Author", "Category", "Shelf", "Total", "Available", "Issued", "Price"]
        data = [
            [r["isbn"], r["title"], r["author"] or "-", r["category"] or "-", r["shelf_number"],
             r["total_copies"], r["available_copies"], r["issued_copies"], f"${r['price']:.2f}"]
            for r in rows
        ]
        return {
            "title": "Book Inventory & Shelf Report",
            "headers": headers,
            "rows": data,
            "csv": ReportExporter.to_csv(headers, data)
        }

    def generate_overdue_report(self) -> Dict[str, Any]:
        sql = """
        SELECT br.borrowing_id, (m.first_name || ' ' || m.last_name) as member, m.member_code,
               b.title as book_title, c.barcode, br.due_date,
               (julianday('now') - julianday(br.due_date)) as days_past
        FROM borrowings br
        JOIN members m ON br.member_id = m.member_id
        JOIN books b ON br.book_id = b.book_id
        JOIN book_copies c ON br.copy_id = c.copy_id
        WHERE br.status IN ('ACTIVE', 'OVERDUE') AND br.due_date < DATE('now')
        ORDER BY br.due_date ASC;
        """
        rows = self.db_manager.fetch_all(sql)
        headers = ["Loan ID", "Member", "Member Code", "Book Title", "Barcode", "Due Date", "Days Late"]
        data = [
            [r["borrowing_id"], r["member"], r["member_code"], r["book_title"], r["barcode"],
             r["due_date"], max(1, int(r["days_past"]))]
            for r in rows
        ]
        return {
            "title": "Overdue Circulation Loans Report",
            "headers": headers,
            "rows": data,
            "csv": ReportExporter.to_csv(headers, data)
        }

    def generate_financial_ledger_report(self) -> Dict[str, Any]:
        sql = """
        SELECT f.fine_id, (m.first_name || ' ' || m.last_name) as member, m.member_code,
               f.fine_type, f.amount, f.paid_amount, f.balance_amount, f.status, f.created_at
        FROM fines f
        JOIN members m ON f.member_id = m.member_id
        ORDER BY f.fine_id DESC;
        """
        rows = self.db_manager.fetch_all(sql)
        headers = ["Fine ID", "Member", "Member Code", "Type", "Assessed", "Paid", "Balance", "Status", "Date"]
        data = [
            [r["fine_id"], r["member"], r["member_code"], r["fine_type"], f"${r['amount']:.2f}",
             f"${r['paid_amount']:.2f}", f"${r['balance_amount']:.2f}", r["status"], r["created_at"]]
            for r in rows
        ]
        return {
            "title": "Financial Ledger & Fine Collections Report",
            "headers": headers,
            "rows": data,
            "csv": ReportExporter.to_csv(headers, data)
        }
