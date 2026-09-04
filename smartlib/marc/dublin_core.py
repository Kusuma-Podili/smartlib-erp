"""Dublin Core (DCMES 15) Metadata Converter and Crosswalk.

Translates bidirectional metadata between standard MARC 21 records and
the Dublin Core Metadata Element Set (ISO 15836).
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
import xml.etree.ElementTree as ET
from .records import MarcRecord, DataField, Subfield
from .constants import (
    TAG_TITLE_STATEMENT, TAG_MAIN_ENTRY_PERSONAL_NAME,
    TAG_ADDED_ENTRY_PERSONAL_NAME, TAG_SUBJECT_ADDED_ENTRY_TOPICAL_TERM,
    TAG_SUMMARY_NOTE, TAG_PUBLICATION_DISTRIBUTION, TAG_LANGUAGE_CODE,
    TAG_PHYSICAL_DESCRIPTION, TAG_ISBN, TAG_ISSN, TAG_ELECTRONIC_LOCATION_ACCESS
)


@dataclass
class DublinCoreRecord:
    """Representation of the 15 standard Dublin Core Metadata Elements."""
    title: List[str] = field(default_factory=list)
    creator: List[str] = field(default_factory=list)
    subject: List[str] = field(default_factory=list)
    description: List[str] = field(default_factory=list)
    publisher: List[str] = field(default_factory=list)
    contributor: List[str] = field(default_factory=list)
    date: List[str] = field(default_factory=list)
    type: List[str] = field(default_factory=list)
    format: List[str] = field(default_factory=list)
    identifier: List[str] = field(default_factory=list)
    source: List[str] = field(default_factory=list)
    language: List[str] = field(default_factory=list)
    relation: List[str] = field(default_factory=list)
    coverage: List[str] = field(default_factory=list)
    rights: List[str] = field(default_factory=list)

    def to_xml(self) -> str:
        """Render to Dublin Core XML."""
        dc_ns = "http://purl.org/dc/elements/1.1/"
        oai_dc = ET.Element(
            "{http://www.openarchives.org/OAI/2.0/oai_dc/}dc",
            attrib={"xmlns:dc": dc_ns, "xmlns:oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/"}
        )
        for attr in ["title", "creator", "subject", "description", "publisher",
                     "contributor", "date", "type", "format", "identifier",
                     "source", "language", "relation", "coverage", "rights"]:
            values = getattr(self, attr, [])
            for val in values:
                el = ET.SubElement(oai_dc, f"{{{dc_ns}}}{attr}")
                el.text = val
        return ET.tostring(oai_dc, encoding="utf-8", xml_declaration=True).decode("utf-8")


class DublinCoreConverter:
    """Converts between MarcRecord and DublinCoreRecord."""

    @staticmethod
    def marc_to_dc(record: MarcRecord) -> DublinCoreRecord:
        """Crosswalk MARC 21 record fields into Dublin Core elements."""
        dc = DublinCoreRecord()

        # Title (245)
        t = record.title()
        if t:
            dc.title.append(t)

        # Creator (100, 110, 111)
        a = record.author()
        if a:
            dc.creator.append(a)

        # Subject (650, 651, 655)
        dc.subject.extend(record.subjects())

        # Description (520, 500)
        for f in record.get_fields(TAG_SUMMARY_NOTE, "500"):
            val = f.value()
            if val:
                dc.description.append(val)

        # Publisher and Date (260 / 264)
        pub_info = record.publication_info()
        if pub_info["publisher"]:
            dc.publisher.append(pub_info["publisher"])
        if pub_info["year"]:
            dc.date.append(pub_info["year"])

        # Format (300)
        f300 = record.get_field(TAG_PHYSICAL_DESCRIPTION)
        if f300:
            dc.format.append(f300.value())

        # Identifier (020, 022, 856)
        isbn = record.isbn()
        if isbn:
            dc.identifier.append(f"urn:isbn:{isbn}")

        for f856 in record.get_fields(TAG_ELECTRONIC_LOCATION_ACCESS):
            u = f856.get_subfield("u")
            if u:
                dc.identifier.append(u)

        # Language (041 / 008)
        f041 = record.get_field(TAG_LANGUAGE_CODE)
        if f041:
            lang = f041.get_subfield("a")
            if lang:
                dc.language.append(lang)

        # Type default
        dc.type.append("Text")

        return dc

    @staticmethod
    def dc_to_marc(dc: DublinCoreRecord) -> MarcRecord:
        """Generate basic MARC 21 record from Dublin Core elements."""
        rec = MarcRecord()
        if dc.title:
            rec.add_data_field(TAG_TITLE_STATEMENT, "1", "0", [Subfield("a", dc.title[0])])
        if dc.creator:
            rec.add_data_field(TAG_MAIN_ENTRY_PERSONAL_NAME, "1", " ", [Subfield("a", dc.creator[0])])
        for s in dc.subject:
            rec.add_data_field(TAG_SUBJECT_ADDED_ENTRY_TOPICAL_TERM, " ", "0", [Subfield("a", s)])
        if dc.description:
            rec.add_data_field(TAG_SUMMARY_NOTE, " ", " ", [Subfield("a", dc.description[0])])
        if dc.publisher or dc.date:
            sfs = []
            if dc.publisher:
                sfs.append(Subfield("b", dc.publisher[0]))
            if dc.date:
                sfs.append(Subfield("c", dc.date[0]))
            rec.add_data_field(TAG_PUBLICATION_DISTRIBUTION, " ", " ", sfs)
        for ident in dc.identifier:
            if ident.startswith("urn:isbn:"):
                rec.add_data_field(TAG_ISBN, " ", " ", [Subfield("a", ident.replace("urn:isbn:", ""))])
            elif ident.startswith("http"):
                rec.add_data_field(TAG_ELECTRONIC_LOCATION_ACCESS, "4", "0", [Subfield("u", ident)])
        return rec
