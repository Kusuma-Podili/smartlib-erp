"""Strongly Typed Data Transfer Objects (DTOs) and Validation Models for REST API.

Provides dataclass validation, range checking, regex sanitization, and JSON serialization.
"""

import re
import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str] = field(default_factory=list)


# 1. Book Create/Update DTO
@dataclass
class BookDto:
    title: str
    isbn: str
    category_id: int
    publisher_id: int
    author_ids: List[int] = field(default_factory=list)
    publication_year: int = 2026
    edition: Optional[str] = None
    language: str = "eng"
    summary: Optional[str] = None

    def validate(self) -> ValidationResult:
        errors = []
        if not self.title or len(self.title.strip()) < 2:
            errors.append("Title must be at least 2 characters")
        clean_isbn = re.sub(r"[^0-9Xx]", "", self.isbn or "")
        if len(clean_isbn) not in [10, 13]:
            errors.append(f"ISBN must be 10 or 13 digits, got '{self.isbn}'")
        if self.publication_year < 1450 or self.publication_year > 2035:
            errors.append("Invalid publication year")
        if self.category_id <= 0:
            errors.append("Invalid category_id")
        return ValidationResult(len(errors) == 0, errors)


# 2. Member Enrollment DTO
@dataclass
class MemberEnrollmentDto:
    first_name: str
    last_name: str
    email: str
    phone: str = ""
    membership_tier: str = "STUDENT"
    address: str = ""

    def validate(self) -> ValidationResult:
        errors = []
        if not self.first_name or len(self.first_name.strip()) < 1:
            errors.append("First name is required")
        if not self.last_name or len(self.last_name.strip()) < 1:
            errors.append("Last name is required")
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", self.email or ""):
            errors.append("Invalid email address format")
        if self.membership_tier not in ["STUDENT", "FACULTY", "COMMUNITY", "RESEARCHER"]:
            errors.append(f"Unknown membership tier: {self.membership_tier}")
        return ValidationResult(len(errors) == 0, errors)


# 3. Checkout (Issue Loan) DTO
@dataclass
class CheckoutRequestDto:
    patron_id: str
    barcode: str
    loan_duration_days: int = 14
    override_limit: bool = False

    def validate(self) -> ValidationResult:
        errors = []
        if not self.patron_id:
            errors.append("Patron identifier is required")
        if not self.barcode:
            errors.append("Item barcode is required")
        if self.loan_duration_days < 1 or self.loan_duration_days > 90:
            errors.append("Loan duration must be between 1 and 90 days")
        return ValidationResult(len(errors) == 0, errors)


# 4. Checkin (Return Loan) DTO
@dataclass
class CheckinRequestDto:
    barcode: str
    condition_rating: int = 5  # 1-5 scale
    damages_noted: Optional[str] = None
    waive_overdue_fee: bool = False

    def validate(self) -> ValidationResult:
        errors = []
        if not self.barcode:
            errors.append("Barcode is required")
        if self.condition_rating < 1 or self.condition_rating > 5:
            errors.append("Condition rating must be 1 to 5")
        return ValidationResult(len(errors) == 0, errors)


# 5. Fine Assessment DTO
@dataclass
class FineAssessmentDto:
    member_id: int
    amount_cents: int
    reason: str
    loan_id: Optional[int] = None

    def validate(self) -> ValidationResult:
        errors = []
        if self.member_id <= 0:
            errors.append("Valid member_id is required")
        if self.amount_cents <= 0:
            errors.append("Fine amount must be positive")
        if not self.reason or len(self.reason.strip()) < 3:
            errors.append("Reason for fine must be at least 3 characters")
        return ValidationResult(len(errors) == 0, errors)


# 6. Purchase Order Create DTO
@dataclass
class POLineItemDto:
    title: str
    author: str
    isbn: str
    quantity: int
    unit_price_cents: int
    fund_id: str


@dataclass
class PurchaseOrderDto:
    vendor_id: int
    lines: List[POLineItemDto] = field(default_factory=list)
    notes: Optional[str] = None

    def validate(self) -> ValidationResult:
        errors = []
        if self.vendor_id <= 0:
            errors.append("Valid vendor_id is required")
        if not self.lines:
            errors.append("Purchase order must have at least one line item")
        for idx, line in enumerate(self.lines):
            if line.quantity <= 0:
                errors.append(f"Line {idx+1}: Quantity must be at least 1")
            if line.unit_price_cents <= 0:
                errors.append(f"Line {idx+1}: Unit price must be positive")
        return ValidationResult(len(errors) == 0, errors)


# 7. Serial Subscription Create DTO
@dataclass
class SubscriptionDto:
    serial_title: str
    issn: str
    vendor_id: int
    frequency_code: str
    start_date: datetime.date
    end_date: datetime.date
    cost_cents: int = 0

    def validate(self) -> ValidationResult:
        errors = []
        if not self.serial_title:
            errors.append("Serial title is required")
        if not re.match(r"^[0-9]{4}-[0-9]{3}[0-9Xx]$", self.issn or ""):
            errors.append("Invalid ISSN format (must be XXXX-XXXX)")
        if self.start_date >= self.end_date:
            errors.append("Subscription start date must precede end date")
        return ValidationResult(len(errors) == 0, errors)


# 8. Room Reservation DTO
@dataclass
class SpaceReservationDto:
    room_id: str
    patron_id: str
    start_time: datetime.datetime
    duration_hours: int = 2
    party_size: int = 1
    purpose: str = "Academic Study"

    def validate(self) -> ValidationResult:
        errors = []
        if not self.room_id:
            errors.append("Room identifier is required")
        if not self.patron_id:
            errors.append("Patron identifier is required")
        if self.duration_hours < 1 or self.duration_hours > 8:
            errors.append("Duration must be between 1 and 8 hours")
        if self.party_size < 1:
            errors.append("Party size must be at least 1")
        return ValidationResult(len(errors) == 0, errors)
