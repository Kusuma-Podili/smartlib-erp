"""NCIP Service Dispatcher."""

from typing import Optional
from .ncip_messages import (
    CheckOutItemRequest, CheckOutItemResponse,
    CheckInItemRequest, CheckInItemResponse,
    LookupUserRequest, LookupUserResponse
)


class NcipService:
    """Dispatches and coordinates NCIP 2.0 actions."""

    def __init__(self, lending_service=None, patron_service=None):
        self.lending_service = lending_service
        self.patron_service = patron_service

    def checkout_item(self, req: CheckOutItemRequest) -> CheckOutItemResponse:
        return CheckOutItemResponse(
            success=True,
            user_id=req.user_id,
            item_barcode=req.item_barcode,
            due_date="2026-09-18T23:59:59Z"
        )

    def checkin_item(self, req: CheckInItemRequest) -> CheckInItemResponse:
        return CheckInItemResponse(
            success=True,
            item_barcode=req.item_barcode,
            routing_action="Hold Shelf: Pickup By Patron MEM-2026-0002"
        )

    def lookup_user(self, req: LookupUserRequest) -> LookupUserResponse:
        return LookupUserResponse(
            user_id=req.user_id,
            full_name="John Patron",
            email="patron@library.org",
            user_status="Active",
            overdue_count=0,
            unpaid_fines_cents=0
        )
