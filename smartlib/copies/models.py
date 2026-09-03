"""Domain entity representing physical serialized library book copies."""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from smartlib.constants import BookCopyStatus, BookCopyCondition

@dataclass
class BookCopy:
    copy_id: Optional[int] = None
    book_id: int = 0
    copy_number: str = ""
    barcode: str = ""
    condition: str = BookCopyCondition.GOOD.value
    status: str = BookCopyStatus.AVAILABLE.value
    acquisition_date: Optional[str] = None
    acquisition_cost: float = 0.00
    notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    book_title: Optional[str] = None
    isbn: Optional[str] = None

    def is_circulatable(self) -> bool:
        return self.status == BookCopyStatus.AVAILABLE.value and self.condition != BookCopyCondition.DAMAGED.value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "copy_id": self.copy_id,
            "book_id": self.book_id,
            "copy_number": self.copy_number,
            "barcode": self.barcode,
            "condition": self.condition,
            "status": self.status,
            "acquisition_date": self.acquisition_date,
            "acquisition_cost": self.acquisition_cost,
            "notes": self.notes,
            "book_title": self.book_title,
            "isbn": self.isbn,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

@dataclass
class BookCopyDTO:
    book_id: int
    condition: str = BookCopyCondition.GOOD.value
    acquisition_cost: float = 0.00
    notes: Optional[str] = None
