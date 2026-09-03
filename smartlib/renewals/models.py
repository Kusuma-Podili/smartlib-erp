"""Renewal request domain entity."""
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class RenewalRecord:
    renewal_id: Optional[int] = None
    borrowing_id: int = 0
    requested_by_member_id: int = 0
    approved_by_librarian_id: Optional[int] = None
    previous_due_date: str = ""
    new_due_date: str = ""
    renewal_date: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "renewal_id": self.renewal_id,
            "borrowing_id": self.borrowing_id,
            "requested_by_member_id": self.requested_by_member_id,
            "approved_by_librarian_id": self.approved_by_librarian_id,
            "previous_due_date": self.previous_due_date,
            "new_due_date": self.new_due_date,
            "renewal_date": self.renewal_date
        }
