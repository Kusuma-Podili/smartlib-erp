"""Consortium Resource Sharing Routing and Balance-of-Trade Tracker."""

from typing import List, Dict, Optional
from .models import PartnerInstitution, IllRequest, IllRequestType, IllStatus


class ConsortiumRouter:
    """Selects optimal fulfillment partners based on reciprocal agreements and load."""

    def __init__(self):
        self.routing_priority_list: List[str] = []

    def set_priority(self, partner_ids: List[str]):
        self.routing_priority_list = partner_ids

    def select_next_supplier(self, attempted_partners: List[str]) -> Optional[str]:
        for p_id in self.routing_priority_list:
            if p_id not in attempted_partners:
                return p_id
        return None


class ReciprocalAgreementTracker:
    """Tracks lending vs borrowing ratios to ensure balanced consortium participation."""

    def __init__(self):
        self.borrowed_counts: Dict[str, int] = {}
        self.lent_counts: Dict[str, int] = {}

    def record_borrowed(self, partner_id: str):
        self.borrowed_counts[partner_id] = self.borrowed_counts.get(partner_id, 0) + 1

    def record_lent(self, partner_id: str):
        self.lent_counts[partner_id] = self.lent_counts.get(partner_id, 0) + 1

    def get_balance(self, partner_id: str) -> int:
        """Net balance: lent - borrowed (positive means net lender)."""
        return self.lent_counts.get(partner_id, 0) - self.borrowed_counts.get(partner_id, 0)
