"""MARC 21 Authority Records and Heading Verification Engine.

Provides models and verification routines for authorized personal names, corporate names,
uniform titles, topical terms, and cross-references (See also, See from).
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from .records import MarcRecord, DataField, Subfield


@dataclass
class AuthorityHeading:
    """An established authority heading with see-also and see-from references."""
    tag: str
    heading: str
    see_from: List[str] = field(default_factory=list)
    see_also: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


class MarcAuthorityRecord:
    """Represents a MARC 21 Authority format record (names, subjects, series)."""

    def __init__(self, raw_record: Optional[MarcRecord] = None):
        self.record = raw_record if raw_record is not None else MarcRecord()

    def get_authorized_heading(self) -> Optional[AuthorityHeading]:
        """Extract primary authorized heading from 1XX field."""
        for tag in ["100", "110", "111", "130", "150", "151"]:
            df = self.record.get_field(tag)
            if df:
                val = df.value()
                see_from = [f.value() for f in self.record.get_fields(f"4{tag[1:]}")]
                see_also = [f.value() for f in self.record.get_fields(f"5{tag[1:]}")]
                notes = [f.value() for f in self.record.get_fields("680")]
                return AuthorityHeading(
                    tag=tag,
                    heading=val,
                    see_from=see_from,
                    see_also=see_also,
                    notes=notes
                )
        return None


class AuthorityVerificationEngine:
    """Validates bibliographic record headings against an authority control database."""

    def __init__(self):
        self._authorized_headings: Dict[str, AuthorityHeading] = {}
        self._variants_map: Dict[str, str] = {}

    def add_authority(self, auth_record: MarcAuthorityRecord):
        """Index an authority record for verification."""
        heading = auth_record.get_authorized_heading()
        if not heading:
            return
        key = heading.heading.lower().strip()
        self._authorized_headings[key] = heading
        for var in heading.see_from:
            self._variants_map[var.lower().strip()] = heading.heading

    def verify_bib_record(self, record: MarcRecord) -> Dict[str, List[str]]:
        """Verify headings in bibliographic record, returning unverified or redirected headings."""
        results = {
            "authorized": [],
            "redirected": [],
            "unverified": []
        }

        # Check author (100)
        f100 = record.get_field("100")
        if f100:
            val = f100.get_subfield("a")
            if val:
                k = val.lower().strip()
                if k in self._authorized_headings:
                    results["authorized"].append(val)
                elif k in self._variants_map:
                    results["redirected"].append(f"{val} -> {self._variants_map[k]}")
                else:
                    results["unverified"].append(val)

        # Check subjects (650)
        for f650 in record.get_fields("650"):
            val = f650.get_subfield("a")
            if val:
                k = val.lower().strip()
                if k in self._authorized_headings:
                    results["authorized"].append(val)
                elif k in self._variants_map:
                    results["redirected"].append(f"{val} -> {self._variants_map[k]}")
                else:
                    results["unverified"].append(val)

        return results
