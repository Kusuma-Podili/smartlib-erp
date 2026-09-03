"""
Persistence repository for librarian personnel.
"""

from typing import Optional, List
from smartlib.database.connection import DatabaseManager
from smartlib.librarians.models import Librarian

class LibrarianRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, lib: Librarian) -> Librarian:
        sql = """
        INSERT INTO librarians 
        (user_id, employee_code, full_name, phone, department, shift, desk_location)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(
            sql,
            (lib.user_id, lib.employee_code, lib.full_name, lib.phone, lib.department, lib.shift, lib.desk_location)
        )
        self.db_manager.get_connection().commit()
        lib.librarian_id = cursor.lastrowid
        return lib

    def get_by_user_id(self, user_id: int) -> Optional[Librarian]:
        sql = """
        SELECT librarian_id, user_id, employee_code, full_name, phone, department, shift, desk_location, hire_date
        FROM librarians WHERE user_id = ?;
        """
        row = self.db_manager.fetch_one(sql, (user_id,))
        return Librarian(**dict(row)) if row else None

    def get_by_employee_code(self, code: str) -> Optional[Librarian]:
        sql = """
        SELECT librarian_id, user_id, employee_code, full_name, phone, department, shift, desk_location, hire_date
        FROM librarians WHERE employee_code = ?;
        """
        row = self.db_manager.fetch_one(sql, (code.strip(),))
        return Librarian(**dict(row)) if row else None

    def list_all(self) -> List[Librarian]:
        sql = """
        SELECT librarian_id, user_id, employee_code, full_name, phone, department, shift, desk_location, hire_date
        FROM librarians ORDER BY librarian_id ASC;
        """
        rows = self.db_manager.fetch_all(sql)
        return [Librarian(**dict(r)) for r in rows]
