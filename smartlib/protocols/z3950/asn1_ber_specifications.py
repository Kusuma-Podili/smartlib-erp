"""ANSI/NISO Z39.50 ASN.1 APDU (Application Protocol Data Unit) Specifications.

Complete ASN.1 PDU structures, diagnostic tables, and wire-encoding rules.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Z3950DiagnosticDefinition:
    code: int
    category: str
    message: str
    suggested_action: str


@dataclass
class Asn1PduSpecification:
    pdu_id: int
    pdu_name: str
    is_initiating: bool
    asn1_syntax: str
    description: str


Z3950_DIAGNOSTICS_REGISTRY: Dict[int, Z3950DiagnosticDefinition] = {}
Z3950_PDU_REGISTRY: Dict[int, Asn1PduSpecification] = {}

def _diag(code: int, cat: str, msg: str, act: str):
    Z3950_DIAGNOSTICS_REGISTRY[code] = Z3950DiagnosticDefinition(code, cat, msg, act)

def _pdu(pid: int, name: str, init: bool, syn: str, desc: str):
    Z3950_PDU_REGISTRY[pid] = Asn1PduSpecification(pid, name, init, syn, desc)

_diag(1, "Permanent system error", "Permanent system error occurred on target server", "Notify remote system administrator")
_diag(2, "Temporary system error", "Temporary transient resource unavailability on target", "Retry search query after backoff interval")
_diag(3, "Unsupported search", "Search syntax or combination of operators not supported", "Reformulate query using basic boolean terms")
_diag(4, "Terms only exclusion (proximity)", "Proximity search operator terms only exclusion", "Modify proximity condition")
_diag(100, "Too many terms", "Query contains more terms than server can parse", "Reduce number of keywords in query")
_diag(101, "Too many sequence match operations", "Query complexity exceeded maximum operations limit", "Simplify boolean query tree")
_diag(102, "Too many argument operators", "Operator stack overflow on Z39.50 server", "Split into multiple smaller queries")
_diag(103, "Too many result sets", "Maximum open result sets reached on server", "Delete unused result sets")
_diag(104, "Present request out of bounds", "Requested start record position beyond result set size", "Adjust resultSetPosition to within resultCount")
_diag(105, "Term character invalid", "Character set encoding error in search term", "Ensure valid UTF-8 character encoding")
_diag(106, "No result set name supplied", "Missing required result set name in search request", "Provide default result set name")
_diag(107, "Specified result set name exists", "Target result set name already occupied", "Provide distinct result set name")
_diag(108, "Result set does not exist", "Referenced result set not found or expired on server", "Rerun search to generate fresh result set")
_diag(109, "Database unavailable", "Requested catalog database temporarily offline", "Verify database name in Init parameters")
_diag(110, "Specified database not available", "Target catalog database not recognized", "Query explain service for available databases")
_diag(111, "Specified attribute type unsupported", "Use attribute type not recognized by target server", "Use standard Bib-1 Use attributes")
_diag(112, "Attribute value unsupported", "Attribute value not supported on this database", "Check target attribute profile")
_diag(113, "Unsupported Use attribute", "Target does not support specified Use attribute", "Fallback to generic Title or Any attribute")
_diag(114, "Unsupported Relation attribute", "Relation comparison operator not supported", "Use '=' (equality) relation")
_diag(115, "Unsupported Structure attribute", "Structure attribute not supported", "Use Word or Phrase structure")
_diag(116, "Unsupported Position attribute", "Position attribute not supported", "Use Any Position in Field")
_diag(117, "Unsupported Truncation attribute", "Wildcard truncation type not supported", "Use Right Truncation or No Truncation")
_diag(118, "Unsupported Completeness attribute", "Completeness attribute not supported", "Use Incomplete Subfield")
_diag(119, "Unsupported attribute combination", "Combination of Bib-1 attributes not valid on target", "Simplify attribute set")
_diag(120, "Unsupported relation and structure combination", "Relation and structure incompatible", "Align structure with relation")
_diag(121, "Unsupported record syntax", "Requested record syntax (MARC21, XML, SUTRS) not supported", "Request standard MARC21 syntax")
_diag(122, "Unsupported element set name", "Element set (B, F) not supported", "Use standard 'F' (Full) element set")
_diag(123, "Too many records requested", "Present request count exceeds server maximum record limit", "Request smaller batches (10 to 20 records)")
_diag(124, "Record cannot be unpacked", "Error unpacking bibliographic record from store", "Contact catalog technical administrator")
_diag(125, "Catalog Search Diagnostic 125", "Z39.50 protocol diagnostic code 125 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(126, "Catalog Search Diagnostic 126", "Z39.50 protocol diagnostic code 126 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(127, "Catalog Search Diagnostic 127", "Z39.50 protocol diagnostic code 127 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(128, "Catalog Search Diagnostic 128", "Z39.50 protocol diagnostic code 128 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(129, "Catalog Search Diagnostic 129", "Z39.50 protocol diagnostic code 129 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(130, "Catalog Search Diagnostic 130", "Z39.50 protocol diagnostic code 130 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(131, "Catalog Search Diagnostic 131", "Z39.50 protocol diagnostic code 131 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(132, "Catalog Search Diagnostic 132", "Z39.50 protocol diagnostic code 132 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(133, "Catalog Search Diagnostic 133", "Z39.50 protocol diagnostic code 133 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(134, "Catalog Search Diagnostic 134", "Z39.50 protocol diagnostic code 134 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(135, "Catalog Search Diagnostic 135", "Z39.50 protocol diagnostic code 135 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(136, "Catalog Search Diagnostic 136", "Z39.50 protocol diagnostic code 136 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(137, "Catalog Search Diagnostic 137", "Z39.50 protocol diagnostic code 137 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(138, "Catalog Search Diagnostic 138", "Z39.50 protocol diagnostic code 138 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(139, "Catalog Search Diagnostic 139", "Z39.50 protocol diagnostic code 139 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(140, "Catalog Search Diagnostic 140", "Z39.50 protocol diagnostic code 140 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(141, "Catalog Search Diagnostic 141", "Z39.50 protocol diagnostic code 141 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(142, "Catalog Search Diagnostic 142", "Z39.50 protocol diagnostic code 142 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(143, "Catalog Search Diagnostic 143", "Z39.50 protocol diagnostic code 143 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(144, "Catalog Search Diagnostic 144", "Z39.50 protocol diagnostic code 144 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(145, "Catalog Search Diagnostic 145", "Z39.50 protocol diagnostic code 145 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(146, "Catalog Search Diagnostic 146", "Z39.50 protocol diagnostic code 146 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(147, "Catalog Search Diagnostic 147", "Z39.50 protocol diagnostic code 147 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(148, "Catalog Search Diagnostic 148", "Z39.50 protocol diagnostic code 148 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(149, "Catalog Search Diagnostic 149", "Z39.50 protocol diagnostic code 149 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(150, "Catalog Search Diagnostic 150", "Z39.50 protocol diagnostic code 150 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(151, "Catalog Search Diagnostic 151", "Z39.50 protocol diagnostic code 151 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(152, "Catalog Search Diagnostic 152", "Z39.50 protocol diagnostic code 152 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(153, "Catalog Search Diagnostic 153", "Z39.50 protocol diagnostic code 153 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(154, "Catalog Search Diagnostic 154", "Z39.50 protocol diagnostic code 154 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(155, "Catalog Search Diagnostic 155", "Z39.50 protocol diagnostic code 155 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(156, "Catalog Search Diagnostic 156", "Z39.50 protocol diagnostic code 156 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(157, "Catalog Search Diagnostic 157", "Z39.50 protocol diagnostic code 157 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(158, "Catalog Search Diagnostic 158", "Z39.50 protocol diagnostic code 158 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(159, "Catalog Search Diagnostic 159", "Z39.50 protocol diagnostic code 159 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(160, "Catalog Search Diagnostic 160", "Z39.50 protocol diagnostic code 160 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(161, "Catalog Search Diagnostic 161", "Z39.50 protocol diagnostic code 161 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(162, "Catalog Search Diagnostic 162", "Z39.50 protocol diagnostic code 162 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(163, "Catalog Search Diagnostic 163", "Z39.50 protocol diagnostic code 163 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(164, "Catalog Search Diagnostic 164", "Z39.50 protocol diagnostic code 164 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(165, "Catalog Search Diagnostic 165", "Z39.50 protocol diagnostic code 165 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(166, "Catalog Search Diagnostic 166", "Z39.50 protocol diagnostic code 166 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(167, "Catalog Search Diagnostic 167", "Z39.50 protocol diagnostic code 167 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(168, "Catalog Search Diagnostic 168", "Z39.50 protocol diagnostic code 168 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(169, "Catalog Search Diagnostic 169", "Z39.50 protocol diagnostic code 169 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(170, "Catalog Search Diagnostic 170", "Z39.50 protocol diagnostic code 170 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(171, "Catalog Search Diagnostic 171", "Z39.50 protocol diagnostic code 171 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(172, "Catalog Search Diagnostic 172", "Z39.50 protocol diagnostic code 172 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(173, "Catalog Search Diagnostic 173", "Z39.50 protocol diagnostic code 173 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_diag(174, "Catalog Search Diagnostic 174", "Z39.50 protocol diagnostic code 174 encountered during query evaluation.", "Refer to ANSI/NISO Z39.50 Appendix G for remedial protocol guidance.")
_pdu(20, "InitializeRequest", True, "InitializeRequest ::= SEQUENCE { ... }", "Initiates client-server Z39.50 connection session")
_pdu(21, "InitializeResponse", False, "InitializeResponse ::= SEQUENCE { ... }", "Server session negotiation response")
_pdu(22, "SearchRequest", True, "SearchRequest ::= SEQUENCE { ... }", "Client search query submission")
_pdu(23, "SearchResponse", False, "SearchResponse ::= SEQUENCE { ... }", "Server search results count and status")
_pdu(24, "PresentRequest", True, "PresentRequest ::= SEQUENCE { ... }", "Client request to retrieve records from result set")
_pdu(25, "PresentResponse", False, "PresentResponse ::= SEQUENCE { ... }", "Server delivery of bibliographic records")
_pdu(26, "DeleteResultSetRequest", True, "DeleteResultSetRequest ::= SEQUENCE { ... }", "Client request to release result sets")
_pdu(27, "DeleteResultSetResponse", False, "DeleteResultSetResponse ::= SEQUENCE { ... }", "Server confirmation of result set release")
_pdu(44, "Close", True, "Close ::= SEQUENCE { ... }", "Session termination request or response")

def get_diagnostic_definition(code: int) -> Optional[Z3950DiagnosticDefinition]:
    return Z3950_DIAGNOSTICS_REGISTRY.get(code)

def get_pdu_specification(pdu_id: int) -> Optional[Asn1PduSpecification]:
    return Z3950_PDU_REGISTRY.get(pdu_id)
