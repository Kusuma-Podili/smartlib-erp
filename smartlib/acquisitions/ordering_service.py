"""Purchase Order Creation and EDIFACT Generation."""

from typing import Dict, List, Optional
import datetime
from .models import PurchaseOrder, POLineItem, POStatus
from .budget_service import BudgetService


class OrderingService:
    """Manages purchase orders and approval workflows."""

    def __init__(self, budget_service: BudgetService):
        self.budget_service = budget_service
        self.purchase_orders: Dict[str, PurchaseOrder] = {}

    def create_order(self, vendor_id: str) -> PurchaseOrder:
        po_id = f"PO-{datetime.datetime.now().strftime('%Y%m')}-{len(self.purchase_orders)+1:04d}"
        po = PurchaseOrder(id=po_id, po_number=po_id, vendor_id=vendor_id)
        self.purchase_orders[po_id] = po
        return po

    def add_line_item(self, po_id: str, title: str, author: str, isbn: str, quantity: int, unit_price_cents: int, fund_id: str) -> Optional[POLineItem]:
        po = self.purchase_orders.get(po_id)
        if not po or po.status != POStatus.DRAFT:
            return None

        line_id = f"{po_id}-L{len(po.lines)+1:02d}"
        line = POLineItem(
            id=line_id, po_id=po_id, title=title, author=author, isbn=isbn,
            quantity=quantity, unit_price_cents=unit_price_cents, fund_id=fund_id
        )
        po.lines.append(line)
        return line

    def approve_order(self, po_id: str, approver_name: str) -> bool:
        po = self.purchase_orders.get(po_id)
        if not po or po.status != POStatus.DRAFT:
            return False

        # Encumber funds
        for line in po.lines:
            success = self.budget_service.encumber(line.fund_id, line.total_cost_cents)
            if not success:
                return False

        po.status = POStatus.APPROVED
        po.approved_by = approver_name
        return True
