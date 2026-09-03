"""
Unified authentication service with automatic role-based redirect resolution.
Eliminates manual role selection upon login.
"""

from typing import Optional, Dict, Any
from smartlib.users.repository import UserRepository
from smartlib.authentication.hasher import PasswordHasher
from smartlib.authentication.session_manager import SessionManager
from smartlib.authentication.security_utils import BruteForceProtector
from smartlib.authentication.rbac import get_role_dashboard_url
from smartlib.audit.audit_service import AuditService
from smartlib.constants import UserStatus, AuditAction
from smartlib.errors import AuthenticationError, InvalidCredentialsError, AccountInactiveError

class AuthService:
    def __init__(
        self,
        user_repo: Optional[UserRepository] = None,
        hasher: Optional[PasswordHasher] = None,
        session_mgr: Optional[SessionManager] = None,
        brute_force: Optional[BruteForceProtector] = None,
        audit_service: Optional[AuditService] = None
    ):
        self.user_repo = user_repo or UserRepository()
        self.hasher = hasher or PasswordHasher()
        self.session_mgr = session_mgr or SessionManager()
        self.brute_force = brute_force or BruteForceProtector()
        self.audit_service = audit_service or AuditService()

    def authenticate(
        self,
        username_or_email: str,
        password: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Authenticate user credentials, enforce brute-force locks, create secure session,
        and determine post-login target dashboard route automatically.
        """
        if not username_or_email or not password:
            raise InvalidCredentialsError("Username and password are required.")

        user = self.user_repo.get_by_username_or_email(username_or_email)
        if not user:
            self.audit_service.log(
                action=AuditAction.FAILED_LOGIN.value,
                entity_type="User",
                username=username_or_email,
                description="Failed login attempt: non-existent account.",
                ip_address=ip_address
            )
            raise InvalidCredentialsError()

        # Check account lockout
        self.brute_force.check_lockout(user.to_dict(include_sensitive=True))

        # Check active status
        if user.status != UserStatus.ACTIVE.value:
            raise AccountInactiveError(status=user.status)

        # Verify cryptographic password hash
        is_valid = self.hasher.verify_password(password, user.password_hash, user.salt)
        if not is_valid:
            self.brute_force.record_failed_attempt(user.user_id, user.failed_login_attempts)
            self.audit_service.log(
                action=AuditAction.FAILED_LOGIN.value,
                entity_type="User",
                entity_id=user.user_id,
                username=user.username,
                user_id=user.user_id,
                description="Failed login: password mismatch.",
                ip_address=ip_address
            )
            raise InvalidCredentialsError()

        # Reset failed attempts and update last login timestamp
        self.brute_force.reset_attempts(user.user_id)
        self.user_repo.update_last_login(user.user_id)

        # Create session token
        token = self.session_mgr.create_session(
            user_id=user.user_id,
            ip_address=ip_address,
            user_agent=user_agent
        )

        # Automatic post-login role detection
        target_dashboard = get_role_dashboard_url(user.role)

        self.audit_service.log(
            action=AuditAction.LOGIN.value,
            entity_type="User",
            entity_id=user.user_id,
            username=user.username,
            user_id=user.user_id,
            description=f"User logged in successfully with role '{user.role}'. Routed to '{target_dashboard}'.",
            ip_address=ip_address
        )

        return {
            "session_token": token,
            "user": user.to_dict(include_sensitive=False),
            "redirect_url": target_dashboard
        }

    def logout(self, token: str) -> None:
        """Revoke session and record audit event."""
        if token:
            try:
                session_data = self.session_mgr.validate_session(token)
                self.audit_service.log(
                    action=AuditAction.LOGOUT.value,
                    entity_type="User",
                    entity_id=session_data.get("user_id"),
                    username=session_data.get("username", "UNKNOWN"),
                    user_id=session_data.get("user_id"),
                    description="User logged out."
                )
            except Exception:
                pass
            self.session_mgr.revoke_session(token)
