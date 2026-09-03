"""
User account management service orchestrating validation, hashing, and audit tracking.
"""

from typing import Optional, List, Dict, Any
from smartlib.users.models import User, UserDTO
from smartlib.users.repository import UserRepository
from smartlib.authentication.hasher import PasswordHasher
from smartlib.audit.audit_service import AuditService
from smartlib.constants import UserRole, UserStatus, AuditAction
from smartlib.errors import DuplicateEntityError, UserNotFoundError, ValidationError
from smartlib.validation.validators import validate_email, validate_username, validate_password_complexity

class UserService:
    def __init__(
        self,
        repo: Optional[UserRepository] = None,
        hasher: Optional[PasswordHasher] = None,
        audit_service: Optional[AuditService] = None
    ):
        self.repo = repo or UserRepository()
        self.hasher = hasher or PasswordHasher()
        self.audit_service = audit_service or AuditService()

    def register_user(self, dto: UserDTO, actor_username: str = "SYSTEM") -> User:
        """Create and persist a new user account with validated credentials."""
        clean_username = validate_username(dto.username)
        clean_email = validate_email(dto.email)
        validate_password_complexity(dto.password)

        if self.repo.get_by_username(clean_username):
            raise DuplicateEntityError("User", "username", clean_username)
        if self.repo.get_by_email(clean_email):
            raise DuplicateEntityError("User", "email", clean_email)

        pwd_hash, salt = self.hasher.hash_password(dto.password)
        role = dto.role.upper() if UserRole.has_role(dto.role) else UserRole.MEMBER.value

        user = User(
            username=clean_username,
            email=clean_email,
            password_hash=pwd_hash,
            salt=salt,
            role=role,
            status=dto.status
        )
        created_user = self.repo.create(user)

        self.audit_service.log(
            action=AuditAction.USER_CREATE.value,
            entity_type="User",
            entity_id=created_user.user_id,
            username=actor_username,
            description=f"Created user '{clean_username}' with role '{role}'."
        )
        return created_user

    def get_user_by_id(self, user_id: int) -> User:
        u = self.repo.get_by_id(user_id)
        if not u:
            raise UserNotFoundError(user_id)
        return u

    def change_password(self, user_id: int, old_password: str, new_password: str, actor_username: str) -> bool:
        u = self.get_user_by_id(user_id)
        if not self.hasher.verify_password(old_password, u.password_hash, u.salt):
            raise ValidationError("Current password does not match.", {"old_password": "Incorrect current password."})
        validate_password_complexity(new_password)
        new_hash, new_salt = self.hasher.hash_password(new_password)
        self.repo.update_password(user_id, new_hash, new_salt)

        self.audit_service.log(
            action=AuditAction.PASSWORD_CHANGE.value,
            entity_type="User",
            entity_id=user_id,
            username=actor_username,
            description=f"Password changed for user ID {user_id}."
        )
        return True

    def set_user_status(self, user_id: int, status: str, actor_username: str) -> bool:
        u = self.get_user_by_id(user_id)
        old_status = u.status
        if status.upper() not in [s.value for s in UserStatus]:
            raise ValidationError(f"Invalid user status '{status}'.", {"status": "Unrecognized status."})

        self.repo.update_status(user_id, status.upper())
        self.audit_service.log(
            action=AuditAction.USER_STATUS_CHANGE.value,
            entity_type="User",
            entity_id=user_id,
            username=actor_username,
            description=f"Changed status from '{old_status}' to '{status.upper()}'.",
            old_data={"status": old_status},
            new_data={"status": status.upper()}
        )
        return True

    def list_users(self, role: Optional[str] = None, status: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[User]:
        return self.repo.list_all(role=role, status=status, limit=limit, offset=offset)
