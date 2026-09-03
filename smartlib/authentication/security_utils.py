"""
Brute-force protection, account lockout tracking, and security rate limiters.
"""

import datetime
from typing import Optional
from smartlib.database.connection import DatabaseManager
from smartlib.constants import MAX_FAILED_LOGIN_ATTEMPTS, LOCKOUT_DURATION_MINUTES
from smartlib.errors import AccountLockedError

class BruteForceProtector:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()
        self.max_attempts = MAX_FAILED_LOGIN_ATTEMPTS
        self.lockout_minutes = LOCKOUT_DURATION_MINUTES

    def check_lockout(self, user_row: dict) -> None:
        """Verify whether user is currently locked out."""
        locked_until_str = user_row.get("locked_until")
        if locked_until_str:
            try:
                locked_until = datetime.datetime.strptime(locked_until_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
                now = datetime.datetime.now(datetime.timezone.utc)
                if now < locked_until:
                    remaining = int((locked_until - now).total_seconds() // 60) + 1
                    raise AccountLockedError(minutes_remaining=remaining)
            except ValueError:
                pass

    def record_failed_attempt(self, user_id: int, current_failures: int) -> int:
        """Increment failed login count, lock account if threshold exceeded."""
        new_count = current_failures + 1
        if new_count >= self.max_attempts:
            now = datetime.datetime.now(datetime.timezone.utc)
            lock_until = (now + datetime.timedelta(minutes=self.lockout_minutes)).strftime("%Y-%m-%d %H:%M:%S")
            self.db_manager.execute(
                """
                UPDATE users 
                SET failed_login_attempts = ?, locked_until = ?, status = 'LOCKED'
                WHERE user_id = ?;
                """,
                (new_count, lock_until, user_id)
            )
        else:
            self.db_manager.execute(
                "UPDATE users SET failed_login_attempts = ? WHERE user_id = ?;",
                (new_count, user_id)
            )
        self.db_manager.get_connection().commit()
        return new_count

    def reset_attempts(self, user_id: int) -> None:
        """Reset failed login count and clear lockout upon successful authentication."""
        self.db_manager.execute(
            """
            UPDATE users 
            SET failed_login_attempts = 0, locked_until = NULL, 
                status = CASE WHEN status = 'LOCKED' THEN 'ACTIVE' ELSE status END
            WHERE user_id = ?;
            """,
            (user_id,)
        )
        self.db_manager.get_connection().commit()
