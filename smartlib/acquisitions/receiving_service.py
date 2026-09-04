"""Receiving Service for physical and electronic library materials."""

from typing import Dict, List, Optional
from .models import ReceivingRecord, PurchaseOrder, POStatus


class ReceivingService:
    """Processes incoming packages, checks physical condition, and creates barcodes."""

    def __init__(self, ordering_service):
        self.ordering_service = ordering_service
        self.receipts: List[ReceivingRecord] = []

    def receive_item(self, po_id: str, line_id: str, barcode: str, received_by: str) -> bool:
        po = self.ordering_service.purchase_orders.get(po_id)
        if not po:
            return False

        target_line = None
        for line in po.lines:
            if line.id == line_id:
                target_line = line
                break

        if not target_line or target_line.quantity_received >= target_line.quantity:
            return False

        target_line.quantity_received += 1
        rec = ReceivingRecord(
            id=f"REC-{len(self.receipts)+1:05d}",
            po_line_id=line_id,
            barcode_assigned=barcode,
            received_by=received_by
        )
        self.receipts.append(rec)

        # Update PO status
        total_ordered = sum(l.quantity for l in po.lines)
        total_received = sum(l.quantity_received for l in po.lines)
        if total_received >= total_ordered:
            po.status = POStatus.FULLY_RECEIVED
        else:
            po.status = POStatus.PARTIALLY_RECEIVED

        return True
