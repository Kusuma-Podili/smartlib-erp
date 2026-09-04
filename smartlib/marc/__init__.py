"""MARC 21 Bibliographic and Authority metadata processing package.

Provides full parsing, serializing, and conversion tools for ISO 2709,
MARCXML, Dublin Core, MODS 3.7, and Authority record verification.
"""

from .records import MarcRecord, DataField, ControlField, Subfield, Leader
from .iso2709 import Iso2709Reader, Iso2709Writer
from .marcxml import MarcXmlReader, MarcXmlWriter
from .dublin_core import DublinCoreConverter, DublinCoreRecord
from .mods import ModsConverter
from .authorities import MarcAuthorityRecord, AuthorityVerificationEngine

__all__ = [
    "MarcRecord",
    "DataField",
    "ControlField",
    "Subfield",
    "Leader",
    "Iso2709Reader",
    "Iso2709Writer",
    "MarcXmlReader",
    "MarcXmlWriter",
    "DublinCoreConverter",
    "DublinCoreRecord",
    "ModsConverter",
    "MarcAuthorityRecord",
    "AuthorityVerificationEngine",
]
