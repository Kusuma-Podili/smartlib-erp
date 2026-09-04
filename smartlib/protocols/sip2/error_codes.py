"""3M SIP2 Standard Diagnostic and Hardware Error Code Reference Table.

Defines kiosk error conditions, peripheral hardware alert codes, and recovery procedures.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Sip2ErrorCodeDefinition:
    error_code: str
    subsystem: str
    title: str
    screen_message: str
    remedy_action: str


SIP2_ERROR_REGISTRY: Dict[str, Sip2ErrorCodeDefinition] = {}

def _err(code: str, sub: str, title: str, msg: str, rem: str):
    SIP2_ERROR_REGISTRY[code] = Sip2ErrorCodeDefinition(code, sub, title, msg, rem)

_err("ERR-001", "Hardware", "Thermal Printer Out of Paper", "Receipt printer out of paper. Please contact library staff.", "Refill 80mm thermal paper roll in kiosk compartment")
_err("ERR-002", "Hardware", "Barcode Scanner Read Timeout", "Unable to read item barcode. Please reposition item under laser.", "Align barcode parallel to scan window at 10-15cm distance")
_err("ERR-003", "Hardware", "Desensitizer Deactivation Fault", "Magnetic security strip not deactivated. Item cannot leave desk.", "Re-pass item spine through deactivation coil")
_err("ERR-004", "Security", "RFID Security Gate Tamper Alert", "Security gate EAS transponder alarm triggered.", "Verify patron checkout receipt at circulation desk")
_err("ERR-005", "Protocol", "SIP2 Checksum LRC / CRC Mismatch", "Communication packet checksum verification failed.", "Resend command packet with valid calculated checksum")
_err("ERR-006", "Protocol", "Sequence Number Out of Sequence", "Client message sequence counter does not match ACS state.", "Synchronize sequence counter via 97 request SC resend")
_err("ERR-007", "Circulation", "Patron Borrowing Limit Exceeded", "Patron has reached maximum allowable concurrent loans.", "Patron must return items before borrowing additional titles")
_err("ERR-008", "Circulation", "Patron Card Suspended / Blocked", "Borrowing privileges suspended due to delinquent dues.", "Settle outstanding fines at cashiering desk")
_err("ERR-009", "Circulation", "Item Has Active Hold for Another Patron", "Item is reserved by another member. Cannot be checked out.", "Transfer item to hold shelf for designated recipient")
_err("ERR-010", "Circulation", "Non-Circulating Reference Material", "Item is non-circulating. Library use only.", "Return item to reference stacks")
_err("ERR-011", "Automated Handling", "Sorter Lane #11 Jam Alert", "Conveyor transport jam detected at bin #11.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-012", "Automated Handling", "Sorter Lane #12 Jam Alert", "Conveyor transport jam detected at bin #12.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-013", "Automated Handling", "Sorter Lane #13 Jam Alert", "Conveyor transport jam detected at bin #13.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-014", "Automated Handling", "Sorter Lane #14 Jam Alert", "Conveyor transport jam detected at bin #14.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-015", "Automated Handling", "Sorter Lane #15 Jam Alert", "Conveyor transport jam detected at bin #15.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-016", "Automated Handling", "Sorter Lane #16 Jam Alert", "Conveyor transport jam detected at bin #16.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-017", "Automated Handling", "Sorter Lane #17 Jam Alert", "Conveyor transport jam detected at bin #17.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-018", "Automated Handling", "Sorter Lane #18 Jam Alert", "Conveyor transport jam detected at bin #18.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-019", "Automated Handling", "Sorter Lane #19 Jam Alert", "Conveyor transport jam detected at bin #19.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-020", "Automated Handling", "Sorter Lane #20 Jam Alert", "Conveyor transport jam detected at bin #20.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-021", "Automated Handling", "Sorter Lane #21 Jam Alert", "Conveyor transport jam detected at bin #21.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-022", "Automated Handling", "Sorter Lane #22 Jam Alert", "Conveyor transport jam detected at bin #22.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-023", "Automated Handling", "Sorter Lane #23 Jam Alert", "Conveyor transport jam detected at bin #23.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-024", "Automated Handling", "Sorter Lane #24 Jam Alert", "Conveyor transport jam detected at bin #24.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-025", "Automated Handling", "Sorter Lane #25 Jam Alert", "Conveyor transport jam detected at bin #25.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-026", "Automated Handling", "Sorter Lane #26 Jam Alert", "Conveyor transport jam detected at bin #26.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-027", "Automated Handling", "Sorter Lane #27 Jam Alert", "Conveyor transport jam detected at bin #27.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-028", "Automated Handling", "Sorter Lane #28 Jam Alert", "Conveyor transport jam detected at bin #28.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-029", "Automated Handling", "Sorter Lane #29 Jam Alert", "Conveyor transport jam detected at bin #29.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-030", "Automated Handling", "Sorter Lane #30 Jam Alert", "Conveyor transport jam detected at bin #30.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-031", "Automated Handling", "Sorter Lane #31 Jam Alert", "Conveyor transport jam detected at bin #31.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-032", "Automated Handling", "Sorter Lane #32 Jam Alert", "Conveyor transport jam detected at bin #32.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-033", "Automated Handling", "Sorter Lane #33 Jam Alert", "Conveyor transport jam detected at bin #33.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-034", "Automated Handling", "Sorter Lane #34 Jam Alert", "Conveyor transport jam detected at bin #34.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-035", "Automated Handling", "Sorter Lane #35 Jam Alert", "Conveyor transport jam detected at bin #35.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-036", "Automated Handling", "Sorter Lane #36 Jam Alert", "Conveyor transport jam detected at bin #36.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-037", "Automated Handling", "Sorter Lane #37 Jam Alert", "Conveyor transport jam detected at bin #37.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-038", "Automated Handling", "Sorter Lane #38 Jam Alert", "Conveyor transport jam detected at bin #38.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-039", "Automated Handling", "Sorter Lane #39 Jam Alert", "Conveyor transport jam detected at bin #39.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-040", "Automated Handling", "Sorter Lane #40 Jam Alert", "Conveyor transport jam detected at bin #40.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-041", "Automated Handling", "Sorter Lane #41 Jam Alert", "Conveyor transport jam detected at bin #41.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-042", "Automated Handling", "Sorter Lane #42 Jam Alert", "Conveyor transport jam detected at bin #42.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-043", "Automated Handling", "Sorter Lane #43 Jam Alert", "Conveyor transport jam detected at bin #43.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-044", "Automated Handling", "Sorter Lane #44 Jam Alert", "Conveyor transport jam detected at bin #44.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-045", "Automated Handling", "Sorter Lane #45 Jam Alert", "Conveyor transport jam detected at bin #45.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-046", "Automated Handling", "Sorter Lane #46 Jam Alert", "Conveyor transport jam detected at bin #46.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-047", "Automated Handling", "Sorter Lane #47 Jam Alert", "Conveyor transport jam detected at bin #47.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-048", "Automated Handling", "Sorter Lane #48 Jam Alert", "Conveyor transport jam detected at bin #48.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-049", "Automated Handling", "Sorter Lane #49 Jam Alert", "Conveyor transport jam detected at bin #49.", "Clear physical jam and reset bin sorter interlock.")
_err("ERR-050", "Automated Handling", "Sorter Lane #50 Jam Alert", "Conveyor transport jam detected at bin #50.", "Clear physical jam and reset bin sorter interlock.")

def lookup_sip2_error(code: str) -> Optional[Sip2ErrorCodeDefinition]:
    return SIP2_ERROR_REGISTRY.get(code.strip().upper())
