"""MARC 21 Record, DataField, ControlField, Subfield, and Leader data structures.

Provides complete object-oriented representations of MARC bibliographic records,
including fluent builder methods, validation, search, and transformation logic.
"""

from typing import List, Dict, Optional, Tuple, Any, Iterator
import json
import re
from dataclasses import dataclass, field
from .constants import (
    LEADER_LENGTH, is_control_field, validate_tag,
    RECORD_STATUS_NEW, RECORD_TYPE_LANGUAGE_MATERIAL,
    BIB_LEVEL_MONOGRAPH, CONTROL_TYPE_NO_SPECIFIED,
    ENCODING_UTF8, CATALOGING_FORM_ISBD, MULTIPART_NOT_SPECIFIED,
    TAG_TITLE_STATEMENT, TAG_ISBN, TAG_MAIN_ENTRY_PERSONAL_NAME,
    TAG_PUBLICATION_DISTRIBUTION, TAG_PHYSICAL_DESCRIPTION,
    TAG_SUBJECT_ADDED_ENTRY_TOPICAL_TERM, TAG_ELECTRONIC_LOCATION_ACCESS
)


@dataclass
class Subfield:
    """Represents a single MARC subfield (delimiter code and value)."""
    code: str
    value: str

    def __post_init__(self):
        if not self.code or len(self.code) != 1:
            raise ValueError(f"Subfield code must be exactly 1 character, got: '{self.code}'")
        if self.value is None:
            self.value = ""

    def __repr__(self) -> str:
        return f"${self.code} {self.value}"

    def to_dict(self) -> Dict[str, str]:
        return {self.code: self.value}


class ControlField:
    """Represents a MARC control field (tags 001-009) with string data."""
    def __init__(self, tag: str, data: str = ""):
        if not validate_tag(tag):
            raise ValueError(f"Invalid control tag: '{tag}'")
        if not is_control_field(tag):
            raise ValueError(f"Tag '{tag}' is not a valid control field (must be 001-009)")
        self.tag = tag
        self.data = data or ""

    def __repr__(self) -> str:
        return f"ControlField({self.tag}, '{self.data}')"

    def to_dict(self) -> Dict[str, Any]:
        return {"tag": self.tag, "data": self.data}


class DataField:
    """Represents a MARC variable data field (tags 010-999) with indicators and subfields."""
    def __init__(self, tag: str, ind1: str = " ", ind2: str = " ", subfields: Optional[List[Subfield]] = None):
        if not validate_tag(tag):
            raise ValueError(f"Invalid data field tag: '{tag}'")
        self.tag = tag
        self.ind1 = (ind1 or " ")[:1]
        self.ind2 = (ind2 or " ")[:1]
        self.subfields: List[Subfield] = subfields if subfields is not None else []

    def add_subfield(self, code: str, value: str) -> "DataField":
        """Append a subfield to this field."""
        self.subfields.append(Subfield(code=code, value=value))
        return self

    def get_subfield(self, code: str) -> Optional[str]:
        """Return the value of the first matching subfield code, or None."""
        for sf in self.subfields:
            if sf.code == code:
                return sf.value
        return None

    def get_subfields(self, code: str) -> List[str]:
        """Return values of all matching subfield codes."""
        return [sf.value for sf in self.subfields if sf.code == code]

    def remove_subfields(self, code: str) -> int:
        """Remove all subfields matching code, returning the count removed."""
        orig_len = len(self.subfields)
        self.subfields = [sf for sf in self.subfields if sf.code != code]
        return orig_len - len(self.subfields)

    def value(self, separator: str = " ") -> str:
        """Concatenate all subfield values with separator."""
        return separator.join(sf.value for sf in self.subfields if sf.value)

    def __repr__(self) -> str:
        sf_str = " ".join(repr(sf) for sf in self.subfields)
        return f"{self.tag} {self.ind1}{self.ind2} {sf_str}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tag": self.tag,
            "ind1": self.ind1,
            "ind2": self.ind2,
            "subfields": [{sf.code: sf.value} for sf in self.subfields]
        }


class Leader:
    """Represents the 24-character MARC 21 Leader."""
    def __init__(self, raw: str = "00000nam a2200000 a 4500"):
        if len(raw) != LEADER_LENGTH:
            raw = raw.ljust(LEADER_LENGTH, " ")[:LEADER_LENGTH]
        self.raw = list(raw)

    @property
    def record_length(self) -> int:
        try:
            return int("".join(self.raw[0:5]))
        except ValueError:
            return 0

    @record_length.setter
    def record_length(self, length: int):
        formatted = f"{length:05d}"
        self.raw[0:5] = list(formatted)

    @property
    def record_status(self) -> str:
        return self.raw[5]

    @record_status.setter
    def record_status(self, val: str):
        self.raw[5] = val[:1]

    @property
    def record_type(self) -> str:
        return self.raw[6]

    @record_type.setter
    def record_type(self, val: str):
        self.raw[6] = val[:1]

    @property
    def bib_level(self) -> str:
        return self.raw[7]

    @bib_level.setter
    def bib_level(self, val: str):
        self.raw[7] = val[:1]

    @property
    def char_encoding(self) -> str:
        return self.raw[9]

    @char_encoding.setter
    def char_encoding(self, val: str):
        self.raw[9] = val[:1]

    @property
    def base_address_of_data(self) -> int:
        try:
            return int("".join(self.raw[12:17]))
        except ValueError:
            return 0

    @base_address_of_data.setter
    def base_address_of_data(self, addr: int):
        formatted = f"{addr:05d}"
        self.raw[12:17] = list(formatted)

    def to_string(self) -> str:
        return "".join(self.raw)

    def __repr__(self) -> str:
        return f"Leader('{self.to_string()}')"


class MarcRecord:
    """Complete MARC 21 Bibliographic Record containing Leader, ControlFields, and DataFields."""

    def __init__(self, leader_str: Optional[str] = None):
        self.leader = Leader(leader_str if leader_str else "00000nam a2200000 a 4500")
        self.control_fields: List[ControlField] = []
        self.data_fields: List[DataField] = []

    def add_control_field(self, tag: str, data: str) -> ControlField:
        """Add a control field to the record."""
        cf = ControlField(tag=tag, data=data)
        self.control_fields.append(cf)
        return cf

    def add_data_field(self, tag: str, ind1: str = " ", ind2: str = " ", subfields: Optional[List[Subfield]] = None) -> DataField:
        """Add a data field to the record."""
        df = DataField(tag=tag, ind1=ind1, ind2=ind2, subfields=subfields)
        self.data_fields.append(df)
        return df

    def get_field(self, tag: str) -> Optional[Any]:
        """Get first control or data field matching tag."""
        if is_control_field(tag):
            for cf in self.control_fields:
                if cf.tag == tag:
                    return cf
        else:
            for df in self.data_fields:
                if df.tag == tag:
                    return df
        return None

    def get_fields(self, *tags: str) -> List[Any]:
        """Get all fields matching any of the specified tags."""
        result: List[Any] = []
        for tag in tags:
            if is_control_field(tag):
                result.extend([cf for cf in self.control_fields if cf.tag == tag])
            else:
                result.extend([df for df in self.data_fields if df.tag == tag])
        return result

    def title(self) -> Optional[str]:
        """Extract main title from 245$a and 245$b."""
        f245 = self.get_field(TAG_TITLE_STATEMENT)
        if not f245:
            return None
        parts = []
        a = f245.get_subfield("a")
        if a:
            parts.append(a.strip().rstrip(" /:;,"))
        b = f245.get_subfield("b")
        if b:
            parts.append(b.strip().rstrip(" /:;,"))
        return " : ".join(parts) if parts else None

    def author(self) -> Optional[str]:
        """Extract primary author from 100$a."""
        f100 = self.get_field(TAG_MAIN_ENTRY_PERSONAL_NAME)
        if f100:
            val = f100.get_subfield("a")
            if val:
                return val.strip().rstrip(",")
        return None

    def isbn(self) -> Optional[str]:
        """Extract ISBN from 020$a."""
        f020 = self.get_field(TAG_ISBN)
        if f020:
            val = f020.get_subfield("a")
            if val:
                match = re.search(r"[0-9Xx\-]{10,17}", val)
                if match:
                    return match.group(0).replace("-", "")
                return val.split()[0]
        return None

    def subjects(self) -> List[str]:
        """Extract all subject headings from 650 fields."""
        results = []
        for f in self.get_fields(TAG_SUBJECT_ADDED_ENTRY_TOPICAL_TERM):
            val = f.value(" -- ")
            if val:
                results.append(val)
        return results

    def publication_info(self) -> Dict[str, Optional[str]]:
        """Extract place, publisher, and year from 260 or 264."""
        f260 = self.get_field(TAG_PUBLICATION_DISTRIBUTION) or self.get_field("264")
        if not f260:
            return {"place": None, "publisher": None, "year": None}
        place = f260.get_subfield("a")
        publisher = f260.get_subfield("b")
        year = f260.get_subfield("c")
        return {
            "place": place.strip().rstrip(" :;,") if place else None,
            "publisher": publisher.strip().rstrip(" :;,") if publisher else None,
            "year": re.sub(r"[^0-9]", "", year) if year else None
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert record to standard JSON-compatible dictionary."""
        fields_list = []
        for cf in sorted(self.control_fields, key=lambda x: x.tag):
            fields_list.append({cf.tag: cf.data})
        for df in sorted(self.data_fields, key=lambda x: x.tag):
            subfields_data = [{sf.code: sf.value} for sf in df.subfields]
            fields_list.append({
                df.tag: {
                    "ind1": df.ind1,
                    "ind2": df.ind2,
                    "subfields": subfields_data
                }
            })
        return {
            "leader": self.leader.to_string(),
            "fields": fields_list
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MarcRecord":
        """Reconstruct a MarcRecord from dictionary representation."""
        rec = cls(leader_str=data.get("leader"))
        for item in data.get("fields", []):
            for tag, val in item.items():
                if is_control_field(tag):
                    rec.add_control_field(tag=tag, data=str(val))
                else:
                    ind1 = val.get("ind1", " ")
                    ind2 = val.get("ind2", " ")
                    df = rec.add_data_field(tag=tag, ind1=ind1, ind2=ind2)
                    for sf_dict in val.get("subfields", []):
                        for c, v in sf_dict.items():
                            df.add_subfield(code=c, value=str(v))
        return rec
