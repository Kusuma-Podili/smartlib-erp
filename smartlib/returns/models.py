"""Book return check-in record entity."""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from smartlib.constants import BookCopyCondition

@dataclass
class ReturnRecord:
    return_id: Optional[int] = None
    borrowing_id: int = 0
    returned_date: str = ""
    received_by_librarian_id: Optional[int] = None
    overdue_days: int = 0
    fine_amount: float = 0.00
    condition_on_return: str = BookCopyCondition.GOOD.value
    notes: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "return_id": self.return_id,
            "borrowing_id": self.borrowing_id,
            "returned_date": self.returned_date,
            "received_by_librarian_id": self.received_by_librarian_id,
            "overdue_days": self.overdue_days,
            "fine_amount": self.fine_amount,
            "condition_on_return": self.condition_on_return,
            "notes": self.notes,
            "created_at": self.created_at
        }
