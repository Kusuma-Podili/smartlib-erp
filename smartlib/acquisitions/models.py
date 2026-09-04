"""Acquisitions data models: Vendors, Funds, Purchase Orders, and Invoices."""

from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
import datetime


class POStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    SENT_TO_VENDOR = "sent_to_vendor"
    PARTIALLY_RECEIVED = "partially_received"
    FULLY_RECEIVED = "fully_received"
    CANCELLED = "cancelled"
    CLOSED = "closed"


class InvoiceStatus(Enum):
    DRAFT = "draft"
    AWAITING_MATCH = "awaiting_match"
    APPROVED = "approved"
    PAID = "paid"
    CANCELLED = "cancelled"


@dataclass
class Vendor:
    id: str
    code: str
    name: str
    contact_person: str
    email: str
    phone: str
    address: str
    tax_identifier: str = ""
    discount_percentage: float = 0.0
    payment_terms_days: int = 30
    is_active: bool = True
    edifact_endpoint: Optional[str] = None


@dataclass
class FiscalYear:
    code: str
    name: str
    start_date: datetime.date
    end_date: datetime.date
    is_closed: bool = False


@dataclass
class Fund:
    id: str
    code: str
    name: str
    fiscal_year_code: str
    allocated_amount_cents: int
    encumbered_cents: int = 0
    expended_cents: int = 0

    @property
    def available_cents(self) -> int:
        return self.allocated_amount_cents - self.encumbered_cents - self.expended_cents


@dataclass
class Ledger:
    id: str
    code: str
    name: str
    fiscal_year_code: str
    funds: List[Fund] = field(default_factory=list)


@dataclass
class POLineItem:
    id: str
    po_id: str
    title: str
    author: Optional[str] = None
    isbn: Optional[str] = None
    quantity: int = 1
    unit_price_cents: int = 0
    fund_id: str = ""
    quantity_received: int = 0

    @property
    def total_cost_cents(self) -> int:
        return self.quantity * self.unit_price_cents


@dataclass
class PurchaseOrder:
    id: str
    po_number: str
    vendor_id: str
    status: POStatus = POStatus.DRAFT
    lines: List[POLineItem] = field(default_factory=list)
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    approved_by: Optional[str] = None
    notes: Optional[str] = None

    @property
    def total_amount_cents(self) -> int:
        return sum(line.total_cost_cents for line in self.lines)


@dataclass
class ReceivingRecord:
    id: str
    po_line_id: str
    barcode_assigned: str
    received_by: str
    condition_notes: str = "New"
    received_at: datetime.datetime = field(default_factory=datetime.datetime.now)


@dataclass
class InvoiceLine:
    id: str
    po_line_id: Optional[str]
    description: str
    amount_cents: int


@dataclass
class Invoice:
    id: str
    invoice_number: str
    vendor_id: str
    status: InvoiceStatus = InvoiceStatus.DRAFT
    lines: List[InvoiceLine] = field(default_factory=list)
    subtotal_cents: int = 0
    tax_cents: int = 0
    shipping_cents: int = 0
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)

    @property
    def total_cents(self) -> int:
        return self.subtotal_cents + self.tax_cents + self.shipping_cents
