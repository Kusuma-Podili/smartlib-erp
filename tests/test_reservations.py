"""
Comprehensive Test Suite 4 (Part B): Reservations
FIFO queue position ordering, duplicate prevention, and return hold fulfillment.
"""

import unittest
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
from smartlib.reservations.reservation_service import ReservationService
from smartlib.constants import ReservationStatus
from smartlib.errors import BusinessRuleViolationError

class TestReservations(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.author_svc = AuthorService()
        self.category_svc = CategoryService()
        self.publisher_svc = PublisherService()
        self.book_svc = BookService()
        self.copy_svc = CopyService()
        self.member_svc = MemberService()
        self.reserve_svc = ReservationService()

        # Seed catalog
        author = self.author_svc.add_author(AuthorDTO(name="Donald Knuth"))
        cat = self.category_svc.add_category(CategoryDTO(code="ALG", name="Algorithms"))
        pub = self.publisher_svc.add_publisher(PublisherDTO(name="Addison-Wesley"))
        self.book = self.book_svc.add_book(
            BookDTO(isbn="9780201896831", title="The Art of Computer Programming",
                    author_id=author.author_id, publisher_id=pub.publisher_id, category_id=cat.category_id)
        )
        self.copy = self.copy_svc.add_copy(BookCopyDTO(book_id=self.book.book_id))

        # Seed 2 members
        self.member1 = self.member_svc.register_member(MemberDTO(first_name="Alice", last_name="Smith", email="alice@test.com"))
        self.member2 = self.member_svc.register_member(MemberDTO(first_name="Bob", last_name="Jones", email="bob@test.com"))

    def test_fifo_queue_ordering_and_duplicate_prevention(self):
        """Verify queue positions (1, 2) and rejection of duplicate active hold requests."""
        # Member 1 reserves
        res1 = self.reserve_svc.reserve_book(self.member1.member_id, self.book.book_id)
        self.assertEqual(res1.queue_position, 1)
        self.assertEqual(res1.status, ReservationStatus.PENDING.value)

        # Duplicate reservation by Member 1 should fail
        with self.assertRaises(BusinessRuleViolationError):
            self.reserve_svc.reserve_book(self.member1.member_id, self.book.book_id)

        # Member 2 reserves
        res2 = self.reserve_svc.reserve_book(self.member2.member_id, self.book.book_id)
        self.assertEqual(res2.queue_position, 2)

    def test_reservation_hold_fulfillment_on_return(self):
        """Verify returned book transitions the head of the reservation queue to READY_FOR_PICKUP."""
        self.reserve_svc.reserve_book(self.member1.member_id, self.book.book_id)
        self.reserve_svc.reserve_book(self.member2.member_id, self.book.book_id)

        # Book returns: hold fulfillment scanner triggers
        notified_res = self.reserve_svc.process_returned_book_holds(self.book.book_id, hold_days=3)
        self.assertIsNotNone(notified_res)
        self.assertEqual(notified_res.member_id, self.member1.member_id)
        self.assertEqual(notified_res.status, ReservationStatus.READY_FOR_PICKUP.value)
        self.assertIsNotNone(notified_res.hold_expiry_date)

if __name__ == "__main__":
    unittest.main()
