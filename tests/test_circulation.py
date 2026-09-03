"""
Comprehensive Test Suite 4 (Part A): Circulation Desk
Book checkout/issuing, Quotas, Expiry limits, Returns, Overdue calculation, and Renewals.
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
from smartlib.books.models import BookDTO
from smartlib.copies.copy_service import CopyService
from smartlib.copies.models import BookCopyDTO
from smartlib.members.member_service import MemberService
from smartlib.members.models import MemberDTO
from smartlib.borrowing.issue_service import IssueService
from smartlib.returns.return_service import ReturnService
from smartlib.renewals.renewal_service import RenewalService
from smartlib.constants import MembershipType, BorrowingStatus, BookCopyStatus, BookCopyCondition
from smartlib.errors import CopyUnavailableError, BorrowingLimitReachedError, BusinessRuleViolationError

class TestCirculationDesk(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.author_svc = AuthorService()
        self.category_svc = CategoryService()
        self.publisher_svc = PublisherService()
        self.book_svc = BookService()
        self.copy_svc = CopyService()
        self.member_svc = MemberService()
        self.issue_svc = IssueService()
        self.return_svc = ReturnService()
        self.renew_svc = RenewalService()

        # Seed test catalog
        self.author = self.author_svc.add_author(AuthorDTO(name="Kent Beck"))
        self.category = self.category_svc.add_category(CategoryDTO(code="TDD", name="Test Driven Development"))
        self.publisher = self.publisher_svc.add_publisher(PublisherDTO(name="Addison-Wesley"))
        self.book = self.book_svc.add_book(
            BookDTO(
                isbn="9780321146533",
                title="Test-Driven Development by Example",
                author_id=self.author.author_id,
                publisher_id=self.publisher.publisher_id,
                category_id=self.category.category_id,
                price=39.99
            )
        )
        self.copy1 = self.copy_svc.add_copy(BookCopyDTO(book_id=self.book.book_id))
        self.copy2 = self.copy_svc.add_copy(BookCopyDTO(book_id=self.book.book_id))

        # Seed member (Student tier: max 3 books)
        self.member = self.member_svc.register_member(
            MemberDTO(first_name="Linus", last_name="Torvalds", email="linus@kernel.org", membership_type=MembershipType.STUDENT.value)
        )

    def test_complete_issue_and_return_cycle(self):
        """Test successful book checkout, availability drop, check-in, and copy status restoration."""
        # Issue book
        loan = self.issue_svc.issue_book(self.member.member_id, self.book.book_id)
        self.assertIsNotNone(loan.borrowing_id)
        self.assertEqual(loan.status, BorrowingStatus.ACTIVE.value)

        # Verify book availability decreased
        b_after = self.book_svc.get_book(self.book.book_id)
        self.assertEqual(b_after.available_copies, 1)
        self.assertEqual(b_after.issued_copies, 1)

        # Return book on time
        ret_record, fine = self.return_svc.process_return(loan.borrowing_id)
        self.assertEqual(fine, 0.0)
        self.assertEqual(ret_record.overdue_days, 0)

        # Verify book availability restored
        b_final = self.book_svc.get_book(self.book.book_id)
        self.assertEqual(b_final.available_copies, 2)
        self.assertEqual(b_final.issued_copies, 0)

    def test_borrowing_limit_enforcement(self):
        """Verify member cannot exceed tier borrowing quota (Student limit = 3)."""
        # Add extra book copies to satisfy inventory
        b2 = self.book_svc.add_book(
            BookDTO(isbn="9780131103627", title="The C Programming Language",
                    author_id=self.author.author_id, publisher_id=self.publisher.publisher_id, category_id=self.category.category_id)
        )
        self.copy_svc.add_copy(BookCopyDTO(book_id=b2.book_id))
        b3 = self.book_svc.add_book(
            BookDTO(isbn="9780201616224", title="The Pragmatic Programmer",
                    author_id=self.author.author_id, publisher_id=self.publisher.publisher_id, category_id=self.category.category_id)
        )
        self.copy_svc.add_copy(BookCopyDTO(book_id=b3.book_id))
        b4 = self.book_svc.add_book(
            BookDTO(isbn="9780134494166", title="Clean Architecture",
                    author_id=self.author.author_id, publisher_id=self.publisher.publisher_id, category_id=self.category.category_id)
        )
        self.copy_svc.add_copy(BookCopyDTO(book_id=b4.book_id))

        # Borrow 3 books (quota limit)
        self.issue_svc.issue_book(self.member.member_id, self.book.book_id)
        self.issue_svc.issue_book(self.member.member_id, b2.book_id)
        self.issue_svc.issue_book(self.member.member_id, b3.book_id)

        # 4th borrow must fail with BorrowingLimitReachedError
        with self.assertRaises(BorrowingLimitReachedError):
            self.issue_svc.issue_book(self.member.member_id, b4.book_id)

    def test_overdue_return_and_fine_generation(self):
        """Verify returning an overdue book calculates late days and assesses fine."""
        loan = self.issue_svc.issue_book(self.member.member_id, self.book.book_id)

        # Simulate return 5 days after due date (student grace period = 1 day -> 4 billable late days)
        due = datetime.datetime.strptime(loan.due_date, "%Y-%m-%d").date()
        simulated_return_date = (due + datetime.timedelta(days=5)).strftime("%Y-%m-%d")

        ret_record, fine = self.return_svc.process_return(loan.borrowing_id, return_date=simulated_return_date)
        self.assertEqual(ret_record.overdue_days, 4)
        # Student tier daily fine rate is $5.00 -> 4 * 5.00 = $20.00
        self.assertEqual(fine, 20.00)

    def test_loan_renewal_flow(self):
        """Verify loan renewal extends due date and increments renewal count up to maximum."""
        loan = self.issue_svc.issue_book(self.member.member_id, self.book.book_id)
        self.assertEqual(loan.renewal_count, 0)

        # 1st renewal
        renew1 = self.renew_svc.request_renewal(loan.borrowing_id, self.member.member_id)
        self.assertNotEqual(renew1.previous_due_date, renew1.new_due_date)

        # 2nd renewal
        renew2 = self.renew_svc.request_renewal(loan.borrowing_id, self.member.member_id)
        self.assertIsNotNone(renew2.renewal_id)

        # 3rd renewal (exceeds max 2 renewals)
        with self.assertRaises(BusinessRuleViolationError):
            self.renew_svc.request_renewal(loan.borrowing_id, self.member.member_id)

if __name__ == "__main__":
    unittest.main()
