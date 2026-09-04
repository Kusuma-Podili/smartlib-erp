"""SIP2 Server session handler for self-checkout kiosks and sorters."""

from typing import Optional, Dict, Any
import datetime
from .constants import (
    CMD_SC_STATUS_REQ, CMD_ACS_STATUS_RESP,
    CMD_LOGIN_REQ, CMD_LOGIN_RESP,
    CMD_PATRON_STATUS_REQ, CMD_PATRON_STATUS_RESP,
    CMD_PATRON_INFO_REQ, CMD_PATRON_INFO_RESP,
    CMD_CHECKOUT_REQ, CMD_CHECKOUT_RESP,
    CMD_CHECKIN_REQ, CMD_CHECKIN_RESP,
    CMD_FEE_PAID_REQ, CMD_FEE_PAID_RESP,
    FIELD_INSTITUTION_ID, FIELD_PATRON_ID, FIELD_ITEM_ID,
    FIELD_PERSONAL_NAME, FIELD_TITLE_ID, FIELD_SCREEN_MSG,
    FIELD_DUE_DATE, FIELD_FEE_AMOUNT, FIELD_CURRENCY_CODE
)
from .pdu import Sip2Message, format_sip2_timestamp, format_sip2_message, parse_sip2_message


class Sip2ServerHandler:
    """Processes incoming SIP2 client messages and routes to Library ERP services."""

    def __init__(self, institution_name: str = "SmartLib Central Library"):
        self.institution_name = institution_name
        self.authenticated_terminals: Dict[str, bool] = {}

    def handle_message(self, raw_str: str) -> str:
        """Route raw message to appropriate handler method."""
        try:
            req = parse_sip2_message(raw_str)
        except Exception as e:
            err_msg = Sip2Message(command="96").add_field(FIELD_SCREEN_MSG, f"Parse error: {str(e)}")
            return format_sip2_message(err_msg)

        cmd = req.command
        if cmd == CMD_SC_STATUS_REQ:
            resp = self._handle_sc_status(req)
        elif cmd == CMD_LOGIN_REQ:
            resp = self._handle_login(req)
        elif cmd == CMD_PATRON_STATUS_REQ or cmd == CMD_PATRON_INFO_REQ:
            resp = self._handle_patron_info(req)
        elif cmd == CMD_CHECKOUT_REQ:
            resp = self._handle_checkout(req)
        elif cmd == CMD_CHECKIN_REQ:
            resp = self._handle_checkin(req)
        elif cmd == CMD_FEE_PAID_REQ:
            resp = self._handle_fee_paid(req)
        else:
            resp = Sip2Message(command="96").add_field(FIELD_SCREEN_MSG, f"Unsupported command {cmd}")

        return format_sip2_message(resp)

    def _handle_sc_status(self, req: Sip2Message) -> Sip2Message:
        """ACS Status Response (98)."""
        # Fixed field: 1 char on-line status (Y), 1 char checkin ok (Y), 1 char checkout ok (Y),
        # 1 char ACS renewal ok (Y), 1 char status update ok (Y), 1 char offline ok (N),
        # 3 chars timeout (030), 3 chars retries (003), 18 chars date/time, 4 chars version (02.00)
        now_str = format_sip2_timestamp()
        fixed = f"YYYYYN030003{now_str}0200"
        resp = Sip2Message(command=CMD_ACS_STATUS_RESP, fixed_fields=fixed)
        resp.add_field(FIELD_INSTITUTION_ID, self.institution_name)
        resp.add_field(FIELD_SCREEN_MSG, "SmartLib SIP2 Server Online")
        return resp

    def _handle_login(self, req: Sip2Message) -> Sip2Message:
        """Login Response (94)."""
        resp = Sip2Message(command=CMD_LOGIN_RESP, fixed_fields="1")  # 1 = success
        resp.add_field(FIELD_SCREEN_MSG, "Authentication Successful")
        return resp

    def _handle_patron_info(self, req: Sip2Message) -> Sip2Message:
        """Patron Information Response (64)."""
        patron_id = req.get_field(FIELD_PATRON_ID) or "UNKNOWN"
        now_str = format_sip2_timestamp()
        # Fixed: 14 chars patron status flags, 2 chars language (000), 18 chars timestamp,
        # 4 chars hold items count, 4 chars overdue count, 4 chars charged count, 4 chars fine items,
        # 4 chars recall items, 4 chars unavailable hold items
        fixed = f"              000{now_str}000000000001000000000000"
        resp = Sip2Message(command=CMD_PATRON_INFO_RESP, fixed_fields=fixed)
        resp.add_field(FIELD_INSTITUTION_ID, self.institution_name)
        resp.add_field(FIELD_PATRON_ID, patron_id)
        resp.add_field(FIELD_PERSONAL_NAME, "Patron John Doe")
        resp.add_field(FIELD_SCREEN_MSG, "Account Active - Good Standing")
        return resp

    def _handle_checkout(self, req: Sip2Message) -> Sip2Message:
        """Checkout Response (12)."""
        patron_id = req.get_field(FIELD_PATRON_ID) or ""
        item_id = req.get_field(FIELD_ITEM_ID) or ""
        now_str = format_sip2_timestamp()
        due_date = (datetime.datetime.now() + datetime.timedelta(days=14)).strftime("%Y%m%d    235900")
        # Fixed: 1 char ok (1), 1 char renewal ok (N), 1 char magnetic media (N), 1 char desensitize (Y),
        # 18 chars timestamp
        fixed = f"1NNY{now_str}"
        resp = Sip2Message(command=CMD_CHECKOUT_RESP, fixed_fields=fixed)
        resp.add_field(FIELD_INSTITUTION_ID, self.institution_name)
        resp.add_field(FIELD_PATRON_ID, patron_id)
        resp.add_field(FIELD_ITEM_ID, item_id)
        resp.add_field(FIELD_TITLE_ID, "Clean Code: A Handbook of Agile Software Craftsmanship")
        resp.add_field(FIELD_DUE_DATE, due_date)
        resp.add_field(FIELD_SCREEN_MSG, "Item checked out successfully")
        return resp

    def _handle_checkin(self, req: Sip2Message) -> Sip2Message:
        """Checkin Response (10)."""
        item_id = req.get_field(FIELD_ITEM_ID) or ""
        now_str = format_sip2_timestamp()
        # Fixed: 1 char ok (1), 1 char resensitize (Y), 1 char magnetic media (N), 1 char alert (N),
        # 18 chars timestamp
        fixed = f"1YNN{now_str}"
        resp = Sip2Message(command=CMD_CHECKIN_RESP, fixed_fields=fixed)
        resp.add_field(FIELD_INSTITUTION_ID, self.institution_name)
        resp.add_field(FIELD_ITEM_ID, item_id)
        resp.add_field(FIELD_TITLE_ID, "Clean Code: A Handbook of Agile Software Craftsmanship")
        resp.add_field(FIELD_SCREEN_MSG, "Item checked in - Return to General Stacks")
        return resp

    def _handle_fee_paid(self, req: Sip2Message) -> Sip2Message:
        """Fee Paid Response (38)."""
        patron_id = req.get_field(FIELD_PATRON_ID) or ""
        fee_amt = req.get_field(FIELD_FEE_AMOUNT) or "0.00"
        now_str = format_sip2_timestamp()
        # Fixed: 1 char payment accepted (Y), 18 chars timestamp
        fixed = f"Y{now_str}"
        resp = Sip2Message(command=CMD_FEE_PAID_RESP, fixed_fields=fixed)
        resp.add_field(FIELD_INSTITUTION_ID, self.institution_name)
        resp.add_field(FIELD_PATRON_ID, patron_id)
        resp.add_field(FIELD_FEE_AMOUNT, fee_amt)
        resp.add_field(FIELD_CURRENCY_CODE, "INR")
        resp.add_field(FIELD_SCREEN_MSG, "Fine payment recorded successfully")
        return resp


class Sip2ServerSession:
    """Manages state for an open client connection."""

    def __init__(self, handler: Sip2ServerHandler):
        self.handler = handler
        self.sequence_num = 1

    def process_incoming(self, raw_data: str) -> str:
        return self.handler.handle_message(raw_data)
