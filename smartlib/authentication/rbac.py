"""
Role-Based Access Control (RBAC) hierarchy, permission validation, and access guards.
"""

from functools import wraps
from typing import List, Callable, Optional, Dict, Any
from smartlib.constants import UserRole
from smartlib.errors import AuthorizationError

ROLE_HIERARCHY = {
    UserRole.ADMIN.value: 3,
    UserRole.LIBRARIAN.value: 2,
    UserRole.MEMBER.value: 1
}

def has_role_or_higher(user_role: str, minimum_required_role: str) -> bool:
    """Check if user role meets or exceeds required tier."""
    user_level = ROLE_HIERARCHY.get(user_role.upper(), 0)
    req_level = ROLE_HIERARCHY.get(minimum_required_role.upper(), 999)
    return user_level >= req_level

def require_role(required_role: str):
    """Decorator restricting method execution to specific role or higher."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            if not current_user:
                # Look for current_user in args if passed
                for a in args:
                    if isinstance(a, dict) and "role" in a:
                        current_user = a
                        break
            if not current_user or "role" not in current_user:
                raise AuthorizationError("Authentication required for this operation.")
            user_role = current_user["role"]
            if not has_role_or_higher(user_role, required_role):
                raise AuthorizationError(
                    f"Forbidden: Action requires '{required_role}' privilege. Your role is '{user_role}'.",
                    required_role=required_role
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator

def get_role_dashboard_url(role: str) -> str:
    """Return canonical dashboard route for a given user role."""
    r = role.upper()
    if r == UserRole.ADMIN.value:
        return "/admin/dashboard"
    elif r == UserRole.LIBRARIAN.value:
        return "/librarian/dashboard"
    elif r == UserRole.MEMBER.value:
        return "/member/dashboard"
    return "/login"
