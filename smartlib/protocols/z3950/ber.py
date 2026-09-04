"""ASN.1 Basic Encoding Rules (BER) Decoder and Encoder."""

from enum import IntEnum
from typing import Tuple, List, Optional, Union
import io


class TagClass(IntEnum):
    UNIVERSAL = 0x00
    APPLICATION = 0x40
    CONTEXT_SPECIFIC = 0x80
    PRIVATE = 0xC0


class BerElement:
    """Represents an ASN.1 Type-Length-Value (TLV) element."""
    def __init__(self, tag: int, tag_class: TagClass = TagClass.UNIVERSAL, is_constructed: bool = False, value: bytes = b""):
        self.tag = tag
        self.tag_class = tag_class
        self.is_constructed = is_constructed
        self.value = value

    def to_bytes(self) -> bytes:
        return BerEncoder.encode_element(self)


class BerEncoder:
    """Encodes Python types and BerElements into BER byte strings."""

    @staticmethod
    def encode_identifier(tag: int, tag_class: TagClass, is_constructed: bool) -> bytes:
        constructed_bit = 0x20 if is_constructed else 0x00
        first_byte = tag_class | constructed_bit
        if tag < 31:
            return bytes([first_byte | tag])
        # High tag number form
        octets = [tag & 0x7F]
        tag >>= 7
        while tag > 0:
            octets.append((tag & 0x7F) | 0x80)
            tag >>= 7
        octets.reverse()
        return bytes([first_byte | 0x1F]) + bytes(octets)

    @staticmethod
    def encode_length(length: int) -> bytes:
        if length < 128:
            return bytes([length])
        octets = []
        while length > 0:
            octets.append(length & 0xFF)
            length >>= 8
        octets.reverse()
        return bytes([0x80 | len(octets)]) + bytes(octets)

    @classmethod
    def encode_element(cls, el: BerElement) -> bytes:
        header = cls.encode_identifier(el.tag, el.tag_class, el.is_constructed)
        length = cls.encode_length(len(el.value))
        return header + length + el.value

    @classmethod
    def encode_integer(cls, val: int) -> BerElement:
        # Minimum two's complement encoding
        if val == 0:
            return BerElement(tag=2, value=b"\x00")
        octets = []
        temp = val
        if val > 0:
            while temp > 0:
                octets.append(temp & 0xFF)
                temp >>= 8
            if octets[-1] & 0x80:
                octets.append(0)
        else:
            while temp < -1:
                octets.append(temp & 0xFF)
                temp >>= 8
            if not (octets[-1] & 0x80):
                octets.append(0xFF)
        octets.reverse()
        return BerElement(tag=2, value=bytes(octets))

    @classmethod
    def encode_string(cls, text: str, tag: int = 4) -> BerElement:
        return BerElement(tag=tag, value=text.encode("utf-8"))

    @classmethod
    def encode_sequence(cls, elements: List[BerElement], tag: int = 16) -> BerElement:
        val = b"".join(el.to_bytes() for el in elements)
        return BerElement(tag=tag, tag_class=TagClass.UNIVERSAL, is_constructed=True, value=val)


class BerDecoder:
    """Decodes BER byte streams into BerElements."""

    @staticmethod
    def decode_element(stream: io.BytesIO) -> Optional[BerElement]:
        first = stream.read(1)
        if not first:
            return None
        b = first[0]
        tag_class = TagClass(b & 0xC0)
        is_constructed = bool(b & 0x20)
        tag = b & 0x1F

        if tag == 0x1F:
            tag = 0
            while True:
                next_b = stream.read(1)
                if not next_b:
                    return None
                val = next_b[0]
                tag = (tag << 7) | (val & 0x7F)
                if not (val & 0x80):
                    break

        # Length decoding
        len_b = stream.read(1)
        if not len_b:
            return None
        lb = len_b[0]
        if lb < 128:
            length = lb
        else:
            num_bytes = lb & 0x7F
            length = 0
            for _ in range(num_bytes):
                chunk = stream.read(1)
                if not chunk:
                    return None
                length = (length << 8) | chunk[0]

        value = stream.read(length)
        return BerElement(tag=tag, tag_class=tag_class, is_constructed=is_constructed, value=value)
