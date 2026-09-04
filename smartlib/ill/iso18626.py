"""ISO 18626 Resource Sharing standard XML parser and message generator."""

from typing import Optional, Dict, Any
import xml.etree.ElementTree as ET
import datetime
from .models import IllRequest, IllRequestType, IllServiceType, IllStatus

ISO18626_NS = "http://standards.iso.org/iso/18626"


class Iso18626MessageBuilder:
    """Constructs ISO 18626 XML documents for cross-library communication."""

    @staticmethod
    def build_request_message(ill_request: IllRequest, sender_id: str, recipient_id: str) -> str:
        """Build ISO 18626 request message."""
        root = ET.Element(f"{{{ISO18626_NS}}}request", attrib={"xmlns": ISO18626_NS})
        
        # Header
        header = ET.SubElement(root, "header")
        ET.SubElement(header, "supplyingAgencyId").text = recipient_id
        ET.SubElement(header, "requestingAgencyId").text = sender_id
        ET.SubElement(header, "timestamp").text = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        ET.SubElement(header, "requestingAgencyRequestId").text = ill_request.id
        
        # Bibliographic Info
        bib = ET.SubElement(root, "bibliographicInfo")
        ET.SubElement(bib, "title").text = ill_request.title
        if ill_request.author:
            ET.SubElement(bib, "author").text = ill_request.author
        if ill_request.isbn:
            ET.SubElement(bib, "isbn").text = ill_request.isbn
        if ill_request.issn:
            ET.SubElement(bib, "issn").text = ill_request.issn
        if ill_request.article_title:
            ET.SubElement(bib, "articleTitle").text = ill_request.article_title
        if ill_request.pages:
            ET.SubElement(bib, "pages").text = ill_request.pages

        # Service Info
        service = ET.SubElement(root, "serviceInfo")
        ET.SubElement(service, "serviceType").text = ill_request.service_type.value
        ET.SubElement(service, "serviceLevel").text = "Normal"

        return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")

    @staticmethod
    def build_supplying_message(request_id: str, sender_id: str, recipient_id: str, action: str, note: str = "") -> str:
        """Build ISO 18626 supplying agency response message."""
        root = ET.Element(f"{{{ISO18626_NS}}}supplyingAgencyMessage", attrib={"xmlns": ISO18626_NS})
        header = ET.SubElement(root, "header")
        ET.SubElement(header, "supplyingAgencyId").text = sender_id
        ET.SubElement(header, "requestingAgencyId").text = recipient_id
        ET.SubElement(header, "timestamp").text = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        ET.SubElement(header, "requestingAgencyRequestId").text = request_id
        
        msg_info = ET.SubElement(root, "messageConfirmation")
        ET.SubElement(msg_info, "action").text = action
        if note:
            ET.SubElement(msg_info, "note").text = note

        return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")


class Iso18626Parser:
    """Parses incoming ISO 18626 XML requests and confirmations."""

    @staticmethod
    def parse_request(xml_str: str) -> Dict[str, Any]:
        root = ET.fromstring(xml_str)
        # Strip namespace if present
        def find_text(path: str) -> Optional[str]:
            for el in root.iter():
                if el.tag.split("}")[-1] == path:
                    return el.text
            return None

        return {
            "request_id": find_text("requestingAgencyRequestId"),
            "sender": find_text("requestingAgencyId"),
            "recipient": find_text("supplyingAgencyId"),
            "title": find_text("title") or "Unknown Title",
            "author": find_text("author"),
            "isbn": find_text("isbn"),
            "article_title": find_text("articleTitle"),
            "service_type": find_text("serviceType") or "physical_loan"
        }
