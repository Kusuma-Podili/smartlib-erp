"""
Data repository for user account persistence and querying.
"""

from typing import Optional, List, Dict, Any
from smartlib.database.connection import DatabaseManager
from smartlib.users.models import User
from smartlib.constants import UserStatus

class UserRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, user: User) -> User:
        sql = """
        INSERT INTO users (username, email, password_hash, salt, role, status)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(
            sql,
            (user.username, user.email, user.password_hash, user.salt, user.role, user.status)
        )
        self.db_manager.get_connection().commit()
        user.user_id = cursor.lastrowid
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        sql = """
        SELECT user_id, username, email, password_hash, salt, role, status,
               failed_login_attempts, locked_until, last_login_at, created_at, updated_at
        FROM users WHERE user_id = ?;
        """
        row = self.db_manager.fetch_one(sql, (user_id,))
        return User(**dict(row)) if row else None

    def get_by_username(self, username: str) -> Optional[User]:
        sql = """
        SELECT user_id, username, email, password_hash, salt, role, status,
               failed_login_attempts, locked_until, last_login_at, created_at, updated_at
        FROM users WHERE LOWER(username) = LOWER(?);
        """
        row = self.db_manager.fetch_one(sql, (username.strip(),))
        return User(**dict(row)) if row else None

    def get_by_email(self, email: str) -> Optional[User]:
        sql = """
        SELECT user_id, username, email, password_hash, salt, role, status,
               failed_login_attempts, locked_until, last_login_at, created_at, updated_at
        FROM users WHERE LOWER(email) = LOWER(?);
        """
        row = self.db_manager.fetch_one(sql, (email.strip(),))
        return User(**dict(row)) if row else None

    def get_by_username_or_email(self, identifier: str) -> Optional[User]:
        clean = identifier.strip().lower()
        sql = """
        SELECT user_id, username, email, password_hash, salt, role, status,
               failed_login_attempts, locked_until, last_login_at, created_at, updated_at
        FROM users WHERE LOWER(username) = ? OR LOWER(email) = ?;
        """
        row = self.db_manager.fetch_one(sql, (clean, clean))
        return User(**dict(row)) if row else None

    def update_password(self, user_id: int, password_hash: str, salt: str) -> bool:
        sql = """
        UPDATE users 
        SET password_hash = ?, salt = ?, updated_at = CURRENT_TIMESTAMP 
        WHERE user_id = ?;
        """
        self.db_manager.execute(sql, (password_hash, salt, user_id))
        self.db_manager.get_connection().commit()
        return True

    def update_status(self, user_id: int, status: str) -> bool:
        sql = """
        UPDATE users 
        SET status = ?, updated_at = CURRENT_TIMESTAMP 
        WHERE user_id = ?;
        """
        self.db_manager.execute(sql, (status, user_id))
        self.db_manager.get_connection().commit()
        return True

    def update_last_login(self, user_id: int) -> None:
        sql = """
        UPDATE users 
        SET last_login_at = CURRENT_TIMESTAMP, failed_login_attempts = 0, locked_until = NULL
        WHERE user_id = ?;
        """
        self.db_manager.execute(sql, (user_id,))
        self.db_manager.get_connection().commit()

    def list_all(self, role: Optional[str] = None, status: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[User]:
        clauses = []
        params = []
        if role:
            clauses.append("role = ?")
            params.append(role.upper())
        if status:
            clauses.append("status = ?")
            params.append(status.upper())
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        sql = f"""
        SELECT user_id, username, email, password_hash, salt, role, status,
               failed_login_attempts, locked_until, last_login_at, created_at, updated_at
        FROM users
        {where}
        ORDER BY user_id ASC
        LIMIT ? OFFSET ?;
        """
        params.extend([limit, offset])
        rows = self.db_manager.fetch_all(sql, tuple(params))
        return [User(**dict(r)) for r in rows]

    def count(self, role: Optional[str] = None, status: Optional[str] = None) -> int:
        clauses = []
        params = []
        if role:
            clauses.append("role = ?")
            params.append(role.upper())
        if status:
            clauses.append("status = ?")
            params.append(status.upper())
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        sql = f"SELECT COUNT(*) as cnt FROM users {where};"
        row = self.db_manager.fetch_one(sql, tuple(params))
        return int(row["cnt"]) if row else 0
