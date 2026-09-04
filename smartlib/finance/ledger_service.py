"""General Ledger Double-Entry Bookkeeping Service."""

from typing import Dict, List, Optional, Tuple
import datetime
from .models import Account, JournalEntry, JournalLine, AccountType, NormalBalance
from .chart_of_accounts import STANDARD_LIBRARY_ACCOUNTS


class GeneralLedgerService:
    """Manages postings, ledger balance verification, and journal entries."""

    def __init__(self):
        # Deep copy or reference standard chart of accounts
        self.accounts: Dict[str, Account] = {
            code: Account(
                code=a.code, name=a.name, account_type=a.account_type,
                normal_balance=a.normal_balance, description=a.description
            )
            for code, a in STANDARD_LIBRARY_ACCOUNTS.items()
        }
        self.journal_entries: List[JournalEntry] = []

    def get_account(self, code: str) -> Optional[Account]:
        return self.accounts.get(code)

    def record_journal_entry(self, ref_num: str, date: datetime.date, description: str,
                             lines: List[JournalLine], posted_by: str = "System") -> Tuple[bool, Optional[JournalEntry], str]:
        entry = JournalEntry(
            id=f"JE-{len(self.journal_entries)+1:06d}",
            reference_number=ref_num,
            date=date,
            description=description,
            lines=lines,
            posted_by=posted_by
        )

        if not entry.is_balanced():
            return False, None, f"Unbalanced entry: Debits ({entry.total_debits}) != Credits ({entry.total_credits})"

        # Verify all accounts exist
        for line in lines:
            if line.account_code not in self.accounts:
                return False, None, f"Unknown account code '{line.account_code}'"

        # Apply posting
        for line in lines:
            acct = self.accounts[line.account_code]
            acct.apply_posting(line.debit_cents, line.credit_cents)

        entry.posted = True
        entry.posted_at = datetime.datetime.now()
        self.journal_entries.append(entry)
        return True, entry, "Posted successfully"

    def record_patron_fine_payment(self, fine_id: str, amount_cents: int, payment_method: str = "cash") -> Tuple[bool, Optional[JournalEntry], str]:
        """Convenience helper: Debit Cash/Clearing, Credit Fine Revenue."""
        cash_account = "1010" if payment_method.lower() == "cash" else "1030"
        lines = [
            JournalLine(account_code=cash_account, debit_cents=amount_cents, memo=f"Fine payment received ({payment_method})"),
            JournalLine(account_code="4010", credit_cents=amount_cents, memo=f"Overdue fine revenue for fine #{fine_id}")
        ]
        return self.record_journal_entry(
            ref_num=f"FINE-PMT-{fine_id}",
            date=datetime.date.today(),
            description=f"Patron fine collection #{fine_id}",
            lines=lines
        )

    def verify_trial_balance(self) -> Tuple[bool, int, int]:
        """Verify that total debits equal total credits across all accounts."""
        total_debits = 0
        total_credits = 0
        for acct in self.accounts.values():
            if acct.normal_balance == NormalBalance.DEBIT:
                if acct.balance_cents >= 0:
                    total_debits += acct.balance_cents
                else:
                    total_credits += abs(acct.balance_cents)
            else:
                if acct.balance_cents >= 0:
                    total_credits += acct.balance_cents
                else:
                    total_debits += abs(acct.balance_cents)

        is_balanced = (total_debits == total_credits)
        return is_balanced, total_debits, total_credits
