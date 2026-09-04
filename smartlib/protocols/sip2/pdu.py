"""SIP2 Protocol Data Unit (PDU) parser, formatter, and checksum routines."""

from typing import Dict, List, Optional, Tuple
import datetime
from dataclasses import dataclass, field
from .constants import (
    SIP2_FIELD_DELIMITER, FIELD_SEQUENCE_NUM, FIELD_CHECKSUM
)


@dataclass
class Sip2Field:
    identifier: str
    value: str

    def __repr__(self) -> str:
        return f"{self.identifier}{self.value}"


@dataclass
class Sip2Message:
    command: str
    fixed_fields: str = ""
    variable_fields: List[Sip2Field] = field(default_factory=list)
    sequence_num: Optional[int] = None
    checksum: Optional[str] = None

    def get_field(self, identifier: str) -> Optional[str]:
        for f in self.variable_fields:
            if f.identifier == identifier:
                return f.value
        return None

    def get_all_fields(self, identifier: str) -> List[str]:
        return [f.value for f in self.variable_fields if f.identifier == identifier]

    def add_field(self, identifier: str, value: str) -> "Sip2Message":
        self.variable_fields.append(Sip2Field(identifier=identifier, value=value))
        return self


def calculate_sip2_checksum(raw_str: str) -> str:
    """Calculate 4-character hex checksum (2's complement of sum of bytes)."""
    val = sum(ord(c) for c in raw_str)
    checksum = (-val) & 0xFFFF
    return f"{checksum:04X}"


def format_sip2_timestamp(dt: Optional[datetime.datetime] = None) -> str:
    """Format datetime as YYYYMMDDZZZZHHMMSS (standard SIP2 timestamp)."""
    if dt is None:
        dt = datetime.datetime.now()
    return dt.strftime("%Y%m%d    %H%M%S")


def format_sip2_message(msg: Sip2Message, use_checksum: bool = True) -> str:
    """Serialize Sip2Message to wire format string."""
    parts = [msg.command, msg.fixed_fields]
    for vf in msg.variable_fields:
        parts.append(f"{vf.identifier}{vf.value}{SIP2_FIELD_DELIMITER}")

    if msg.sequence_num is not None:
        parts.append(f"{FIELD_SEQUENCE_NUM}{msg.sequence_num}{SIP2_FIELD_DELIMITER}")

    raw_without_chk = "".join(parts)
    if use_checksum:
        chk_prefix = f"{FIELD_CHECKSUM}"
        chk_val = calculate_sip2_checksum(raw_without_chk + chk_prefix)
        return f"{raw_without_chk}{chk_prefix}{chk_val}\r"
    return f"{raw_without_chk}\r"


def parse_sip2_message(raw_msg: str) -> Sip2Message:
    """Parse raw wire format string into Sip2Message."""
    clean = raw_msg.strip("\r\n")
    if len(clean) < 2:
        raise ValueError("Invalid SIP2 message: too short")

    cmd = clean[:2]
    body = clean[2:]

    # Check for checksum
    chk_index = body.rfind(f"{FIELD_CHECKSUM}")
    extracted_chk = None
    if chk_index != -1 and len(body) >= chk_index + 6:
        extracted_chk = body[chk_index+2:chk_index+6]
        body = body[:chk_index]

    # Split variable fields by delimiter
    tokens = body.split(SIP2_FIELD_DELIMITER)
    fixed_part = tokens[0] if tokens else ""
    var_tokens = tokens[1:] if len(tokens) > 1 else []

    msg = Sip2Message(command=cmd, fixed_fields=fixed_part, checksum=extracted_chk)

    for tok in var_tokens:
        if len(tok) >= 2:
            f_id = tok[:2]
            f_val = tok[2:]
            if f_id == FIELD_SEQUENCE_NUM:
                try:
                    msg.sequence_num = int(f_val)
                except ValueError:
                    pass
            else:
                msg.add_field(f_id, f_val)

    return msg
