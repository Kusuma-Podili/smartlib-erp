"""Book master management business service."""
from typing import Optional, List, Tuple
from smartlib.books.models import Book, BookDTO, BookFilter
from smartlib.books.repository import BookRepository
from smartlib.books.search_engine import BookSearchEngine
from smartlib.validation.validators import validate_isbn, validate_positive_number
from smartlib.audit.audit_service import AuditService
from smartlib.constants import AuditAction, BookCopyStatus
from smartlib.errors import DuplicateEntityError, EntityNotFoundError, ValidationError

class BookService:
    def __init__(self, repo: Optional[BookRepository] = None, audit_svc: Optional[AuditService] = None):
        self.repo = repo or BookRepository()
        self.search_engine = BookSearchEngine(self.repo)
        self.audit_svc = audit_svc or AuditService()

    def add_book(self, dto: BookDTO, actor_username: str = "librarian") -> Book:
        if not dto.title or not dto.title.strip():
            raise ValidationError("Book title is required.", {"title": "Required field."})

        clean_isbn = validate_isbn(dto.isbn)
        if self.repo.get_by_isbn(clean_isbn):
            raise DuplicateEntityError("Book", "ISBN", clean_isbn)

        validate_positive_number(dto.price, "Price")

        book = Book(
            isbn=clean_isbn,
            title=dto.title.strip(),
            subtitle=dto.subtitle.strip() if dto.subtitle else None,
            author_id=dto.author_id,
            publisher_id=dto.publisher_id,
            category_id=dto.category_id,
            edition=dto.edition,
            publication_year=dto.publication_year,
            language=dto.language,
            description=dto.description,
            shelf_number=dto.shelf_number,
            rack_number=dto.rack_number,
            price=dto.price,
            total_copies=0,
            available_copies=0,
            status=BookCopyStatus.AVAILABLE.value
        )
        created = self.repo.create(book)
        self.audit_svc.log(
            action=AuditAction.BOOK_CREATE.value,
            entity_type="Book",
            entity_id=created.book_id,
            username=actor_username,
            description=f"Created book title '{created.title}' (ISBN: {created.isbn})."
        )
        return created

    def get_book(self, book_id: int) -> Book:
        b = self.repo.get_by_id(book_id)
        if not b:
            raise EntityNotFoundError("Book", book_id)
        return b

    def get_book_by_isbn(self, isbn: str) -> Book:
        clean_isbn = validate_isbn(isbn)
        b = self.repo.get_by_isbn(clean_isbn)
        if not b:
            raise EntityNotFoundError("Book with ISBN", clean_isbn)
        return b

    def search(self, spec: BookFilter) -> Tuple[List[Book], int]:
        return self.repo.search_books(spec)
