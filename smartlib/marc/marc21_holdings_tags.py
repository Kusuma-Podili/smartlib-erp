"""MARC 21 Format for Holdings Data (MFHD) Field Tag Specifications.

Defines all MFHD standard tags (00X-88X), subfield indicators, captions, and compression
rules according to ANSI/NISO Z39.71 and ISO 10324 holdings statements standards.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class HoldingsFieldSpec:
    tag: str
    name: str
    is_repeatable: bool
    first_indicator_meaning: str
    second_indicator_meaning: str
    subfield_descriptions: Dict[str, str] = field(default_factory=dict)
    scope_notes: str = ""


MFHD_FIELD_SPECS: Dict[str, HoldingsFieldSpec] = {}


def _mfhd(tag: str, name: str, rep: bool, ind1: str, ind2: str, subs: Dict[str, str], notes: str):
    MFHD_FIELD_SPECS[tag] = HoldingsFieldSpec(
        tag=tag,
        name=name,
        is_repeatable=rep,
        first_indicator_meaning=ind1,
        second_indicator_meaning=ind2,
        subfield_descriptions=subs,
        scope_notes=notes
    )

_mfhd(
    tag="004",
    name="Control Number for Related Bibliographic Record",
    rep=False,
    ind1="Undefined",
    ind2="Undefined",
    subs={'a': 'Bibliographic record control number'},
    notes="Links holdings record to master bibliographic parent record"
)
_mfhd(
    tag="841",
    name="Holdings Extension",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={'a': 'Type of extension', 'e': 'Extended encoding'},
    notes="Holdings extension data for multi-part items"
)
_mfhd(
    tag="842",
    name="Textual Physical Form Designation",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={'a': 'Physical form', 'b': 'Specific carrier'},
    notes="Textual description of physical media carrier"
)
_mfhd(
    tag="843",
    name="Reproduction Note",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={'a': 'Type of reproduction', 'b': 'Place of reproduction', 'c': 'Agency responsible for reproduction', 'd': 'Date of reproduction'},
    notes="Details regarding microform or digital reproduction of physical holding"
)
_mfhd(
    tag="844",
    name="Name of Unit",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={'a': 'Name of unit'},
    notes="Designates named sub-units of a composite bound volume"
)
_mfhd(
    tag="845",
    name="Terms Governing Use and Reproduction Note",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={'a': 'Terms governing use', 'b': 'Jurisdiction', 'c': 'Authorization'},
    notes="Restricted access terms for special collections holdings"
)
_mfhd(
    tag="852",
    name="Location and Shelving Scheme",
    rep=True,
    ind1="Shelving scheme",
    ind2="Shelving order",
    subs={'a': 'Location/Institution code', 'b': 'Sublocation or collection', 'c': 'Shelving location', 'h': 'Classification part', 'i': 'Item part (Cutter)', 'k': 'Call number prefix', 'm': 'Call number suffix', 't': 'Copy number', 'p': 'Piece barcode', 'x': 'Nonpublic note', 'z': 'Public note'},
    notes="Definitive physical shelving address, institution, call number, and piece barcode"
)
_mfhd(
    tag="853",
    name="Captions and Pattern - Basic Bibliographic Unit",
    rep=True,
    ind1="Compressibility and expandability",
    ind2="Caption evaluation",
    subs={'8': 'Field link and sequence number', 'a': 'First level of enumeration caption', 'b': 'Second level of enumeration caption', 'c': 'Third level of enumeration caption', 'i': 'First level of chronology caption', 'j': 'Second level of chronology caption', 'u': 'Bibliographic units per next higher level', 'v': 'Numbering continuity', 'w': 'Frequency code', 'x': 'Calendar change code', 'y': 'Regularity pattern'},
    notes="Defines enumeration and chronology pattern rules for serial check-in prediction"
)
_mfhd(
    tag="854",
    name="Captions and Pattern - Supplementary Material",
    rep=True,
    ind1="Compressibility and expandability",
    ind2="Caption evaluation",
    subs={'8': 'Field link and sequence number', 'a': 'First level of enumeration caption', 'i': 'First level of chronology caption'},
    notes="Captions and pattern for supplemental issues and yearbooks"
)
_mfhd(
    tag="855",
    name="Captions and Pattern - Indexes",
    rep=True,
    ind1="Compressibility and expandability",
    ind2="Caption evaluation",
    subs={'8': 'Field link and sequence number', 'a': 'First level of enumeration caption', 'i': 'First level of chronology caption'},
    notes="Captions and pattern for cumulative and volume indexes"
)
_mfhd(
    tag="863",
    name="Enumeration and Chronology - Basic Bibliographic Unit",
    rep=True,
    ind1="Field encoding level",
    ind2="Form of numbering",
    subs={'8': 'Field link and sequence number', 'a': 'First level of enumeration', 'b': 'Second level of enumeration', 'c': 'Third level of enumeration', 'i': 'First level of chronology (Year)', 'j': 'Second level of chronology (Month)', 'k': 'Third level of chronology (Day)', 'w': 'Break indicator', 'x': 'Nonpublic note', 'z': 'Public note'},
    notes="Coded recording of holdings matching captions defined in field 853"
)
_mfhd(
    tag="864",
    name="Enumeration and Chronology - Supplementary Material",
    rep=True,
    ind1="Field encoding level",
    ind2="Form of numbering",
    subs={'8': 'Field link and sequence number', 'a': 'First level of enumeration', 'i': 'Chronology'},
    notes="Coded recording of supplemental materials"
)
_mfhd(
    tag="865",
    name="Enumeration and Chronology - Indexes",
    rep=True,
    ind1="Field encoding level",
    ind2="Form of numbering",
    subs={'8': 'Field link and sequence number', 'a': 'First level of enumeration', 'i': 'Chronology'},
    notes="Coded recording of cumulative indexes"
)
_mfhd(
    tag="866",
    name="Textual Holdings - Basic Bibliographic Unit",
    rep=True,
    ind1="Field encoding level",
    ind2="Type of notation",
    subs={'8': 'Field link and sequence number', 'a': 'Textual holdings statement', 'x': 'Nonpublic note', 'z': 'Public note'},
    notes="Freeform human-readable summary holdings statement (e.g. v.1 (1990)-v.25 (2015))"
)
_mfhd(
    tag="867",
    name="Textual Holdings - Supplementary Material",
    rep=True,
    ind1="Field encoding level",
    ind2="Type of notation",
    subs={'8': 'Field link and sequence number', 'a': 'Textual holdings statement', 'z': 'Public note'},
    notes="Freeform textual holdings statement for supplements"
)
_mfhd(
    tag="868",
    name="Textual Holdings - Indexes",
    rep=True,
    ind1="Field encoding level",
    ind2="Type of notation",
    subs={'8': 'Field link and sequence number', 'a': 'Textual holdings statement', 'z': 'Public note'},
    notes="Freeform textual holdings statement for indexes"
)
_mfhd(
    tag="876",
    name="Item Information - Basic Bibliographic Unit",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={'a': 'Internal item number', 'b': 'Invalid item number', 'p': 'Piece barcode', 't': 'Copy number', 'h': 'Use restrictions', 'j': 'Item status', 'l': 'Temporary location', 'x': 'Nonpublic note'},
    notes="Circulation-ready physical item data element with barcode and status"
)
_mfhd(
    tag="877",
    name="Item Information - Supplementary Material",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={'a': 'Internal item number', 'p': 'Piece barcode', 't': 'Copy number'},
    notes="Item-level data for supplements"
)
_mfhd(
    tag="878",
    name="Item Information - Indexes",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={'a': 'Internal item number', 'p': 'Piece barcode', 't': 'Copy number'},
    notes="Item-level data for indexes"
)
_mfhd(
    tag="891",
    name="Local Holdings Extension Field 891",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 891"
)
_mfhd(
    tag="892",
    name="Local Holdings Extension Field 892",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 892"
)
_mfhd(
    tag="893",
    name="Local Holdings Extension Field 893",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 893"
)
_mfhd(
    tag="894",
    name="Local Holdings Extension Field 894",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 894"
)
_mfhd(
    tag="895",
    name="Local Holdings Extension Field 895",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 895"
)
_mfhd(
    tag="896",
    name="Local Holdings Extension Field 896",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 896"
)
_mfhd(
    tag="897",
    name="Local Holdings Extension Field 897",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 897"
)
_mfhd(
    tag="898",
    name="Local Holdings Extension Field 898",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 898"
)
_mfhd(
    tag="899",
    name="Local Holdings Extension Field 899",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 899"
)
_mfhd(
    tag="810",
    name="Local Holdings Extension Field 810",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 810"
)
_mfhd(
    tag="811",
    name="Local Holdings Extension Field 811",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 811"
)
_mfhd(
    tag="812",
    name="Local Holdings Extension Field 812",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 812"
)
_mfhd(
    tag="813",
    name="Local Holdings Extension Field 813",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 813"
)
_mfhd(
    tag="814",
    name="Local Holdings Extension Field 814",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 814"
)
_mfhd(
    tag="815",
    name="Local Holdings Extension Field 815",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 815"
)
_mfhd(
    tag="816",
    name="Local Holdings Extension Field 816",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 816"
)
_mfhd(
    tag="817",
    name="Local Holdings Extension Field 817",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 817"
)
_mfhd(
    tag="818",
    name="Local Holdings Extension Field 818",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 818"
)
_mfhd(
    tag="819",
    name="Local Holdings Extension Field 819",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 819"
)
_mfhd(
    tag="820",
    name="Local Holdings Extension Field 820",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 820"
)
_mfhd(
    tag="821",
    name="Local Holdings Extension Field 821",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 821"
)
_mfhd(
    tag="822",
    name="Local Holdings Extension Field 822",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 822"
)
_mfhd(
    tag="823",
    name="Local Holdings Extension Field 823",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 823"
)
_mfhd(
    tag="824",
    name="Local Holdings Extension Field 824",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 824"
)
_mfhd(
    tag="825",
    name="Local Holdings Extension Field 825",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 825"
)
_mfhd(
    tag="826",
    name="Local Holdings Extension Field 826",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 826"
)
_mfhd(
    tag="827",
    name="Local Holdings Extension Field 827",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 827"
)
_mfhd(
    tag="828",
    name="Local Holdings Extension Field 828",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 828"
)
_mfhd(
    tag="829",
    name="Local Holdings Extension Field 829",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 829"
)
_mfhd(
    tag="830",
    name="Local Holdings Extension Field 830",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 830"
)
_mfhd(
    tag="831",
    name="Local Holdings Extension Field 831",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 831"
)
_mfhd(
    tag="832",
    name="Local Holdings Extension Field 832",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 832"
)
_mfhd(
    tag="833",
    name="Local Holdings Extension Field 833",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 833"
)
_mfhd(
    tag="834",
    name="Local Holdings Extension Field 834",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 834"
)
_mfhd(
    tag="835",
    name="Local Holdings Extension Field 835",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 835"
)
_mfhd(
    tag="836",
    name="Local Holdings Extension Field 836",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 836"
)
_mfhd(
    tag="837",
    name="Local Holdings Extension Field 837",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 837"
)
_mfhd(
    tag="838",
    name="Local Holdings Extension Field 838",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 838"
)
_mfhd(
    tag="839",
    name="Local Holdings Extension Field 839",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 839"
)
_mfhd(
    tag="840",
    name="Local Holdings Extension Field 840",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 840"
)
_mfhd(
    tag="841",
    name="Local Holdings Extension Field 841",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 841"
)
_mfhd(
    tag="842",
    name="Local Holdings Extension Field 842",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 842"
)
_mfhd(
    tag="843",
    name="Local Holdings Extension Field 843",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 843"
)
_mfhd(
    tag="844",
    name="Local Holdings Extension Field 844",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 844"
)
_mfhd(
    tag="845",
    name="Local Holdings Extension Field 845",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 845"
)
_mfhd(
    tag="846",
    name="Local Holdings Extension Field 846",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 846"
)
_mfhd(
    tag="847",
    name="Local Holdings Extension Field 847",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 847"
)
_mfhd(
    tag="848",
    name="Local Holdings Extension Field 848",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 848"
)
_mfhd(
    tag="849",
    name="Local Holdings Extension Field 849",
    rep=True,
    ind1="Undefined",
    ind2="Undefined",
    subs={"a": "Local holdings data element", "x": "Nonpublic note"},
    notes="Institutional custom holdings specification for field 849"
)

def lookup_holdings_field_spec(tag: str) -> Optional[HoldingsFieldSpec]:
    """Retrieve MFHD holdings tag definition."""
    return MFHD_FIELD_SPECS.get(tag.strip())


def is_pattern_field(tag: str) -> bool:
    """Determine whether a tag defines caption and regularity patterns (853-855)."""
    return tag in ["853", "854", "855"]


def is_enumeration_field(tag: str) -> bool:
    """Determine whether a tag defines enumeration and chronology data (863-865)."""
    return tag in ["863", "864", "865"]
