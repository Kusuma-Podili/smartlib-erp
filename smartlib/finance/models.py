"""Financial and General Ledger Data Models."""

from enum import Enum, auto
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
import datetime


class AccountType(Enum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class NormalBalance(Enum):
    DEBIT = "debit"
    CREDIT = "credit"


@dataclass
class Account:
    code: str
    name: str
    account_type: AccountType
    normal_balance: NormalBalance
    description: str = ""
    is_active: bool = True
    parent_code: Optional[str] = None
    balance_cents: int = 0

    def apply_posting(self, debit_cents: int, credit_cents: int):
        if self.normal_balance == NormalBalance.DEBIT:
            self.balance_cents += (debit_cents - credit_cents)
        else:
            self.balance_cents += (credit_cents - debit_cents)


@dataclass
class JournalLine:
    account_code: str
    debit_cents: int = 0
    credit_cents: int = 0
    memo: str = ""

    def __post_init__(self):
        if self.debit_cents < 0 or self.credit_cents < 0:
            raise ValueError("Debits and credits must be non-negative")
        if self.debit_cents > 0 and self.credit_cents > 0:
            raise ValueError("A line item cannot have both debit and credit")


@dataclass
class JournalEntry:
    id: str
    reference_number: str
    date: datetime.date
    description: str
    lines: List[JournalLine] = field(default_factory=list)
    posted: bool = False
    posted_at: Optional[datetime.datetime] = None
    posted_by: Optional[str] = None

    @property
    def total_debits(self) -> int:
        return sum(line.debit_cents for line in self.lines)

    @property
    def total_credits(self) -> int:
        return sum(line.credit_cents for line in self.lines)

    def is_balanced(self) -> bool:
        return self.total_debits == self.total_credits and self.total_debits > 0


@dataclass
class FiscalPeriod:
    id: str
    name: str
    start_date: datetime.date
    end_date: datetime.date
    is_closed: bool = False


@dataclass
class CashRegisterSession:
    id: str
    cashier_id: str
    opened_at: datetime.datetime
    opening_cash_cents: int
    closed_at: Optional[datetime.datetime] = None
    closing_cash_cents: Optional[int] = None
    expected_cash_cents: int = 0
    total_fines_collected_cents: int = 0
    discrepancy_cents: int = 0
