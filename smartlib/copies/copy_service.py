"""Physical copy operations service. Synchronizes book master totals automatically."""
from typing import Optional, List
from smartlib.copies.models import BookCopy, BookCopyDTO
from smartlib.copies.repository import CopyRepository
from smartlib.copies.barcode_generator import BarcodeGenerator
from smartlib.books.repository import BookRepository
from smartlib.audit.audit_service import AuditService
from smartlib.constants import BookCopyStatus, BookCopyCondition, AuditAction
from smartlib.errors import EntityNotFoundError

class CopyService:
    def __init__(
        self,
        copy_repo: Optional[CopyRepository] = None,
        book_repo: Optional[BookRepository] = None,
        audit_svc: Optional[AuditService] = None
    ):
        self.copy_repo = copy_repo or CopyRepository()
        self.repo = self.copy_repo
        self.book_repo = book_repo or BookRepository()
        self.audit_svc = audit_svc or AuditService()

    def add_copy(self, dto: BookCopyDTO, actor_username: str = "librarian") -> BookCopy:
        book = self.book_repo.get_by_id(dto.book_id)
        if not book:
            raise EntityNotFoundError("Book", dto.book_id)

        next_idx = self.copy_repo.get_next_copy_index(dto.book_id)
        barcode = BarcodeGenerator.generate_barcode(book.isbn, next_idx)
        copy_num = BarcodeGenerator.generate_copy_number(next_idx, book_id=dto.book_id)

        copy = BookCopy(
            book_id=dto.book_id,
            copy_number=copy_num,
            barcode=barcode,
            condition=dto.condition,
            status=BookCopyStatus.AVAILABLE.value,
            acquisition_cost=dto.acquisition_cost,
            notes=dto.notes
        )
        created_copy = self.copy_repo.create(copy)
        self.book_repo.update_copy_counts(dto.book_id)

        self.audit_svc.log(
            action=AuditAction.COPY_CREATE.value,
            entity_type="BookCopy",
            entity_id=created_copy.copy_id,
            username=actor_username,
            description=f"Added copy '{copy_num}' (Barcode: {barcode}) for '{book.title}'."
        )
        return created_copy

    def add_multiple_copies(self, book_id: int, count: int, cost: float = 0.00, actor_username: str = "librarian") -> List[BookCopy]:
        created = []
        for _ in range(count):
            created.append(self.add_copy(BookCopyDTO(book_id=book_id, acquisition_cost=cost), actor_username=actor_username))
        return created

    def mark_copy_status(self, copy_id: int, status: str, condition: Optional[str] = None, actor_username: str = "librarian") -> BookCopy:
        copy = self.copy_repo.get_by_id(copy_id)
        if not copy:
            raise EntityNotFoundError("BookCopy", copy_id)

        old_status = copy.status
        self.copy_repo.update_status_and_condition(copy_id, status, condition)
        self.book_repo.update_copy_counts(copy.book_id)

        self.audit_svc.log(
            action=AuditAction.COPY_STATUS_CHANGE.value,
            entity_type="BookCopy",
            entity_id=copy_id,
            username=actor_username,
            description=f"Changed copy {copy.copy_number} status from {old_status} to {status}."
        )
        return self.copy_repo.get_by_id(copy_id)

    def get_copy_by_barcode(self, barcode: str) -> BookCopy:
        c = self.copy_repo.get_by_barcode(barcode)
        if not c:
            raise EntityNotFoundError("BookCopy with barcode", barcode)
        return c

    def list_copies_for_book(self, book_id: int) -> List[BookCopy]:
        return self.copy_repo.list_by_book_id(book_id)
