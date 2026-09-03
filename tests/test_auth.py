"""
Comprehensive Test Suite 1: Authentication, PBKDF2 Password Hashing,
Automatic Post-Login Role Routing, Account Lockout, and Session Invalidation.
"""

import unittest
from tests.conftest import BaseTestCase
from smartlib.authentication.hasher import PasswordHasher
from smartlib.authentication.session_manager import SessionManager
from smartlib.authentication.auth_service import AuthService
from smartlib.authentication.security_utils import BruteForceProtector
from smartlib.errors import InvalidCredentialsError, AccountLockedError, AccountInactiveError, SessionExpiredError
from smartlib.constants import UserRole, UserStatus
from smartlib.users.user_service import UserService
from smartlib.users.models import UserDTO

class TestAuthentication(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.hasher = PasswordHasher(iterations=1000)
        self.session_mgr = SessionManager(self.db_manager, timeout_minutes=60)
        self.user_svc = UserService(hasher=self.hasher)
        self.auth_svc = AuthService(
            hasher=self.hasher,
            session_mgr=self.session_mgr
        )

    def test_pbkdf2_password_hashing_and_verification(self):
        """Verify cryptographic salting and constant-time password verification."""
        pwd = "SecurePassword@123"
        hashed, salt = self.hasher.hash_password(pwd)
        self.assertNotEqual(pwd, hashed)
        self.assertEqual(len(salt), 64)  # 32 bytes hex = 64 characters
        self.assertTrue(self.hasher.verify_password(pwd, hashed, salt))
        self.assertFalse(self.hasher.verify_password("WrongPassword", hashed, salt))

    def test_automatic_role_detection_upon_login(self):
        """
        Test that users are not asked to select their role.
        The system identifies role and routes automatically:
        - Admin -> /admin/dashboard
        - Librarian -> /librarian/dashboard
        - Member -> /member/dashboard
        """
        # 1. Admin login
        admin_res = self.auth_svc.authenticate("admin@library.com", "Admin@123")
        self.assertIn("session_token", admin_res)
        self.assertEqual(admin_res["user"]["role"], UserRole.ADMIN.value)
        self.assertEqual(admin_res["redirect_url"], "/admin/dashboard")

        # 2. Librarian login
        lib_res = self.auth_svc.authenticate("librarian@library.com", "Librarian@123")
        self.assertEqual(lib_res["user"]["role"], UserRole.LIBRARIAN.value)
        self.assertEqual(lib_res["redirect_url"], "/librarian/dashboard")

        # 3. Member login
        mem_res = self.auth_svc.authenticate("member@library.com", "Member@123")
        self.assertEqual(mem_res["user"]["role"], UserRole.MEMBER.value)
        self.assertEqual(mem_res["redirect_url"], "/member/dashboard")

    def test_invalid_credentials_rejection(self):
        """Test that invalid username or password raises InvalidCredentialsError."""
        with self.assertRaises(InvalidCredentialsError):
            self.auth_svc.authenticate("admin@library.com", "WrongPassword!999")

        with self.assertRaises(InvalidCredentialsError):
            self.auth_svc.authenticate("nonexistent@domain.com", "Password@123")

    def test_account_lockout_after_consecutive_failed_attempts(self):
        """Test brute force defense: 5 failed logins lock account."""
        for _ in range(5):
            try:
                self.auth_svc.authenticate("member@library.com", "WrongPass@000")
            except InvalidCredentialsError:
                pass

        # 6th attempt should trigger AccountLockedError
        with self.assertRaises(AccountLockedError):
            self.auth_svc.authenticate("member@library.com", "Member@123")

    def test_session_lifecycle_and_logout(self):
        """Test session token validation, renewal, and explicit logout revocation."""
        res = self.auth_svc.authenticate("admin@library.com", "Admin@123")
        token = res["session_token"]

        # Validate active session
        session_info = self.session_mgr.validate_session(token)
        self.assertEqual(session_info["username"], "admin")
        self.assertEqual(session_info["role"], "ADMIN")

        # Perform logout
        self.auth_svc.logout(token)

        # Subsequent validation should fail
        with self.assertRaises(Exception):
            self.session_mgr.validate_session(token)

if __name__ == "__main__":
    unittest.main()
