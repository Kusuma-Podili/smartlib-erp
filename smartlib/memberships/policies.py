"""Membership policy resolver and circulation limits engine."""
from typing import Dict, Any
from smartlib.constants import MembershipType

DEFAULT_POLICIES: Dict[str, Dict[str, Any]] = {
    MembershipType.STUDENT.value: {
        "max_borrow_limit": 3,
        "loan_duration_days": 14,
        "grace_period_days": 1,
        "max_renewals": 2,
        "daily_fine_rate": 5.00
    },
    MembershipType.FACULTY.value: {
        "max_borrow_limit": 10,
        "loan_duration_days": 60,
        "grace_period_days": 3,
        "max_renewals": 4,
        "daily_fine_rate": 2.00
    },
    MembershipType.STAFF.value: {
        "max_borrow_limit": 5,
        "loan_duration_days": 30,
        "grace_period_days": 2,
        "max_renewals": 3,
        "daily_fine_rate": 5.00
    },
    MembershipType.GENERAL.value: {
        "max_borrow_limit": 2,
        "loan_duration_days": 14,
        "grace_period_days": 1,
        "max_renewals": 1,
        "daily_fine_rate": 10.00
    }
}
