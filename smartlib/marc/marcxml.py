"""MARCXML 2.0 Parser and Writer.

Converts between MarcRecord objects and the official Library of Congress MARCXML
schema representation using Python standard library xml.etree.ElementTree.
"""

from typing import List, Optional
import xml.etree.ElementTree as ET
from .records import MarcRecord, DataField, ControlField, Subfield
from .constants import is_control_field

MARCXML_NS = "http://www.loc.gov/MARC21/slim"
NS_MAP = {"marc": MARCXML_NS}


class MarcXmlWriter:
    """Serializes MarcRecord objects to MARCXML elements or strings."""

    @staticmethod
    def record_to_xml(record: MarcRecord) -> ET.Element:
        """Convert a MarcRecord to an xml.etree.ElementTree.Element."""
        rec_el = ET.Element(f"{{{MARCXML_NS}}}record")

        # Leader
        leader_el = ET.SubElement(rec_el, f"{{{MARCXML_NS}}}leader")
        leader_el.text = record.leader.to_string()

        # Control fields
        for cf in sorted(record.control_fields, key=lambda f: f.tag):
            cf_el = ET.SubElement(rec_el, f"{{{MARCXML_NS}}}controlfield")
            cf_el.set("tag", cf.tag)
            cf_el.text = cf.data

        # Data fields
        for df in sorted(record.data_fields, key=lambda f: f.tag):
            df_el = ET.SubElement(rec_el, f"{{{MARCXML_NS}}}datafield")
            df_el.set("tag", df.tag)
            df_el.set("ind1", df.ind1)
            df_el.set("ind2", df.ind2)
            for sf in df.subfields:
                sf_el = ET.SubElement(df_el, f"{{{MARCXML_NS}}}subfield")
                sf_el.set("code", sf.code)
                sf_el.text = sf.value

        return rec_el

    @classmethod
    def records_to_collection_xml(cls, records: List[MarcRecord]) -> str:
        """Serialize a list of MarcRecords to a MARCXML collection string."""
        collection_el = ET.Element(f"{{{MARCXML_NS}}}collection")
        for rec in records:
            collection_el.append(cls.record_to_xml(rec))
        return ET.tostring(collection_el, encoding="utf-8", xml_declaration=True).decode("utf-8")


class MarcXmlReader:
    """Parses MARCXML documents into MarcRecord instances."""

    @staticmethod
    def xml_to_record(element: ET.Element) -> MarcRecord:
        """Parse a single <marc:record> element into a MarcRecord."""
        # Find leader
        leader_el = element.find(f"{{{MARCXML_NS}}}leader")
        leader_str = leader_el.text if leader_el is not None and leader_el.text else None
        rec = MarcRecord(leader_str=leader_str)

        # Control fields
        for cf_el in element.findall(f"{{{MARCXML_NS}}}controlfield"):
            tag = cf_el.get("tag", "001")
            data = cf_el.text or ""
            rec.add_control_field(tag=tag, data=data)

        # Data fields
        for df_el in element.findall(f"{{{MARCXML_NS}}}datafield"):
            tag = df_el.get("tag", "999")
            ind1 = df_el.get("ind1", " ")
            ind2 = df_el.get("ind2", " ")
            df = rec.add_data_field(tag=tag, ind1=ind1, ind2=ind2)
            for sf_el in df_el.findall(f"{{{MARCXML_NS}}}subfield"):
                code = sf_el.get("code", "a")
                val = sf_el.text or ""
                df.add_subfield(code=code, value=val)

        return rec

    @classmethod
    def parse_xml(cls, xml_content: str) -> List[MarcRecord]:
        """Parse XML string containing single or multiple MARC records."""
        root = ET.fromstring(xml_content)
        records: List[MarcRecord] = []
        if root.tag.endswith("record"):
            records.append(cls.xml_to_record(root))
        elif root.tag.endswith("collection"):
            for rec_el in root.findall(f"{{{MARCXML_NS}}}record"):
                records.append(cls.xml_to_record(rec_el))
        return records
