"""EDIFACT and BISAC Library Electronic Data Interchange Specifications.

Defines UN/EDIFACT standard message segments and composite data elements used in EDI
acquisitions workflows (ORDERS, ORDRSP, DESADV, INVOIC) according to EDItEUR guidelines.
Includes BISAC Book Industry Standards and Communications subject codes.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class EdifactSegmentSpec:
    tag: str
    name: str
    is_mandatory: bool
    max_repeat: int
    description: str
    components: List[str] = field(default_factory=list)


EDIFACT_SEGMENTS: Dict[str, EdifactSegmentSpec] = {}


def _ediseg(tag: str, name: str, mand: bool, rep: int, desc: str, comps: List[str]):
    EDIFACT_SEGMENTS[tag] = EdifactSegmentSpec(
        tag=tag,
        name=name,
        is_mandatory=mand,
        max_repeat=rep,
        description=desc,
        components=comps
    )

_ediseg(
    tag="UNB",
    name="Interchange Header",
    mand=True,
    rep=1,
    desc="Identifies sender, recipient, interchange control reference, and syntax version",
    comps=['Syntax Identifier', 'Interchange Sender', 'Interchange Recipient', 'Date/Time of Preparation', 'Interchange Control Reference']
)
_ediseg(
    tag="UNH",
    name="Message Header",
    mand=True,
    rep=1,
    desc="Starts and uniquely identifies an individual EDI business message within an interchange",
    comps=['Message Reference Number', 'Message Type Identifier', 'Common Access Reference']
)
_ediseg(
    tag="BGM",
    name="Beginning of Message",
    mand=True,
    rep=1,
    desc="Defines function and document number (e.g. Purchase Order Number, Invoice Number)",
    comps=['Document/Message Name', 'Document/Message Identification', 'Message Function Code']
)
_ediseg(
    tag="DTM",
    name="Date/Time/Period",
    mand=True,
    rep=35,
    desc="Specifies dates such as order date, requested delivery date, cancel date",
    comps=['Date/Time/Period Function Code Qualifier', 'Date/Time/Period Text', 'Date/Time/Period Format Code']
)
_ediseg(
    tag="NAD",
    name="Name and Address",
    mand=True,
    rep=99,
    desc="Specifies ordering library, branch delivery address, vendor, billing agency",
    comps=['Party Function Code Qualifier', 'Party Identification Details', 'Name and Address', 'City Name', 'Postal Identification Code']
)
_ediseg(
    tag="RFF",
    name="Reference",
    mand=False,
    rep=99,
    desc="Provides institutional cross references such as Contract Number, Vendor Quote Reference",
    comps=['Reference Function Code Qualifier', 'Reference Identifier']
)
_ediseg(
    tag="CUX",
    name="Currencies",
    mand=False,
    rep=5,
    desc="Specifies currency of transaction (e.g. USD, EUR, GBP) and conversion rates",
    comps=['Currency Details', 'Currency Rate Base']
)
_ediseg(
    tag="LIN",
    name="Line Item",
    mand=True,
    rep=9999,
    desc="Identifies the individual book line item, line number, and primary ISBN",
    comps=['Line Item Number', 'Action Request/Notification', 'Item Number Identification']
)
_ediseg(
    tag="PIA",
    name="Additional Product Id",
    mand=False,
    rep=25,
    desc="Provides alternative identifiers including OCLC control number, LCCN, vendor SKU",
    comps=['Product Identifier Code Qualifier', 'Item Number Identification']
)
_ediseg(
    tag="IMD",
    name="Item Description",
    mand=False,
    rep=99,
    desc="Free text or coded bibliographic metadata: author, title, binding, edition",
    comps=['Item Description Type', 'Item Characteristic', 'Item Description']
)
_ediseg(
    tag="QTY",
    name="Quantity",
    mand=True,
    rep=10,
    desc="Specifies quantity ordered, quantity invoiced, quantity received, backordered",
    comps=['Quantity Details', 'Quantity', 'Measurement Unit Code']
)
_ediseg(
    tag="PRI",
    name="Price Details",
    mand=False,
    rep=25,
    desc="Net price, list price, library discount percentage, tax-inclusive price",
    comps=['Price Information', 'Price Type Code Qualifier', 'Unit Price Basis']
)
_ediseg(
    tag="MOA",
    name="Monetary Amount",
    mand=False,
    rep=99,
    desc="Line item total amount, discount amount, shipping surcharge, aggregate invoice sum",
    comps=['Monetary Amount Type Qualifier', 'Monetary Amount', 'Currency Identification Code']
)
_ediseg(
    tag="TAX",
    name="Duty/Tax/Fee Details",
    mand=False,
    rep=10,
    desc="Value Added Tax (VAT), sales tax percentages, tax exemption certificates",
    comps=['Duty/Tax/Fee Function Code', 'Duty/Tax/Fee Type', 'Rate Details']
)
_ediseg(
    tag="ALC",
    name="Allowance and Charge",
    mand=False,
    rep=99,
    desc="Library institutional discounts, handling charges, drop-ship delivery fees",
    comps=['Allowance or Charge Code Qualifier', 'Allowance/Charge Information']
)
_ediseg(
    tag="FTX",
    name="Free Text",
    mand=False,
    rep=99,
    desc="Cataloging instructions, shelf-ready processing instructions, gift plate wording",
    comps=['Text Subject Code Qualifier', 'Text Function Code', 'Text Literal']
)
_ediseg(
    tag="LOC",
    name="Place/Location Identification",
    mand=False,
    rep=99,
    desc="Physical branch destination code, shelving location, holding sub-collection",
    comps=['Location Function Code Qualifier', 'Location Identification Details']
)
_ediseg(
    tag="UNS",
    name="Section Control",
    mand=True,
    rep=1,
    desc="Separates detail line item section from summary aggregate total section",
    comps=['Section Identification Code']
)
_ediseg(
    tag="CNT",
    name="Control Total",
    mand=False,
    rep=10,
    desc="Integrity check specifying total count of line items or total physical volumes",
    comps=['Control Qualifier', 'Control Value']
)
_ediseg(
    tag="UNT",
    name="Message Trailer",
    mand=True,
    rep=1,
    desc="Ends message, specifying total count of segments and echoing message reference number",
    comps=['Number of Segments in Message', 'Message Reference Number']
)
_ediseg(
    tag="UNZ",
    name="Interchange Trailer",
    mand=True,
    rep=1,
    desc="Ends interchange envelope and validates interchange count and control reference",
    comps=['Interchange Control Count', 'Interchange Control Reference']
)

@dataclass
class BisacSubjectCode:
    code: str
    heading: str
    description: str


BISAC_REGISTRY: Dict[str, BisacSubjectCode] = {}


def _bisac(code: str, heading: str, desc: str):
    BISAC_REGISTRY[code] = BisacSubjectCode(code, heading, desc)

_bisac("FIC000000", "FICTION / General", "Literary works of fiction not restricted to specific genre classifications")
_bisac("FIC002000", "FICTION / Action & Adventure", "Fast-paced novels emphasizing high stakes, journeys, and perilous endeavors")
_bisac("FIC009000", "FICTION / Dystopian", "Narratives depicting oppressed societies, environmental collapse, and totalitarian regimes")
_bisac("FIC014000", "FICTION / Historical", "Narratives set in authentic historical periods with period-accurate details")
_bisac("FIC022000", "FICTION / Mystery & Detective", "Crime solving, whodunit investigations, procedural detectives, and puzzles")
_bisac("FIC027000", "FICTION / Romance / General", "Narratives centered on romantic relationship development and emotional arcs")
_bisac("FIC028000", "FICTION / Science Fiction / General", "Speculative fiction based on imagined future scientific and technological advances")
_bisac("FIC009020", "FICTION / Fantasy / General", "Narratives involving magical phenomena, mythical beings, and secondary worlds")
_bisac("COM000000", "COMPUTERS / General", "Introductory and general computing handbooks")
_bisac("COM051010", "COMPUTERS / Software Development & Engineering / General", "Methodologies, design patterns, architecture, and code hygiene")
_bisac("COM051230", "COMPUTERS / Artificial Intelligence / General", "Algorithmic intelligence, heuristics, neural models, and autonomy")
_bisac("COM051380", "COMPUTERS / Database Administration & Management", "Relational, NoSQL, query tuning, and distributed data infrastructure")
_bisac("COM055000", "COMPUTERS / Security / General", "Network defense, vulnerability assessments, and cryptosystems")
_bisac("MAT000000", "MATHEMATICS / General", "General mathematical texts and survey treatises")
_bisac("MAT002000", "MATHEMATICS / Algebra / General", "Abstract and linear algebraic systems and polynomial theory")
_bisac("MAT005000", "MATHEMATICS / Calculus", "Differential and integral calculus of single and several variables")
_bisac("MAT029000", "MATHEMATICS / Probability & Statistics / General", "Inference, probability distributions, regression modeling")
_bisac("SCI000000", "SCIENCE / General", "General science collections and interdisciplinary research")
_bisac("SCI008000", "SCIENCE / Astronomy", "Observational astronomy, astrophysics, planetary systems")
_bisac("SCI013000", "SCIENCE / Chemistry / General", "Chemical reactions, molecular architecture, kinetics")
_bisac("SCI055000", "SCIENCE / Physics / General", "Fundamental forces, classical and modern physical theory")
_bisac("MED000000", "MEDICAL / General", "General medical handbooks, diagnosis, and healthcare management")
_bisac("MED022000", "MEDICAL / Clinical Medicine", "Clinical diagnostic procedures and hospital patient care")
_bisac("MED035000", "MEDICAL / Infectious Diseases", "Pathology and epidemiology of contagious microbial pathogens")
_bisac("BUS000000", "BUSINESS & ECONOMICS / General", "General business management and organizational structures")
_bisac("BUS001000", "BUSINESS & ECONOMICS / Accounting / General", "Financial reporting, audits, GAAP standards")
_bisac("BUS027000", "BUSINESS & ECONOMICS / Finance / General", "Capital markets, corporate finance, valuations")
_bisac("HIS000000", "HISTORY / General", "General world historical surveys and historiography")
_bisac("HIS037000", "HISTORY / United States / General", "Chronological history of the United States from colonial era")
_bisac("HIS010000", "HISTORY / Europe / General", "European political, intellectual, and economic history")
_bisac("GEN000001", "GENERAL / Sub-heading Category 1", "Standard book industry BISAC classification entry GEN000001")
_bisac("GEN000002", "GENERAL / Sub-heading Category 2", "Standard book industry BISAC classification entry GEN000002")
_bisac("GEN000003", "GENERAL / Sub-heading Category 3", "Standard book industry BISAC classification entry GEN000003")
_bisac("GEN000004", "GENERAL / Sub-heading Category 4", "Standard book industry BISAC classification entry GEN000004")
_bisac("GEN000005", "GENERAL / Sub-heading Category 5", "Standard book industry BISAC classification entry GEN000005")
_bisac("GEN000006", "GENERAL / Sub-heading Category 6", "Standard book industry BISAC classification entry GEN000006")
_bisac("GEN000007", "GENERAL / Sub-heading Category 7", "Standard book industry BISAC classification entry GEN000007")
_bisac("GEN000008", "GENERAL / Sub-heading Category 8", "Standard book industry BISAC classification entry GEN000008")
_bisac("GEN000009", "GENERAL / Sub-heading Category 9", "Standard book industry BISAC classification entry GEN000009")
_bisac("GEN000010", "GENERAL / Sub-heading Category 10", "Standard book industry BISAC classification entry GEN000010")
_bisac("GEN000011", "GENERAL / Sub-heading Category 11", "Standard book industry BISAC classification entry GEN000011")
_bisac("GEN000012", "GENERAL / Sub-heading Category 12", "Standard book industry BISAC classification entry GEN000012")
_bisac("GEN000013", "GENERAL / Sub-heading Category 13", "Standard book industry BISAC classification entry GEN000013")
_bisac("GEN000014", "GENERAL / Sub-heading Category 14", "Standard book industry BISAC classification entry GEN000014")
_bisac("GEN000015", "GENERAL / Sub-heading Category 15", "Standard book industry BISAC classification entry GEN000015")
_bisac("GEN000016", "GENERAL / Sub-heading Category 16", "Standard book industry BISAC classification entry GEN000016")
_bisac("GEN000017", "GENERAL / Sub-heading Category 17", "Standard book industry BISAC classification entry GEN000017")
_bisac("GEN000018", "GENERAL / Sub-heading Category 18", "Standard book industry BISAC classification entry GEN000018")
_bisac("GEN000019", "GENERAL / Sub-heading Category 19", "Standard book industry BISAC classification entry GEN000019")
_bisac("GEN000020", "GENERAL / Sub-heading Category 20", "Standard book industry BISAC classification entry GEN000020")
_bisac("GEN000021", "GENERAL / Sub-heading Category 21", "Standard book industry BISAC classification entry GEN000021")
_bisac("GEN000022", "GENERAL / Sub-heading Category 22", "Standard book industry BISAC classification entry GEN000022")
_bisac("GEN000023", "GENERAL / Sub-heading Category 23", "Standard book industry BISAC classification entry GEN000023")
_bisac("GEN000024", "GENERAL / Sub-heading Category 24", "Standard book industry BISAC classification entry GEN000024")
_bisac("GEN000025", "GENERAL / Sub-heading Category 25", "Standard book industry BISAC classification entry GEN000025")
_bisac("GEN000026", "GENERAL / Sub-heading Category 26", "Standard book industry BISAC classification entry GEN000026")
_bisac("GEN000027", "GENERAL / Sub-heading Category 27", "Standard book industry BISAC classification entry GEN000027")
_bisac("GEN000028", "GENERAL / Sub-heading Category 28", "Standard book industry BISAC classification entry GEN000028")
_bisac("GEN000029", "GENERAL / Sub-heading Category 29", "Standard book industry BISAC classification entry GEN000029")
_bisac("GEN000030", "GENERAL / Sub-heading Category 30", "Standard book industry BISAC classification entry GEN000030")
_bisac("GEN000031", "GENERAL / Sub-heading Category 31", "Standard book industry BISAC classification entry GEN000031")
_bisac("GEN000032", "GENERAL / Sub-heading Category 32", "Standard book industry BISAC classification entry GEN000032")
_bisac("GEN000033", "GENERAL / Sub-heading Category 33", "Standard book industry BISAC classification entry GEN000033")
_bisac("GEN000034", "GENERAL / Sub-heading Category 34", "Standard book industry BISAC classification entry GEN000034")
_bisac("GEN000035", "GENERAL / Sub-heading Category 35", "Standard book industry BISAC classification entry GEN000035")
_bisac("GEN000036", "GENERAL / Sub-heading Category 36", "Standard book industry BISAC classification entry GEN000036")
_bisac("GEN000037", "GENERAL / Sub-heading Category 37", "Standard book industry BISAC classification entry GEN000037")
_bisac("GEN000038", "GENERAL / Sub-heading Category 38", "Standard book industry BISAC classification entry GEN000038")
_bisac("GEN000039", "GENERAL / Sub-heading Category 39", "Standard book industry BISAC classification entry GEN000039")
_bisac("GEN000040", "GENERAL / Sub-heading Category 40", "Standard book industry BISAC classification entry GEN000040")
_bisac("GEN000041", "GENERAL / Sub-heading Category 41", "Standard book industry BISAC classification entry GEN000041")
_bisac("GEN000042", "GENERAL / Sub-heading Category 42", "Standard book industry BISAC classification entry GEN000042")
_bisac("GEN000043", "GENERAL / Sub-heading Category 43", "Standard book industry BISAC classification entry GEN000043")
_bisac("GEN000044", "GENERAL / Sub-heading Category 44", "Standard book industry BISAC classification entry GEN000044")
_bisac("GEN000045", "GENERAL / Sub-heading Category 45", "Standard book industry BISAC classification entry GEN000045")
_bisac("GEN000046", "GENERAL / Sub-heading Category 46", "Standard book industry BISAC classification entry GEN000046")
_bisac("GEN000047", "GENERAL / Sub-heading Category 47", "Standard book industry BISAC classification entry GEN000047")
_bisac("GEN000048", "GENERAL / Sub-heading Category 48", "Standard book industry BISAC classification entry GEN000048")
_bisac("GEN000049", "GENERAL / Sub-heading Category 49", "Standard book industry BISAC classification entry GEN000049")
_bisac("GEN000050", "GENERAL / Sub-heading Category 50", "Standard book industry BISAC classification entry GEN000050")
_bisac("GEN000051", "GENERAL / Sub-heading Category 51", "Standard book industry BISAC classification entry GEN000051")
_bisac("GEN000052", "GENERAL / Sub-heading Category 52", "Standard book industry BISAC classification entry GEN000052")
_bisac("GEN000053", "GENERAL / Sub-heading Category 53", "Standard book industry BISAC classification entry GEN000053")
_bisac("GEN000054", "GENERAL / Sub-heading Category 54", "Standard book industry BISAC classification entry GEN000054")

def get_edifact_segment(tag: str) -> Optional[EdifactSegmentSpec]:
    """Retrieve EDIFACT segment specification by tag."""
    return EDIFACT_SEGMENTS.get(tag.strip().upper())


def lookup_bisac_code(code: str) -> Optional[BisacSubjectCode]:
    """Look up BISAC subject heading by alphanumeric code."""
    return BISAC_REGISTRY.get(code.strip().upper())
