"""Expanded Branch & Fund Ledger Chart of Accounts for Multi-Campus Libraries.

Defines sub-accounts across Central, Medical, Law, Engineering, and Branch libraries.
"""

from typing import Dict, List, Optional
from .models import Account, AccountType, NormalBalance


EXPANDED_BRANCH_ACCOUNTS: Dict[str, Account] = {}

def _bacc(code: str, name: str, acct_type: AccountType, norm: NormalBalance, branch: str, desc: str):
    full_name = f"[{branch}] {name}"
    EXPANDED_BRANCH_ACCOUNTS[code] = Account(code=code, name=full_name, account_type=acct_type, normal_balance=norm, description=desc)

_bacc("1010", "Circulation Till Cash", AccountType.ASSET, NormalBalance.DEBIT, "Central Main Library", "Daily drawer cash")
_bacc("1510", "Monograph Collection Asset", AccountType.ASSET, NormalBalance.DEBIT, "Central Main Library", "Capitalized books")
_bacc("1710", "Branch Tech & Hardware", AccountType.ASSET, NormalBalance.DEBIT, "Central Main Library", "Branch hardware")
_bacc("4010", "Overdue Fine Revenue", AccountType.REVENUE, NormalBalance.CREDIT, "Central Main Library", "Collected fines")
_bacc("5010", "Book Acquisitions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Central Main Library", "Book purchases")
_bacc("5015", "Journal Subscriptions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Central Main Library", "Serials purchases")
_bacc("5410", "Branch Electricity & Climate", AccountType.EXPENSE, NormalBalance.DEBIT, "Central Main Library", "Utilities")
_bacc("1020", "Circulation Till Cash", AccountType.ASSET, NormalBalance.DEBIT, "Science & Engineering Library", "Daily drawer cash")
_bacc("1520", "Monograph Collection Asset", AccountType.ASSET, NormalBalance.DEBIT, "Science & Engineering Library", "Capitalized books")
_bacc("1720", "Branch Tech & Hardware", AccountType.ASSET, NormalBalance.DEBIT, "Science & Engineering Library", "Branch hardware")
_bacc("4020", "Overdue Fine Revenue", AccountType.REVENUE, NormalBalance.CREDIT, "Science & Engineering Library", "Collected fines")
_bacc("5020", "Book Acquisitions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Science & Engineering Library", "Book purchases")
_bacc("5025", "Journal Subscriptions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Science & Engineering Library", "Serials purchases")
_bacc("5420", "Branch Electricity & Climate", AccountType.EXPENSE, NormalBalance.DEBIT, "Science & Engineering Library", "Utilities")
_bacc("1030", "Circulation Till Cash", AccountType.ASSET, NormalBalance.DEBIT, "Health Sciences & Medical Library", "Daily drawer cash")
_bacc("1530", "Monograph Collection Asset", AccountType.ASSET, NormalBalance.DEBIT, "Health Sciences & Medical Library", "Capitalized books")
_bacc("1730", "Branch Tech & Hardware", AccountType.ASSET, NormalBalance.DEBIT, "Health Sciences & Medical Library", "Branch hardware")
_bacc("4030", "Overdue Fine Revenue", AccountType.REVENUE, NormalBalance.CREDIT, "Health Sciences & Medical Library", "Collected fines")
_bacc("5030", "Book Acquisitions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Health Sciences & Medical Library", "Book purchases")
_bacc("5035", "Journal Subscriptions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Health Sciences & Medical Library", "Serials purchases")
_bacc("5430", "Branch Electricity & Climate", AccountType.EXPENSE, NormalBalance.DEBIT, "Health Sciences & Medical Library", "Utilities")
_bacc("1040", "Circulation Till Cash", AccountType.ASSET, NormalBalance.DEBIT, "Law & Jurisprudence Library", "Daily drawer cash")
_bacc("1540", "Monograph Collection Asset", AccountType.ASSET, NormalBalance.DEBIT, "Law & Jurisprudence Library", "Capitalized books")
_bacc("1740", "Branch Tech & Hardware", AccountType.ASSET, NormalBalance.DEBIT, "Law & Jurisprudence Library", "Branch hardware")
_bacc("4040", "Overdue Fine Revenue", AccountType.REVENUE, NormalBalance.CREDIT, "Law & Jurisprudence Library", "Collected fines")
_bacc("5040", "Book Acquisitions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Law & Jurisprudence Library", "Book purchases")
_bacc("5045", "Journal Subscriptions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Law & Jurisprudence Library", "Serials purchases")
_bacc("5440", "Branch Electricity & Climate", AccountType.EXPENSE, NormalBalance.DEBIT, "Law & Jurisprudence Library", "Utilities")
_bacc("1050", "Circulation Till Cash", AccountType.ASSET, NormalBalance.DEBIT, "Architecture & Fine Arts Library", "Daily drawer cash")
_bacc("1550", "Monograph Collection Asset", AccountType.ASSET, NormalBalance.DEBIT, "Architecture & Fine Arts Library", "Capitalized books")
_bacc("1750", "Branch Tech & Hardware", AccountType.ASSET, NormalBalance.DEBIT, "Architecture & Fine Arts Library", "Branch hardware")
_bacc("4050", "Overdue Fine Revenue", AccountType.REVENUE, NormalBalance.CREDIT, "Architecture & Fine Arts Library", "Collected fines")
_bacc("5050", "Book Acquisitions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Architecture & Fine Arts Library", "Book purchases")
_bacc("5055", "Journal Subscriptions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Architecture & Fine Arts Library", "Serials purchases")
_bacc("5450", "Branch Electricity & Climate", AccountType.EXPENSE, NormalBalance.DEBIT, "Architecture & Fine Arts Library", "Utilities")
_bacc("1060", "Circulation Till Cash", AccountType.ASSET, NormalBalance.DEBIT, "Business & Economics Library", "Daily drawer cash")
_bacc("1560", "Monograph Collection Asset", AccountType.ASSET, NormalBalance.DEBIT, "Business & Economics Library", "Capitalized books")
_bacc("1760", "Branch Tech & Hardware", AccountType.ASSET, NormalBalance.DEBIT, "Business & Economics Library", "Branch hardware")
_bacc("4060", "Overdue Fine Revenue", AccountType.REVENUE, NormalBalance.CREDIT, "Business & Economics Library", "Collected fines")
_bacc("5060", "Book Acquisitions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Business & Economics Library", "Book purchases")
_bacc("5065", "Journal Subscriptions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Business & Economics Library", "Serials purchases")
_bacc("5460", "Branch Electricity & Climate", AccountType.EXPENSE, NormalBalance.DEBIT, "Business & Economics Library", "Utilities")
_bacc("1070", "Circulation Till Cash", AccountType.ASSET, NormalBalance.DEBIT, "Children & Youth Community Branch", "Daily drawer cash")
_bacc("1570", "Monograph Collection Asset", AccountType.ASSET, NormalBalance.DEBIT, "Children & Youth Community Branch", "Capitalized books")
_bacc("1770", "Branch Tech & Hardware", AccountType.ASSET, NormalBalance.DEBIT, "Children & Youth Community Branch", "Branch hardware")
_bacc("4070", "Overdue Fine Revenue", AccountType.REVENUE, NormalBalance.CREDIT, "Children & Youth Community Branch", "Collected fines")
_bacc("5070", "Book Acquisitions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Children & Youth Community Branch", "Book purchases")
_bacc("5075", "Journal Subscriptions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Children & Youth Community Branch", "Serials purchases")
_bacc("5470", "Branch Electricity & Climate", AccountType.EXPENSE, NormalBalance.DEBIT, "Children & Youth Community Branch", "Utilities")
_bacc("1080", "Circulation Till Cash", AccountType.ASSET, NormalBalance.DEBIT, "Rare Books & Special Collections Archive", "Daily drawer cash")
_bacc("1580", "Monograph Collection Asset", AccountType.ASSET, NormalBalance.DEBIT, "Rare Books & Special Collections Archive", "Capitalized books")
_bacc("1780", "Branch Tech & Hardware", AccountType.ASSET, NormalBalance.DEBIT, "Rare Books & Special Collections Archive", "Branch hardware")
_bacc("4080", "Overdue Fine Revenue", AccountType.REVENUE, NormalBalance.CREDIT, "Rare Books & Special Collections Archive", "Collected fines")
_bacc("5080", "Book Acquisitions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Rare Books & Special Collections Archive", "Book purchases")
_bacc("5085", "Journal Subscriptions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Rare Books & Special Collections Archive", "Serials purchases")
_bacc("5480", "Branch Electricity & Climate", AccountType.EXPENSE, NormalBalance.DEBIT, "Rare Books & Special Collections Archive", "Utilities")
_bacc("1090", "Circulation Till Cash", AccountType.ASSET, NormalBalance.DEBIT, "Mobile Bookmobile & Outreach Fleet", "Daily drawer cash")
_bacc("1590", "Monograph Collection Asset", AccountType.ASSET, NormalBalance.DEBIT, "Mobile Bookmobile & Outreach Fleet", "Capitalized books")
_bacc("1790", "Branch Tech & Hardware", AccountType.ASSET, NormalBalance.DEBIT, "Mobile Bookmobile & Outreach Fleet", "Branch hardware")
_bacc("4090", "Overdue Fine Revenue", AccountType.REVENUE, NormalBalance.CREDIT, "Mobile Bookmobile & Outreach Fleet", "Collected fines")
_bacc("5090", "Book Acquisitions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Mobile Bookmobile & Outreach Fleet", "Book purchases")
_bacc("5095", "Journal Subscriptions Expense", AccountType.EXPENSE, NormalBalance.DEBIT, "Mobile Bookmobile & Outreach Fleet", "Serials purchases")
_bacc("5490", "Branch Electricity & Climate", AccountType.EXPENSE, NormalBalance.DEBIT, "Mobile Bookmobile & Outreach Fleet", "Utilities")

def get_branch_account(code: str) -> Optional[Account]:
    return EXPANDED_BRANCH_ACCOUNTS.get(code)
