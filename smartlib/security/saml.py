"""SAML 2.0 Web Browser SSO Service Provider (SP) Engine."""

import base64
import uuid
import datetime
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional

SAML2_ASSERTION_NS = "urn:oasis:names:tc:SAML:2.0:assertion"
SAML2_PROTOCOL_NS = "urn:oasis:names:tc:SAML:2.0:protocol"


class SamlAuthnRequest:
    """Constructs SAML 2.0 AuthnRequest XML."""

    @staticmethod
    def create_authn_request(issuer: str, acs_url: str) -> str:
        req_id = f"_{uuid.uuid4().hex}"
        issue_instant = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        root = ET.Element(f"{{{SAML2_PROTOCOL_NS}}}AuthnRequest", attrib={
            "ID": req_id,
            "Version": "2.0",
            "IssueInstant": issue_instant,
            "Destination": "https://idp.university.edu/idp/profile/SAML2/Redirect/SSO",
            "AssertionConsumerServiceURL": acs_url,
            "ProtocolBinding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
        })
        iss = ET.SubElement(root, f"{{{SAML2_ASSERTION_NS}}}Issuer")
        iss.text = issuer
        return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")


class SamlServiceProvider:
    """Parses incoming SAML Response assertions."""

    @staticmethod
    def parse_response(b64_xml_response: str) -> Dict[str, Any]:
        xml_bytes = base64.b64decode(b64_xml_response)
        root = ET.fromstring(xml_bytes)
        # Find attributes
        attributes = {}
        for attr_el in root.iter():
            if attr_el.tag.endswith("Attribute"):
                name = attr_el.get("Name", "")
                val_el = attr_el.find(f"{{{SAML2_ASSERTION_NS}}}AttributeValue")
                if val_el is not None and val_el.text:
                    attributes[name] = val_el.text

        return {
            "status": "SUCCESS",
            "name_id": attributes.get("eduPersonTargetedID", "patron@university.edu"),
            "attributes": attributes
        }
