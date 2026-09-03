"""
Comprehensive Test Suite 3: Patron Management, Membership Tiers,
Borrowing Limits, and Automated Expiration Auditing.
"""

import unittest
import datetime
from tests.conftest import BaseTestCase
from smartlib.members.member_service import MemberService
from smartlib.members.models import MemberDTO
from smartlib.memberships.tier_service import MembershipTierService
from smartlib.memberships.expiration_checker import MembershipExpirationChecker
from smartlib.constants import MembershipType, MembershipStatus
from smartlib.errors import DuplicateEntityError, ValidationError

class TestMembersAndMemberships(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.member_svc = MemberService()
        self.tier_svc = MembershipTierService()
        self.exp_checker = MembershipExpirationChecker()

    def test_member_registration_and_code_generation(self):
        """Verify patron registration generates standardized MEM-YYYY-XXXX card ID."""
        dto = MemberDTO(
            first_name="Grace",
            last_name="Hopper",
            email="ghopper@navy.mil",
            phone="+1-555-1945",
            membership_type=MembershipType.FACULTY.value,
            duration_days=365
        )
        member = self.member_svc.register_member(dto, actor_username="librarian")
        self.assertIsNotNone(member.member_id)
        self.assertTrue(member.member_code.startswith("MEM-"))
        self.assertEqual(member.membership_type, "FACULTY")
        self.assertEqual(member.status, "ACTIVE")
        self.assertFalse(member.is_expired())

    def test_membership_tier_rules_and_limits(self):
        """Verify tier-specific quota rules: Student (3 books), Faculty (10 books)."""
        student_tier = self.tier_svc.get_tier(MembershipType.STUDENT.value)
        self.assertEqual(student_tier.max_borrow_limit, 3)
        self.assertEqual(student_tier.loan_duration_days, 14)

        faculty_tier = self.tier_svc.get_tier(MembershipType.FACULTY.value)
        self.assertEqual(faculty_tier.max_borrow_limit, 10)
        self.assertEqual(faculty_tier.loan_duration_days, 60)

    def test_member_search_and_filtering(self):
        """Verify patron multi-field search by name, email, code, status."""
        dto = MemberDTO(first_name="Ada", last_name="Lovelace", email="ada@analytical.org", membership_type=MembershipType.STUDENT.value)
        self.member_svc.register_member(dto)

        results, total = self.member_svc.search(query="Lovelace")
        self.assertEqual(total, 1)
        self.assertEqual(results[0].first_name, "Ada")

        # Filter by status
        active_results, total_active = self.member_svc.search(status="ACTIVE")
        self.assertTrue(total_active >= 2)

    def test_member_deactivation_and_activation(self):
        """Verify patron suspension and reactivation."""
        dto = MemberDTO(first_name="Alan", last_name="Turing", email="turing@bletchley.uk")
        m = self.member_svc.register_member(dto)
        self.assertEqual(m.status, "ACTIVE")

        # Deactivate
        updated = self.member_svc.set_member_status(m.member_id, MembershipStatus.SUSPENDED.value)
        self.assertEqual(updated.status, "SUSPENDED")
        self.assertFalse(updated.is_active())

        # Reactivate
        reactivated = self.member_svc.set_member_status(m.member_id, MembershipStatus.ACTIVE.value)
        self.assertEqual(reactivated.status, "ACTIVE")
        self.assertTrue(reactivated.is_active())

    def test_automatic_expired_membership_detection(self):
        """Verify scanner detects expired memberships and updates status to EXPIRED."""
        # Register a member with expired date (1 day duration in the past)
        dto = MemberDTO(first_name="Old", last_name="Patron", email="old@patron.com", duration_days=-5)
        m = self.member_svc.register_member(dto)

        # Before scan: check is_expired method
        self.assertTrue(m.is_expired())

        # Run automated expiration scanner
        expired_ids = self.exp_checker.scan_and_expire()
        self.assertIn(m.member_id, expired_ids)

        # After scan: status in database is EXPIRED
        updated = self.member_svc.get_member(m.member_id)
        self.assertEqual(updated.status, MembershipStatus.EXPIRED.value)

if __name__ == "__main__":
    unittest.main()
