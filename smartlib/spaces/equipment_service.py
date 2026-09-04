"""Equipment Checkout and Inspection Service."""

from typing import List, Dict, Optional
import datetime
from .models import EquipmentItem, EquipmentLoan, EquipmentCategory


class EquipmentCheckoutService:
    """Manages tech lending desks (laptops, cameras, projectors)."""

    def __init__(self):
        self.items: Dict[str, EquipmentItem] = {}
        self.loans: List[EquipmentLoan] = []

    def add_item(self, item: EquipmentItem):
        self.items[item.id] = item

    def checkout_equipment(self, item_id: str, patron_id: str, loan_hours: int = 4) -> Optional[EquipmentLoan]:
        item = self.items.get(item_id)
        if not item or item.is_checked_out:
            return None

        now = datetime.datetime.now()
        due = now + datetime.timedelta(hours=loan_hours)
        loan = EquipmentLoan(
            id=f"EQ-LOAN-{len(self.loans)+1:05d}",
            equipment_id=item_id,
            patron_id=patron_id,
            loaned_at=now,
            due_at=due,
            accessories_included=["Power Adapter", "Carrying Sleeve"]
        )
        item.is_checked_out = True
        self.loans.append(loan)
        return loan

    def checkin_equipment(self, loan_id: str, condition_notes: str = "Good") -> bool:
        loan = next((l for l in self.loans if l.id == loan_id), None)
        if not loan or loan.returned_at:
            return False

        loan.returned_at = datetime.datetime.now()
        item = self.items.get(loan.equipment_id)
        if item:
            item.is_checked_out = False
        return True
