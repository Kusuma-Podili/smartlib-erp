"""Fine assessment domain entity."""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from smartlib.constants import FineType, FineStatus

@dataclass
class Fine:
    fine_id: Optional[int] = None
    member_id: int = 0
    borrowing_id: Optional[int] = None
    fine_type: str = FineType.OVERDUE.value
    amount: float = 0.00
    paid_amount: float = 0.00
    balance_amount: float = 0.00
    status: str = FineStatus.UNPAID.value
    reason: Optional[str] = None
    created_at: Optional[str] = None

    # Joined fields
    member_name: Optional[str] = None
    member_code: Optional[str] = None
    book_title: Optional[str] = None

    def is_outstanding(self) -> bool:
        return self.status in (FineStatus.UNPAID.value, FineStatus.PARTIALLY_PAID.value) and self.balance_amount > 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fine_id": self.fine_id,
            "member_id": self.member_id,
            "borrowing_id": self.borrowing_id,
            "fine_type": self.fine_type,
            "amount": self.amount,
            "paid_amount": self.paid_amount,
            "balance_amount": self.balance_amount,
            "status": self.status,
            "reason": self.reason,
            "member_name": self.member_name,
            "member_code": self.member_code,
            "book_title": self.book_title,
            "created_at": self.created_at
        }
