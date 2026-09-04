"""SIP2 Client for self-check kiosks, sorters, and integration testing."""

import socket
from typing import Optional
from .pdu import Sip2Message, format_sip2_message, parse_sip2_message, format_sip2_timestamp
from .constants import (
    CMD_SC_STATUS_REQ, CMD_LOGIN_REQ, CMD_PATRON_INFO_REQ,
    CMD_CHECKOUT_REQ, CMD_CHECKIN_REQ,
    FIELD_INSTITUTION_ID, FIELD_PATRON_ID, FIELD_ITEM_ID,
    FIELD_TERMINAL_LOCATION
)


class Sip2Client:
    """Client for connecting to SIP2 automated materials servers."""

    def __init__(self, host: str = "127.0.0.1", port: int = 6001, institution: str = "SmartLib"):
        self.host = host
        self.port = port
        self.institution = institution
        self._sock: Optional[socket.socket] = None

    def connect(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self.host, self.port))

    def disconnect(self):
        if self._sock:
            self._sock.close()
            self._sock = None

    def send_and_receive(self, msg: Sip2Message) -> Sip2Message:
        if not self._sock:
            raise RuntimeError("Client not connected")
        payload = format_sip2_message(msg).encode("utf-8")
        self._sock.sendall(payload)
        resp_bytes = self._sock.recv(4096)
        return parse_sip2_message(resp_bytes.decode("utf-8", errors="replace"))

    def check_status(self) -> Sip2Message:
        """Send 99 Status Request."""
        msg = Sip2Message(command=CMD_SC_STATUS_REQ, fixed_fields="000")
        return self.send_and_receive(msg)

    def checkout_item(self, patron_id: str, item_barcode: str) -> Sip2Message:
        """Send 11 Checkout Request."""
        now_str = format_sip2_timestamp()
        fixed = f"SC{now_str}{now_str}"
        msg = Sip2Message(command=CMD_CHECKOUT_REQ, fixed_fields=fixed)
        msg.add_field(FIELD_INSTITUTION_ID, self.institution)
        msg.add_field(FIELD_PATRON_ID, patron_id)
        msg.add_field(FIELD_ITEM_ID, item_barcode)
        return self.send_and_receive(msg)

    def checkin_item(self, item_barcode: str) -> Sip2Message:
        """Send 09 Checkin Request."""
        now_str = format_sip2_timestamp()
        fixed = f"N{now_str}{now_str}"
        msg = Sip2Message(command=CMD_CHECKIN_REQ, fixed_fields=fixed)
        msg.add_field(FIELD_INSTITUTION_ID, self.institution)
        msg.add_field(FIELD_ITEM_ID, item_barcode)
        msg.add_field(FIELD_TERMINAL_LOCATION, "Main Desk Kiosk 1")
        return self.send_and_receive(msg)
