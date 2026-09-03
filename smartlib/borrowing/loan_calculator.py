"""Loan due date calculator based on membership tier."""
import datetime
from typing import Optional
from smartlib.utilities.date_utils import add_days, today_iso

class LoanCalculator:
    @staticmethod
    def calculate_due_date(loan_duration_days: int, start_date: Optional[str] = None) -> str:
        base = start_date or today_iso()
        return add_days(base, loan_duration_days)
