"""Circulation borrowing loan entity and DTO."""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from smartlib.constants import BorrowingStatus

@dataclass
class BorrowingRecord:
    borrowing_id: Optional[int] = None
    member_id: int = 0
    book_id: int = 0
    copy_id: int = 0
    issued_by_librarian_id: Optional[int] = None
    issue_date: str = ""
    due_date: str = ""
    renewal_count: int = 0
    max_renewals_allowed: int = 2
    status: str = BorrowingStatus.ACTIVE.value
    notes: Optional[str] = None
    created_at: Optional[str] = None

    # Joined fields
    book_title: Optional[str] = None
    isbn: Optional[str] = None
    copy_number: Optional[str] = None
    barcode: Optional[str] = None
    member_name: Optional[str] = None
    member_code: Optional[str] = None

    def is_active(self) -> bool:
        return self.status in (BorrowingStatus.ACTIVE.value, BorrowingStatus.OVERDUE.value)

    def is_overdue(self) -> bool:
        return self.status == BorrowingStatus.OVERDUE.value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "borrowing_id": self.borrowing_id,
            "member_id": self.member_id,
            "book_id": self.book_id,
            "copy_id": self.copy_id,
            "issued_by_librarian_id": self.issued_by_librarian_id,
            "issue_date": self.issue_date,
            "due_date": self.due_date,
            "renewal_count": self.renewal_count,
            "max_renewals_allowed": self.max_renewals_allowed,
            "status": self.status,
            "notes": self.notes,
            "book_title": self.book_title,
            "isbn": self.isbn,
            "copy_number": self.copy_number,
            "barcode": self.barcode,
            "member_name": self.member_name,
            "member_code": self.member_code,
            "created_at": self.created_at
        }
