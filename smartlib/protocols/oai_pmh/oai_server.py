"""OAI-PMH 2.0 Repository Server."""

from typing import Dict, List, Optional
import xml.etree.ElementTree as ET
import datetime

OAI_NS = "http://www.openarchives.org/OAI/2.0/"


class OaiPmhServer:
    """Handles the six standard OAI-PMH verbs."""

    def __init__(self, repository_name: str = "SmartLib Digital Repository", base_url: str = "http://localhost:8000/oai"):
        self.repository_name = repository_name
        self.base_url = base_url

    def handle_request(self, params: Dict[str, str]) -> str:
        verb = params.get("verb", "Identify")
        root = ET.Element(f"{{{OAI_NS}}}OAI-PMH")
        resp_date = ET.SubElement(root, f"{{{OAI_NS}}}responseDate")
        resp_date.text = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        req_el = ET.SubElement(root, f"{{{OAI_NS}}}request", attrib={"verb": verb})
        req_el.text = self.base_url

        if verb == "Identify":
            self._handle_identify(root)
        elif verb == "ListMetadataFormats":
            self._handle_metadata_formats(root)
        elif verb == "ListSets":
            self._handle_list_sets(root)
        elif verb == "ListIdentifiers":
            self._handle_list_identifiers(root)
        elif verb == "ListRecords":
            self._handle_list_records(root)
        elif verb == "GetRecord":
            self._handle_get_record(root, params.get("identifier", ""))
        else:
            err = ET.SubElement(root, f"{{{OAI_NS}}}error", attrib={"code": "badVerb"})
            err.text = f"Illegal OAI verb '{verb}'"

        return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")

    def _handle_identify(self, root: ET.Element):
        id_el = ET.SubElement(root, f"{{{OAI_NS}}}Identify")
        name = ET.SubElement(id_el, f"{{{OAI_NS}}}repositoryName")
        name.text = self.repository_name
        url = ET.SubElement(id_el, f"{{{OAI_NS}}}baseURL")
        url.text = self.base_url
        ver = ET.SubElement(id_el, f"{{{OAI_NS}}}protocolVersion")
        ver.text = "2.0"
        admin = ET.SubElement(id_el, f"{{{OAI_NS}}}adminEmail")
        admin.text = "library-admin@smartlib.org"
        earliest = ET.SubElement(id_el, f"{{{OAI_NS}}}earliestDatestamp")
        earliest.text = "2020-01-01T00:00:00Z"
        gran = ET.SubElement(id_el, f"{{{OAI_NS}}}granularity")
        gran.text = "YYYY-MM-DDThh:mm:ssZ"

    def _handle_metadata_formats(self, root: ET.Element):
        mf_el = ET.SubElement(root, f"{{{OAI_NS}}}ListMetadataFormats")
        f1 = ET.SubElement(mf_el, f"{{{OAI_NS}}}metadataFormat")
        p1 = ET.SubElement(f1, f"{{{OAI_NS}}}metadataPrefix")
        p1.text = "oai_dc"
        s1 = ET.SubElement(f1, f"{{{OAI_NS}}}schema")
        s1.text = "http://www.openarchives.org/OAI/2.0/oai_dc.xsd"
        ns1 = ET.SubElement(f1, f"{{{OAI_NS}}}metadataNamespace")
        ns1.text = "http://www.openarchives.org/OAI/2.0/oai_dc/"

        f2 = ET.SubElement(mf_el, f"{{{OAI_NS}}}metadataFormat")
        p2 = ET.SubElement(f2, f"{{{OAI_NS}}}metadataPrefix")
        p2.text = "marc21"
        s2 = ET.SubElement(f2, f"{{{OAI_NS}}}schema")
        s2.text = "http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd"
        ns2 = ET.SubElement(f2, f"{{{OAI_NS}}}metadataNamespace")
        ns2.text = "http://www.loc.gov/MARC21/slim"

    def _handle_list_sets(self, root: ET.Element):
        sets_el = ET.SubElement(root, f"{{{OAI_NS}}}ListSets")
        s1 = ET.SubElement(sets_el, f"{{{OAI_NS}}}set")
        spec1 = ET.SubElement(s1, f"{{{OAI_NS}}}setSpec")
        spec1.text = "cs_books"
        name1 = ET.SubElement(s1, f"{{{OAI_NS}}}setName")
        name1.text = "Computer Science Monographs"

    def _handle_list_identifiers(self, root: ET.Element):
        li_el = ET.SubElement(root, f"{{{OAI_NS}}}ListIdentifiers")
        h = ET.SubElement(li_el, f"{{{OAI_NS}}}header")
        ident = ET.SubElement(h, f"{{{OAI_NS}}}identifier")
        ident.text = "oai:smartlib.org:item/001"
        ds = ET.SubElement(h, f"{{{OAI_NS}}}datestamp")
        ds.text = "2026-09-04T10:00:00Z"

    def _handle_list_records(self, root: ET.Element):
        lr_el = ET.SubElement(root, f"{{{OAI_NS}}}ListRecords")
        rec = ET.SubElement(lr_el, f"{{{OAI_NS}}}record")
        h = ET.SubElement(rec, f"{{{OAI_NS}}}header")
        ident = ET.SubElement(h, f"{{{OAI_NS}}}identifier")
        ident.text = "oai:smartlib.org:item/001"
        ds = ET.SubElement(h, f"{{{OAI_NS}}}datestamp")
        ds.text = "2026-09-04T10:00:00Z"

    def _handle_get_record(self, root: ET.Element, identifier: str):
        gr_el = ET.SubElement(root, f"{{{OAI_NS}}}GetRecord")
        rec = ET.SubElement(gr_el, f"{{{OAI_NS}}}record")
        h = ET.SubElement(rec, f"{{{OAI_NS}}}header")
        ident = ET.SubElement(h, f"{{{OAI_NS}}}identifier")
        ident.text = identifier or "oai:smartlib.org:item/001"
        ds = ET.SubElement(h, f"{{{OAI_NS}}}datestamp")
        ds.text = "2026-09-04T10:00:00Z"
