"""ILL Service and State Transition Engine."""

from typing import Dict, List, Optional
import datetime
from .models import IllRequest, IllRequestType, IllServiceType, IllStatus, PartnerInstitution


class IllWorkflowEngine:
    """Enforces valid state transitions and audit trails for ILL lifecycles."""

    VALID_TRANSITIONS = {
        IllStatus.SUBMITTED: [IllStatus.VERIFIED, IllStatus.CANCELLED],
        IllStatus.VERIFIED: [IllStatus.LOCATING_SUPPLIER, IllStatus.CANCELLED],
        IllStatus.LOCATING_SUPPLIER: [IllStatus.REQUESTED_FROM_PARTNER, IllStatus.UNFILLED],
        IllStatus.REQUESTED_FROM_PARTNER: [IllStatus.ACCEPTED_BY_PARTNER, IllStatus.REJECTED_BY_PARTNER],
        IllStatus.REJECTED_BY_PARTNER: [IllStatus.LOCATING_SUPPLIER, IllStatus.UNFILLED],
        IllStatus.ACCEPTED_BY_PARTNER: [IllStatus.IN_TRANSIT_INBOUND, IllStatus.COMPLETED],
        IllStatus.IN_TRANSIT_INBOUND: [IllStatus.RECEIVED_AT_LIBRARY],
        IllStatus.RECEIVED_AT_LIBRARY: [IllStatus.READY_FOR_PATRON],
        IllStatus.READY_FOR_PATRON: [IllStatus.CHECKED_OUT_TO_PATRON, IllStatus.CANCELLED],
        IllStatus.CHECKED_OUT_TO_PATRON: [IllStatus.RETURNED_BY_PATRON],
        IllStatus.RETURNED_BY_PATRON: [IllStatus.IN_TRANSIT_OUTBOUND],
        IllStatus.IN_TRANSIT_OUTBOUND: [IllStatus.RETURNED_TO_PARTNER],
        IllStatus.RETURNED_TO_PARTNER: [IllStatus.COMPLETED],
    }

    @classmethod
    def can_transition(cls, current: IllStatus, target: IllStatus) -> bool:
        allowed = cls.VALID_TRANSITIONS.get(current, [])
        return target in allowed


class IllService:
    """High-level management service for Interlibrary Loan operations."""

    def __init__(self):
        self.requests: Dict[str, IllRequest] = {}
        self.partners: Dict[str, PartnerInstitution] = {}

    def register_partner(self, partner: PartnerInstitution):
        self.partners[partner.id] = partner

    def create_borrowing_request(self, patron_id: str, title: str, author: Optional[str] = None,
                                 isbn: Optional[str] = None, service_type: IllServiceType = IllServiceType.PHYSICAL_LOAN) -> IllRequest:
        req_id = f"ILL-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{len(self.requests)+1:03d}"
        req = IllRequest(
            id=req_id,
            request_type=IllRequestType.BORROWING,
            service_type=service_type,
            patron_id=patron_id,
            title=title,
            author=author,
            isbn=isbn
        )
        self.requests[req_id] = req
        return req

    def transition_status(self, request_id: str, new_status: IllStatus, note: Optional[str] = None) -> bool:
        req = self.requests.get(request_id)
        if not req:
            return False
        if not IllWorkflowEngine.can_transition(req.status, new_status):
            return False

        req.status = new_status
        req.updated_at = datetime.datetime.now()
        if note:
            req.notes.append(f"[{req.updated_at.isoformat()}] {note}")
        return True

    def mark_shipped_to_patron(self, request_id: str, tracking_number: str, carrier: str) -> bool:
        req = self.requests.get(request_id)
        if not req:
            return False
        req.tracking_number = tracking_number
        req.shipping_carrier = carrier
        return self.transition_status(request_id, IllStatus.IN_TRANSIT_INBOUND, f"Shipped via {carrier} (#{tracking_number})")

    def get_pending_borrowing_requests(self) -> List[IllRequest]:
        return [r for r in self.requests.values() if r.request_type == IllRequestType.BORROWING and not r.is_terminal()]

    def get_pending_lending_requests(self) -> List[IllRequest]:
        return [r for r in self.requests.values() if r.request_type == IllRequestType.LENDING and not r.is_terminal()]
