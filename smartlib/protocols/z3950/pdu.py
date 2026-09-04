"""Z39.50 PDU (Protocol Data Unit) Structures."""

from typing import List, Optional
from dataclasses import dataclass, field
from .ber import BerElement, BerEncoder, BerDecoder, TagClass
from .constants import (
    PDU_INIT_REQUEST, PDU_INIT_RESPONSE,
    PDU_SEARCH_REQUEST, PDU_SEARCH_RESPONSE
)


@dataclass
class Z3950Pdu:
    reference_id: Optional[str] = None


@dataclass
class InitRequest(Z3950Pdu):
    protocol_version: str = "3"
    options: List[str] = field(default_factory=lambda: ["search", "present"])
    preferred_message_size: int = 1048576
    maximum_record_size: int = 2097152
    id_authentication: Optional[str] = None
    implementation_id: str = "SmartLib-Z3950-Client"
    implementation_name: str = "SmartLib Library ERP"
    implementation_version: str = "2.0"

    def to_ber(self) -> BerElement:
        seq = [
            BerEncoder.encode_string(self.protocol_version),
            BerEncoder.encode_integer(self.preferred_message_size),
            BerEncoder.encode_integer(self.maximum_record_size),
            BerEncoder.encode_string(self.implementation_name)
        ]
        val = b"".join(el.to_bytes() for el in seq)
        return BerElement(tag=PDU_INIT_REQUEST, tag_class=TagClass.CONTEXT_SPECIFIC, is_constructed=True, value=val)


@dataclass
class InitResponse(Z3950Pdu):
    result: bool = True
    protocol_version: str = "3"
    preferred_message_size: int = 1048576
    maximum_record_size: int = 2097152
    implementation_id: str = "SmartLib-Z3950-Server"
    implementation_name: str = "SmartLib Enterprise ERP Z39.50 Gateway"
    implementation_version: str = "2.0"

    def to_ber(self) -> BerElement:
        seq = [
            BerEncoder.encode_string(self.protocol_version),
            BerEncoder.encode_integer(1 if self.result else 0),
            BerEncoder.encode_integer(self.preferred_message_size),
            BerEncoder.encode_integer(self.maximum_record_size),
            BerEncoder.encode_string(self.implementation_name)
        ]
        val = b"".join(el.to_bytes() for el in seq)
        return BerElement(tag=PDU_INIT_RESPONSE, tag_class=TagClass.CONTEXT_SPECIFIC, is_constructed=True, value=val)


@dataclass
class SearchRequest(Z3950Pdu):
    query: str = ""
    database_names: List[str] = field(default_factory=lambda: ["Default"])
    result_set_name: str = "default"


@dataclass
class SearchResponse(Z3950Pdu):
    search_status: bool = True
    result_count: int = 0
    number_of_records_returned: int = 0
    next_result_set_position: int = 1

    def to_ber(self) -> BerElement:
        seq = [
            BerEncoder.encode_integer(1 if self.search_status else 0),
            BerEncoder.encode_integer(self.result_count),
            BerEncoder.encode_integer(self.number_of_records_returned),
            BerEncoder.encode_integer(self.next_result_set_position)
        ]
        val = b"".join(el.to_bytes() for el in seq)
        return BerElement(tag=PDU_SEARCH_RESPONSE, tag_class=TagClass.CONTEXT_SPECIFIC, is_constructed=True, value=val)
