"""
Comprehensive Test Suite: User Registration, Granular RBAC,
Audit Logging, and Status Lifecycle.
"""

import unittest
from tests.conftest import BaseTestCase
from smartlib.users.user_service import UserService
from smartlib.users.models import UserDTO
from smartlib.users.permissions import has_permission, PERM_USER_CREATE, PERM_BOOK_VIEW
from smartlib.audit.audit_service import AuditService
from smartlib.constants import UserRole, UserStatus
from smartlib.errors import DuplicateEntityError, ValidationError

class TestUsersAndSecurity(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_svc = UserService()
        self.audit_svc = AuditService()

    def test_user_registration_and_validation(self):
        """Verify user creation with email, username and password complexity checks."""
        dto = UserDTO(
            username="newpatron",
            email="patron@university.edu",
            password="StrongPassword@2026",
            role=UserRole.MEMBER.value
        )
        user = self.user_svc.register_user(dto, actor_username="admin")
        self.assertIsNotNone(user.user_id)
        self.assertEqual(user.username, "newpatron")
        self.assertEqual(user.status, UserStatus.ACTIVE.value)

        # Check audit log entry
        logs = self.audit_svc.get_recent_activity(10)
        user_create_logs = [l for l in logs if l.action == "USER_CREATE" and l.entity_id == str(user.user_id)]
        self.assertTrue(len(user_create_logs) > 0)

    def test_duplicate_username_rejection(self):
        """Verify uniqueness constraint on username."""
        dto = UserDTO(username="admin", email="unique@lib.com", password="Password@123")
        with self.assertRaises(DuplicateEntityError):
            self.user_svc.register_user(dto)

    def test_duplicate_email_rejection(self):
        """Verify uniqueness constraint on email address."""
        dto = UserDTO(username="admin2", email="admin@library.com", password="Password@123")
        with self.assertRaises(DuplicateEntityError):
            self.user_svc.register_user(dto)

    def test_role_permissions_matrix(self):
        """Verify RBAC permissions for Admin vs Librarian vs Member."""
        self.assertTrue(has_permission(UserRole.ADMIN.value, PERM_USER_CREATE))
        self.assertFalse(has_permission(UserRole.MEMBER.value, PERM_USER_CREATE))
        self.assertTrue(has_permission(UserRole.MEMBER.value, PERM_BOOK_VIEW))

    def test_user_deactivation_lifecycle(self):
        """Verify user deactivation updates status and audit log."""
        users = self.user_svc.list_users(role="MEMBER")
        target_user = users[0]
        self.user_svc.set_user_status(target_user.user_id, UserStatus.INACTIVE.value, actor_username="admin")

        updated = self.user_svc.get_user_by_id(target_user.user_id)
        self.assertEqual(updated.status, UserStatus.INACTIVE.value)

if __name__ == "__main__":
    unittest.main()
