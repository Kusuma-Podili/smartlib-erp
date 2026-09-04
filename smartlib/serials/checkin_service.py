"""Serials Rapid Check-In Desk and Routing List Processor."""

from typing import Dict, Optional, List
import datetime
from .models import IssueInstance, IssueStatus, RoutingList


class SerialsCheckinService:
    """Manages physical receipt of serial issues and generates routing slips."""

    def __init__(self):
        self.issues: Dict[str, IssueInstance] = {}
        self.routing_lists: Dict[str, RoutingList] = {}

    def register_issues(self, issue_list: List[IssueInstance]):
        for iss in issue_list:
            self.issues[iss.id] = iss

    def checkin_issue(self, issue_id: str, barcode: str) -> bool:
        iss = self.issues.get(issue_id)
        if not iss:
            return False
        iss.status = IssueStatus.ARRIVED
        iss.arrived_date = datetime.date.today()
        iss.barcode = barcode
        return True

    def generate_routing_slip(self, subscription_id: str, issue_id: str) -> Optional[str]:
        iss = self.issues.get(issue_id)
        rl = self.routing_lists.get(subscription_id)
        if not iss or not rl or not rl.recipient_patron_ids:
            return None

        lines = [
            "========================================",
            "        SERIAL ROUTING SLIP             ",
            "========================================",
            f"Issue: {iss.enumeration} ({iss.chronology})",
            f"Date Checked In: {iss.arrived_date}",
            "Please read and forward to next recipient:",
        ]
        for idx, patron in enumerate(rl.recipient_patron_ids, start=1):
            lines.append(f"  [ ] {idx}. Patron #{patron}")
        lines.append("Return to Library Periodicals Desk when done.")
        lines.append("========================================")
        return "\n".join(lines)
