"""Database repository for book master records and complex multi-field searches."""
from typing import Optional, List, Dict, Any, Tuple
from smartlib.database.connection import DatabaseManager
from smartlib.books.models import Book, BookFilter

class BookRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, book: Book) -> Book:
        sql = """
        INSERT INTO books (
            isbn, title, subtitle, author_id, publisher_id, category_id,
            edition, publication_year, language, description, shelf_number, rack_number,
            price, total_copies, available_copies, issued_copies, lost_copies, damaged_copies, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(
            sql,
            (
                book.isbn, book.title, book.subtitle, book.author_id, book.publisher_id, book.category_id,
                book.edition, book.publication_year, book.language, book.description, book.shelf_number, book.rack_number,
                book.price, book.total_copies, book.available_copies, book.issued_copies, book.lost_copies, book.damaged_copies, book.status
            )
        )
        self.db_manager.get_connection().commit()
        book.book_id = cursor.lastrowid
        return book

    def get_by_id(self, book_id: int) -> Optional[Book]:
        sql = """
        SELECT b.*, a.name as author_name, c.name as category_name, p.name as publisher_name
        FROM books b
        LEFT JOIN authors a ON b.author_id = a.author_id
        LEFT JOIN categories c ON b.category_id = c.category_id
        LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
        WHERE b.book_id = ?;
        """
        row = self.db_manager.fetch_one(sql, (book_id,))
        return Book(**dict(row)) if row else None

    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        sql = """
        SELECT b.*, a.name as author_name, c.name as category_name, p.name as publisher_name
        FROM books b
        LEFT JOIN authors a ON b.author_id = a.author_id
        LEFT JOIN categories c ON b.category_id = c.category_id
        LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
        WHERE b.isbn = ?;
        """
        row = self.db_manager.fetch_one(sql, (isbn.strip(),))
        return Book(**dict(row)) if row else None

    def update_copy_counts(self, book_id: int) -> None:
        counts = self.db_manager.fetch_all(
            """
            SELECT status, COUNT(*) as cnt
            FROM book_copies
            WHERE book_id = ?
            GROUP BY status;
            """,
            (book_id,)
        )
        status_map = {r["status"]: r["cnt"] for r in counts}
        avail = status_map.get("AVAILABLE", 0)
        issued = status_map.get("ISSUED", 0)
        lost = status_map.get("LOST", 0)
        damaged = status_map.get("DAMAGED", 0) + status_map.get("IN_MAINTENANCE", 0)
        total = sum(status_map.values())
        book_status = "AVAILABLE" if avail > 0 else ("ISSUED" if issued > 0 else "UNAVAILABLE")

        self.db_manager.execute(
            """
            UPDATE books
            SET total_copies = ?, available_copies = ?, issued_copies = ?,
                lost_copies = ?, damaged_copies = ?, status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE book_id = ?;
            """,
            (total, avail, issued, lost, damaged, book_status, book_id)
        )
        self.db_manager.get_connection().commit()

    def search_books(self, spec: BookFilter) -> Tuple[List[Book], int]:
        clauses = []
        params = []
        if spec.query:
            clauses.append("(b.title LIKE ? OR b.subtitle LIKE ? OR b.isbn LIKE ? OR a.name LIKE ?)")
            q = f"%{spec.query.strip()}%"
            params.extend([q, q, q, q])
        if spec.isbn:
            clauses.append("b.isbn = ?")
            params.append(spec.isbn.strip())
        if spec.author_id:
            clauses.append("b.author_id = ?")
            params.append(spec.author_id)
        if spec.category_id:
            clauses.append("b.category_id = ?")
            params.append(spec.category_id)
        if spec.publisher_id:
            clauses.append("b.publisher_id = ?")
            params.append(spec.publisher_id)
        if spec.language:
            clauses.append("LOWER(b.language) = LOWER(?)")
            params.append(spec.language.strip())
        if spec.shelf_number:
            clauses.append("b.shelf_number = ?")
            params.append(spec.shelf_number)
        if spec.rack_number:
            clauses.append("b.rack_number = ?")
            params.append(spec.rack_number)
        if spec.available_only:
            clauses.append("b.available_copies > 0 AND b.status = 'AVAILABLE'")

        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        count_sql = f"""
        SELECT COUNT(*) as total
        FROM books b
        LEFT JOIN authors a ON b.author_id = a.author_id
        LEFT JOIN categories c ON b.category_id = c.category_id
        LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
        {where};
        """
        total_row = self.db_manager.fetch_one(count_sql, tuple(params))
        total_count = int(total_row["total"]) if total_row else 0

        valid_sort_fields = {
            "title": "b.title",
            "created_at": "b.created_at",
            "publication_year": "b.publication_year",
            "price": "b.price"
        }
        sort_col = valid_sort_fields.get(spec.sort_by, "b.title")
        sort_order = "DESC" if spec.sort_dir.upper() == "DESC" else "ASC"

        query_sql = f"""
        SELECT b.*, a.name as author_name, c.name as category_name, p.name as publisher_name
        FROM books b
        LEFT JOIN authors a ON b.author_id = a.author_id
        LEFT JOIN categories c ON b.category_id = c.category_id
        LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
        {where}
        ORDER BY {sort_col} {sort_order}
        LIMIT ? OFFSET ?;
        """
        page_params = list(params) + [spec.limit, spec.offset]
        rows = self.db_manager.fetch_all(query_sql, tuple(page_params))
        books = [Book(**dict(r)) for r in rows]
        return books, total_count
