"""Domain entities and DTOs for library patrons."""
from dataclasses import dataclass
from typing import Optional, Dict, Any
import datetime
from smartlib.constants import MembershipType, MembershipStatus

@dataclass
class Member:
    member_id: Optional[int] = None
    user_id: int = 0
    member_code: str = ""       # e.g. "MEM-2026-0001"
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: Optional[str] = None
    address: Optional[str] = None
    membership_type: str = MembershipType.STUDENT.value
    registration_date: Optional[str] = None
    expiry_date: str = ""
    status: str = MembershipStatus.ACTIVE.value
    notes: Optional[str] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def is_active(self) -> bool:
        return self.status == MembershipStatus.ACTIVE.value

    def is_expired(self, as_of_date: Optional[str] = None) -> bool:
        current = datetime.date.today()
        if as_of_date:
            try:
                current = datetime.datetime.strptime(as_of_date, "%Y-%m-%d").date()
            except ValueError:
                pass
        exp = datetime.datetime.strptime(self.expiry_date, "%Y-%m-%d").date()
        return current > exp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "member_id": self.member_id,
            "user_id": self.user_id,
            "member_code": self.member_code,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "membership_type": self.membership_type,
            "registration_date": self.registration_date,
            "expiry_date": self.expiry_date,
            "status": self.status,
            "notes": self.notes
        }

@dataclass
class MemberDTO:
    first_name: str
    last_name: str
    email: str
    membership_type: str = MembershipType.STUDENT.value
    phone: Optional[str] = None
    address: Optional[str] = None
    password: Optional[str] = None
    duration_days: int = 365
    notes: Optional[str] = None
