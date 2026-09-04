"""Standard Library Chart of Accounts (COA) Directory.

Comprehensive GAAP/GASB compliant chart of accounts tailored for public, academic,
and institutional libraries, covering operating cash, fines receivables, book collections,
endowments, grants, circulation revenue, and acquisitions expenditures.
"""

from typing import Dict, Optional, List
from .models import Account, AccountType, NormalBalance


STANDARD_LIBRARY_ACCOUNTS: Dict[str, Account] = {}

def _add(code: str, name: str, acct_type: AccountType, norm: NormalBalance, desc: str = ""):
    STANDARD_LIBRARY_ACCOUNTS[code] = Account(code=code, name=name, account_type=acct_type, normal_balance=norm, description=desc)

# ====================================================================
# 1000-1999: ASSETS
# ====================================================================
# Current Assets: Cash & Equivalents
_add("1010", "Cash on Hand - Main Circulation Desk", AccountType.ASSET, NormalBalance.DEBIT, "Daily till cash at main desk")
_add("1011", "Cash on Hand - Reference Desk", AccountType.ASSET, NormalBalance.DEBIT, "Petty cash and till at reference desk")
_add("1012", "Cash on Hand - Childrens Library Desk", AccountType.ASSET, NormalBalance.DEBIT, "Petty cash at branch children section")
_add("1015", "Petty Cash Fund", AccountType.ASSET, NormalBalance.DEBIT, "Librarian emergency supplies petty cash")
_add("1020", "Operating Bank Account - Central", AccountType.ASSET, NormalBalance.DEBIT, "Primary municipal/university checking account")
_add("1025", "Payroll Bank Account", AccountType.ASSET, NormalBalance.DEBIT, "Dedicated staff salary account")
_add("1030", "Payment Gateway Clearing - Stripe", AccountType.ASSET, NormalBalance.DEBIT, "Online member fine payments clearing")
_add("1031", "Payment Gateway Clearing - PayPal", AccountType.ASSET, NormalBalance.DEBIT, "PayPal balance awaiting transfer")
_add("1032", "Payment Gateway Clearing - Razorpay/UPI", AccountType.ASSET, NormalBalance.DEBIT, "UPI online cashier clearing account")

# Current Assets: Receivables
_add("1110", "Accounts Receivable - Patron Overdue Fines", AccountType.ASSET, NormalBalance.DEBIT, "Outstanding unpaid overdue fines")
_add("1112", "Accounts Receivable - Lost Book Replacements", AccountType.ASSET, NormalBalance.DEBIT, "Assessed fees for lost or damaged books")
_add("1115", "Accounts Receivable - Interlibrary Loan Fees", AccountType.ASSET, NormalBalance.DEBIT, "Fees due from external partner libraries")
_add("1120", "Allowance for Uncollectible Patron Fines", AccountType.ASSET, NormalBalance.CREDIT, "Contra-asset reserve for waived or aged fines")
_add("1150", "Grants Receivable", AccountType.ASSET, NormalBalance.DEBIT, "Awarded government and foundation grants due")

# Non-Current Assets: Fixed & Library Collections
_add("1510", "Library Book Collection - Circulating Monograph", AccountType.ASSET, NormalBalance.DEBIT, "Capitalized value of circulating physical books")
_add("1520", "Library Book Collection - Reference Materials", AccountType.ASSET, NormalBalance.DEBIT, "Non-circulating encyclopedias, dictionaries, atlases")
_add("1530", "Library Book Collection - Rare Books & Archives", AccountType.ASSET, NormalBalance.DEBIT, "Special collections and historical manuscripts")
_add("1540", "Digital Media Collection - E-Books & Audio", AccountType.ASSET, NormalBalance.DEBIT, "Perpetual license digital holdings")
_add("1610", "Furniture and Fixtures - Reading Rooms", AccountType.ASSET, NormalBalance.DEBIT, "Study carrels, reading tables, library seating")
_add("1620", "Furniture and Fixtures - Book Stacks & Shelving", AccountType.ASSET, NormalBalance.DEBIT, "High-density mobile compact shelving units")
_add("1710", "Computer Equipment - Patron OPAC Kiosks", AccountType.ASSET, NormalBalance.DEBIT, "Public access terminals and catalog search PCs")
_add("1720", "Computer Equipment - Self-Checkout Kiosks", AccountType.ASSET, NormalBalance.DEBIT, "3M SIP2 automated self-check stations")
_add("1730", "Computer Equipment - Automated Materials Handling", AccountType.ASSET, NormalBalance.DEBIT, "RFID book return sorters and barcode conveyor")
_add("1790", "Accumulated Depreciation - Hardware & Fixtures", AccountType.ASSET, NormalBalance.CREDIT, "Contra-asset depreciation on equipment")

# ====================================================================
# 2000-2999: LIABILITIES
# ====================================================================
_add("2010", "Accounts Payable - Book Vendors", AccountType.LIABILITY, NormalBalance.CREDIT, "Invoices due to monograph and media jobbers")
_add("2015", "Accounts Payable - Journal & Serial Publishers", AccountType.LIABILITY, NormalBalance.CREDIT, "Periodical subscription liabilities")
_add("2020", "Accounts Payable - Library Supplies & Services", AccountType.LIABILITY, NormalBalance.CREDIT, "Barcode labels, book tape, binding bills")
_add("2110", "Patron Security Deposits", AccountType.LIABILITY, NormalBalance.CREDIT, "Refundable caution deposits from members")
_add("2120", "Unearned / Deferred Revenue - Membership Fees", AccountType.LIABILITY, NormalBalance.CREDIT, "Annual membership dues received in advance")
_add("2130", "Unearned / Deferred Revenue - Room Booking Fees", AccountType.LIABILITY, NormalBalance.CREDIT, "Conference hall and study carrel advance deposits")
_add("2210", "Accrued Salaries and Wages", AccountType.LIABILITY, NormalBalance.CREDIT, "Earned but unpaid librarian salaries")
_add("2220", "Sales and Circulation Tax Payable", AccountType.LIABILITY, NormalBalance.CREDIT, "Tax collected on photocopying and merchandise")

# ====================================================================
# 3000-3999: EQUITY & FUND BALANCES
# ====================================================================
_add("3010", "Unrestricted General Operating Fund Balance", AccountType.EQUITY, NormalBalance.CREDIT, "Accumulated library operational surplus")
_add("3020", "Restricted Endowment Fund - Childrens Literacy", AccountType.EQUITY, NormalBalance.CREDIT, "Donor restricted endowment principal")
_add("3025", "Restricted Endowment Fund - Science & Technology", AccountType.EQUITY, NormalBalance.CREDIT, "Endowment for academic STEM acquisitions")
_add("3030", "Capital Improvement Reserve Fund", AccountType.EQUITY, NormalBalance.CREDIT, "Allocated reserve for building expansion and renovation")

# ====================================================================
# 4000-4999: REVENUE
# ====================================================================
_add("4010", "Patron Overdue Fine Collections", AccountType.REVENUE, NormalBalance.CREDIT, "Revenue collected from daily overdue fines")
_add("4015", "Lost Book Replacement Charges", AccountType.REVENUE, NormalBalance.CREDIT, "Fees charged to patrons for lost materials")
_add("4020", "Annual Patron Membership Fees", AccountType.REVENUE, NormalBalance.CREDIT, "Subscription fees for library membership tiers")
_add("4030", "Photocopying and Printing Services", AccountType.REVENUE, NormalBalance.CREDIT, "Public printer and copier revenue")
_add("4040", "Meeting Room and Space Rental Fees", AccountType.REVENUE, NormalBalance.CREDIT, "Facility rental for community events and workshops")
_add("4050", "Interlibrary Loan Document Delivery Fees", AccountType.REVENUE, NormalBalance.CREDIT, "Service fees charged for external article delivery")
_add("4110", "Municipal Library Operating Appropriations", AccountType.REVENUE, NormalBalance.CREDIT, "City / State government funding grant")
_add("4120", "Private Foundation Grants", AccountType.REVENUE, NormalBalance.CREDIT, "Grants for digitization and archive conservation")
_add("4130", "Individual Donations & Book Drive Bequests", AccountType.REVENUE, NormalBalance.CREDIT, "Unrestricted donor contributions")
_add("4140", "Book Sale Proceeds - Discarded / Weed Materials", AccountType.REVENUE, NormalBalance.CREDIT, "Friends of the Library annual book sale income")

# ====================================================================
# 5000-5999: EXPENSES
# ====================================================================
_add("5010", "Acquisitions - Print Monographs & Books", AccountType.EXPENSE, NormalBalance.DEBIT, "Expense for non-capitalized book acquisitions")
_add("5015", "Acquisitions - Electronic Books & Audio", AccountType.EXPENSE, NormalBalance.DEBIT, "E-book access licenses and digital audio")
_add("5020", "Acquisitions - Periodical & Journal Subscriptions", AccountType.EXPENSE, NormalBalance.DEBIT, "Annual serial subscriptions and database licenses")
_add("5030", "Acquisitions - Audiovisual Media (DVD/Blu-ray)", AccountType.EXPENSE, NormalBalance.DEBIT, "Educational media and documentary films")
_add("5110", "Collection Maintenance - Book Binding & Repair", AccountType.EXPENSE, NormalBalance.DEBIT, "Commercial bindery and mending tape expenses")
_add("5120", "Collection Maintenance - RFID Tags & Barcodes", AccountType.EXPENSE, NormalBalance.DEBIT, "Physical barcode labels and RFID transponders")
_add("5210", "Staff Salaries - Librarians & Catalogers", AccountType.EXPENSE, NormalBalance.DEBIT, "Professional staff compensation")
_add("5220", "Staff Salaries - Circulation Clerks & Pages", AccountType.EXPENSE, NormalBalance.DEBIT, "Hourly circulation desk staff and page shelvers")
_add("5310", "Technology - Integrated Library System (ILS) Hosting", AccountType.EXPENSE, NormalBalance.DEBIT, "Cloud hosting and server infrastructure")
_add("5320", "Technology - RFID Gates & Hardware Maintenance", AccountType.EXPENSE, NormalBalance.DEBIT, "Self-check kiosks and security gate servicing")
_add("5410", "Facilities - Electricity, Heating & Air Conditioning", AccountType.EXPENSE, NormalBalance.DEBIT, "Climate control for archive preservation")
_add("5420", "Facilities - Janitorial and Building Custodial", AccountType.EXPENSE, NormalBalance.DEBIT, "Cleaning services and facility maintenance")
_add("5510", "Patron Services - Programs & Author Visits", AccountType.EXPENSE, NormalBalance.DEBIT, "Honorariums for guest speakers and workshops")
_add("5610", "Bank & Payment Gateway Processing Fees", AccountType.EXPENSE, NormalBalance.DEBIT, "Credit card transaction fees on fine payments")
_add("5910", "Depreciation Expense - Library Equipment", AccountType.EXPENSE, NormalBalance.DEBIT, "Annual depreciation on computer hardware and furniture")

def get_standard_account(code: str) -> Optional[Account]:
    return STANDARD_LIBRARY_ACCOUNTS.get(code)

def list_accounts_by_type(acct_type: AccountType) -> List[Account]:
    return [a for a in STANDARD_LIBRARY_ACCOUNTS.values() if a.account_type == acct_type]
