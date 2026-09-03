"""
Enterprise date, time, duration, and business day calculations.
"""

import datetime
from typing import Optional, Union

ISO_FORMAT = "%Y-%m-%d"
DATETIME_ISO_FORMAT = "%Y-%m-%d %H:%M:%S"

def now_utc() -> datetime.datetime:
    """Get current UTC datetime."""
    return datetime.datetime.now(datetime.timezone.utc)

def now_iso() -> str:
    """Return current UTC timestamp as ISO string."""
    return now_utc().strftime(DATETIME_ISO_FORMAT)

def today_iso() -> str:
    """Return current date in YYYY-MM-DD format."""
    return datetime.date.today().strftime(ISO_FORMAT)

def parse_date(date_input: Union[str, datetime.date, datetime.datetime]) -> datetime.date:
    """Parse date string or object into datetime.date."""
    if isinstance(date_input, datetime.datetime):
        return date_input.date()
    if isinstance(date_input, datetime.date):
        return date_input
    if isinstance(date_input, str):
        cleaned = date_input.strip()
        for fmt in (ISO_FORMAT, DATETIME_ISO_FORMAT, "%Y-%m-%dT%H:%M:%S", "%Y/%m/%d", "%d-%m-%Y"):
            try:
                return datetime.datetime.strptime(cleaned, fmt).date()
            except ValueError:
                continue
    raise ValueError(f"Unable to parse date string: {date_input}")

def parse_datetime(dt_input: Union[str, datetime.datetime]) -> datetime.datetime:
    """Parse datetime string or object into datetime.datetime."""
    if isinstance(dt_input, datetime.datetime):
        return dt_input
    if isinstance(dt_input, str):
        cleaned = dt_input.strip()
        for fmt in (DATETIME_ISO_FORMAT, "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", ISO_FORMAT):
            try:
                return datetime.datetime.strptime(cleaned, fmt)
            except ValueError:
                continue
    raise ValueError(f"Unable to parse datetime: {dt_input}")

def add_days(date_input: Union[str, datetime.date], days: int) -> str:
    """Add days to a given date and return ISO formatted string."""
    d = parse_date(date_input)
    res = d + datetime.timedelta(days=days)
    return res.strftime(ISO_FORMAT)

def days_between(start_date: Union[str, datetime.date], end_date: Union[str, datetime.date]) -> int:
    """Calculate elapsed calendar days between two dates."""
    d1 = parse_date(start_date)
    d2 = parse_date(end_date)
    return (d2 - d1).days

def is_overdue(due_date: Union[str, datetime.date], as_of: Optional[Union[str, datetime.date]] = None) -> bool:
    """Check if due_date is earlier than as_of date (defaulting to today)."""
    target = parse_date(due_date)
    current = parse_date(as_of) if as_of else datetime.date.today()
    return current > target

def calculate_overdue_days(due_date: Union[str, datetime.date], return_date: Optional[Union[str, datetime.date]] = None) -> int:
    """Return overdue days. Returns 0 if returned on or before due date."""
    d_due = parse_date(due_date)
    d_ret = parse_date(return_date) if return_date else datetime.date.today()
    diff = (d_ret - d_due).days
    return max(0, diff)

def is_expired(expiry_date: Union[str, datetime.date], as_of: Optional[Union[str, datetime.date]] = None) -> bool:
    """Check if an expiry date has passed."""
    exp = parse_date(expiry_date)
    current = parse_date(as_of) if as_of else datetime.date.today()
    return current > exp
