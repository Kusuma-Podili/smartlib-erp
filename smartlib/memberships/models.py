"""Membership tier domain model and DTO."""
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class MembershipTier:
    tier_id: Optional[int] = None
    tier_type: str = ""         # STUDENT, FACULTY, STAFF, GENERAL
    name: str = ""
    max_borrow_limit: int = 3
    loan_duration_days: int = 14
    grace_period_days: int = 1
    max_renewals: int = 2
    daily_fine_rate: float = 10.00
    description: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tier_id": self.tier_id,
            "tier_type": self.tier_type,
            "name": self.name,
            "max_borrow_limit": self.max_borrow_limit,
            "loan_duration_days": self.loan_duration_days,
            "grace_period_days": self.grace_period_days,
            "max_renewals": self.max_renewals,
            "daily_fine_rate": self.daily_fine_rate,
            "description": self.description,
            "created_at": self.created_at
        }
