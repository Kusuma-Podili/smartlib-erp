"""ISO 28560 RFID Tag Data Model and Memory Encoder for Library Materials."""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class RfidIso28560Tag:
    primary_item_identifier: str  # Barcode
    type_of_usage: int = 1        # 1 = Circulating library material
    part_number: int = 1
    total_parts: int = 1
    owner_library_isin: str = "IN-SMARTLIB"
    eas_theft_prevention_armed: bool = True
    shelf_location: Optional[str] = None


class RfidTagEncoder:
    """Encodes RFID chip memory blocks conforming to ISO 28560-2."""

    AFI_CIRCULATING_ARMED = 0xC2    # In library (theft alarm active)
    AFI_CHECKED_OUT = 0x07          # Checked out to patron (safe to pass gate)

    @classmethod
    def get_afi_byte(cls, checked_out: bool) -> int:
        return cls.AFI_CHECKED_OUT if checked_out else cls.AFI_CIRCULATING_ARMED

    @classmethod
    def encode_tag_data(cls, tag: RfidIso28560Tag) -> bytes:
        # Construct ISO 28560 block bytes
        barcode_bytes = tag.primary_item_identifier.encode("ascii")
        header = bytes([0x01, len(barcode_bytes)])
        usage = bytes([tag.type_of_usage, tag.part_number, tag.total_parts])
        return header + barcode_bytes + usage
