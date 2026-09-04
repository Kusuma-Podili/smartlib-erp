"""Serials data models: Subscriptions, Frequency, Issues, and Claims."""

from enum import Enum, auto
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
import datetime


class IssueStatus(Enum):
    EXPECTED = "expected"
    ARRIVED = "arrived"
    LATE = "late"
    CLAIMED = "claimed"
    BOUND = "bound"
    LOST = "lost"


class FrequencyType(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    BIMONTHLY = "bimonthly"
    QUARTERLY = "quarterly"
    SEMIANNUAL = "semiannual"
    ANNUAL = "annual"
    IRREGULAR = "irregular"


@dataclass
class FrequencyPattern:
    id: str
    code: str
    name: str
    frequency_type: FrequencyType
    issues_per_year: int
    issues_per_volume: int
    months_between_issues: int = 1


@dataclass
class Subscription:
    id: str
    serial_title_id: str
    vendor_id: str
    start_date: datetime.date
    end_date: datetime.date
    auto_renew: bool = True
    cost_cents: int = 0
    fund_id: str = ""
    is_active: bool = True


@dataclass
class IssueInstance:
    id: str
    subscription_id: str
    volume_number: str
    issue_number: str
    enumeration: str
    chronology: str
    expected_date: datetime.date
    arrived_date: Optional[datetime.date] = None
    status: IssueStatus = IssueStatus.EXPECTED
    barcode: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class ClaimNotice:
    id: str
    issue_id: str
    vendor_id: str
    claim_count: int = 1
    sent_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    response_note: Optional[str] = None
    resolved: bool = False


@dataclass
class BindingUnit:
    id: str
    subscription_id: str
    title: str
    volume: str
    issues_included: List[str] = field(default_factory=list)
    binder_name: str = "Central University Bindery"
    sent_to_bindery_at: Optional[datetime.date] = None
    returned_from_bindery_at: Optional[datetime.date] = None
    spine_title: str = ""


@dataclass
class RoutingList:
    id: str
    subscription_id: str
    recipient_patron_ids: List[str] = field(default_factory=list)


@dataclass
class SerialTitle:
    id: str
    title: str
    issn: str
    publisher: str
    frequency_code: str
    current_subscription_id: Optional[str] = None
