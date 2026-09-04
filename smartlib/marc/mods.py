"""Metadata Object Description Schema (MODS 3.7) Converter.

Generates and parses MODS XML bibliographic metadata from MARC 21 records.
"""

from typing import Optional
import xml.etree.ElementTree as ET
from .records import MarcRecord
from .constants import (
    TAG_TITLE_STATEMENT, TAG_MAIN_ENTRY_PERSONAL_NAME,
    TAG_PUBLICATION_DISTRIBUTION, TAG_SUMMARY_NOTE,
    TAG_SUBJECT_ADDED_ENTRY_TOPICAL_TERM, TAG_PHYSICAL_DESCRIPTION
)

MODS_NS = "http://www.loc.gov/mods/v3"


class ModsConverter:
    """Translates MarcRecord into standard MODS 3.7 XML elements."""

    @staticmethod
    def marc_to_mods_xml(record: MarcRecord) -> str:
        """Convert a MarcRecord to MODS 3.7 XML document."""
        mods_el = ET.Element(f"{{{MODS_NS}}}mods", attrib={"version": "3.7"})

        # Title Info
        f245 = record.get_field(TAG_TITLE_STATEMENT)
        if f245:
            title_info = ET.SubElement(mods_el, f"{{{MODS_NS}}}titleInfo")
            a = f245.get_subfield("a")
            if a:
                t_el = ET.SubElement(title_info, f"{{{MODS_NS}}}title")
                t_el.text = a.strip().rstrip(" /:;,")
            b = f245.get_subfield("b")
            if b:
                sub_el = ET.SubElement(title_info, f"{{{MODS_NS}}}subTitle")
                sub_el.text = b.strip().rstrip(" /:;,")

        # Author / Name
        f100 = record.get_field(TAG_MAIN_ENTRY_PERSONAL_NAME)
        if f100:
            name_el = ET.SubElement(mods_el, f"{{{MODS_NS}}}name", attrib={"type": "personal"})
            np = ET.SubElement(name_el, f"{{{MODS_NS}}}namePart")
            np.text = f100.get_subfield("a") or ""
            role_el = ET.SubElement(name_el, f"{{{MODS_NS}}}role")
            role_term = ET.SubElement(role_el, f"{{{MODS_NS}}}roleTerm", attrib={"type": "text"})
            role_term.text = "creator"

        # Type of Resource
        res_el = ET.SubElement(mods_el, f"{{{MODS_NS}}}typeOfResource")
        res_el.text = "text"

        # Origin Info
        pub_info = record.publication_info()
        if any(pub_info.values()):
            orig_el = ET.SubElement(mods_el, f"{{{MODS_NS}}}originInfo")
            if pub_info["place"]:
                pl_el = ET.SubElement(orig_el, f"{{{MODS_NS}}}place")
                pt_el = ET.SubElement(pl_el, f"{{{MODS_NS}}}placeTerm", attrib={"type": "text"})
                pt_el.text = pub_info["place"]
            if pub_info["publisher"]:
                pb_el = ET.SubElement(orig_el, f"{{{MODS_NS}}}publisher")
                pb_el.text = pub_info["publisher"]
            if pub_info["year"]:
                di_el = ET.SubElement(orig_el, f"{{{MODS_NS}}}dateIssued")
                di_el.text = pub_info["year"]

        # Physical Description
        f300 = record.get_field(TAG_PHYSICAL_DESCRIPTION)
        if f300:
            pd_el = ET.SubElement(mods_el, f"{{{MODS_NS}}}physicalDescription")
            ext_el = ET.SubElement(pd_el, f"{{{MODS_NS}}}extent")
            ext_el.text = f300.value()

        # Abstract
        f520 = record.get_field(TAG_SUMMARY_NOTE)
        if f520:
            abs_el = ET.SubElement(mods_el, f"{{{MODS_NS}}}abstract")
            abs_el.text = f520.value()

        # Subject Headings
        for s in record.subjects():
            subj_el = ET.SubElement(mods_el, f"{{{MODS_NS}}}subject")
            top_el = ET.SubElement(subj_el, f"{{{MODS_NS}}}topic")
            top_el.text = s

        # Identifier
        isbn = record.isbn()
        if isbn:
            id_el = ET.SubElement(mods_el, f"{{{MODS_NS}}}identifier", attrib={"type": "isbn"})
            id_el.text = isbn

        return ET.tostring(mods_el, encoding="utf-8", xml_declaration=True).decode("utf-8")
