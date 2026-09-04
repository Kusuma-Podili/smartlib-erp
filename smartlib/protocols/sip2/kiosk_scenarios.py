"""SIP2 Self-Checkout Kiosk Simulation Workflows and Integration Test Scenarios."""

from typing import Dict, List, Any, Optional
import datetime
from .pdu import Sip2Message, format_sip2_message, parse_sip2_message
from .constants import (
    CMD_SC_STATUS_REQ, CMD_LOGIN_REQ, CMD_PATRON_STATUS_REQ,
    CMD_CHECKOUT_REQ, CMD_CHECKIN_REQ, CMD_FEE_PAID_REQ
)


class KioskWorkflowSimulator:
    """Simulates real-world patron self-check interactions with automated validation."""

    def __init__(self, server_handler):
        self.handler = server_handler
        self.session_log: List[Dict[str, str]] = []

    def simulate_startup_handshake(self, terminal_user: str, terminal_pwd: str) -> bool:
        """Step 1: 99 Status Request -> 98 Status Response, Step 2: 93 Login Request -> 94 Login Response."""
        req99 = Sip2Message(command=CMD_SC_STATUS_REQ, fixed_fields="000")
        resp98_str = self.handler.handle_message(format_sip2_message(req99))
        resp98 = parse_sip2_message(resp98_str)
        if resp98.command != "98":
            return False

        req93 = Sip2Message(command=CMD_LOGIN_REQ, fixed_fields="00")
        req93.add_field("CN", terminal_user)
        req93.add_field("CO", terminal_pwd)
        resp94_str = self.handler.handle_message(format_sip2_message(req93))
        resp94 = parse_sip2_message(resp94_str)
        return resp94.command == "94" and resp94.fixed_fields == "1"

    def simulate_patron_checkout(self, patron_id: str, item_barcodes: List[str]) -> List[Dict[str, Any]]:
        """Simulates complete checkout session for multiple items."""
        results = []
        for barcode in item_barcodes:
            req11 = Sip2Message(command=CMD_CHECKOUT_REQ, fixed_fields="SC20260904    12000020260918    235900")
            req11.add_field("AA", patron_id)
            req11.add_field("AB", barcode)
            resp_str = self.handler.handle_message(format_sip2_message(req11))
            resp12 = parse_sip2_message(resp_str)
            ok = resp12.fixed_fields.startswith("1")
            results.append({
                "barcode": barcode,
                "success": ok,
                "title": resp12.get_field("AJ") or "Unknown Title",
                "due_date": resp12.get_field("AH") or "2026-09-18"
            })
        return results
