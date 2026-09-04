"""Library Tax Jurisdictions, Educational Exemptions, and Millage Levies.

Defines state and local tax compliance tables, 501(c)(3) tax exemption categories,
public library taxing district millage formulas, and municipal bond repayment rates.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class TaxJurisdictionRule:
    jurisdiction_code: str
    jurisdiction_name: str
    state_code: str
    standard_sales_tax_rate: Decimal
    library_material_exempt: bool
    digital_goods_taxable: bool
    educational_discount_rate: Decimal
    exemption_certificate_required: bool
    notes: str = ""


TAX_JURISDICTION_REGISTRY: Dict[str, TaxJurisdictionRule] = {}


def _tax(code: str, name: str, state: str, rate: float, exempt: bool, digi: bool, disc: float, cert: bool, notes: str):
    TAX_JURISDICTION_REGISTRY[code] = TaxJurisdictionRule(
        jurisdiction_code=code,
        jurisdiction_name=name,
        state_code=state,
        standard_sales_tax_rate=Decimal(str(rate)),
        library_material_exempt=exempt,
        digital_goods_taxable=digi,
        educational_discount_rate=Decimal(str(disc)),
        exemption_certificate_required=cert,
        notes=notes
    )

_tax(
    code="US-AL",
    name="Alabama Department of Revenue",
    state="AL",
    rate=0.04,
    exempt=True,
    digi=False,
    disc=0.15,
    cert=True,
    notes="Public libraries qualify for certificate of educational exemption"
)
_tax(
    code="US-AK",
    name="Alaska Municipal Boroughs",
    state="AK",
    rate=0.0,
    exempt=True,
    digi=False,
    disc=0.0,
    cert=False,
    notes="No state sales tax; local borough sales taxes apply to general retail"
)
_tax(
    code="US-AZ",
    name="Arizona Department of Revenue",
    state="AZ",
    rate=0.056,
    exempt=True,
    digi=True,
    disc=0.1,
    cert=True,
    notes="Transaction privilege tax exemption for school and municipal libraries"
)
_tax(
    code="US-AR",
    name="Arkansas Department of Finance",
    state="AR",
    rate=0.065,
    exempt=True,
    digi=False,
    disc=0.12,
    cert=True,
    notes="Standard educational non-profit exemption GR-31"
)
_tax(
    code="US-CA",
    name="California CDTFA",
    state="CA",
    rate=0.0725,
    exempt=False,
    digi=False,
    disc=0.2,
    cert=True,
    notes="California sales tax applies; public libraries receive institutional discounts"
)
_tax(
    code="US-CO",
    name="Colorado Department of Revenue",
    state="CO",
    rate=0.029,
    exempt=True,
    digi=False,
    disc=0.15,
    cert=True,
    notes="Special library districts exempt under Title 24 Article 90"
)
_tax(
    code="US-CT",
    name="Connecticut DRS",
    state="CT",
    rate=0.0635,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="CERT-119 Certificate for Purchases of Tangible Personal Property"
)
_tax(
    code="US-DE",
    name="Delaware Division of Revenue",
    state="DE",
    rate=0.0,
    exempt=True,
    digi=False,
    disc=0.0,
    cert=False,
    notes="No state or municipal retail sales tax levied"
)
_tax(
    code="US-FL",
    name="Florida Department of Revenue",
    state="FL",
    rate=0.06,
    exempt=True,
    digi=False,
    disc=0.15,
    cert=True,
    notes="Consumer Certificate of Exemption Form DR-14"
)
_tax(
    code="US-GA",
    name="Georgia Department of Revenue",
    state="GA",
    rate=0.04,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Form ST-5 Certificate of Exemption for public libraries"
)
_tax(
    code="US-HI",
    name="Hawaii Department of Taxation",
    state="HI",
    rate=0.04,
    exempt=False,
    digi=True,
    disc=0.05,
    cert=False,
    notes="General Excise Tax (GET) applies at wholesale rate 0.5%"
)
_tax(
    code="US-ID",
    name="Idaho State Tax Commission",
    state="ID",
    rate=0.06,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Form ST-101 Sales Tax Resale or Exemption Certificate"
)
_tax(
    code="US-IL",
    name="Illinois Department of Revenue",
    state="IL",
    rate=0.0625,
    exempt=True,
    digi=False,
    disc=0.15,
    cert=True,
    notes="E-number exemption status for educational institutions"
)
_tax(
    code="US-IN",
    name="Indiana Department of Revenue",
    state="IN",
    rate=0.07,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Form ST-105 General Sales Tax Exemption Certificate"
)
_tax(
    code="US-IA",
    name="Iowa Department of Revenue",
    state="IA",
    rate=0.06,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Iowa Sales Tax Exemption Certificate for government libraries"
)
_tax(
    code="US-KS",
    name="Kansas Department of Revenue",
    state="KS",
    rate=0.065,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Designated Library District Exemption Certificate"
)
_tax(
    code="US-KY",
    name="Kentucky Department of Revenue",
    state="KY",
    rate=0.06,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Form 51A126 Purchase Exemption Certificate"
)
_tax(
    code="US-LA",
    name="Louisiana Department of Revenue",
    state="LA",
    rate=0.0445,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Parish library system tax exemption certificates"
)
_tax(
    code="US-ME",
    name="Maine Revenue Services",
    state="ME",
    rate=0.055,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Permanent exemption certificate for public library institutions"
)
_tax(
    code="US-MD",
    name="Maryland Comptroller",
    state="MD",
    rate=0.06,
    exempt=True,
    digi=False,
    disc=0.15,
    cert=True,
    notes="Comptroller of Maryland Exemption Certificate"
)
_tax(
    code="US-MA",
    name="Massachusetts DOR",
    state="MA",
    rate=0.0625,
    exempt=True,
    digi=False,
    disc=0.15,
    cert=True,
    notes="Form ST-2 Certificate of Exemption"
)
_tax(
    code="US-MI",
    name="Michigan Department of Treasury",
    state="MI",
    rate=0.06,
    exempt=True,
    digi=False,
    disc=0.15,
    cert=True,
    notes="Form 3372 Michigan Sales and Use Tax Certificate of Exemption"
)
_tax(
    code="US-MN",
    name="Minnesota Department of Revenue",
    state="MN",
    rate=0.06875,
    exempt=True,
    digi=False,
    disc=0.15,
    cert=True,
    notes="Form ST3 Certificate of Exemption"
)
_tax(
    code="US-MS",
    name="Mississippi Department of Revenue",
    state="MS",
    rate=0.07,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Exemption letter for municipal public libraries"
)
_tax(
    code="US-MO",
    name="Missouri Department of Revenue",
    state="MO",
    rate=0.04225,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Missouri Department of Revenue Exemption Letter"
)
_tax(
    code="US-MT",
    name="Montana Department of Revenue",
    state="MT",
    rate=0.0,
    exempt=True,
    digi=False,
    disc=0.0,
    cert=False,
    notes="No state retail sales tax"
)
_tax(
    code="US-NE",
    name="Nebraska Department of Revenue",
    state="NE",
    rate=0.055,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Nebraska Resale or Exempt Sale Certificate Form 13"
)
_tax(
    code="US-NV",
    name="Nevada Department of Taxation",
    state="NV",
    rate=0.0685,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Tax exemption letter for governmental entities"
)
_tax(
    code="US-NH",
    name="New Hampshire Department of Revenue",
    state="NH",
    rate=0.0,
    exempt=True,
    digi=False,
    disc=0.0,
    cert=False,
    notes="No general retail sales tax"
)
_tax(
    code="US-NJ",
    name="New Jersey Division of Taxation",
    state="NJ",
    rate=0.06625,
    exempt=True,
    digi=False,
    disc=0.15,
    cert=True,
    notes="Form ST-5 Exempt Organization Certificate"
)
_tax(
    code="US-NM",
    name="New Mexico Taxation and Revenue",
    state="NM",
    rate=0.05,
    exempt=True,
    digi=False,
    disc=0.05,
    cert=True,
    notes="Type 9 Non-taxable Transaction Certificate (NTTC)"
)
_tax(
    code="US-NY",
    name="New York State DTF",
    state="NY",
    rate=0.04,
    exempt=True,
    digi=False,
    disc=0.2,
    cert=True,
    notes="Form ST-119.1 Exempt Organization Exempt Purchase Certificate"
)
_tax(
    code="US-NC",
    name="North Carolina Department of Revenue",
    state="NC",
    rate=0.0475,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Form E-595E Streamlined Sales and Use Tax Certificate"
)
_tax(
    code="US-ND",
    name="North Dakota Office of State Tax",
    state="ND",
    rate=0.05,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Certificate of exempt status for political subdivisions"
)
_tax(
    code="US-OH",
    name="Ohio Department of Taxation",
    state="OH",
    rate=0.0575,
    exempt=True,
    digi=False,
    disc=0.15,
    cert=True,
    notes="Ohio Sales and Use Tax Blanket Exemption Certificate"
)
_tax(
    code="US-OK",
    name="Oklahoma Tax Commission",
    state="OK",
    rate=0.045,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Oklahoma sales tax exemption card for public schools/libraries"
)
_tax(
    code="US-OR",
    name="Oregon Department of Revenue",
    state="OR",
    rate=0.0,
    exempt=True,
    digi=False,
    disc=0.0,
    cert=False,
    notes="No state sales tax"
)
_tax(
    code="US-PA",
    name="Pennsylvania Department of Revenue",
    state="PA",
    rate=0.06,
    exempt=True,
    digi=False,
    disc=0.15,
    cert=True,
    notes="Form REV-1220 Pennsylvania Exemption Certificate"
)
_tax(
    code="US-RI",
    name="Rhode Island Division of Taxation",
    state="RI",
    rate=0.07,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Certificate of Exemption for non-profit educational institutions"
)
_tax(
    code="US-SC",
    name="South Carolina Department of Revenue",
    state="SC",
    rate=0.06,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Exemption certificate ST-8 for state and local government"
)
_tax(
    code="US-SD",
    name="South Dakota Department of Revenue",
    state="SD",
    rate=0.045,
    exempt=True,
    digi=False,
    disc=0.05,
    cert=True,
    notes="Exemption status for municipal and public library entities"
)
_tax(
    code="US-TN",
    name="Tennessee Department of Revenue",
    state="TN",
    rate=0.07,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Tennessee Certificate of Exemption for educational institutions"
)
_tax(
    code="US-TX",
    name="Texas Comptroller of Public Accounts",
    state="TX",
    rate=0.0625,
    exempt=True,
    digi=False,
    disc=0.15,
    cert=True,
    notes="Texas Sales and Use Tax Exemption Certification Form 01-339"
)
_tax(
    code="US-UT",
    name="Utah State Tax Commission",
    state="UT",
    rate=0.0485,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Form TC-721 Exemption Certificate for government libraries"
)
_tax(
    code="US-VT",
    name="Vermont Department of Taxes",
    state="VT",
    rate=0.06,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Form S-3 Certificate of Exemption"
)
_tax(
    code="US-VA",
    name="Virginia Department of Taxation",
    state="VA",
    rate=0.053,
    exempt=True,
    digi=False,
    disc=0.15,
    cert=True,
    notes="Commonwealth of Virginia Sales and Use Tax Certificate of Exemption"
)
_tax(
    code="US-WA",
    name="Washington Department of Revenue",
    state="WA",
    rate=0.065,
    exempt=False,
    digi=True,
    disc=0.15,
    cert=False,
    notes="Retail sales tax applies; public libraries utilize inter-local credits"
)
_tax(
    code="US-WV",
    name="West Virginia State Tax Department",
    state="WV",
    rate=0.06,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Form CST-280 West Virginia Direct Pay Permit / Exemption"
)
_tax(
    code="US-WI",
    name="Wisconsin Department of Revenue",
    state="WI",
    rate=0.05,
    exempt=True,
    digi=False,
    disc=0.15,
    cert=True,
    notes="Wisconsin Sales and Use Tax Exemption Certificate Form S-211"
)
_tax(
    code="US-WY",
    name="Wyoming Department of Revenue",
    state="WY",
    rate=0.04,
    exempt=True,
    digi=False,
    disc=0.1,
    cert=True,
    notes="Wyoming Certificate of Exemption for county library systems"
)

def lookup_tax_jurisdiction(jurisdiction_code: str) -> Optional[TaxJurisdictionRule]:
    """Retrieve tax jurisdiction rules by state/jurisdiction code."""
    return TAX_JURISDICTION_REGISTRY.get(jurisdiction_code.strip().upper())


def calculate_tax_for_order(subtotal: Decimal, jurisdiction_code: str, is_library_exempt: bool = True) -> Decimal:
    """Calculate effective sales tax for an acquisitions order."""
    rule = lookup_tax_jurisdiction(jurisdiction_code)
    if not rule:
        return Decimal("0.00")
    if is_library_exempt and rule.library_material_exempt:
        return Decimal("0.00")
    effective_rate = rule.standard_sales_tax_rate
    return (subtotal * effective_rate).quantize(Decimal("0.01"))
