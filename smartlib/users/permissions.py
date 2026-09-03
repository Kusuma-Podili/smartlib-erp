"""
Granular permission definitions and role-permission matrices.
"""

from typing import Set, Dict
from smartlib.constants import UserRole

# Permission Constants
PERM_USER_VIEW = "user:view"
PERM_USER_CREATE = "user:create"
PERM_USER_EDIT = "user:edit"
PERM_USER_DELETE = "user:delete"

PERM_BOOK_VIEW = "book:view"
PERM_BOOK_CREATE = "book:create"
PERM_BOOK_EDIT = "book:edit"
PERM_BOOK_DELETE = "book:delete"

PERM_COPY_VIEW = "copy:view"
PERM_COPY_MANAGE = "copy:manage"

PERM_CIRCULATION_ISSUE = "circulation:issue"
PERM_CIRCULATION_RETURN = "circulation:return"
PERM_CIRCULATION_RENEW = "circulation:renew"

PERM_RESERVATION_VIEW = "reservation:view"
PERM_RESERVATION_CREATE = "reservation:create"
PERM_RESERVATION_MANAGE = "reservation:manage"

PERM_FINE_VIEW = "fine:view"
PERM_FINE_COLLECT = "fine:collect"
PERM_FINE_WAIVE = "fine:waive"

PERM_REPORTS_VIEW = "reports:view"
PERM_ANALYTICS_VIEW = "analytics:view"
PERM_AUDIT_VIEW = "audit:view"
PERM_SETTINGS_MANAGE = "settings:manage"

ROLE_PERMISSIONS: Dict[str, Set[str]] = {
    UserRole.ADMIN.value: {
        PERM_USER_VIEW, PERM_USER_CREATE, PERM_USER_EDIT, PERM_USER_DELETE,
        PERM_BOOK_VIEW, PERM_BOOK_CREATE, PERM_BOOK_EDIT, PERM_BOOK_DELETE,
        PERM_COPY_VIEW, PERM_COPY_MANAGE,
        PERM_CIRCULATION_ISSUE, PERM_CIRCULATION_RETURN, PERM_CIRCULATION_RENEW,
        PERM_RESERVATION_VIEW, PERM_RESERVATION_CREATE, PERM_RESERVATION_MANAGE,
        PERM_FINE_VIEW, PERM_FINE_COLLECT, PERM_FINE_WAIVE,
        PERM_REPORTS_VIEW, PERM_ANALYTICS_VIEW, PERM_AUDIT_VIEW, PERM_SETTINGS_MANAGE
    },
    UserRole.LIBRARIAN.value: {
        PERM_USER_VIEW,
        PERM_BOOK_VIEW, PERM_BOOK_CREATE, PERM_BOOK_EDIT,
        PERM_COPY_VIEW, PERM_COPY_MANAGE,
        PERM_CIRCULATION_ISSUE, PERM_CIRCULATION_RETURN, PERM_CIRCULATION_RENEW,
        PERM_RESERVATION_VIEW, PERM_RESERVATION_CREATE, PERM_RESERVATION_MANAGE,
        PERM_FINE_VIEW, PERM_FINE_COLLECT,
        PERM_REPORTS_VIEW
    },
    UserRole.MEMBER.value: {
        PERM_BOOK_VIEW,
        PERM_RESERVATION_CREATE,
        PERM_CIRCULATION_RENEW
    }
}

def has_permission(role: str, permission_code: str) -> bool:
    perms = ROLE_PERMISSIONS.get(role.upper(), set())
    return permission_code in perms
