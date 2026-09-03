"""Persistence repository for library patrons."""
from typing import Optional, List, Dict, Any, Tuple
from smartlib.database.connection import DatabaseManager
from smartlib.members.models import Member

class MemberRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, m: Member) -> Member:
        sql = """
        INSERT INTO members (
            user_id, member_code, first_name, last_name, email, phone, address,
            membership_type, registration_date, expiry_date, status, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        reg_date = m.registration_date or "CURRENT_TIMESTAMP"
        cursor = self.db_manager.execute(
            sql,
            (
                m.user_id, m.member_code, m.first_name, m.last_name, m.email,
                m.phone, m.address, m.membership_type, m.registration_date,
                m.expiry_date, m.status, m.notes
            )
        )
        self.db_manager.get_connection().commit()
        m.member_id = cursor.lastrowid
        return m

    def get_by_id(self, member_id: int) -> Optional[Member]:
        sql = """
        SELECT member_id, user_id, member_code, first_name, last_name, email, phone, address,
               membership_type, registration_date, expiry_date, status, notes
        FROM members WHERE member_id = ?;
        """
        row = self.db_manager.fetch_one(sql, (member_id,))
        return Member(**dict(row)) if row else None

    def get_by_user_id(self, user_id: int) -> Optional[Member]:
        sql = """
        SELECT member_id, user_id, member_code, first_name, last_name, email, phone, address,
               membership_type, registration_date, expiry_date, status, notes
        FROM members WHERE user_id = ?;
        """
        row = self.db_manager.fetch_one(sql, (user_id,))
        return Member(**dict(row)) if row else None

    def get_by_member_code(self, code: str) -> Optional[Member]:
        sql = """
        SELECT member_id, user_id, member_code, first_name, last_name, email, phone, address,
               membership_type, registration_date, expiry_date, status, notes
        FROM members WHERE LOWER(member_code) = LOWER(?);
        """
        row = self.db_manager.fetch_one(sql, (code.strip(),))
        return Member(**dict(row)) if row else None

    def get_by_email(self, email: str) -> Optional[Member]:
        sql = """
        SELECT member_id, user_id, member_code, first_name, last_name, email, phone, address,
               membership_type, registration_date, expiry_date, status, notes
        FROM members WHERE LOWER(email) = LOWER(?);
        """
        row = self.db_manager.fetch_one(sql, (email.strip(),))
        return Member(**dict(row)) if row else None

    def update_status(self, member_id: int, status: str) -> None:
        self.db_manager.execute(
            "UPDATE members SET status = ? WHERE member_id = ?;",
            (status, member_id)
        )
        self.db_manager.get_connection().commit()

    def update_profile(self, m: Member) -> None:
        sql = """
        UPDATE members 
        SET first_name = ?, last_name = ?, phone = ?, address = ?, notes = ?
        WHERE member_id = ?;
        """
        self.db_manager.execute(sql, (m.first_name, m.last_name, m.phone, m.address, m.notes, m.member_id))
        self.db_manager.get_connection().commit()

    def search_members(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        membership_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[Member], int]:
        clauses = []
        params = []
        if query:
            q = f"%{query.strip()}%"
            clauses.append("(first_name LIKE ? OR last_name LIKE ? OR member_code LIKE ? OR email LIKE ? OR phone LIKE ?)")
            params.extend([q, q, q, q, q])
        if status:
            clauses.append("status = ?")
            params.append(status.upper())
        if membership_type:
            clauses.append("membership_type = ?")
            params.append(membership_type.upper())

        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        count_sql = f"SELECT COUNT(*) as total FROM members {where};"
        total_row = self.db_manager.fetch_one(count_sql, tuple(params))
        total_count = int(total_row["total"]) if total_row else 0

        list_sql = f"""
        SELECT member_id, user_id, member_code, first_name, last_name, email, phone, address,
               membership_type, registration_date, expiry_date, status, notes
        FROM members
        {where}
        ORDER BY member_id DESC
        LIMIT ? OFFSET ?;
        """
        page_params = list(params) + [limit, offset]
        rows = self.db_manager.fetch_all(list_sql, tuple(page_params))
        members = [Member(**dict(r)) for r in rows]
        return members, total_count
