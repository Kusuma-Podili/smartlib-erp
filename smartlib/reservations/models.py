"""Reservation hold domain entity."""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from smartlib.constants import ReservationStatus

@dataclass
class Reservation:
    reservation_id: Optional[int] = None
    book_id: int = 0
    member_id: int = 0
    reservation_date: Optional[str] = None
    queue_position: int = 1
    status: str = ReservationStatus.PENDING.value
    available_since: Optional[str] = None
    hold_expiry_date: Optional[str] = None
    fulfilled_at: Optional[str] = None

    # Joined fields
    book_title: Optional[str] = None
    isbn: Optional[str] = None
    member_name: Optional[str] = None
    member_code: Optional[str] = None

    def is_active(self) -> bool:
        return self.status in (ReservationStatus.PENDING.value, ReservationStatus.READY_FOR_PICKUP.value)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "reservation_id": self.reservation_id,
            "book_id": self.book_id,
            "member_id": self.member_id,
            "reservation_date": self.reservation_date,
            "queue_position": self.queue_position,
            "status": self.status,
            "available_since": self.available_since,
            "hold_expiry_date": self.hold_expiry_date,
            "fulfilled_at": self.fulfilled_at,
            "book_title": self.book_title,
            "isbn": self.isbn,
            "member_name": self.member_name,
            "member_code": self.member_code
        }
