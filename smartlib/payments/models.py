"""Cashier payment transaction entity."""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from smartlib.constants import PaymentMethod

@dataclass
class PaymentTransaction:
    payment_id: Optional[int] = None
    fine_id: int = 0
    member_id: int = 0
    processed_by_librarian_id: Optional[int] = None
    amount: float = 0.00
    payment_method: str = PaymentMethod.CASH.value
    receipt_number: str = ""   # e.g. "REC-2026-00001"
    transaction_reference: Optional[str] = None
    payment_date: Optional[str] = None
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "payment_id": self.payment_id,
            "fine_id": self.fine_id,
            "member_id": self.member_id,
            "processed_by_librarian_id": self.processed_by_librarian_id,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "receipt_number": self.receipt_number,
            "transaction_reference": self.transaction_reference,
            "payment_date": self.payment_date,
            "notes": self.notes
        }
