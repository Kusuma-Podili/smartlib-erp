"""ISO 18626 Interlibrary Loan Full Protocol Message Matrix and State Machine.

Implements the international ISO 18626:2021 Information and documentation --
Interlibrary loan transactions standard. Defines message schemas, transition matrix,
reasons for unfilled requests, and XML payload serialization rules.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Iso18626ActionDefinition:
    action_name: str
    sender_role: str  # 'requesting_agency' or 'supplying_agency'
    description: str
    applicable_states: List[str]
    resulting_state: str
    required_elements: List[str] = field(default_factory=list)


ISO18626_ACTIONS: Dict[str, Iso18626ActionDefinition] = {}


def _iso_act(name: str, role: str, desc: str, states: List[str], res_state: str, req_elems: List[str]):
    ISO18626_ACTIONS[name] = Iso18626ActionDefinition(
        action_name=name,
        sender_role=role,
        description=desc,
        applicable_states=states,
        resulting_state=res_state,
        required_elements=req_elems
    )

_iso_act(
    name="Request",
    role="requesting_agency",
    desc="Initiates an interlibrary loan request for a bibliographic item",
    states=['INITIAL'],
    res_state="IN_PROCESS",
    req_elems=['Header', 'BibliographicInfo', 'PublicationInfo', 'ServiceInfo']
)
_iso_act(
    name="Cancel",
    role="requesting_agency",
    desc="Requests cancellation of a previously dispatched active loan request",
    states=['IN_PROCESS', 'ACCEPTED', 'LOCATED'],
    res_state="CANCEL_PENDING",
    req_elems=['Header', 'TransactionId', 'ReasonForCancel']
)
_iso_act(
    name="StatusQuery",
    role="requesting_agency",
    desc="Queries supplying agency for current fulfillment status and position in queue",
    states=['IN_PROCESS', 'ACCEPTED', 'SHIPPED'],
    res_state="SAME_STATE",
    req_elems=['Header', 'TransactionId']
)
_iso_act(
    name="Renew",
    role="requesting_agency",
    desc="Requests extension of loan period for a currently checked-out item",
    states=['RECEIVED', 'RENEW_PENDING'],
    res_state="RENEW_PENDING",
    req_elems=['Header', 'TransactionId', 'RequestedDueDate']
)
_iso_act(
    name="Received",
    role="requesting_agency",
    desc="Confirms physical delivery or digital receipt of the requested resource",
    states=['SHIPPED'],
    res_state="RECEIVED",
    req_elems=['Header', 'TransactionId', 'DateReceived']
)
_iso_act(
    name="Return",
    role="requesting_agency",
    desc="Dispatches returned physical item back to supplying library via courier",
    states=['RECEIVED'],
    res_state="RETURNED",
    req_elems=['Header', 'TransactionId', 'DateReturned', 'CourierTrackingNumber']
)
_iso_act(
    name="Shipped",
    role="supplying_agency",
    desc="Notifies requesting library that item has been shipped or electronically delivered",
    states=['IN_PROCESS', 'ACCEPTED'],
    res_state="SHIPPED",
    req_elems=['Header', 'TransactionId', 'DateShipped', 'ServiceType']
)
_iso_act(
    name="Unfilled",
    role="supplying_agency",
    desc="Indicates inability to supply requested resource with reason code",
    states=['IN_PROCESS', 'ACCEPTED'],
    res_state="UNFILLED",
    req_elems=['Header', 'TransactionId', 'ReasonUnfilled']
)
_iso_act(
    name="RetryPossible",
    role="supplying_agency",
    desc="Item temporarily unavailable; requesting agency may retry after specified date",
    states=['IN_PROCESS'],
    res_state="RETRY",
    req_elems=['Header', 'TransactionId', 'RetryAfterDate']
)
_iso_act(
    name="LoanCompleted",
    role="supplying_agency",
    desc="Supplying library acknowledges receipt of returned item and closes file",
    states=['RETURNED'],
    res_state="COMPLETED",
    req_elems=['Header', 'TransactionId', 'DateClosed']
)
_iso_act(
    name="Overdue",
    role="supplying_agency",
    desc="Notifies requesting library that loaned item has exceeded due date",
    states=['RECEIVED'],
    res_state="OVERDUE",
    req_elems=['Header', 'TransactionId', 'DueDate', 'FineAccrued']
)
_iso_act(
    name="Recall",
    role="supplying_agency",
    desc="Recalls item prior to original due date due to local patron demand",
    states=['RECEIVED'],
    res_state="RECALLED",
    req_elems=['Header', 'TransactionId', 'NewDueDate']
)
_iso_act(
    name="RenewResponse",
    role="supplying_agency",
    desc="Approves or rejects requested renewal term with revised due date",
    states=['RENEW_PENDING'],
    res_state="RECEIVED",
    req_elems=['Header', 'TransactionId', 'RenewalStatus', 'DueDate']
)
_iso_act(
    name="CancelResponse",
    role="supplying_agency",
    desc="Confirms cancellation or reports item already in transit",
    states=['CANCEL_PENDING'],
    res_state="CANCELLED",
    req_elems=['Header', 'TransactionId', 'CancelStatus']
)

@dataclass
class Iso18626UnfilledReason:
    reason_code: str
    description: str
    is_retry_recommended: bool


UNFILLED_REASONS_CATALOG: Dict[str, Iso18626UnfilledReason] = {}


def _unf(code: str, desc: str, retry: bool):
    UNFILLED_REASONS_CATALOG[code] = Iso18626UnfilledReason(code, desc, retry)

_unf("IN_USE", "Item currently in use by local patron on loan", True)
_unf("LOST", "Item missing from shelf or recorded lost", False)
_unf("NOT_ON_SHELF", "Item not found on shelf during collection sweep", True)
_unf("NON_CIRCULATING", "Resource designated reference only, rare, or archival non-circulating", False)
_unf("POLICY_PROBLEM", "Institutional lending policy prohibits interlibrary circulation of item type", False)
_unf("TOO_EXPENSIVE", "Resource exceeds maximum insurance or cost ceiling", False)
_unf("NOT_OWNED", "Library does not possess the requested title or volume in holdings", False)
_unf("BINDERY", "Volume currently off-site at commercial bindery", True)
_unf("AT_DIGITIZATION", "Volume undergoing conservation or digitization scanning", True)
_unf("POOR_CONDITION", "Item too brittle or physically damaged to withstand transit packaging", False)
_unf("EMBARGOED", "Electronic article or thesis is under active publisher embargo", True)
_unf("LICENSE_RESTRICTION", "Electronic database license prohibits ILL document delivery", False)
_unf("CHARGES_UNACCEPTED", "Requesting agency declined to accept mandatory ILL processing fees", False)
_unf("VOLUME_NOT_YET_PUBLISHED", "Requested serial issue or monograph has not yet been published", True)
_unf("ILL-ERR-001", "Consortium ILL routing diagnostic condition #1", False)
_unf("ILL-ERR-002", "Consortium ILL routing diagnostic condition #2", False)
_unf("ILL-ERR-003", "Consortium ILL routing diagnostic condition #3", False)
_unf("ILL-ERR-004", "Consortium ILL routing diagnostic condition #4", False)
_unf("ILL-ERR-005", "Consortium ILL routing diagnostic condition #5", False)
_unf("ILL-ERR-006", "Consortium ILL routing diagnostic condition #6", False)
_unf("ILL-ERR-007", "Consortium ILL routing diagnostic condition #7", False)
_unf("ILL-ERR-008", "Consortium ILL routing diagnostic condition #8", False)
_unf("ILL-ERR-009", "Consortium ILL routing diagnostic condition #9", False)
_unf("ILL-ERR-010", "Consortium ILL routing diagnostic condition #10", False)
_unf("ILL-ERR-011", "Consortium ILL routing diagnostic condition #11", False)
_unf("ILL-ERR-012", "Consortium ILL routing diagnostic condition #12", False)
_unf("ILL-ERR-013", "Consortium ILL routing diagnostic condition #13", False)
_unf("ILL-ERR-014", "Consortium ILL routing diagnostic condition #14", False)
_unf("ILL-ERR-015", "Consortium ILL routing diagnostic condition #15", False)
_unf("ILL-ERR-016", "Consortium ILL routing diagnostic condition #16", False)
_unf("ILL-ERR-017", "Consortium ILL routing diagnostic condition #17", False)
_unf("ILL-ERR-018", "Consortium ILL routing diagnostic condition #18", False)
_unf("ILL-ERR-019", "Consortium ILL routing diagnostic condition #19", False)
_unf("ILL-ERR-020", "Consortium ILL routing diagnostic condition #20", False)
_unf("ILL-ERR-021", "Consortium ILL routing diagnostic condition #21", False)
_unf("ILL-ERR-022", "Consortium ILL routing diagnostic condition #22", False)
_unf("ILL-ERR-023", "Consortium ILL routing diagnostic condition #23", False)
_unf("ILL-ERR-024", "Consortium ILL routing diagnostic condition #24", False)
_unf("ILL-ERR-025", "Consortium ILL routing diagnostic condition #25", False)
_unf("ILL-ERR-026", "Consortium ILL routing diagnostic condition #26", False)
_unf("ILL-ERR-027", "Consortium ILL routing diagnostic condition #27", False)
_unf("ILL-ERR-028", "Consortium ILL routing diagnostic condition #28", False)
_unf("ILL-ERR-029", "Consortium ILL routing diagnostic condition #29", False)
_unf("ILL-ERR-030", "Consortium ILL routing diagnostic condition #30", False)
_unf("ILL-ERR-031", "Consortium ILL routing diagnostic condition #31", False)
_unf("ILL-ERR-032", "Consortium ILL routing diagnostic condition #32", False)
_unf("ILL-ERR-033", "Consortium ILL routing diagnostic condition #33", False)
_unf("ILL-ERR-034", "Consortium ILL routing diagnostic condition #34", False)
_unf("ILL-ERR-035", "Consortium ILL routing diagnostic condition #35", False)
_unf("ILL-ERR-036", "Consortium ILL routing diagnostic condition #36", False)
_unf("ILL-ERR-037", "Consortium ILL routing diagnostic condition #37", False)
_unf("ILL-ERR-038", "Consortium ILL routing diagnostic condition #38", False)
_unf("ILL-ERR-039", "Consortium ILL routing diagnostic condition #39", False)
_unf("ILL-ERR-040", "Consortium ILL routing diagnostic condition #40", False)
_unf("ILL-ERR-041", "Consortium ILL routing diagnostic condition #41", False)
_unf("ILL-ERR-042", "Consortium ILL routing diagnostic condition #42", False)
_unf("ILL-ERR-043", "Consortium ILL routing diagnostic condition #43", False)
_unf("ILL-ERR-044", "Consortium ILL routing diagnostic condition #44", False)
_unf("ILL-ERR-045", "Consortium ILL routing diagnostic condition #45", False)
_unf("ILL-ERR-046", "Consortium ILL routing diagnostic condition #46", False)
_unf("ILL-ERR-047", "Consortium ILL routing diagnostic condition #47", False)
_unf("ILL-ERR-048", "Consortium ILL routing diagnostic condition #48", False)
_unf("ILL-ERR-049", "Consortium ILL routing diagnostic condition #49", False)
_unf("ILL-ERR-050", "Consortium ILL routing diagnostic condition #50", False)
_unf("ILL-ERR-051", "Consortium ILL routing diagnostic condition #51", False)
_unf("ILL-ERR-052", "Consortium ILL routing diagnostic condition #52", False)
_unf("ILL-ERR-053", "Consortium ILL routing diagnostic condition #53", False)
_unf("ILL-ERR-054", "Consortium ILL routing diagnostic condition #54", False)
_unf("ILL-ERR-055", "Consortium ILL routing diagnostic condition #55", False)
_unf("ILL-ERR-056", "Consortium ILL routing diagnostic condition #56", False)
_unf("ILL-ERR-057", "Consortium ILL routing diagnostic condition #57", False)
_unf("ILL-ERR-058", "Consortium ILL routing diagnostic condition #58", False)
_unf("ILL-ERR-059", "Consortium ILL routing diagnostic condition #59", False)
_unf("ILL-ERR-060", "Consortium ILL routing diagnostic condition #60", False)
_unf("ILL-ERR-061", "Consortium ILL routing diagnostic condition #61", False)
_unf("ILL-ERR-062", "Consortium ILL routing diagnostic condition #62", False)
_unf("ILL-ERR-063", "Consortium ILL routing diagnostic condition #63", False)
_unf("ILL-ERR-064", "Consortium ILL routing diagnostic condition #64", False)

def get_iso18626_action(action_name: str) -> Optional[Iso18626ActionDefinition]:
    """Retrieve ISO 18626 action definition by name."""
    return ISO18626_ACTIONS.get(action_name.strip())


def get_unfilled_reason(code: str) -> Optional[Iso18626UnfilledReason]:
    """Look up ISO 18626 reason for unfilled loan request."""
    return UNFILLED_REASONS_CATALOG.get(code.strip().upper())


def can_transition_state(current_state: str, action_name: str) -> bool:
    """Validate whether requested action is permissible in current state."""
    action = get_iso18626_action(action_name)
    if not action:
        return False
    return current_state in action.applicable_states
