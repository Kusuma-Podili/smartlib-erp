"""Overdue days and grace period assessor."""
import datetime
from typing import Tuple
from smartlib.utilities.date_utils import calculate_overdue_days

class OverdueChecker:
    @staticmethod
    def assess_overdue(due_date: str, return_date: str, grace_period_days: int = 1) -> Tuple[int, bool]:
        raw_overdue = calculate_overdue_days(due_date, return_date)
        if raw_overdue <= grace_period_days:
            return 0, False
        effective_late = raw_overdue - grace_period_days
        return effective_late, True
