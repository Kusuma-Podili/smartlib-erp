"""
Comprehensive Test Suite 2: Authors, Categories, Publishers,
Book Master Catalog, ISBN Validations, Physical Copy Barcodes & Status Tracking.
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
from smartlib.books.models import BookDTO, BookFilter
from smartlib.copies.copy_service import CopyService
from smartlib.copies.models import BookCopyDTO
from smartlib.constants import BookCopyStatus, BookCopyCondition
from smartlib.errors import DuplicateEntityError, ValidationError

class TestBooksAndCatalog(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.author_svc = AuthorService()
        self.category_svc = CategoryService()
        self.publisher_svc = PublisherService()
        self.book_svc = BookService()
        self.copy_svc = CopyService()

    def test_complete_catalog_creation_and_inventory_flow(self):
        """
        Verify:
        Admin/Librarian creates Author -> Category -> Publisher -> Book
        -> Adds physical copies -> Barcodes are automatically generated
        -> Book total and available copies count update automatically.
        """
        # 1. Author
        author = self.author_svc.add_author(AuthorDTO(name="Robert C. Martin", nationality="American"))
        self.assertIsNotNone(author.author_id)

        # 2. Category (Dewey 005)
        cat = self.category_svc.add_category(CategoryDTO(code="CS-PROG", name="Computer Programming", dewey_decimal_class="005.1"))
        self.assertIsNotNone(cat.category_id)

        # 3. Publisher
        pub = self.publisher_svc.add_publisher(PublisherDTO(name="Prentice Hall", country="USA"))
        self.assertIsNotNone(pub.publisher_id)

        # 4. Book (Clean Code, ISBN-13)
        book_dto = BookDTO(
            isbn="9780132350884",
            title="Clean Code: A Handbook of Agile Software Craftsmanship",
            author_id=author.author_id,
            publisher_id=pub.publisher_id,
            category_id=cat.category_id,
            price=45.00,
            shelf_number="TECH-A",
            rack_number="R-04"
        )
        book = self.book_svc.add_book(book_dto)
        self.assertEqual(book.total_copies, 0)
        self.assertEqual(book.available_copies, 0)

        # 5. Add 3 physical copies
        copies = self.copy_svc.add_multiple_copies(book.book_id, count=3, cost=40.00)
        self.assertEqual(len(copies), 3)
        self.assertTrue(copies[0].copy_number.startswith("COPY-") and copies[0].copy_number.endswith("-001"))
        self.assertEqual(copies[0].barcode, "BC-9780132350884-001")
        self.assertTrue(copies[1].copy_number.startswith("COPY-") and copies[1].copy_number.endswith("-002"))
        self.assertEqual(copies[1].barcode, "BC-9780132350884-002")

        # 6. Verify master book record synchronization
        updated_book = self.book_svc.get_book(book.book_id)
        self.assertEqual(updated_book.total_copies, 3)
        self.assertEqual(updated_book.available_copies, 3)
        self.assertEqual(updated_book.issued_copies, 0)
        self.assertTrue(updated_book.is_available())

        # 7. Test copy status transition (e.g. Issue COPY-002)
        self.copy_svc.mark_copy_status(copies[1].copy_id, BookCopyStatus.ISSUED.value)
        book_after_issue = self.book_svc.get_book(book.book_id)
        self.assertEqual(book_after_issue.total_copies, 3)
        self.assertEqual(book_after_issue.available_copies, 2)
        self.assertEqual(book_after_issue.issued_copies, 1)

    def test_isbn_validation_and_duplicate_prevention(self):
        """Verify ISBN checksum enforcement and duplicate rejection."""
        author = self.author_svc.add_author(AuthorDTO(name="Martin Fowler"))
        cat = self.category_svc.add_category(CategoryDTO(code="ENG", name="Software Engineering"))
        pub = self.publisher_svc.add_publisher(PublisherDTO(name="Addison-Wesley"))

        # Invalid ISBN checksum
        bad_dto = BookDTO(
            isbn="9780132350889",
            title="Refactoring",
            author_id=author.author_id,
            publisher_id=pub.publisher_id,
            category_id=cat.category_id
        )
        with self.assertRaises(ValidationError):
            self.book_svc.add_book(bad_dto)

        # Valid ISBN-10 (0132350882)
        valid_dto = BookDTO(
            isbn="0132350882",
            title="Clean Code",
            author_id=author.author_id,
            publisher_id=pub.publisher_id,
            category_id=cat.category_id
        )
        book1 = self.book_svc.add_book(valid_dto)
        self.assertIsNotNone(book1.book_id)

        # Duplicate ISBN
        with self.assertRaises(DuplicateEntityError):
            self.book_svc.add_book(valid_dto)

    def test_multi_criteria_search_and_faceted_filtering(self):
        """Verify full text keyword search, category filtering, and availability flags."""
        author = self.author_svc.add_author(AuthorDTO(name="Joshua Bloch"))
        cat = self.category_svc.add_category(CategoryDTO(code="JAVA", name="Java Programming"))
        pub = self.publisher_svc.add_publisher(PublisherDTO(name="Pearson"))

        book_dto = BookDTO(
            isbn="9780134685991",
            title="Effective Java",
            author_id=author.author_id,
            publisher_id=pub.publisher_id,
            category_id=cat.category_id
        )
        book = self.book_svc.add_book(book_dto)
        self.copy_svc.add_copy(BookCopyDTO(book_id=book.book_id))

        # Search by keyword
        res, total = self.book_svc.search(BookFilter(query="Effective"))
        self.assertEqual(total, 1)
        self.assertEqual(res[0].title, "Effective Java")

        # Search by availability
        res_avail, total_avail = self.book_svc.search(BookFilter(available_only=True))
        self.assertTrue(total_avail >= 1)

if __name__ == "__main__":
    unittest.main()
