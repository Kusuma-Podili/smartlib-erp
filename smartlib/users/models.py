"""
User domain entities and Data Transfer Objects (DTOs).
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from smartlib.constants import UserRole, UserStatus

@dataclass
class User:
    user_id: Optional[int] = None
    username: str = ""
    email: str = ""
    password_hash: str = ""
    salt: str = ""
    role: str = UserRole.MEMBER.value
    status: str = UserStatus.ACTIVE.value
    failed_login_attempts: int = 0
    locked_until: Optional[str] = None
    last_login_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE.value

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN.value

    def is_librarian(self) -> bool:
        return self.role == UserRole.LIBRARIAN.value

    def is_member(self) -> bool:
        return self.role == UserRole.MEMBER.value

    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        data = {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "status": self.status,
            "last_login_at": self.last_login_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        if include_sensitive:
            data["password_hash"] = self.password_hash
            data["salt"] = self.salt
            data["failed_login_attempts"] = self.failed_login_attempts
            data["locked_until"] = self.locked_until
        return data

@dataclass
class UserDTO:
    username: str
    email: str
    password: str
    role: str = UserRole.MEMBER.value
    status: str = UserStatus.ACTIVE.value
