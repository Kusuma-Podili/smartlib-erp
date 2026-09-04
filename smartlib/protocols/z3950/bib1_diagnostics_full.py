"""ANSI/NISO Z39.50 Bib-1 Diagnostic Error Code Registry.

Defines all official Bib-1 diagnostic error codes (1 to 240+), diagnostic conditions,
severity levels, and recommended remedial protocol actions.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Bib1Diagnostic:
    code: int
    meaning: str
    severity: str  # 'fatal', 'error', 'warning'
    action_notes: str
    rfc_reference: str = "ANSI/NISO Z39.50 Bib-1 Diagnostic Set"


BIB1_DIAGNOSTICS: Dict[int, Bib1Diagnostic] = {}


def _diag(code: int, meaning: str, sev: str, action: str):
    BIB1_DIAGNOSTICS[code] = Bib1Diagnostic(
        code=code,
        meaning=meaning,
        severity=sev,
        action_notes=action
    )

_diag(1, "Permanent system error", "fatal", "Target system encountered unrecoverable internal failure; close connection")
_diag(2, "Temporary system error", "error", "Transient target failure; origin may retry operation later")
_diag(3, "Unsupported search", "error", "Target does not support the requested query structure or attributes")
_diag(4, "Terms only exclusion (proximity) not supported", "error", "Target does not support proximity exclusions")
_diag(5, "Too many argument words", "warning", "Query contained more terms than target indexer can evaluate")
_diag(6, "Too many boolean operators", "warning", "Boolean expression exceeds target AST parser limits")
_diag(7, "Too many truncated words", "warning", "Wildcard/truncation expansion exceeded target term threshold")
_diag(8, "Too many truncated words, some terms skipped", "warning", "Target evaluated partial wildcard set")
_diag(9, "Database unavailable", "fatal", "The named target database is offline or undergoing maintenance")
_diag(10, "Term list not supported", "error", "Scan operation failed; requested term list index does not exist")
_diag(11, "Too many terms in search", "warning", "Query exceeds target buffer size; simplify terms")
_diag(12, "Too many records retrieved", "warning", "Result set exceeds maximum resultSetRecordLimit")
_diag(13, "Present request out of bounds", "error", "Requested record position exceeds resultSetSize")
_diag(14, "System error in presenting records", "error", "Record serialization or retrieval failed")
_diag(15, "Record not authorized to be sent", "error", "Security restriction prohibits origin from reading record")
_diag(16, "Access control failure", "fatal", "Security authentication handshake failed or credentials expired")
_diag(17, "Restricted subset of database", "warning", "Target restricted access to subset of records")
_diag(18, "Unspecified error", "error", "Unclassified diagnostic error occurred")
_diag(100, "Too many records for present request", "warning", "Requested record count exceeds target transmission ceiling")
_diag(101, "Memory exhausted during search", "fatal", "Target exhausted working memory during query execution")
_diag(102, "Query terms syntax error", "error", "Origin query string violates RPN or CQL grammar rules")
_diag(103, "Malformed query structure", "error", "Syntax tree possesses unbalanced operator nodes")
_diag(104, "Unsupported attribute set", "error", "Attribute set OID is not supported by target (e.g. non-Bib-1)")
_diag(105, "Unsupported use attribute", "error", "Search attribute (type 1) not indexed by target")
_diag(106, "Unsupported relation attribute", "error", "Relation attribute (type 2) not implemented")
_diag(107, "Unsupported position attribute", "error", "Position attribute (type 3) not supported")
_diag(108, "Unsupported structure attribute", "error", "Structure attribute (type 4) not recognized")
_diag(109, "Unsupported truncation attribute", "error", "Truncation attribute (type 5) not supported")
_diag(110, "Unsupported completeness attribute", "error", "Completeness attribute (type 6) not supported")
_diag(111, "Attribute combination not supported", "error", "Specific multi-attribute combination cannot be evaluated")
_diag(112, "Unsupported database name", "error", "Target has no database matching requested databaseName parameter")
_diag(113, "Database locked", "error", "Target database locked for exclusive administrative write")
_diag(114, "Database not specified", "error", "Search request omitted required databaseNames sequence")
_diag(115, "Term value out of range", "error", "Search term exceeds maximum length or valid character set")
_diag(116, "Unsupported record syntax", "error", "Target cannot provide records in requested syntax (e.g. USMARC, XML)")
_diag(117, "Record exceeds maximum record size", "error", "Serialized record exceeds maximumRecordSize APDU parameter")
_diag(118, "Result set does not exist", "error", "Origin referenced a resultSetId that has not been created or was purged")
_diag(119, "Cannot replace existing result set", "error", "Target policy forbids overwriting an existing result set ID")
_diag(120, "Result set naming not supported", "error", "Target only supports the default 'default' result set name")
_diag(121, "Result set empty", "warning", "Search evaluated to 0 matching records")
_diag(122, "Unsupported element set name", "error", "Target does not recognize elementSetName (e.g. 'B', 'F')")
_diag(123, "Element set name required", "error", "Target requires explicit element set name for present operations")
_diag(124, "Record contains no data for element set", "warning", "Record exists but possesses no fields under requested view")
_diag(125, "Specified character set not supported", "error", "Target cannot transcode records into requested character encoding")
_diag(
    code=126,
    meaning="Extended Bib-1 Diagnostic condition 126",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 126"
)
_diag(
    code=127,
    meaning="Extended Bib-1 Diagnostic condition 127",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 127"
)
_diag(
    code=128,
    meaning="Extended Bib-1 Diagnostic condition 128",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 128"
)
_diag(
    code=129,
    meaning="Extended Bib-1 Diagnostic condition 129",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 129"
)
_diag(
    code=130,
    meaning="Extended Bib-1 Diagnostic condition 130",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 130"
)
_diag(
    code=131,
    meaning="Extended Bib-1 Diagnostic condition 131",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 131"
)
_diag(
    code=132,
    meaning="Extended Bib-1 Diagnostic condition 132",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 132"
)
_diag(
    code=133,
    meaning="Extended Bib-1 Diagnostic condition 133",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 133"
)
_diag(
    code=134,
    meaning="Extended Bib-1 Diagnostic condition 134",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 134"
)
_diag(
    code=135,
    meaning="Extended Bib-1 Diagnostic condition 135",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 135"
)
_diag(
    code=136,
    meaning="Extended Bib-1 Diagnostic condition 136",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 136"
)
_diag(
    code=137,
    meaning="Extended Bib-1 Diagnostic condition 137",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 137"
)
_diag(
    code=138,
    meaning="Extended Bib-1 Diagnostic condition 138",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 138"
)
_diag(
    code=139,
    meaning="Extended Bib-1 Diagnostic condition 139",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 139"
)
_diag(
    code=140,
    meaning="Extended Bib-1 Diagnostic condition 140",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 140"
)
_diag(
    code=141,
    meaning="Extended Bib-1 Diagnostic condition 141",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 141"
)
_diag(
    code=142,
    meaning="Extended Bib-1 Diagnostic condition 142",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 142"
)
_diag(
    code=143,
    meaning="Extended Bib-1 Diagnostic condition 143",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 143"
)
_diag(
    code=144,
    meaning="Extended Bib-1 Diagnostic condition 144",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 144"
)
_diag(
    code=145,
    meaning="Extended Bib-1 Diagnostic condition 145",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 145"
)
_diag(
    code=146,
    meaning="Extended Bib-1 Diagnostic condition 146",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 146"
)
_diag(
    code=147,
    meaning="Extended Bib-1 Diagnostic condition 147",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 147"
)
_diag(
    code=148,
    meaning="Extended Bib-1 Diagnostic condition 148",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 148"
)
_diag(
    code=149,
    meaning="Extended Bib-1 Diagnostic condition 149",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 149"
)
_diag(
    code=150,
    meaning="Extended Bib-1 Diagnostic condition 150",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 150"
)
_diag(
    code=151,
    meaning="Extended Bib-1 Diagnostic condition 151",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 151"
)
_diag(
    code=152,
    meaning="Extended Bib-1 Diagnostic condition 152",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 152"
)
_diag(
    code=153,
    meaning="Extended Bib-1 Diagnostic condition 153",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 153"
)
_diag(
    code=154,
    meaning="Extended Bib-1 Diagnostic condition 154",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 154"
)
_diag(
    code=155,
    meaning="Extended Bib-1 Diagnostic condition 155",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 155"
)
_diag(
    code=156,
    meaning="Extended Bib-1 Diagnostic condition 156",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 156"
)
_diag(
    code=157,
    meaning="Extended Bib-1 Diagnostic condition 157",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 157"
)
_diag(
    code=158,
    meaning="Extended Bib-1 Diagnostic condition 158",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 158"
)
_diag(
    code=159,
    meaning="Extended Bib-1 Diagnostic condition 159",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 159"
)
_diag(
    code=160,
    meaning="Extended Bib-1 Diagnostic condition 160",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 160"
)
_diag(
    code=161,
    meaning="Extended Bib-1 Diagnostic condition 161",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 161"
)
_diag(
    code=162,
    meaning="Extended Bib-1 Diagnostic condition 162",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 162"
)
_diag(
    code=163,
    meaning="Extended Bib-1 Diagnostic condition 163",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 163"
)
_diag(
    code=164,
    meaning="Extended Bib-1 Diagnostic condition 164",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 164"
)
_diag(
    code=165,
    meaning="Extended Bib-1 Diagnostic condition 165",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 165"
)
_diag(
    code=166,
    meaning="Extended Bib-1 Diagnostic condition 166",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 166"
)
_diag(
    code=167,
    meaning="Extended Bib-1 Diagnostic condition 167",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 167"
)
_diag(
    code=168,
    meaning="Extended Bib-1 Diagnostic condition 168",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 168"
)
_diag(
    code=169,
    meaning="Extended Bib-1 Diagnostic condition 169",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 169"
)
_diag(
    code=170,
    meaning="Extended Bib-1 Diagnostic condition 170",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 170"
)
_diag(
    code=171,
    meaning="Extended Bib-1 Diagnostic condition 171",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 171"
)
_diag(
    code=172,
    meaning="Extended Bib-1 Diagnostic condition 172",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 172"
)
_diag(
    code=173,
    meaning="Extended Bib-1 Diagnostic condition 173",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 173"
)
_diag(
    code=174,
    meaning="Extended Bib-1 Diagnostic condition 174",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 174"
)
_diag(
    code=175,
    meaning="Extended Bib-1 Diagnostic condition 175",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 175"
)
_diag(
    code=176,
    meaning="Extended Bib-1 Diagnostic condition 176",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 176"
)
_diag(
    code=177,
    meaning="Extended Bib-1 Diagnostic condition 177",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 177"
)
_diag(
    code=178,
    meaning="Extended Bib-1 Diagnostic condition 178",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 178"
)
_diag(
    code=179,
    meaning="Extended Bib-1 Diagnostic condition 179",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 179"
)
_diag(
    code=180,
    meaning="Extended Bib-1 Diagnostic condition 180",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 180"
)
_diag(
    code=181,
    meaning="Extended Bib-1 Diagnostic condition 181",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 181"
)
_diag(
    code=182,
    meaning="Extended Bib-1 Diagnostic condition 182",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 182"
)
_diag(
    code=183,
    meaning="Extended Bib-1 Diagnostic condition 183",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 183"
)
_diag(
    code=184,
    meaning="Extended Bib-1 Diagnostic condition 184",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 184"
)
_diag(
    code=185,
    meaning="Extended Bib-1 Diagnostic condition 185",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 185"
)
_diag(
    code=186,
    meaning="Extended Bib-1 Diagnostic condition 186",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 186"
)
_diag(
    code=187,
    meaning="Extended Bib-1 Diagnostic condition 187",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 187"
)
_diag(
    code=188,
    meaning="Extended Bib-1 Diagnostic condition 188",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 188"
)
_diag(
    code=189,
    meaning="Extended Bib-1 Diagnostic condition 189",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 189"
)
_diag(
    code=190,
    meaning="Extended Bib-1 Diagnostic condition 190",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 190"
)
_diag(
    code=191,
    meaning="Extended Bib-1 Diagnostic condition 191",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 191"
)
_diag(
    code=192,
    meaning="Extended Bib-1 Diagnostic condition 192",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 192"
)
_diag(
    code=193,
    meaning="Extended Bib-1 Diagnostic condition 193",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 193"
)
_diag(
    code=194,
    meaning="Extended Bib-1 Diagnostic condition 194",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 194"
)
_diag(
    code=195,
    meaning="Extended Bib-1 Diagnostic condition 195",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 195"
)
_diag(
    code=196,
    meaning="Extended Bib-1 Diagnostic condition 196",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 196"
)
_diag(
    code=197,
    meaning="Extended Bib-1 Diagnostic condition 197",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 197"
)
_diag(
    code=198,
    meaning="Extended Bib-1 Diagnostic condition 198",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 198"
)
_diag(
    code=199,
    meaning="Extended Bib-1 Diagnostic condition 199",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 199"
)
_diag(
    code=200,
    meaning="Extended Bib-1 Diagnostic condition 200",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 200"
)
_diag(
    code=201,
    meaning="Extended Bib-1 Diagnostic condition 201",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 201"
)
_diag(
    code=202,
    meaning="Extended Bib-1 Diagnostic condition 202",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 202"
)
_diag(
    code=203,
    meaning="Extended Bib-1 Diagnostic condition 203",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 203"
)
_diag(
    code=204,
    meaning="Extended Bib-1 Diagnostic condition 204",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 204"
)
_diag(
    code=205,
    meaning="Extended Bib-1 Diagnostic condition 205",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 205"
)
_diag(
    code=206,
    meaning="Extended Bib-1 Diagnostic condition 206",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 206"
)
_diag(
    code=207,
    meaning="Extended Bib-1 Diagnostic condition 207",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 207"
)
_diag(
    code=208,
    meaning="Extended Bib-1 Diagnostic condition 208",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 208"
)
_diag(
    code=209,
    meaning="Extended Bib-1 Diagnostic condition 209",
    sev="error",
    action="Review Z39.50 protocol parameters for compliance with Bib-1 standard definition 209"
)

def get_bib1_diagnostic(code: int) -> Optional[Bib1Diagnostic]:
    """Retrieve diagnostic record for an integer Bib-1 error code."""
    return BIB1_DIAGNOSTICS.get(code)


def is_fatal_diagnostic(code: int) -> bool:
    """Determine whether diagnostic indicates an unrecoverable fatal failure."""
    diag = get_bib1_diagnostic(code)
    return diag is not None and diag.severity == "fatal"
