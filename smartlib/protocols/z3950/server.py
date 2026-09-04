"""Z39.50 Federated Search Gateway Server."""

import io
from typing import Dict, Any, List
from .ber import BerDecoder, BerElement, TagClass
from .pdu import InitResponse, SearchResponse
from .constants import PDU_INIT_REQUEST, PDU_SEARCH_REQUEST


class Z3950Server:
    """Accepts and processes Z39.50 search & retrieval queries."""

    def __init__(self, catalog_backend=None):
        self.catalog_backend = catalog_backend

    def process_pdu_bytes(self, raw_bytes: bytes) -> bytes:
        stream = io.BytesIO(raw_bytes)
        element = BerDecoder.decode_element(stream)
        if not element:
            return b""

        if element.tag_class == TagClass.CONTEXT_SPECIFIC:
            if element.tag == PDU_INIT_REQUEST:
                resp = InitResponse(result=True)
                return resp.to_ber().to_bytes()
            elif element.tag == PDU_SEARCH_REQUEST:
                # Mock result count from catalog
                resp = SearchResponse(search_status=True, result_count=42, number_of_records_returned=0)
                return resp.to_ber().to_bytes()

        return b""
