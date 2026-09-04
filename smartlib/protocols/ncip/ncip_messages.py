"""NCIP 2.0 XML Messages and Object Models."""

from typing import Optional, List
from dataclasses import dataclass, field
import xml.etree.ElementTree as ET

NCIP_NS = "http://www.niso.org/2008/ncip"


@dataclass
class NcipInitiationHeader:
    from_agency_id: str
    to_agency_id: str


@dataclass
class CheckOutItemRequest:
    user_id: str
    item_barcode: str
    desired_due_date: Optional[str] = None


@dataclass
class CheckOutItemResponse:
    success: bool
    user_id: str
    item_barcode: str
    due_date: str
    problem_detail: Optional[str] = None


@dataclass
class CheckInItemRequest:
    item_barcode: str


@dataclass
class CheckInItemResponse:
    success: bool
    item_barcode: str
    routing_action: str = "Reshelve"
    problem_detail: Optional[str] = None


@dataclass
class LookupUserRequest:
    user_id: str


@dataclass
class LookupUserResponse:
    user_id: str
    full_name: str
    email: str
    user_status: str
    overdue_count: int
    unpaid_fines_cents: int
