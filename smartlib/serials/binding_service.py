"""Serials Bindery Preparation and Shipment Tracker."""

from typing import List, Dict, Optional
import datetime
from .models import BindingUnit, IssueStatus, IssueInstance


class SerialsBindingService:
    """Collates completed journal volumes for bindery shipments."""

    def __init__(self, checkin_service):
        self.checkin_service = checkin_service
        self.binding_units: Dict[str, BindingUnit] = {}

    def assemble_binding_unit(self, subscription_id: str, title: str, volume: str, issue_ids: List[str]) -> BindingUnit:
        unit_id = f"BIND-{subscription_id}-V{volume}"
        spine = f"{title} Vol. {volume}"
        unit = BindingUnit(
            id=unit_id,
            subscription_id=subscription_id,
            title=title,
            volume=volume,
            issues_included=issue_ids,
            spine_title=spine
        )
        # Mark issues as bound
        for i_id in issue_ids:
            iss = self.checkin_service.issues.get(i_id)
            if iss:
                iss.status = IssueStatus.BOUND

        self.binding_units[unit_id] = unit
        return unit
