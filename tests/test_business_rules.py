"""
Comprehensive Test Suite 5 (Part B): Complete 12 Business Rules Verification
and Full End-to-End Workflow Integration.
"""

import unittest
import datetime
from tests.conftest import BaseTestCase
from smartlib.authors.author_service import AuthorService
from smartlib.authors.models import AuthorDTO
from smartlib.categories.category_service import CategoryService
from smartlib.categories.models import CategoryDTO
from smartlib.publishers.publisher_service import PublisherService
from smartlib.publishers.models import PublisherDTO
from smartlib.books.book_service import BookService
from smartlib.books.models import BookDTO, BookFilter
from smartlib.copies.copy_service import CopyService
from smartlib.copies.models import BookCopyDTO
from smartlib.members.member_service import MemberService
from smartlib.members.models import MemberDTO
from smartlib.borrowing.issue_service import IssueService
from smartlib.returns.return_service import ReturnService
from smartlib.renewals.renewal_service import RenewalService
from smartlib.reservations.reservation_service import ReservationService
from smartlib.fines.fine_service import FineService
from smartlib.payments.payment_service import PaymentService
from smartlib.analytics.dashboard_metrics import DashboardMetrics
from smartlib.authentication.auth_service import AuthService
from smartlib.users.permissions import has_permission, PERM_USER_CREATE, PERM_BOOK_VIEW
from smartlib.constants import (
    UserRole, UserStatus, MembershipType, MembershipStatus,
    BorrowingStatus, BookCopyStatus, BookCopyCondition, FineType, FineStatus, PaymentMethod
)
from smartlib.errors import (
    CopyUnavailableError, BorrowingLimitReachedError, MembershipExpiredError,
    BusinessRuleViolationError, ValidationError
)

class TestBusinessRulesAndEndToEnd(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.auth_svc = AuthService()
        self.author_svc = AuthorService()
        self.category_svc = CategoryService()
        self.publisher_svc = PublisherService()
        self.book_svc = BookService()
        self.copy_svc = CopyService()
        self.member_svc = MemberService()
        self.issue_svc = IssueService()
        self.return_svc = ReturnService()
        self.renew_svc = RenewalService()
        self.reserve_svc = ReservationService()
        self.fine_svc = FineService()
        self.payment_svc = PaymentService()
        self.metrics = DashboardMetrics()

        # Seed standard catalog
        self.author = self.author_svc.add_author(AuthorDTO(name="Steve McConnell"))
        self.category = self.category_svc.add_category(CategoryDTO(code="CODE-ENG", name="Software Construction"))
        self.publisher = self.publisher_svc.add_publisher(PublisherDTO(name="Microsoft Press"))
        self.book = self.book_svc.add_book(
            BookDTO(isbn="9780735619678", title="Code Complete (Second Edition)",
                    author_id=self.author.author_id, publisher_id=self.publisher.publisher_id, category_id=self.category.category_id, price=50.00)
        )

    def test_rule_1_book_cannot_be_issued_when_no_copy_available(self):
        """Rule 1: A book cannot be issued when no physical copy is available."""
        member = self.member_svc.register_member(MemberDTO(first_name="R1", last_name="User", email="r1@test.com"))
        # Book has 0 copies added
        with self.assertRaises(CopyUnavailableError):
            self.issue_svc.issue_book(member.member_id, self.book.book_id)

    def test_rule_2_borrowing_limit_enforcement(self):
        """Rule 2: A member cannot exceed the borrowing limit."""
        member = self.member_svc.register_member(
            MemberDTO(first_name="R2", last_name="User", email="r2@test.com", membership_type=MembershipType.GENERAL.value)
        )  # General tier max_borrow_limit = 2

        # Add 3 copies
        c1 = self.copy_svc.add_copy(BookCopyDTO(book_id=self.book.book_id))
        c2 = self.copy_svc.add_copy(BookCopyDTO(book_id=self.book.book_id))
        c3 = self.copy_svc.add_copy(BookCopyDTO(book_id=self.book.book_id))

        self.issue_svc.issue_book(member.member_id, self.book.book_id, copy_id=c1.copy_id)
        self.issue_svc.issue_book(member.member_id, self.book.book_id, copy_id=c2.copy_id)

        # 3rd checkout must be rejected
        with self.assertRaises(BorrowingLimitReachedError):
            self.issue_svc.issue_book(member.member_id, self.book.book_id, copy_id=c3.copy_id)

    def test_rule_3_expired_membership_cannot_borrow(self):
        """Rule 3: An expired membership cannot borrow books."""
        # Expired duration (-10 days)
        member = self.member_svc.register_member(MemberDTO(first_name="R3", last_name="User", email="r3@test.com", duration_days=-10))
        self.copy_svc.add_copy(BookCopyDTO(book_id=self.book.book_id))

        with self.assertRaises(MembershipExpiredError):
            self.issue_svc.issue_book(member.member_id, self.book.book_id)

    def test_rule_4_prevent_duplicate_active_reservations(self):
        """Rule 4: A member cannot create duplicate active reservations for the same book."""
        member = self.member_svc.register_member(MemberDTO(first_name="R4", last_name="User", email="r4@test.com"))
        self.reserve_svc.reserve_book(member.member_id, self.book.book_id)

        with self.assertRaises(BusinessRuleViolationError):
            self.reserve_svc.reserve_book(member.member_id, self.book.book_id)

    def test_rule_5_returning_book_updates_physical_copy(self):
        """Rule 5: Returning a book must correctly update its physical copy status."""
        member = self.member_svc.register_member(MemberDTO(first_name="R5", last_name="User", email="r5@test.com"))
        copy = self.copy_svc.add_copy(BookCopyDTO(book_id=self.book.book_id))

        loan = self.issue_svc.issue_book(member.member_id, self.book.book_id, copy_id=copy.copy_id)
        copy_issued = self.copy_svc.copy_repo.get_by_id(copy.copy_id)
        self.assertEqual(copy_issued.status, BookCopyStatus.ISSUED.value)

        self.return_svc.process_return(loan.borrowing_id)
        copy_returned = self.copy_svc.copy_repo.get_by_id(copy.copy_id)
        self.assertEqual(copy_returned.status, BookCopyStatus.AVAILABLE.value)

    def test_rule_6_overdue_fines_calculated_correctly(self):
        """Rule 6: Overdue fines must be calculated correctly."""
        member = self.member_svc.register_member(
            MemberDTO(first_name="R6", last_name="User", email="r6@test.com", membership_type=MembershipType.GENERAL.value)
        )  # General tier: rate = $10.00/day, grace = 1 day
        copy = self.copy_svc.add_copy(BookCopyDTO(book_id=self.book.book_id))
        loan = self.issue_svc.issue_book(member.member_id, self.book.book_id, copy_id=copy.copy_id)

        due = datetime.datetime.strptime(loan.due_date, "%Y-%m-%d").date()
        ret_date = (due + datetime.timedelta(days=6)).strftime("%Y-%m-%d")  # 6 days past due - 1 grace = 5 late days
        rec, fine = self.return_svc.process_return(loan.borrowing_id, return_date=ret_date)

        self.assertEqual(rec.overdue_days, 5)
        self.assertEqual(fine, 50.00)

    def test_rule_7_lost_and_damaged_copies_affect_availability(self):
        """Rule 7: Lost and damaged copies must affect availability."""
        copy = self.copy_svc.add_copy(BookCopyDTO(book_id=self.book.book_id))
        b1 = self.book_svc.get_book(self.book.book_id)
        self.assertEqual(b1.available_copies, 1)

        # Mark copy damaged
        self.copy_svc.mark_copy_status(copy.copy_id, BookCopyStatus.DAMAGED.value, condition=BookCopyCondition.DAMAGED.value)
        b2 = self.book_svc.get_book(self.book.book_id)
        self.assertEqual(b2.available_copies, 0)
        self.assertEqual(b2.damaged_copies, 1)

    def test_rule_8_patron_data_privacy(self):
        """Rule 8: Members can only access their own records."""
        m1 = self.member_svc.register_member(MemberDTO(first_name="P1", last_name="User", email="p1@test.com"))
        m2 = self.member_svc.register_member(MemberDTO(first_name="P2", last_name="User", email="p2@test.com"))
        copy = self.copy_svc.add_copy(BookCopyDTO(book_id=self.book.book_id))
        loan = self.issue_svc.issue_book(m1.member_id, self.book.book_id, copy_id=copy.copy_id)

        # Member 2 cannot renew Member 1's loan
        with self.assertRaises(BusinessRuleViolationError):
            self.renew_svc.request_renewal(loan.borrowing_id, member_id=m2.member_id)

    def test_rule_9_administrative_access_control(self):
        """Rule 9: Only authorized users can perform administrative operations."""
        self.assertTrue(has_permission(UserRole.ADMIN.value, PERM_USER_CREATE))
        self.assertFalse(has_permission(UserRole.MEMBER.value, PERM_USER_CREATE))

    def test_rule_10_deactivated_users_cannot_perform_operations(self):
        """Rule 10: Deactivated users cannot perform normal library operations."""
        member = self.member_svc.register_member(MemberDTO(first_name="R10", last_name="User", email="r10@test.com"))
        self.copy_svc.add_copy(BookCopyDTO(book_id=self.book.book_id))

        # Suspend member
        self.member_svc.set_member_status(member.member_id, MembershipStatus.SUSPENDED.value)
        with self.assertRaises(BusinessRuleViolationError):
            self.issue_svc.issue_book(member.member_id, self.book.book_id)

    def test_rule_11_renewal_rule_compliance(self):
        """Rule 11: A renewal must respect configured renewal rules."""
        member = self.member_svc.register_member(MemberDTO(first_name="R11", last_name="User", email="r11@test.com"))
        copy = self.copy_svc.add_copy(BookCopyDTO(book_id=self.book.book_id))
        loan = self.issue_svc.issue_book(member.member_id, self.book.book_id, copy_id=copy.copy_id)

        self.renew_svc.request_renewal(loan.borrowing_id, member.member_id)
        self.renew_svc.request_renewal(loan.borrowing_id, member.member_id)
        # 3rd renewal exceeds limit
        with self.assertRaises(BusinessRuleViolationError):
            self.renew_svc.request_renewal(loan.borrowing_id, member.member_id)

    def test_rule_12_reserved_book_follows_queue(self):
        """Rule 12: A reserved book must follow the reservation queue."""
        m1 = self.member_svc.register_member(MemberDTO(first_name="Q1", last_name="User", email="q1@test.com"))
        m2 = self.member_svc.register_member(MemberDTO(first_name="Q2", last_name="User", email="q2@test.com"))

        r1 = self.reserve_svc.reserve_book(m1.member_id, self.book.book_id)
        r2 = self.reserve_svc.reserve_book(m2.member_id, self.book.book_id)

        self.assertEqual(r1.queue_position, 1)
        self.assertEqual(r2.queue_position, 2)

        # Return event allocates to Q1 first
        ready = self.reserve_svc.process_returned_book_holds(self.book.book_id)
        self.assertEqual(ready.member_id, m1.member_id)

    def test_final_end_to_end_complete_workflow(self):
        """
        Execute the exact complete end-to-end workflow specified in requirements:
        Admin
        -> Creates library categories
        -> Adds authors
        -> Adds books
        -> Adds physical copies
        -> Librarian registers member
        -> Member logs in (automatic role detection)
        -> Searches for book
        -> Librarian issues available copy
        -> Member sees borrowed book
        -> Book becomes overdue
        -> System calculates fine
        -> Librarian returns book
        -> Physical copy becomes available
        -> Fine is recorded
        -> Payment is recorded
        -> Member sees updated history
        -> Admin dashboard updates statistics.
        """
        # 1. Admin creates category
        cat = self.category_svc.add_category(CategoryDTO(code="E2E-ARCH", name="Software Systems Architecture"), actor_username="admin")

        # 2. Admin adds author
        author = self.author_svc.add_author(AuthorDTO(name="Martin Kleppmann"), actor_username="admin")

        # 3. Admin adds book
        book = self.book_svc.add_book(
            BookDTO(
                isbn="9781449373320",
                title="Designing Data-Intensive Applications",
                author_id=author.author_id,
                publisher_id=self.publisher.publisher_id,
                category_id=cat.category_id,
                price=55.00
            ),
            actor_username="admin"
        )

        # 4. Adds physical copies
        copies = self.copy_svc.add_multiple_copies(book.book_id, count=2, cost=50.00, actor_username="admin")
        self.assertEqual(len(copies), 2)

        # 5. Librarian registers member
        member = self.member_svc.register_member(
            MemberDTO(
                first_name="Margaret",
                last_name="Hamilton",
                email="hamilton@apollo.nasa.gov",
                membership_type=MembershipType.FACULTY.value
            ),
            actor_username="librarian"
        )

        # 6. Member logs in (Automatic role detection)
        auth_res = self.auth_svc.authenticate("hamilton@apollo.nasa.gov", "Member@123")
        self.assertEqual(auth_res["user"]["role"], "MEMBER")
        self.assertEqual(auth_res["redirect_url"], "/member/dashboard")

        # 7. Member searches for book
        found_books, total = self.book_svc.search(BookFilter(query="Data-Intensive"))
        self.assertEqual(total, 1)
        self.assertEqual(found_books[0].book_id, book.book_id)

        # 8. Librarian issues available copy
        loan = self.issue_svc.issue_book(
            member_id=member.member_id,
            book_id=book.book_id,
            copy_id=copies[0].copy_id,
            actor_username="librarian"
        )
        self.assertIsNotNone(loan.borrowing_id)

        # 9. Member sees borrowed book in active loans
        member_loans = self.issue_svc.borrow_repo.list_active_by_member(member.member_id)
        self.assertEqual(len(member_loans), 1)
        self.assertEqual(member_loans[0].book_id, book.book_id)

        # 10. Book becomes overdue, system calculates fine on return
        due_date = datetime.datetime.strptime(loan.due_date, "%Y-%m-%d").date()
        simulated_return_date = (due_date + datetime.timedelta(days=7)).strftime("%Y-%m-%d")

        # 11. Librarian returns book & physical copy becomes available
        ret_record, fine_amt = self.return_svc.process_return(
            loan.borrowing_id,
            return_date=simulated_return_date,
            actor_username="librarian"
        )
        self.assertTrue(fine_amt > 0)

        # Verify physical copy is available again
        copy_status = self.copy_svc.copy_repo.get_by_id(copies[0].copy_id)
        self.assertEqual(copy_status.status, BookCopyStatus.AVAILABLE.value)

        # 12. Fine is recorded
        fine = self.fine_svc.assess_fine(
            member_id=member.member_id,
            amount=fine_amt,
            fine_type=FineType.OVERDUE.value,
            borrowing_id=loan.borrowing_id,
            reason="7 days overdue on return"
        )
        self.assertEqual(fine.balance_amount, fine_amt)

        # 13. Payment is recorded
        payment = self.payment_svc.process_payment(
            fine_id=fine.fine_id,
            amount=fine_amt,
            payment_method=PaymentMethod.UPI.value,
            actor_username="librarian"
        )
        self.assertIsNotNone(payment.receipt_number)

        # 14. Member sees updated history (0 outstanding fines, returned loan)
        history = self.issue_svc.borrow_repo.list_history_by_member(member.member_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].status, BorrowingStatus.RETURNED.value)
        outstanding = self.fine_svc.get_outstanding_balance(member.member_id)
        self.assertEqual(outstanding, 0.0)

        # 15. Admin dashboard updates statistics
        kpis = self.metrics.get_summary_kpis()
        self.assertTrue(kpis["total_books"] >= 2)
        self.assertTrue(kpis["total_copies"] >= 2)
        self.assertTrue(kpis["collected_fines"] >= fine_amt)

if __name__ == "__main__":
    unittest.main()
