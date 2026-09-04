"""ISO 2709 tape format encoder and decoder for MARC 21 communication.

Implements byte-accurate reading and writing of standardized MARC communications
exchange records, computing directories, delimiters, field offsets, and record lengths.
"""

from typing import List, Optional, BinaryIO
import io
from .records import MarcRecord, DataField, ControlField, Subfield, Leader
from .constants import (
    LEADER_LENGTH, FIELD_TERMINATOR, RECORD_TERMINATOR,
    SUBFIELD_INDICATOR, is_control_field
)

FT_BYTE = b"\x1e"
RT_BYTE = b"\x1d"
SUBFIELD_BYTE = b"\x1f"


class Iso2709Writer:
    """Serializes MarcRecord objects into standard ISO 2709 binary format."""

    @staticmethod
    def encode_record(record: MarcRecord, encoding: str = "utf-8") -> bytes:
        """Encode a MarcRecord into ISO 2709 bytes."""
        directory_entries: List[bytes] = []
        data_chunks: List[bytes] = []
        current_offset = 0

        # Sort fields: Control fields first, then Data fields
        all_fields = sorted(record.control_fields, key=lambda f: f.tag) +                      sorted(record.data_fields, key=lambda f: f.tag)

        for field in all_fields:
            if isinstance(field, ControlField):
                field_data = field.data.encode(encoding, errors="replace") + FT_BYTE
            elif isinstance(field, DataField):
                subfield_bytes = []
                for sf in field.subfields:
                    subfield_bytes.append(SUBFIELD_BYTE + sf.code.encode("ascii") + sf.value.encode(encoding, errors="replace"))
                ind_bytes = (field.ind1 + field.ind2).encode("ascii")
                field_data = ind_bytes + b"".join(subfield_bytes) + FT_BYTE
            else:
                continue

            field_len = len(field_data)
            entry = f"{field.tag}{field_len:04d}{current_offset:05d}".encode("ascii")
            directory_entries.append(entry)
            data_chunks.append(field_data)
            current_offset += field_len

        directory_bytes = b"".join(directory_entries) + FT_BYTE
        base_address = LEADER_LENGTH + len(directory_bytes)
        total_length = base_address + current_offset + 1  # +1 for RT_BYTE

        # Update leader
        record.leader.record_length = total_length
        record.leader.base_address_of_data = base_address
        leader_bytes = record.leader.to_string().encode("ascii")

        return leader_bytes + directory_bytes + b"".join(data_chunks) + RT_BYTE

    @classmethod
    def write_to_stream(cls, records: List[MarcRecord], stream: BinaryIO, encoding: str = "utf-8"):
        """Write multiple records to an output stream."""
        for rec in records:
            stream.write(cls.encode_record(rec, encoding=encoding))


class Iso2709Reader:
    """Reads and parses ISO 2709 binary MARC streams into MarcRecord objects."""

    def __init__(self, stream: BinaryIO, encoding: str = "utf-8"):
        self.stream = stream
        self.encoding = encoding

    def __iter__(self):
        return self

    def __next__(self) -> MarcRecord:
        record = self.read_record()
        if record is None:
            raise StopIteration
        return record

    def read_record(self) -> Optional[MarcRecord]:
        """Read next ISO 2709 record from stream."""
        leader_raw = self.stream.read(LEADER_LENGTH)
        if not leader_raw or len(leader_raw) < LEADER_LENGTH:
            return None

        try:
            total_len = int(leader_raw[0:5].decode("ascii"))
            base_address = int(leader_raw[12:17].decode("ascii"))
        except (ValueError, UnicodeDecodeError):
            return None

        rem_len = total_len - LEADER_LENGTH
        if rem_len <= 0:
            return None

        body = self.stream.read(rem_len)
        if len(body) < rem_len:
            return None

        directory_part = body[:base_address - LEADER_LENGTH]
        data_part = body[base_address - LEADER_LENGTH:]

        rec = MarcRecord(leader_str=leader_raw.decode("ascii", errors="replace"))

        # Parse directory (12 bytes per entry: 3 tag, 4 len, 5 offset)
        pos = 0
        while pos + 12 <= len(directory_part):
            entry = directory_part[pos:pos+12]
            if entry.startswith(FT_BYTE):
                break
            try:
                tag = entry[0:3].decode("ascii")
                field_len = int(entry[3:7].decode("ascii"))
                field_offset = int(entry[7:12].decode("ascii"))
            except (ValueError, UnicodeDecodeError):
                pos += 12
                continue

            raw_field = data_part[field_offset:field_offset+field_len]
            if raw_field.endswith(FT_BYTE):
                raw_field = raw_field[:-1]

            if is_control_field(tag):
                rec.add_control_field(tag=tag, data=raw_field.decode(self.encoding, errors="replace"))
            else:
                if len(raw_field) >= 2:
                    ind1 = chr(raw_field[0])
                    ind2 = chr(raw_field[1])
                    subfields_data = raw_field[2:]
                    df = rec.add_data_field(tag=tag, ind1=ind1, ind2=ind2)
                    parts = subfields_data.split(SUBFIELD_BYTE)
                    for p in parts:
                        if p:
                            code = chr(p[0])
                            val = p[1:].decode(self.encoding, errors="replace")
                            df.add_subfield(code=code, value=val)

            pos += 12

        return rec
