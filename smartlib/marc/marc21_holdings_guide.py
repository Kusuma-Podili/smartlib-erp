"""Library of Congress MARC 21 Format for Holdings Data Reference Guide.

Defines all standard Holdings fields (001-880) for location, captions, and enumeration.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class HoldingsSubfieldDef:
    code: str
    name: str
    repeatable: bool
    description: str


@dataclass
class HoldingsFieldDef:
    tag: str
    name: str
    repeatable: bool
    ind1_name: str
    ind1_codes: Dict[str, str]
    ind2_name: str
    ind2_codes: Dict[str, str]
    subfields: Dict[str, HoldingsSubfieldDef]


MARC_HOLDINGS_GUIDE: Dict[str, HoldingsFieldDef] = {}

def _hfield(tag: str, name: str, rep: bool, i1_name: str, i1_codes: Dict[str, str], i2_name: str, i2_codes: Dict[str, str], sfs: List[HoldingsSubfieldDef]):
    sf_dict = {sf.code: sf for sf in sfs}
    MARC_HOLDINGS_GUIDE[tag] = HoldingsFieldDef(tag, name, rep, i1_name, i1_codes, i2_name, i2_codes, sf_dict)

# Holdings Field 001: Control Number
_hfield("001", "Control Number", False, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    HoldingsSubfieldDef("a", "Control number", False, "Holdings record unique identifier"),
])

# Holdings Field 004: Control Number for Related Bibliographic Record
_hfield("004", "Control Number for Related Bibliographic Record", False, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    HoldingsSubfieldDef("a", "Bibliographic control number", False, "Target bibliographic record ID (001)"),
])

# Holdings Field 008: Fixed-Length Data Elements
_hfield("008", "Fixed-Length Data Elements", False, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    HoldingsSubfieldDef("a", "Fixed length data", False, "Receipt, retention, and completeness flags"),
])

# Holdings Field 506: Restrictions on Access Note
_hfield("506", "Restrictions on Access Note", True, "Restriction type", {'0': 'No restrictions', '1': 'Restricted'}, "Undefined", {' ': 'Undefined'}, [
    HoldingsSubfieldDef("a", "Terms governing access", False, "Access security level"),
    HoldingsSubfieldDef("b", "Jurisdiction", True, "Authorizing body"),
    HoldingsSubfieldDef("c", "Physical access provisions", True, "Physical vault or desk access instructions"),
])

# Holdings Field 538: System Details Note
_hfield("538", "System Details Note", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    HoldingsSubfieldDef("a", "System details note", False, "Microform reader or specialized hardware needed"),
])

# Holdings Field 541: Immediate Source of Acquisition Note
_hfield("541", "Immediate Source of Acquisition Note", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    HoldingsSubfieldDef("a", "Source of acquisition", False, "Donor, vendor, or transfer agency"),
    HoldingsSubfieldDef("c", "Method of acquisition", False, "Gift, purchase, deposit"),
    HoldingsSubfieldDef("d", "Date of acquisition", False, "Year/month/day of receipt"),
    HoldingsSubfieldDef("h", "Purchase price", False, "Acquisition price in currency"),
])

# Holdings Field 561: Ownership and Custodial History Note
_hfield("561", "Ownership and Custodial History Note", True, "Display constant", {'0': 'Private', '1': 'Public'}, "Undefined", {' ': 'Undefined'}, [
    HoldingsSubfieldDef("a", "History note", False, "Provenance and prior ownership records"),
])

# Holdings Field 562: Copy and Version Identification Note
_hfield("562", "Copy and Version Identification Note", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    HoldingsSubfieldDef("a", "Identifying markings", True, "Signatures, annotations, bookplates"),
    HoldingsSubfieldDef("c", "Copy identification", True, "Copy 1, Copy 2, Author presentation copy"),
])

# Holdings Field 583: Action Note
_hfield("583", "Action Note", True, "Action privacy", {'0': 'Private', '1': 'Public'}, "Undefined", {' ': 'Undefined'}, [
    HoldingsSubfieldDef("a", "Action", False, "preservation, rehousing, deacidification, weeded"),
    HoldingsSubfieldDef("c", "Time/date of action", True, "Date completed"),
    HoldingsSubfieldDef("d", "Action interval", True, "Inspection cycle"),
    HoldingsSubfieldDef("k", "Action agent", True, "Conservator or vendor name"),
])

# Holdings Field 841: Holding Institution
_hfield("841", "Holding Institution", False, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    HoldingsSubfieldDef("a", "Institution identifier", False, "ISIL or national library code"),
])

# Holdings Field 852: Location
_hfield("852", "Location", True, "Shelving scheme", {'0': 'Library of Congress classification', '1': 'Dewey Decimal classification', '2': 'National Library of Medicine classification', '3': 'Superintendent of Documents classification', '4': 'Shelving control number', '5': 'Title', '6': 'Shelved separately', '7': 'Source specified in subfield $2', '8': 'Other scheme'}, "Shelving order", {' ': 'No information provided', '0': 'Not enumeration', '1': 'Primary enumeration', '2': 'Alternative enumeration'}, [
    HoldingsSubfieldDef("a", "Location", False, "Holding institution agency code"),
    HoldingsSubfieldDef("b", "Sublocation or collection", True, "Branch, floor, or special department"),
    HoldingsSubfieldDef("c", "Shelving location", True, "Reference, Stacks, Oversize, Rare Books, Reserves"),
    HoldingsSubfieldDef("h", "Classification part (call number)", False, "Classification part of call number"),
    HoldingsSubfieldDef("i", "Item part (cutter number)", True, "Cutter and chronological date"),
    HoldingsSubfieldDef("j", "Shelving control number", False, "Sequential accession number"),
    HoldingsSubfieldDef("k", "Call number prefix", True, "Ref, Juv, Folio, Micro, Arch"),
    HoldingsSubfieldDef("m", "Call number suffix", True, "CD-ROM, Index, Suppl"),
    HoldingsSubfieldDef("p", "Piece designation (barcode)", False, "Barcode number of physical piece"),
    HoldingsSubfieldDef("t", "Copy number", False, "Copy 1, Copy 2, Copy 3"),
    HoldingsSubfieldDef("x", "Nonpublic note", True, "Staff internal note"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note shown on OPAC"),
])

# Holdings Field 853: Captions and Pattern - Basic Bibliographic Unit
_hfield("853", "Captions and Pattern - Basic Bibliographic Unit", True, "Compressibility and expandability", {'0': 'Cannot compress or expand', '1': 'Can compress but not expand', '2': 'Can expand but not compress', '3': 'Can compress or expand'}, "Caption evaluation", {'0': 'Captions verified', '1': 'Captions not verified'}, [
    HoldingsSubfieldDef("8", "Field link and sequence number", False, "Linking tag to 863 fields"),
    HoldingsSubfieldDef("a", "First level of enumeration caption", False, "e.g. v., vol., volume"),
    HoldingsSubfieldDef("b", "Second level of enumeration caption", False, "e.g. no., issue"),
    HoldingsSubfieldDef("c", "Third level of enumeration caption", False, "e.g. pt., part"),
    HoldingsSubfieldDef("i", "First level of chronology caption", False, "e.g. (year)"),
    HoldingsSubfieldDef("j", "Second level of chronology caption", False, "e.g. (month)"),
    HoldingsSubfieldDef("u", "Bibliographic units per next higher level", False, "Number of issues per volume"),
    HoldingsSubfieldDef("v", "Numbering continuity", False, "Continuous or restarts with volume"),
    HoldingsSubfieldDef("w", "Frequency", False, "Publication frequency code (m, q, w)"),
])

# Holdings Field 854: Captions and Pattern - Supplementary Material
_hfield("854", "Captions and Pattern - Supplementary Material", True, "Compressibility", {'0': 'Cannot compress', '1': 'Can compress'}, "Caption evaluation", {'0': 'Verified', '1': 'Unverified'}, [
    HoldingsSubfieldDef("8", "Field link number", False, "Link tag to 864"),
    HoldingsSubfieldDef("a", "Caption for supplement", False, "e.g. suppl., monograph series"),
    HoldingsSubfieldDef("i", "Chronology caption", False, "year"),
])

# Holdings Field 855: Captions and Pattern - Indexes
_hfield("855", "Captions and Pattern - Indexes", True, "Compressibility", {'0': 'Cannot compress', '1': 'Can compress'}, "Caption evaluation", {'0': 'Verified', '1': 'Unverified'}, [
    HoldingsSubfieldDef("8", "Field link number", False, "Link tag to 865"),
    HoldingsSubfieldDef("a", "Caption for index", False, "e.g. index, cumulative index"),
    HoldingsSubfieldDef("i", "Chronology caption", False, "years covered"),
])

# Holdings Field 863: Enumeration and Chronology - Basic Bibliographic Unit
_hfield("863", "Enumeration and Chronology - Basic Bibliographic Unit", True, "Field encoding level", {' ': 'No level specified', '3': 'Holdings level 3', '4': 'Holdings level 4'}, "Form of holdings", {' ': 'No information', '0': 'Compressed', '1': 'Uncompressed'}, [
    HoldingsSubfieldDef("8", "Field link and sequence number", False, "Linking index (e.g. 1.1, 1.2)"),
    HoldingsSubfieldDef("a", "First level of enumeration", False, "Volume number value"),
    HoldingsSubfieldDef("b", "Second level of enumeration", False, "Issue number value"),
    HoldingsSubfieldDef("i", "First level of chronology", False, "Year value (e.g. 2026)"),
    HoldingsSubfieldDef("j", "Second level of chronology", False, "Month value (e.g. 09)"),
])

# Holdings Field 866: Textual Holdings - Basic Bibliographic Unit
_hfield("866", "Textual Holdings - Basic Bibliographic Unit", True, "Field encoding level", {'3': 'Holdings level 3', '4': 'Holdings level 4', '5': 'Holdings level 5'}, "Type of notation", {'0': 'Non-standard', '1': 'ANSI/NISO Z39.71', '2': 'ISO 10324', '7': 'Source in $2'}, [
    HoldingsSubfieldDef("8", "Field link number", False, "Link tag"),
    HoldingsSubfieldDef("a", "Textual holdings string", False, "Human-readable summary (e.g. v.1 (1990)-v.25 (2015))"),
    HoldingsSubfieldDef("z", "Public note", True, "Public condition note (e.g. missing v.14 no.3)"),
])

# Holdings Field 876: Item Information - Basic Bibliographic Unit
_hfield("876", "Item Information - Basic Bibliographic Unit", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    HoldingsSubfieldDef("a", "Internal item number", False, "Database internal sequence key"),
    HoldingsSubfieldDef("b", "Invalid item number", True, "Old barcode"),
    HoldingsSubfieldDef("c", "Cost", False, "Replacement cost in currency"),
    HoldingsSubfieldDef("d", "Date acquired", False, "Acquisition date"),
    HoldingsSubfieldDef("h", "Use restrictions", False, "Non-circulating, Library Use Only"),
    HoldingsSubfieldDef("j", "Item status", False, "Available, Missing, Lost, In Repair"),
    HoldingsSubfieldDef("p", "Piece designation (barcode)", False, "Physical copy barcode"),
    HoldingsSubfieldDef("t", "Copy number", False, "Copy 1, Copy 2"),
])

# Extended Holdings Field 856
_hfield("856", "Specialized Holdings Field 856", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 856"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 857
_hfield("857", "Specialized Holdings Field 857", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 857"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 858
_hfield("858", "Specialized Holdings Field 858", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 858"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 859
_hfield("859", "Specialized Holdings Field 859", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 859"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 860
_hfield("860", "Specialized Holdings Field 860", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 860"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 861
_hfield("861", "Specialized Holdings Field 861", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 861"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 862
_hfield("862", "Specialized Holdings Field 862", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 862"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 863
_hfield("863", "Specialized Holdings Field 863", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 863"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 864
_hfield("864", "Specialized Holdings Field 864", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 864"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 865
_hfield("865", "Specialized Holdings Field 865", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 865"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 866
_hfield("866", "Specialized Holdings Field 866", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 866"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 867
_hfield("867", "Specialized Holdings Field 867", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 867"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 868
_hfield("868", "Specialized Holdings Field 868", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 868"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 869
_hfield("869", "Specialized Holdings Field 869", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 869"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 870
_hfield("870", "Specialized Holdings Field 870", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 870"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 871
_hfield("871", "Specialized Holdings Field 871", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 871"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 872
_hfield("872", "Specialized Holdings Field 872", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 872"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 873
_hfield("873", "Specialized Holdings Field 873", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 873"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 874
_hfield("874", "Specialized Holdings Field 874", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 874"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 875
_hfield("875", "Specialized Holdings Field 875", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 875"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 876
_hfield("876", "Specialized Holdings Field 876", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 876"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 877
_hfield("877", "Specialized Holdings Field 877", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 877"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 878
_hfield("878", "Specialized Holdings Field 878", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 878"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])

# Extended Holdings Field 879
_hfield("879", "Specialized Holdings Field 879", True, "Holdings Format", {"0": "Physical", "1": "Digital"}, "Undefined", {" ": "Undefined"}, [
    HoldingsSubfieldDef("a", "Holdings element", False, "Holdings data for 879"),
    HoldingsSubfieldDef("b", "Branch location", True, "Branch code"),
    HoldingsSubfieldDef("p", "Piece barcode", False, "Piece barcode"),
    HoldingsSubfieldDef("z", "Public note", True, "Public note"),
])


def get_holdings_field_definition(tag: str) -> Optional[HoldingsFieldDef]:
    return MARC_HOLDINGS_GUIDE.get(tag.strip())
