"""Library Fund Accounting and Grant Tracking Chart of Accounts.

Implements Governmental Accounting Standards Board (GASB) and Financial Accounting
Standards Board (FASB) fund accounting models for public, academic, and special libraries.
Categorizes funds into General Operating, Special Revenue, Capital Projects, and Endowments.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class LibraryFundDefinition:
    fund_code: str
    fund_name: str
    fund_type: str  # 'operating', 'endowment', 'grant', 'capital', 'fiduciary'
    fiscal_year: str
    allocated_amount: Decimal
    encumbered_amount: Decimal
    expended_amount: Decimal
    cash_balance: Decimal
    grant_donor: Optional[str] = None
    restriction_level: str = "unrestricted"  # 'unrestricted', 'temporarily_restricted', 'permanently_restricted'


FUND_CATALOG: Dict[str, LibraryFundDefinition] = {}


def _fund(code: str, name: str, ftype: str, fy: str,
          alloc: float, encumb: float, expend: float, cash: float,
          donor: Optional[str] = None, restr: str = "unrestricted"):
    FUND_CATALOG[code] = LibraryFundDefinition(
        fund_code=code,
        fund_name=name,
        fund_type=ftype,
        fiscal_year=fy,
        allocated_amount=Decimal(str(alloc)),
        encumbered_amount=Decimal(str(encumb)),
        expended_amount=Decimal(str(expend)),
        cash_balance=Decimal(str(cash)),
        grant_donor=donor,
        restriction_level=restr
    )

_fund("F-1001", "Municipal General Operating Fund", "operating", "2026", 1500000.0, 120000.0, 840000.0, 540000.0, "City Treasury", "unrestricted")
_fund("F-1002", "State Library Aid Appropriation", "operating", "2026", 350000.0, 45000.0, 210000.0, 95000.0, "State Dept of Education", "temporarily_restricted")
_fund("F-1003", "County Inter-jurisdictional Cooperative Fund", "operating", "2026", 125000.0, 15000.0, 80000.0, 30000.0, "County Library District", "unrestricted")
_fund("F-2001", "IMLS National Leadership Grant for Digital Archives", "grant", "2026", 250000.0, 30000.0, 145000.0, 75000.0, "Institute of Museum and Library Services", "temporarily_restricted")
_fund("F-2002", "NEH Humanities Research Collections Grant", "grant", "2026", 180000.0, 22000.0, 95000.0, 63000.0, "National Endowment for the Humanities", "temporarily_restricted")
_fund("F-2003", "NSF STEM Learning & Makerspace Equipment Grant", "grant", "2026", 95000.0, 12000.0, 68000.0, 15000.0, "National Science Foundation", "temporarily_restricted")
_fund("F-3001", "Andrew Carnegie Memorial Book Endowment", "endowment", "2026", 500000.0, 0.0, 25000.0, 475000.0, "Carnegie Foundation", "permanently_restricted")
_fund("F-3002", "Eleanor Vance Rare Books and Special Collections Endowment", "endowment", "2026", 750000.0, 0.0, 32000.0, 718000.0, "Vance Estate", "permanently_restricted")
_fund("F-3003", "Arthur Pendelton Science & Technology Periodicals Endowment", "endowment", "2026", 300000.0, 0.0, 14000.0, 286000.0, "Pendelton Bequest", "permanently_restricted")
_fund("F-4001", "Central Branch HVAC and Infrastructure Capital Reserve", "capital", "2026", 800000.0, 350000.0, 250000.0, 200000.0, "Municipal Bond Issue", "unrestricted")
_fund("F-4002", "Automated Material Handling (AMH) RFID Sorter Capital Project", "capital", "2026", 450000.0, 180000.0, 220000.0, 50000.0, "Capital Improvement Plan", "unrestricted")
_fund("F-5001", "Friends of the Library Annual Book Sale Proceeds", "fiduciary", "2026", 45000.0, 2500.0, 28000.0, 14500.0, "Friends of the Library Inc.", "unrestricted")
_fund("F-5002", "Patron Lost Material Replacement Reserve", "fiduciary", "2026", 18500.0, 1200.0, 9200.0, 8100.0, "Circulation Desk Collections", "unrestricted")
_fund("F-5003", "Library Foundation Annual Giving Campaign", "fiduciary", "2026", 85000.0, 5000.0, 42000.0, 38000.0, "Library Foundation", "unrestricted")
_fund("SUB-CEN-MONO", "Central - Monographs & Print Books", "operating", "2026", 17500.0, 2625.0, 10500.0, 7000.0, None, "unrestricted")
_fund("SUB-CEN-EBOOK", "Central - Electronic Books & Overdrive Leases", "operating", "2026", 12500.0, 1875.0, 7500.0, 5000.0, None, "unrestricted")
_fund("SUB-CEN-JOURNAL", "Central - Scholarly Periodicals & Databases", "operating", "2026", 10000.0, 1500.0, 6000.0, 4000.0, None, "unrestricted")
_fund("SUB-CEN-MEDIA", "Central - Streaming Audio & Physical DVDs", "operating", "2026", 5000.0, 750.0, 3000.0, 2000.0, None, "unrestricted")
_fund("SUB-CEN-BIND", "Central - Commercial Preservation & Binding", "operating", "2026", 2500.0, 375.0, 1500.0, 1000.0, None, "unrestricted")
_fund("SUB-CEN-ILL", "Central - Interlibrary Loan Subsidies & Copyright Royalties", "operating", "2026", 2500.0, 375.0, 1500.0, 1000.0, None, "unrestricted")
_fund("SUB-NOR-MONO", "North Branch - Monographs & Print Books", "operating", "2026", 17500.0, 2625.0, 10500.0, 7000.0, None, "unrestricted")
_fund("SUB-NOR-EBOOK", "North Branch - Electronic Books & Overdrive Leases", "operating", "2026", 12500.0, 1875.0, 7500.0, 5000.0, None, "unrestricted")
_fund("SUB-NOR-JOURNAL", "North Branch - Scholarly Periodicals & Databases", "operating", "2026", 10000.0, 1500.0, 6000.0, 4000.0, None, "unrestricted")
_fund("SUB-NOR-MEDIA", "North Branch - Streaming Audio & Physical DVDs", "operating", "2026", 5000.0, 750.0, 3000.0, 2000.0, None, "unrestricted")
_fund("SUB-NOR-BIND", "North Branch - Commercial Preservation & Binding", "operating", "2026", 2500.0, 375.0, 1500.0, 1000.0, None, "unrestricted")
_fund("SUB-NOR-ILL", "North Branch - Interlibrary Loan Subsidies & Copyright Royalties", "operating", "2026", 2500.0, 375.0, 1500.0, 1000.0, None, "unrestricted")
_fund("SUB-EAS-MONO", "Eastside - Monographs & Print Books", "operating", "2026", 17500.0, 2625.0, 10500.0, 7000.0, None, "unrestricted")
_fund("SUB-EAS-EBOOK", "Eastside - Electronic Books & Overdrive Leases", "operating", "2026", 12500.0, 1875.0, 7500.0, 5000.0, None, "unrestricted")
_fund("SUB-EAS-JOURNAL", "Eastside - Scholarly Periodicals & Databases", "operating", "2026", 10000.0, 1500.0, 6000.0, 4000.0, None, "unrestricted")
_fund("SUB-EAS-MEDIA", "Eastside - Streaming Audio & Physical DVDs", "operating", "2026", 5000.0, 750.0, 3000.0, 2000.0, None, "unrestricted")
_fund("SUB-EAS-BIND", "Eastside - Commercial Preservation & Binding", "operating", "2026", 2500.0, 375.0, 1500.0, 1000.0, None, "unrestricted")
_fund("SUB-EAS-ILL", "Eastside - Interlibrary Loan Subsidies & Copyright Royalties", "operating", "2026", 2500.0, 375.0, 1500.0, 1000.0, None, "unrestricted")
_fund("SUB-WES-MONO", "West End - Monographs & Print Books", "operating", "2026", 17500.0, 2625.0, 10500.0, 7000.0, None, "unrestricted")
_fund("SUB-WES-EBOOK", "West End - Electronic Books & Overdrive Leases", "operating", "2026", 12500.0, 1875.0, 7500.0, 5000.0, None, "unrestricted")
_fund("SUB-WES-JOURNAL", "West End - Scholarly Periodicals & Databases", "operating", "2026", 10000.0, 1500.0, 6000.0, 4000.0, None, "unrestricted")
_fund("SUB-WES-MEDIA", "West End - Streaming Audio & Physical DVDs", "operating", "2026", 5000.0, 750.0, 3000.0, 2000.0, None, "unrestricted")
_fund("SUB-WES-BIND", "West End - Commercial Preservation & Binding", "operating", "2026", 2500.0, 375.0, 1500.0, 1000.0, None, "unrestricted")
_fund("SUB-WES-ILL", "West End - Interlibrary Loan Subsidies & Copyright Royalties", "operating", "2026", 2500.0, 375.0, 1500.0, 1000.0, None, "unrestricted")
_fund("SUB-DOW-MONO", "Downtown Campus - Monographs & Print Books", "operating", "2026", 17500.0, 2625.0, 10500.0, 7000.0, None, "unrestricted")
_fund("SUB-DOW-EBOOK", "Downtown Campus - Electronic Books & Overdrive Leases", "operating", "2026", 12500.0, 1875.0, 7500.0, 5000.0, None, "unrestricted")
_fund("SUB-DOW-JOURNAL", "Downtown Campus - Scholarly Periodicals & Databases", "operating", "2026", 10000.0, 1500.0, 6000.0, 4000.0, None, "unrestricted")
_fund("SUB-DOW-MEDIA", "Downtown Campus - Streaming Audio & Physical DVDs", "operating", "2026", 5000.0, 750.0, 3000.0, 2000.0, None, "unrestricted")
_fund("SUB-DOW-BIND", "Downtown Campus - Commercial Preservation & Binding", "operating", "2026", 2500.0, 375.0, 1500.0, 1000.0, None, "unrestricted")
_fund("SUB-DOW-ILL", "Downtown Campus - Interlibrary Loan Subsidies & Copyright Royalties", "operating", "2026", 2500.0, 375.0, 1500.0, 1000.0, None, "unrestricted")
_fund("SUB-MED-MONO", "Medical Library - Monographs & Print Books", "operating", "2026", 17500.0, 2625.0, 10500.0, 7000.0, None, "unrestricted")
_fund("SUB-MED-EBOOK", "Medical Library - Electronic Books & Overdrive Leases", "operating", "2026", 12500.0, 1875.0, 7500.0, 5000.0, None, "unrestricted")
_fund("SUB-MED-JOURNAL", "Medical Library - Scholarly Periodicals & Databases", "operating", "2026", 10000.0, 1500.0, 6000.0, 4000.0, None, "unrestricted")
_fund("SUB-MED-MEDIA", "Medical Library - Streaming Audio & Physical DVDs", "operating", "2026", 5000.0, 750.0, 3000.0, 2000.0, None, "unrestricted")
_fund("SUB-MED-BIND", "Medical Library - Commercial Preservation & Binding", "operating", "2026", 2500.0, 375.0, 1500.0, 1000.0, None, "unrestricted")
_fund("SUB-MED-ILL", "Medical Library - Interlibrary Loan Subsidies & Copyright Royalties", "operating", "2026", 2500.0, 375.0, 1500.0, 1000.0, None, "unrestricted")

def get_fund_by_code(code: str) -> Optional[LibraryFundDefinition]:
    """Look up a library fund definition by account code."""
    return FUND_CATALOG.get(code.strip().upper())


def get_funds_by_type(fund_type: str) -> List[LibraryFundDefinition]:
    """Retrieve all funds matching a specific fund type."""
    clean = fund_type.strip().lower()
    return [f for f in FUND_CATALOG.values() if f.fund_type.lower() == clean]


def calculate_total_financial_balance() -> Dict[str, Decimal]:
    """Calculate aggregated allocations, encumbrances, and cash balances across all funds."""
    total_alloc = Decimal("0.00")
    total_encumb = Decimal("0.00")
    total_expend = Decimal("0.00")
    total_cash = Decimal("0.00")

    for f in FUND_CATALOG.values():
        total_alloc += f.allocated_amount
        total_encumb += f.encumbered_amount
        total_expend += f.expended_amount
        total_cash += f.cash_balance

    return {
        "total_allocated": total_alloc,
        "total_encumbered": total_encumb,
        "total_expended": total_expend,
        "total_cash": total_cash,
        "net_available_balance": total_cash - total_encumb
    }
