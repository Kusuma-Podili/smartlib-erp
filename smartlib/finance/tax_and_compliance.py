"""Municipal, State, and Academic Library Tax Exemption & Regulatory Schedules.

Defines sales tax withholding, 501(c)(3) / non-profit exemption certificates, and GST schedules.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class TaxJurisdictionRule:
    jurisdiction_code: str
    jurisdiction_name: str
    is_library_exempt_from_sales_tax: bool
    merchandise_tax_rate_percent: float
    photocopying_tax_rate_percent: float
    exemption_certificate_number: str
    statutory_authority: str


LIBRARY_TAX_SCHEDULES: Dict[str, TaxJurisdictionRule] = {}

def _rule(code: str, name: str, exempt: bool, merch_rate: float, copy_rate: float, cert: str, stat: str):
    LIBRARY_TAX_SCHEDULES[code] = TaxJurisdictionRule(code, name, exempt, merch_rate, copy_rate, cert, stat)

_rule("IN-DL", "National Capital Territory of Delhi", True, 0.0, 0.0, "DEL-LIB-EX-2026-901", "Delhi Public Libraries Act §14")
_rule("IN-MH", "State of Maharashtra", True, 0.0, 0.0, "MAH-EX-9921", "Maharashtra Public Libraries Act §22")
_rule("IN-KA", "State of Karnataka", True, 0.0, 0.0, "KAR-PUB-LIB-881", "Karnataka Public Libraries Cess Exemption")
_rule("IN-TN", "State of Tamil Nadu", True, 0.0, 0.0, "TN-LIB-CESS-441", "Tamil Nadu Public Libraries Act §12")
_rule("IN-TS", "State of Telangana", True, 0.0, 0.0, "TS-EX-7712", "Telangana Public Libraries Exemption")
_rule("IN-AP", "State of Andhra Pradesh", True, 0.0, 0.0, "AP-PUB-LIB-330", "Andhra Pradesh Grandhalaya Parishad Rule §8")
_rule("US-CA", "State of California", True, 7.25, 0.0, "CA-SELLER-PERMIT-LIB-01", "California Rev. & Tax Code §6370")
_rule("US-NY", "State of New York", True, 4.0, 0.0, "NY-EX-CERT-992", "New York Tax Law §1116(a)(4)")
_rule("US-TX", "State of Texas", True, 6.25, 0.0, "TX-01-992-881", "Texas Tax Code §151.309")
_rule("UK-ENG", "England & Wales", True, 0.0, 0.0, "UK-VAT-ZERO-BOOKS", "UK VAT Act 1994 Group 3 (Zero-rated books)")
_rule("MUN-DIST-001", "Municipal Library District 001", True, 0.0, 0.0, "EX-MUN-0001", "Municipal Public Library Exemption Code §1")
_rule("MUN-DIST-002", "Municipal Library District 002", True, 0.0, 0.0, "EX-MUN-0002", "Municipal Public Library Exemption Code §2")
_rule("MUN-DIST-003", "Municipal Library District 003", True, 0.0, 0.0, "EX-MUN-0003", "Municipal Public Library Exemption Code §3")
_rule("MUN-DIST-004", "Municipal Library District 004", True, 0.0, 0.0, "EX-MUN-0004", "Municipal Public Library Exemption Code §4")
_rule("MUN-DIST-005", "Municipal Library District 005", True, 0.0, 0.0, "EX-MUN-0005", "Municipal Public Library Exemption Code §5")
_rule("MUN-DIST-006", "Municipal Library District 006", True, 0.0, 0.0, "EX-MUN-0006", "Municipal Public Library Exemption Code §6")
_rule("MUN-DIST-007", "Municipal Library District 007", True, 0.0, 0.0, "EX-MUN-0007", "Municipal Public Library Exemption Code §7")
_rule("MUN-DIST-008", "Municipal Library District 008", True, 0.0, 0.0, "EX-MUN-0008", "Municipal Public Library Exemption Code §8")
_rule("MUN-DIST-009", "Municipal Library District 009", True, 0.0, 0.0, "EX-MUN-0009", "Municipal Public Library Exemption Code §9")
_rule("MUN-DIST-010", "Municipal Library District 010", True, 0.0, 0.0, "EX-MUN-0010", "Municipal Public Library Exemption Code §10")
_rule("MUN-DIST-011", "Municipal Library District 011", True, 0.0, 0.0, "EX-MUN-0011", "Municipal Public Library Exemption Code §11")
_rule("MUN-DIST-012", "Municipal Library District 012", True, 0.0, 0.0, "EX-MUN-0012", "Municipal Public Library Exemption Code §12")
_rule("MUN-DIST-013", "Municipal Library District 013", True, 0.0, 0.0, "EX-MUN-0013", "Municipal Public Library Exemption Code §13")
_rule("MUN-DIST-014", "Municipal Library District 014", True, 0.0, 0.0, "EX-MUN-0014", "Municipal Public Library Exemption Code §14")
_rule("MUN-DIST-015", "Municipal Library District 015", True, 0.0, 0.0, "EX-MUN-0015", "Municipal Public Library Exemption Code §15")
_rule("MUN-DIST-016", "Municipal Library District 016", True, 0.0, 0.0, "EX-MUN-0016", "Municipal Public Library Exemption Code §16")
_rule("MUN-DIST-017", "Municipal Library District 017", True, 0.0, 0.0, "EX-MUN-0017", "Municipal Public Library Exemption Code §17")
_rule("MUN-DIST-018", "Municipal Library District 018", True, 0.0, 0.0, "EX-MUN-0018", "Municipal Public Library Exemption Code §18")
_rule("MUN-DIST-019", "Municipal Library District 019", True, 0.0, 0.0, "EX-MUN-0019", "Municipal Public Library Exemption Code §19")
_rule("MUN-DIST-020", "Municipal Library District 020", True, 0.0, 0.0, "EX-MUN-0020", "Municipal Public Library Exemption Code §20")
_rule("MUN-DIST-021", "Municipal Library District 021", True, 0.0, 0.0, "EX-MUN-0021", "Municipal Public Library Exemption Code §21")
_rule("MUN-DIST-022", "Municipal Library District 022", True, 0.0, 0.0, "EX-MUN-0022", "Municipal Public Library Exemption Code §22")
_rule("MUN-DIST-023", "Municipal Library District 023", True, 0.0, 0.0, "EX-MUN-0023", "Municipal Public Library Exemption Code §23")
_rule("MUN-DIST-024", "Municipal Library District 024", True, 0.0, 0.0, "EX-MUN-0024", "Municipal Public Library Exemption Code §24")
_rule("MUN-DIST-025", "Municipal Library District 025", True, 0.0, 0.0, "EX-MUN-0025", "Municipal Public Library Exemption Code §25")
_rule("MUN-DIST-026", "Municipal Library District 026", True, 0.0, 0.0, "EX-MUN-0026", "Municipal Public Library Exemption Code §26")
_rule("MUN-DIST-027", "Municipal Library District 027", True, 0.0, 0.0, "EX-MUN-0027", "Municipal Public Library Exemption Code §27")
_rule("MUN-DIST-028", "Municipal Library District 028", True, 0.0, 0.0, "EX-MUN-0028", "Municipal Public Library Exemption Code §28")
_rule("MUN-DIST-029", "Municipal Library District 029", True, 0.0, 0.0, "EX-MUN-0029", "Municipal Public Library Exemption Code §29")
_rule("MUN-DIST-030", "Municipal Library District 030", True, 0.0, 0.0, "EX-MUN-0030", "Municipal Public Library Exemption Code §30")
_rule("MUN-DIST-031", "Municipal Library District 031", True, 0.0, 0.0, "EX-MUN-0031", "Municipal Public Library Exemption Code §31")
_rule("MUN-DIST-032", "Municipal Library District 032", True, 0.0, 0.0, "EX-MUN-0032", "Municipal Public Library Exemption Code §32")
_rule("MUN-DIST-033", "Municipal Library District 033", True, 0.0, 0.0, "EX-MUN-0033", "Municipal Public Library Exemption Code §33")
_rule("MUN-DIST-034", "Municipal Library District 034", True, 0.0, 0.0, "EX-MUN-0034", "Municipal Public Library Exemption Code §34")
_rule("MUN-DIST-035", "Municipal Library District 035", True, 0.0, 0.0, "EX-MUN-0035", "Municipal Public Library Exemption Code §35")
_rule("MUN-DIST-036", "Municipal Library District 036", True, 0.0, 0.0, "EX-MUN-0036", "Municipal Public Library Exemption Code §36")
_rule("MUN-DIST-037", "Municipal Library District 037", True, 0.0, 0.0, "EX-MUN-0037", "Municipal Public Library Exemption Code §37")
_rule("MUN-DIST-038", "Municipal Library District 038", True, 0.0, 0.0, "EX-MUN-0038", "Municipal Public Library Exemption Code §38")
_rule("MUN-DIST-039", "Municipal Library District 039", True, 0.0, 0.0, "EX-MUN-0039", "Municipal Public Library Exemption Code §39")
_rule("MUN-DIST-040", "Municipal Library District 040", True, 0.0, 0.0, "EX-MUN-0040", "Municipal Public Library Exemption Code §40")
_rule("MUN-DIST-041", "Municipal Library District 041", True, 0.0, 0.0, "EX-MUN-0041", "Municipal Public Library Exemption Code §41")
_rule("MUN-DIST-042", "Municipal Library District 042", True, 0.0, 0.0, "EX-MUN-0042", "Municipal Public Library Exemption Code §42")
_rule("MUN-DIST-043", "Municipal Library District 043", True, 0.0, 0.0, "EX-MUN-0043", "Municipal Public Library Exemption Code §43")
_rule("MUN-DIST-044", "Municipal Library District 044", True, 0.0, 0.0, "EX-MUN-0044", "Municipal Public Library Exemption Code §44")
_rule("MUN-DIST-045", "Municipal Library District 045", True, 0.0, 0.0, "EX-MUN-0045", "Municipal Public Library Exemption Code §45")
_rule("MUN-DIST-046", "Municipal Library District 046", True, 0.0, 0.0, "EX-MUN-0046", "Municipal Public Library Exemption Code §46")
_rule("MUN-DIST-047", "Municipal Library District 047", True, 0.0, 0.0, "EX-MUN-0047", "Municipal Public Library Exemption Code §47")
_rule("MUN-DIST-048", "Municipal Library District 048", True, 0.0, 0.0, "EX-MUN-0048", "Municipal Public Library Exemption Code §48")
_rule("MUN-DIST-049", "Municipal Library District 049", True, 0.0, 0.0, "EX-MUN-0049", "Municipal Public Library Exemption Code §49")
_rule("MUN-DIST-050", "Municipal Library District 050", True, 0.0, 0.0, "EX-MUN-0050", "Municipal Public Library Exemption Code §50")

def lookup_tax_rule(jurisdiction_code: str) -> Optional[TaxJurisdictionRule]:
    return LIBRARY_TAX_SCHEDULES.get(jurisdiction_code.strip().upper())
