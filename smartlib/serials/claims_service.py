"""Serials Automatic Overdue Issue Claiming Service."""

from typing import List, Dict
import datetime
from .models import IssueInstance, IssueStatus, ClaimNotice


class SerialsClaimsService:
    """Detects missing periodical issues and generates claims for vendors."""

    def __init__(self, checkin_service):
        self.checkin_service = checkin_service
        self.claims: List[ClaimNotice] = []

    def scan_for_overdue_issues(self, grace_days: int = 14) -> List[IssueInstance]:
        today = datetime.date.today()
        overdue = []
        for iss in self.checkin_service.issues.values():
            if iss.status == IssueStatus.EXPECTED:
                if (today - iss.expected_date).days > grace_days:
                    iss.status = IssueStatus.LATE
                    overdue.append(iss)
        return overdue

    def file_claim(self, issue_id: str, vendor_id: str) -> ClaimNotice:
        iss = self.checkin_service.issues.get(issue_id)
        if iss:
            iss.status = IssueStatus.CLAIMED
        claim = ClaimNotice(
            id=f"CLM-{len(self.claims)+1:05d}",
            issue_id=issue_id,
            vendor_id=vendor_id
        )
        self.claims.append(claim)
        return claim
