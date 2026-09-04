"""ASN.1 Basic Encoding Rules (BER) Tag and Type Definitions for Z39.50.

Defines ITU-T X.690 / ISO/IEC 8825-1 universal type tags, Z39.50 application-wide tags,
context-specific tag identifiers, and BER byte encoders/decoders.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Asn1TagDefinition:
    tag_number: int
    tag_class: str  # 'UNIVERSAL', 'APPLICATION', 'CONTEXT_SPECIFIC', 'PRIVATE'
    is_constructed: bool
    type_name: str
    description: str


ASN1_TAG_REGISTRY: Dict[str, Asn1TagDefinition] = {}


def _tag(num: int, tclass: str, constr: bool, name: str, desc: str):
    key = f"{tclass.upper()}-{num}"
    ASN1_TAG_REGISTRY[key] = Asn1TagDefinition(
        tag_number=num,
        tag_class=tclass.upper(),
        is_constructed=constr,
        type_name=name,
        description=desc
    )

_tag(
    num=0,
    tclass="UNIVERSAL",
    constr=False,
    name="END_OF_CONTENT",
    desc="Indicates termination of indefinite length encoding in BER"
)
_tag(
    num=1,
    tclass="UNIVERSAL",
    constr=False,
    name="BOOLEAN",
    desc="Logical truth value: single byte (0x00=False, 0xFF=True)"
)
_tag(
    num=2,
    tclass="UNIVERSAL",
    constr=False,
    name="INTEGER",
    desc="Two's complement signed integer of arbitrary length"
)
_tag(
    num=3,
    tclass="UNIVERSAL",
    constr=False,
    name="BIT_STRING",
    desc="Sequence of zero or more bits with leading unused bits indicator"
)
_tag(
    num=4,
    tclass="UNIVERSAL",
    constr=False,
    name="OCTET_STRING",
    desc="Arbitrary sequence of eight-bit binary bytes"
)
_tag(
    num=5,
    tclass="UNIVERSAL",
    constr=False,
    name="NULL",
    desc="Represents an empty value or missing parameter (length 0)"
)
_tag(
    num=6,
    tclass="UNIVERSAL",
    constr=False,
    name="OBJECT_IDENTIFIER",
    desc="Standard dot-separated ISO/IEC OID tree identifier"
)
_tag(
    num=7,
    tclass="UNIVERSAL",
    constr=False,
    name="OBJECT_DESCRIPTOR",
    desc="Human readable text describing an assigned OID"
)
_tag(
    num=8,
    tclass="UNIVERSAL",
    constr=True,
    name="EXTERNAL",
    desc="Payload typed according to an external standard outside ASN.1"
)
_tag(
    num=9,
    tclass="UNIVERSAL",
    constr=False,
    name="REAL",
    desc="Floating point IEEE 754 value representation"
)
_tag(
    num=10,
    tclass="UNIVERSAL",
    constr=False,
    name="ENUMERATED",
    desc="Distinct integer value selected from declared enumeration list"
)
_tag(
    num=11,
    tclass="UNIVERSAL",
    constr=True,
    name="EMBEDDED_PDV",
    desc="Embedded presentation data value"
)
_tag(
    num=12,
    tclass="UNIVERSAL",
    constr=False,
    name="UTF8String",
    desc="Variable length UTF-8 encoded text string"
)
_tag(
    num=13,
    tclass="UNIVERSAL",
    constr=False,
    name="RELATIVE_OID",
    desc="Relative object identifier without root arc"
)
_tag(
    num=16,
    tclass="UNIVERSAL",
    constr=True,
    name="SEQUENCE",
    desc="Ordered collection of one or more typed fields"
)
_tag(
    num=17,
    tclass="UNIVERSAL",
    constr=True,
    name="SET",
    desc="Unordered collection of distinct typed fields"
)
_tag(
    num=18,
    tclass="UNIVERSAL",
    constr=False,
    name="NumericString",
    desc="Digits 0-9 and space character set"
)
_tag(
    num=19,
    tclass="UNIVERSAL",
    constr=False,
    name="PrintableString",
    desc="ASCII printable subset: letters, digits, punctuation"
)
_tag(
    num=20,
    tclass="UNIVERSAL",
    constr=False,
    name="TeletexString",
    desc="T.61 character string for telematic services"
)
_tag(
    num=21,
    tclass="UNIVERSAL",
    constr=False,
    name="VideotexString",
    desc="T.100 and T.101 character string"
)
_tag(
    num=22,
    tclass="UNIVERSAL",
    constr=False,
    name="IA5String",
    desc="International Alphabet No. 5 (standard 7-bit ASCII)"
)
_tag(
    num=23,
    tclass="UNIVERSAL",
    constr=False,
    name="UTCTime",
    desc="Coordinated Universal Time formatted YYMMDDhhmm[ss]Z"
)
_tag(
    num=24,
    tclass="UNIVERSAL",
    constr=False,
    name="GeneralizedTime",
    desc="High precision timestamp YYYYMMDDhhmmss.fffZ"
)
_tag(
    num=25,
    tclass="UNIVERSAL",
    constr=False,
    name="GraphicString",
    desc="General graphic character set"
)
_tag(
    num=26,
    tclass="UNIVERSAL",
    constr=False,
    name="VisibleString",
    desc="Printing characters from ISO 646 (ASCII 32-126)"
)
_tag(
    num=27,
    tclass="UNIVERSAL",
    constr=False,
    name="GeneralString",
    desc="General character string with escape sequences"
)
_tag(
    num=28,
    tclass="UNIVERSAL",
    constr=False,
    name="UniversalString",
    desc="ISO 10646 4-byte UCS-4 character string"
)
_tag(
    num=30,
    tclass="UNIVERSAL",
    constr=False,
    name="BMPString",
    desc="Basic Multilingual Plane 2-byte UCS-2 string"
)
_tag(
    num=20,
    tclass="APPLICATION",
    constr=True,
    name="InitializeRequest",
    desc="Z39.50 origin request to establish session and negotiate protocol options"
)
_tag(
    num=21,
    tclass="APPLICATION",
    constr=True,
    name="InitializeResponse",
    desc="Z39.50 target response accepting or rejecting connection with options"
)
_tag(
    num=22,
    tclass="APPLICATION",
    constr=True,
    name="SearchRequest",
    desc="Z39.50 origin search request specifying query, databases, and result set"
)
_tag(
    num=23,
    tclass="APPLICATION",
    constr=True,
    name="SearchResponse",
    desc="Z39.50 target search response containing record count and status"
)
_tag(
    num=24,
    tclass="APPLICATION",
    constr=True,
    name="PresentRequest",
    desc="Z39.50 origin request to retrieve formatted records from result set"
)
_tag(
    num=25,
    tclass="APPLICATION",
    constr=True,
    name="PresentResponse",
    desc="Z39.50 target response carrying retrieved bibliographic records"
)
_tag(
    num=26,
    tclass="APPLICATION",
    constr=True,
    name="DeleteResultSetRequest",
    desc="Origin request to delete named result sets from target memory"
)
_tag(
    num=27,
    tclass="APPLICATION",
    constr=True,
    name="DeleteResultSetResponse",
    desc="Target response confirming deletion of requested result sets"
)
_tag(
    num=28,
    tclass="APPLICATION",
    constr=True,
    name="AccessControlRequest",
    desc="Target security challenge requesting password, certificate, or token"
)
_tag(
    num=29,
    tclass="APPLICATION",
    constr=True,
    name="AccessControlResponse",
    desc="Origin credentials response answering security challenge"
)
_tag(
    num=30,
    tclass="APPLICATION",
    constr=True,
    name="ResourceControlRequest",
    desc="Target resource monitor message warning of execution cost or progress"
)
_tag(
    num=31,
    tclass="APPLICATION",
    constr=True,
    name="ResourceControlResponse",
    desc="Origin directive to continue, terminate, or adjust search"
)
_tag(
    num=32,
    tclass="APPLICATION",
    constr=True,
    name="TriggerResourceControlRequest",
    desc="Origin request to query current resource usage from target"
)
_tag(
    num=33,
    tclass="APPLICATION",
    constr=True,
    name="ResourceReportRequest",
    desc="Origin request for target accounting and billing report"
)
_tag(
    num=34,
    tclass="APPLICATION",
    constr=True,
    name="ResourceReportResponse",
    desc="Target accounting report containing financial charges"
)
_tag(
    num=35,
    tclass="APPLICATION",
    constr=True,
    name="ScanRequest",
    desc="Origin request to scan index term list around a specified start term"
)
_tag(
    num=36,
    tclass="APPLICATION",
    constr=True,
    name="ScanResponse",
    desc="Target response carrying scanned terms, occurrences, and attributes"
)
_tag(
    num=37,
    tclass="APPLICATION",
    constr=True,
    name="SortRequest",
    desc="Origin request to sort records in a result set by specified keys"
)
_tag(
    num=38,
    tclass="APPLICATION",
    constr=True,
    name="SortResponse",
    desc="Target response confirming completion of sort operation"
)
_tag(
    num=39,
    tclass="APPLICATION",
    constr=True,
    name="Segment",
    desc="Fragment of large serialized record transmitted in multi-part APDU"
)
_tag(
    num=40,
    tclass="APPLICATION",
    constr=True,
    name="ExtendedServicesRequest",
    desc="Origin request for persistent tasks: orders, update, export"
)
_tag(
    num=41,
    tclass="APPLICATION",
    constr=True,
    name="ExtendedServicesResponse",
    desc="Target status response for extended task execution"
)
_tag(
    num=42,
    tclass="APPLICATION",
    constr=True,
    name="Close",
    desc="Graceful session termination APDU with reason code"
)
_tag(
    num=1,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_001",
    desc="Context-specific protocol element definition #1 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=2,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_002",
    desc="Context-specific protocol element definition #2 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=3,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_003",
    desc="Context-specific protocol element definition #3 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=4,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_004",
    desc="Context-specific protocol element definition #4 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=5,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_005",
    desc="Context-specific protocol element definition #5 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=6,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_006",
    desc="Context-specific protocol element definition #6 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=7,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_007",
    desc="Context-specific protocol element definition #7 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=8,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_008",
    desc="Context-specific protocol element definition #8 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=9,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_009",
    desc="Context-specific protocol element definition #9 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=10,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_010",
    desc="Context-specific protocol element definition #10 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=11,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_011",
    desc="Context-specific protocol element definition #11 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=12,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_012",
    desc="Context-specific protocol element definition #12 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=13,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_013",
    desc="Context-specific protocol element definition #13 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=14,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_014",
    desc="Context-specific protocol element definition #14 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=15,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_015",
    desc="Context-specific protocol element definition #15 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=16,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_016",
    desc="Context-specific protocol element definition #16 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=17,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_017",
    desc="Context-specific protocol element definition #17 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=18,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_018",
    desc="Context-specific protocol element definition #18 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=19,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_019",
    desc="Context-specific protocol element definition #19 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=20,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_020",
    desc="Context-specific protocol element definition #20 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=21,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_021",
    desc="Context-specific protocol element definition #21 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=22,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_022",
    desc="Context-specific protocol element definition #22 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=23,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_023",
    desc="Context-specific protocol element definition #23 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=24,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_024",
    desc="Context-specific protocol element definition #24 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=25,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_025",
    desc="Context-specific protocol element definition #25 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=26,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_026",
    desc="Context-specific protocol element definition #26 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=27,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_027",
    desc="Context-specific protocol element definition #27 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=28,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_028",
    desc="Context-specific protocol element definition #28 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=29,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_029",
    desc="Context-specific protocol element definition #29 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=30,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_030",
    desc="Context-specific protocol element definition #30 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=31,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_031",
    desc="Context-specific protocol element definition #31 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=32,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_032",
    desc="Context-specific protocol element definition #32 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=33,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_033",
    desc="Context-specific protocol element definition #33 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=34,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_034",
    desc="Context-specific protocol element definition #34 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=35,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_035",
    desc="Context-specific protocol element definition #35 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=36,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_036",
    desc="Context-specific protocol element definition #36 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=37,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_037",
    desc="Context-specific protocol element definition #37 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=38,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_038",
    desc="Context-specific protocol element definition #38 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=39,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_039",
    desc="Context-specific protocol element definition #39 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=40,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_040",
    desc="Context-specific protocol element definition #40 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=41,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_041",
    desc="Context-specific protocol element definition #41 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=42,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_042",
    desc="Context-specific protocol element definition #42 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=43,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_043",
    desc="Context-specific protocol element definition #43 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=44,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_044",
    desc="Context-specific protocol element definition #44 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=45,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_045",
    desc="Context-specific protocol element definition #45 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=46,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_046",
    desc="Context-specific protocol element definition #46 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=47,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_047",
    desc="Context-specific protocol element definition #47 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=48,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_048",
    desc="Context-specific protocol element definition #48 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=49,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_049",
    desc="Context-specific protocol element definition #49 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=50,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_050",
    desc="Context-specific protocol element definition #50 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=51,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_051",
    desc="Context-specific protocol element definition #51 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=52,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_052",
    desc="Context-specific protocol element definition #52 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=53,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_053",
    desc="Context-specific protocol element definition #53 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=54,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_054",
    desc="Context-specific protocol element definition #54 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=55,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_055",
    desc="Context-specific protocol element definition #55 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=56,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_056",
    desc="Context-specific protocol element definition #56 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=57,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_057",
    desc="Context-specific protocol element definition #57 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=58,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_058",
    desc="Context-specific protocol element definition #58 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=59,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_059",
    desc="Context-specific protocol element definition #59 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=60,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_060",
    desc="Context-specific protocol element definition #60 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=61,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_061",
    desc="Context-specific protocol element definition #61 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=62,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_062",
    desc="Context-specific protocol element definition #62 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=63,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_063",
    desc="Context-specific protocol element definition #63 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=64,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_064",
    desc="Context-specific protocol element definition #64 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=65,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_065",
    desc="Context-specific protocol element definition #65 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=66,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_066",
    desc="Context-specific protocol element definition #66 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=67,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_067",
    desc="Context-specific protocol element definition #67 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=68,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_068",
    desc="Context-specific protocol element definition #68 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=69,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_069",
    desc="Context-specific protocol element definition #69 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=70,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_070",
    desc="Context-specific protocol element definition #70 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=71,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_071",
    desc="Context-specific protocol element definition #71 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=72,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_072",
    desc="Context-specific protocol element definition #72 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=73,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_073",
    desc="Context-specific protocol element definition #73 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=74,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_074",
    desc="Context-specific protocol element definition #74 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=75,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_075",
    desc="Context-specific protocol element definition #75 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=76,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_076",
    desc="Context-specific protocol element definition #76 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=77,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_077",
    desc="Context-specific protocol element definition #77 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=78,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_078",
    desc="Context-specific protocol element definition #78 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=79,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_079",
    desc="Context-specific protocol element definition #79 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=80,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_080",
    desc="Context-specific protocol element definition #80 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=81,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_081",
    desc="Context-specific protocol element definition #81 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=82,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_082",
    desc="Context-specific protocol element definition #82 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=83,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_083",
    desc="Context-specific protocol element definition #83 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=84,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_084",
    desc="Context-specific protocol element definition #84 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=85,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_085",
    desc="Context-specific protocol element definition #85 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=86,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_086",
    desc="Context-specific protocol element definition #86 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=87,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_087",
    desc="Context-specific protocol element definition #87 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=88,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_088",
    desc="Context-specific protocol element definition #88 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=89,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_089",
    desc="Context-specific protocol element definition #89 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=90,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_090",
    desc="Context-specific protocol element definition #90 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=91,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_091",
    desc="Context-specific protocol element definition #91 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=92,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_092",
    desc="Context-specific protocol element definition #92 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=93,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_093",
    desc="Context-specific protocol element definition #93 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=94,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_094",
    desc="Context-specific protocol element definition #94 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=95,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_095",
    desc="Context-specific protocol element definition #95 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=96,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_096",
    desc="Context-specific protocol element definition #96 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=97,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_097",
    desc="Context-specific protocol element definition #97 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=98,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_098",
    desc="Context-specific protocol element definition #98 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=99,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_099",
    desc="Context-specific protocol element definition #99 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=100,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_100",
    desc="Context-specific protocol element definition #100 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=101,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_101",
    desc="Context-specific protocol element definition #101 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=102,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_102",
    desc="Context-specific protocol element definition #102 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=103,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_103",
    desc="Context-specific protocol element definition #103 for Z39.50 ASN.1 APDU grammar"
)
_tag(
    num=104,
    tclass="CONTEXT_SPECIFIC",
    constr=True,
    name="Z3950_Context_Element_104",
    desc="Context-specific protocol element definition #104 for Z39.50 ASN.1 APDU grammar"
)

def encode_ber_length(length: int) -> bytes:
    """Encode an integer length into BER definite length octets."""
    if length < 128:
        return bytes([length])
    len_bytes = []
    temp = length
    while temp > 0:
        len_bytes.insert(0, temp & 0xFF)
        temp >>= 8
    header = 0x80 | len(len_bytes)
    return bytes([header] + len_bytes)


def decode_ber_length(data: bytes, offset: int = 0) -> Tuple[int, int]:
    """Decode BER length octets starting at offset. Returns (length, bytes_consumed)."""
    first = data[offset]
    if (first & 0x80) == 0:
        return first, 1
    num_octets = first & 0x7F
    val = 0
    for idx in range(num_octets):
        val = (val << 8) | data[offset + 1 + idx]
    return val, 1 + num_octets


def encode_ber_tlv(tag_class: int, tag_number: int, is_constructed: bool, payload: bytes) -> bytes:
    """Encode Tag-Length-Value (TLV) triplet in ASN.1 Basic Encoding Rules."""
    tag_byte = (tag_class << 6) | (0x20 if is_constructed else 0x00)
    if tag_number < 31:
        tag_bytes = bytes([tag_byte | tag_number])
    else:
        # High tag number format
        octets = [tag_byte | 0x1F]
        temp = tag_number
        sub_bytes = []
        while temp > 0:
            sub_bytes.insert(0, (temp & 0x7F) | (0x80 if sub_bytes else 0x00))
            temp >>= 7
        octets.extend(sub_bytes)
        tag_bytes = bytes(octets)

    len_bytes = encode_ber_length(len(payload))
    return tag_bytes + len_bytes + payload
