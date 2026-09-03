"""
Session lifecycle, token generation, timeout validation, and revocation manager.
"""

import secrets
import datetime
from typing import Optional, Dict, Any
from smartlib.database.connection import DatabaseManager
from smartlib.constants import DEFAULT_SESSION_TIMEOUT_MINUTES
from smartlib.errors import SessionExpiredError, AuthenticationError

class SessionManager:
    def __init__(self, db_manager: Optional[DatabaseManager] = None, timeout_minutes: int = DEFAULT_SESSION_TIMEOUT_MINUTES):
        self.db_manager = db_manager or DatabaseManager.get_instance()
        self.timeout_minutes = timeout_minutes

    def create_session(self, user_id: int, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> str:
        """Generate a unique secure 48-byte URL-safe token and persist session."""
        token = secrets.token_urlsafe(48)
        now = datetime.datetime.now(datetime.timezone.utc)
        expires_at = now + datetime.timedelta(minutes=self.timeout_minutes)
        sql = """
        INSERT INTO user_sessions (session_token, user_id, ip_address, user_agent, expires_at)
        VALUES (?, ?, ?, ?, ?);
        """
        self.db_manager.execute(
            sql,
            (token, user_id, ip_address, user_agent, expires_at.strftime("%Y-%m-%d %H:%M:%S"))
        )
        self.db_manager.get_connection().commit()
        return token

    def validate_session(self, token: str) -> Dict[str, Any]:
        """
        Validate session token, verify expiry and non-revoked status.
        Sliding expiration: refreshes expires_at on valid activity.
        """
        if not token:
            raise AuthenticationError("Missing session token.")

        sql = """
        SELECT s.session_id, s.session_token, s.user_id, s.expires_at, s.is_revoked,
               u.username, u.email, u.role, u.status
        FROM user_sessions s
        JOIN users u ON s.user_id = u.user_id
        WHERE s.session_token = ?;
        """
        row = self.db_manager.fetch_one(sql, (token,))
        if not row:
            raise AuthenticationError("Invalid or nonexistent session.")
        if bool(row["is_revoked"]):
            raise AuthenticationError("Session has been revoked.")

        now = datetime.datetime.now(datetime.timezone.utc)
        expires_at = datetime.datetime.strptime(row["expires_at"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
        if now > expires_at:
            self.revoke_session(token)
            raise SessionExpiredError("Your session has expired. Please log in again.")

        # Sliding window refresh
        new_expiry = (now + datetime.timedelta(minutes=self.timeout_minutes)).strftime("%Y-%m-%d %H:%M:%S")
        self.db_manager.execute(
            "UPDATE user_sessions SET expires_at = ? WHERE session_token = ?;",
            (new_expiry, token)
        )
        self.db_manager.get_connection().commit()

        return dict(row)

    def revoke_session(self, token: str) -> None:
        """Invalidate a session token (Logout)."""
        self.db_manager.execute(
            "UPDATE user_sessions SET is_revoked = 1 WHERE session_token = ?;",
            (token,)
        )
        self.db_manager.get_connection().commit()

    def revoke_all_for_user(self, user_id: int) -> None:
        """Invalidate all sessions for a user (e.g. on password reset or account suspension)."""
        self.db_manager.execute(
            "UPDATE user_sessions SET is_revoked = 1 WHERE user_id = ?;",
            (user_id,)
        )
        self.db_manager.get_connection().commit()
