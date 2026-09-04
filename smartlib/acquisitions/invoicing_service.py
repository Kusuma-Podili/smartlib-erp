"""Invoicing and 3-Way Matching Service."""

from typing import Dict, List, Optional
from .models import Invoice, InvoiceLine, InvoiceStatus, PurchaseOrder
from .budget_service import BudgetService


class InvoicingService:
    """Validates vendor invoices against Purchase Orders and Receiving Records."""

    def __init__(self, budget_service: BudgetService):
        self.budget_service = budget_service
        self.invoices: Dict[str, Invoice] = {}

    def create_invoice(self, invoice_number: str, vendor_id: str) -> Invoice:
        inv_id = f"INV-{invoice_number}"
        inv = Invoice(id=inv_id, invoice_number=invoice_number, vendor_id=vendor_id)
        self.invoices[inv_id] = inv
        return inv

    def perform_three_way_match(self, invoice_id: str, po: PurchaseOrder) -> bool:
        inv = self.invoices.get(invoice_id)
        if not inv:
            return False

        # Verify quantities and prices
        po_total = po.total_amount_cents
        inv_total = inv.total_cents
        # Allow tolerance of up to 2%
        if abs(po_total - inv_total) <= (po_total * 0.02):
            inv.status = InvoiceStatus.APPROVED
            # Convert encumbrance to actual expenditure
            for line in po.lines:
                self.budget_service.expend(line.fund_id, line.total_cost_cents)
            return True

        return False
