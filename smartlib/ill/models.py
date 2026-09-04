"""Interlibrary Loan data models and lifecycle states."""

from enum import Enum, auto
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
import datetime


class IllRequestType(Enum):
    BORROWING = "borrowing"  # Requesting an item from an external library for our patron
    LENDING = "lending"      # Providing an item from our collection to an external library


class IllServiceType(Enum):
    PHYSICAL_LOAN = "physical_loan"
    COPY_NON_RETURNABLE = "copy_non_returnable"  # Article scan, chapter photocopy
    DIGITAL_DELIVERY = "digital_delivery"        # PDF document delivery


class IllStatus(Enum):
    SUBMITTED = "submitted"
    VERIFIED = "verified"
    LOCATING_SUPPLIER = "locating_supplier"
    REQUESTED_FROM_PARTNER = "requested_from_partner"
    ACCEPTED_BY_PARTNER = "accepted_by_partner"
    REJECTED_BY_PARTNER = "rejected_by_partner"
    IN_TRANSIT_INBOUND = "in_transit_inbound"
    RECEIVED_AT_LIBRARY = "received_at_library"
    READY_FOR_PATRON = "ready_for_patron"
    CHECKED_OUT_TO_PATRON = "checked_out_to_patron"
    RETURNED_BY_PATRON = "returned_by_patron"
    IN_TRANSIT_OUTBOUND = "in_transit_outbound"
    RETURNED_TO_PARTNER = "returned_to_partner"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    UNFILLED = "unfilled"


class DeliveryFormat(Enum):
    PRINT = "print"
    PDF = "pdf"
    TIFF = "tiff"
    PHYSICAL_MEDIA = "physical_media"


@dataclass
class LendingPolicy:
    institution_code: str
    max_loan_days: int = 30
    renewal_allowed: bool = True
    max_renewals: int = 1
    charge_per_loan_cents: int = 0
    charge_per_article_cents: int = 0
    accepts_electronic_delivery: bool = True
    participates_in_reciprocal_borrowing: bool = True


@dataclass
class PartnerInstitution:
    id: str
    name: str
    symbol_oclc: str
    symbol_isin: str
    contact_email: str
    ill_phone: str
    shipping_address: str
    iso18626_endpoint: Optional[str] = None
    is_active: bool = True
    policy: Optional[LendingPolicy] = None


@dataclass
class IllMessage:
    id: str
    ill_request_id: str
    sender: str
    recipient: str
    message_type: str
    content: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)


@dataclass
class IllRequest:
    id: str
    request_type: IllRequestType
    service_type: IllServiceType
    patron_id: str
    status: IllStatus = IllStatus.SUBMITTED
    partner_institution_id: Optional[str] = None
    
    # Bibliographic Details
    title: str = ""
    author: Optional[str] = None
    isbn: Optional[str] = None
    issn: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    year: Optional[str] = None
    pages: Optional[str] = None
    article_title: Optional[str] = None
    
    # Fulfillment Details
    tracking_number: Optional[str] = None
    shipping_carrier: Optional[str] = None
    due_date_to_partner: Optional[datetime.date] = None
    due_date_for_patron: Optional[datetime.date] = None
    charge_cents: int = 0
    copyright_compliance_status: str = "CCL"  # Copyright Compliance Law (CONTU)
    electronic_download_url: Optional[str] = None
    notes: List[str] = field(default_factory=list)
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = field(default_factory=datetime.datetime.now)

    def is_terminal(self) -> bool:
        return self.status in [IllStatus.COMPLETED, IllStatus.CANCELLED, IllStatus.UNFILLED]
