"""ANSI/NISO Z39.50 Bib-1 Attribute Architecture Specification Catalog.

Defines all standard Bib-1 Use (type 1), Relation (type 2), Position (type 3),
Structure (type 4), Truncation (type 5), and Completeness (type 6) attributes.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Bib1AttributeDefinition:
    type_id: int
    attribute_value: int
    name: str
    description: str
    sql_mapping_column: Optional[str] = None


BIB1_ATTRIBUTES: Dict[int, Bib1AttributeDefinition] = {}

def _attr(attr_type: int, val: int, name: str, desc: str, col: Optional[str] = None):
    # Unique key: (attr_type * 10000) + val
    key = attr_type * 10000 + val
    BIB1_ATTRIBUTES[key] = Bib1AttributeDefinition(attr_type, val, name, desc, col)

_attr(1, 1, "Personal name", "Author personal name main or added entry", "authors.name")
_attr(1, 2, "Corporate name", "Corporate author or agency name", "authors.name")
_attr(1, 3, "Conference name", "Conference, symposium, or meeting name", "books.title")
_attr(1, 4, "Title", "Bibliographic monograph or journal title", "books.title")
_attr(1, 5, "Title series", "Series title entry", "books.title")
_attr(1, 6, "Title uniform", "Uniform standardized title", "books.title")
_attr(1, 7, "ISBN", "International Standard Book Number (10 or 13 digits)", "books.isbn")
_attr(1, 8, "ISSN", "International Standard Serial Number", "books.isbn")
_attr(1, 9, "LC call number", "Library of Congress Classification call number", "book_copies.call_number")
_attr(1, 10, "Dewey classification", "Dewey Decimal Classification number", "categories.name")
_attr(1, 11, "UDC classification", "Universal Decimal Classification number", "categories.name")
_attr(1, 12, "Local call number", "Library local shelfmark or classification mark", "book_copies.call_number")
_attr(1, 13, "Control number", "Catalog record system control number (001)", "books.id")
_attr(1, 14, "Government document number", "Government publication document number (074)", "books.isbn")
_attr(1, 15, "Record control number", "National library record control number (LCCN)", "books.id")
_attr(1, 16, "Date of publication", "Imprint publication year (260$c)", "books.publication_year")
_attr(1, 21, "Subject heading", "Topical subject heading (650)", "categories.name")
_attr(1, 25, "Abstract", "Summary or abstract note (520)", "books.summary")
_attr(1, 30, "Date of birth", "Author birth date in authority record", None)
_attr(1, 31, "Date of death", "Author death date in authority record", None)
_attr(1, 32, "Date of creation", "Original manuscript creation date", None)
_attr(1, 45, "Publisher", "Monograph or serial publishing house (260$b)", "publishers.name")
_attr(1, 46, "Place of publication", "City or country of publication (260$a)", None)
_attr(1, 47, "Editor", "Editor statement of responsibility (245$c)", "authors.name")
_attr(1, 48, "Illustrator", "Illustrator of work", "authors.name")
_attr(1, 49, "Translator", "Translator of original language work", "authors.name")
_attr(1, 54, "Language", "ISO 639 language code of text (041)", "books.language")
_attr(1, 58, "Format", "Carrier format or physical extent (300)", "book_copies.status")
_attr(1, 62, "Barcode", "Physical item barcode on book copy (852$p)", "book_copies.barcode")
_attr(1, 1003, "Author", "Any author (personal, corporate, conference)", "authors.name")
_attr(1, 1011, "Keyword", "Keyword search across all bibliographic fields", "books.title")
_attr(1, 1016, "Any", "Unrestricted cross-field search", "books.title")
_attr(1, 1018, "Publisher number", "Publisher assigned music or recording number", None)
_attr(1, 1031, "Material type", "Leader/06 type of record code", None)
_attr(1, 1035, "Anywhere", "Full text search across record and attachments", "books.title")
_attr(2, 1, "Less than", "Numeric or date value less than query term", None)
_attr(2, 2, "Less than or equal", "Numeric or date value less than or equal to query term", None)
_attr(2, 3, "Equal", "Exact match or phrase equality", None)
_attr(2, 4, "Greater than or equal", "Numeric or date value greater than or equal to query term", None)
_attr(2, 5, "Greater than", "Numeric or date value greater than query term", None)
_attr(2, 6, "Not equal", "Inequality comparison", None)
_attr(3, 1, "First in field", "Match must occur at the beginning of the field", None)
_attr(3, 2, "First in subfield", "Match must occur at the start of any subfield", None)
_attr(3, 3, "Any position in field", "Match may occur anywhere in the target field", None)
_attr(4, 1, "Phrase", "Exact word sequence match", None)
_attr(4, 2, "Word", "Individual word token match", None)
_attr(4, 3, "Key", "Pre-normalized indexed key match", None)
_attr(4, 4, "Year", "Four-digit Gregorian calendar year match", None)
_attr(4, 5, "Date (normalized)", "ISO 8601 YYYY-MM-DD format", None)
_attr(4, 6, "Word list", "Set of independent word tokens", None)
_attr(5, 1, "Right truncation", "Wildcard suffix search (term*)", None)
_attr(5, 2, "Left truncation", "Wildcard prefix search (*term)", None)
_attr(5, 3, "Left and right truncation", "Sub-string containment (*term*)", None)
_attr(5, 100, "No truncation", "Literal exact string search", None)
_attr(5, 104, "Process # in search term", "Inline character masking (# replaces 1 character)", None)
_attr(6, 1, "Incomplete subfield", "Match applies to part of a subfield", None)
_attr(6, 2, "Complete subfield", "Match must encompass entire subfield", None)
_attr(6, 3, "Complete field", "Match must encompass entire field", None)

def get_bib1_attribute(attr_type: int, attr_value: int) -> Optional[Bib1AttributeDefinition]:
    key = attr_type * 10000 + attr_value
    return BIB1_ATTRIBUTES.get(key)
