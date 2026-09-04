"""Comprehensive MARC 21 Bibliographic Tag and Subfield Specifications.

Defines validation rules, repeatable flags, indicator values, and subfield names
for all standard MARC 21 bibliographic tags.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class SubfieldSpec:
    code: str
    name: str
    repeatable: bool = False
    required: bool = False


@dataclass
class FieldSpec:
    tag: str
    name: str
    repeatable: bool = True
    ind1_values: Dict[str, str] = field(default_factory=dict)
    ind2_values: Dict[str, str] = field(default_factory=dict)
    subfields: Dict[str, SubfieldSpec] = field(default_factory=dict)

    def validate_indicators(self, ind1: str, ind2: str) -> bool:
        if self.ind1_values and ind1 not in self.ind1_values and " " not in self.ind1_values:
            return False
        if self.ind2_values and ind2 not in self.ind2_values and " " not in self.ind2_values:
            return False
        return True


FIELD_SPECIFICATIONS: Dict[str, FieldSpec] = {}

def _reg(tag: str, name: str, repeatable: bool = True, ind1: Optional[Dict[str, str]] = None, ind2: Optional[Dict[str, str]] = None, sfs: Optional[Dict[str, str]] = None) -> FieldSpec:
    sf_specs = {}
    if sfs:
        for c, n in sfs.items():
            sf_specs[c] = SubfieldSpec(code=c, name=n)
    spec = FieldSpec(
        tag=tag,
        name=name,
        repeatable=repeatable,
        ind1_values=ind1 or {" ": "Undefined"},
        ind2_values=ind2 or {" ": "Undefined"},
        subfields=sf_specs
    )
    FIELD_SPECIFICATIONS[tag] = spec
    return spec

# 010 - Library of Congress Control Number
_reg("010", "Library of Congress Control Number", repeatable=False, sfs={"a": "LC control number", "b": "NUCMC control number", "z": "Canceled/invalid LC control number"})

# 020 - International Standard Book Number (ISBN)
_reg("020", "International Standard Book Number", repeatable=True, sfs={"a": "ISBN", "c": "Terms of availability", "q": "Qualifying information", "z": "Canceled/invalid ISBN"})

# 022 - International Standard Serial Number (ISSN)
_reg("022", "International Standard Serial Number", repeatable=True, sfs={"a": "ISSN", "l": "ISSN-L", "m": "Canceled ISSN-L", "y": "Incorrect ISSN", "z": "Canceled ISSN"})

# 040 - Cataloging Source
_reg("040", "Cataloging Source", repeatable=False, sfs={"a": "Original cataloging agency", "b": "Language of cataloging", "c": "Transcribing agency", "d": "Modifying agency", "e": "Description conventions"})

# 041 - Language Code
_reg("041", "Language Code", repeatable=True, sfs={"a": "Language code of text/sound track", "b": "Language code of summary or abstract", "d": "Language code of sung/spoken text", "h": "Language code of original/intermediate translations"})

# 050 - Library of Congress Call Number
_reg("050", "Library of Congress Call Number", repeatable=True, sfs={"a": "Classification number", "b": "Item number", "3": "Materials specified"})

# 082 - Dewey Decimal Classification Number
_reg("082", "Dewey Decimal Classification Number", repeatable=True, sfs={"a": "Classification number", "b": "Item number", "2": "Edition number"})

# 100 - Main Entry - Personal Name
_reg("100", "Main Entry - Personal Name", repeatable=False, ind1={"0": "Forename", "1": "Surname", "3": "Family name"}, sfs={"a": "Personal name", "b": "Numeration", "c": "Titles and words associated with a name", "d": "Dates associated with a name", "e": "Relator term", "q": "Fuller form of name", "u": "Affiliation"})

# 110 - Main Entry - Corporate Name
_reg("110", "Main Entry - Corporate Name", repeatable=False, ind1={"1": "Jurisdiction name", "2": "Name in direct order"}, sfs={"a": "Corporate name or jurisdiction name as entry element", "b": "Subordinate unit", "c": "Location of meeting", "d": "Date of meeting or treaty signing", "e": "Relator term"})

# 130 - Main Entry - Uniform Title
_reg("130", "Main Entry - Uniform Title", repeatable=False, sfs={"a": "Uniform title", "l": "Language of a work", "f": "Date of a work", "k": "Form subheading", "s": "Version"})

# 240 - Uniform Title
_reg("240", "Uniform Title", repeatable=False, sfs={"a": "Uniform title", "d": "Date of treaty signing", "l": "Language of a work", "m": "Medium of performance for music", "n": "Number of part/section", "p": "Name of part/section"})

# 245 - Title Statement
_reg("245", "Title Statement", repeatable=False, ind1={"0": "No added entry", "1": "Added entry"}, ind2={"0": "No nonfiling characters", "1": "1 nonfiling character", "2": "2 nonfiling characters", "3": "3 nonfiling characters", "4": "4 nonfiling characters"}, sfs={"a": "Title", "b": "Remainder of title", "c": "Statement of responsibility, etc.", "f": "Inclusive dates", "g": "Bulk dates", "h": "Medium", "n": "Number of part/section", "p": "Name of part/section", "s": "Version"})

# 246 - Varying Form of Title
_reg("246", "Varying Form of Title", repeatable=True, sfs={"a": "Title proper/short title", "b": "Remainder of title", "f": "Date or sequential designation", "g": "Miscellaneous information", "n": "Number of part/section", "p": "Name of part/section"})

# 250 - Edition Statement
_reg("250", "Edition Statement", repeatable=True, sfs={"a": "Edition statement", "b": "Remainder of edition statement", "3": "Materials specified"})

# 260 - Publication, Distribution, etc. (Imprint)
_reg("260", "Publication, Distribution, etc.", repeatable=True, sfs={"a": "Place of publication, distribution, etc.", "b": "Name of publisher, distributor, etc.", "c": "Date of publication, distribution, etc.", "e": "Place of manufacture", "f": "Manufacturer", "g": "Date of manufacture"})

# 264 - Production, Publication, Distribution, Manufacture, and Copyright Notice
_reg("264", "Production, Publication, Distribution, Manufacture", repeatable=True, ind2={"0": "Production", "1": "Publication", "2": "Distribution", "3": "Manufacture", "4": "Copyright notice date"}, sfs={"a": "Place of production, publication, distribution, manufacture", "b": "Name of producer, publisher, distributor, manufacturer", "c": "Date of production, publication, distribution, manufacture"})

# 300 - Physical Description
_reg("300", "Physical Description", repeatable=True, sfs={"a": "Extent", "b": "Other physical details", "c": "Dimensions", "e": "Accompanying material", "f": "Type of unit", "g": "Size of unit", "3": "Materials specified"})

# 336 - Content Type
_reg("336", "Content Type", repeatable=True, sfs={"a": "Content type term", "b": "Content type code", "2": "Source"})

# 337 - Media Type
_reg("337", "Media Type", repeatable=True, sfs={"a": "Media type term", "b": "Media type code", "2": "Source"})

# 338 - Carrier Type
_reg("338", "Carrier Type", repeatable=True, sfs={"a": "Carrier type term", "b": "Carrier type code", "2": "Source"})

# 490 - Series Statement
_reg("490", "Series Statement", repeatable=True, ind1={"0": "Series not traced", "1": "Series traced differently"}, sfs={"a": "Series statement", "v": "Volume/sequential designation", "x": "International Standard Serial Number", "3": "Materials specified"})

# 500 - General Note
_reg("500", "General Note", repeatable=True, sfs={"a": "General note", "3": "Materials specified"})

# 502 - Dissertation Note
_reg("502", "Dissertation Note", repeatable=True, sfs={"a": "Dissertation note", "b": "Degree type", "c": "Name of granting institution", "d": "Year degree granted", "g": "Miscellaneous information"})

# 504 - Bibliography, etc. Note
_reg("504", "Bibliography Note", repeatable=True, sfs={"a": "Bibliography note", "b": "Number of references"})

# 505 - Formatted Contents Note
_reg("505", "Formatted Contents Note", repeatable=True, ind1={"0": "Complete contents", "1": "Incomplete contents", "2": "Partial contents"}, sfs={"a": "Formatted contents note", "g": "Miscellaneous information", "r": "Statement of responsibility", "t": "Title", "u": "Uniform Resource Identifier"})

# 520 - Summary, etc.
_reg("520", "Summary Note", repeatable=True, ind1={" ": "Summary", "0": "Subject", "1": "Review", "2": "Scope and content", "3": "Abstract"}, sfs={"a": "Summary, etc.", "b": "Expansion of summary note", "u": "Uniform Resource Identifier", "3": "Materials specified"})

# 650 - Subject Added Entry - Topical Term
_reg("650", "Subject Added Entry - Topical Term", repeatable=True, ind2={"0": "Library of Congress Subject Headings", "1": "LC subject headings for children's literature", "2": "Medical Subject Headings", "3": "National Agricultural Library subject authority file", "4": "Source not specified", "7": "Source specified in subfield $2"}, sfs={"a": "Topical term or geographic name entry element", "b": "Topical term following geographic name", "c": "Location of event", "d": "Active dates", "e": "Relator term", "v": "Form subdivision", "x": "General subdivision", "y": "Chronological subdivision", "z": "Geographic subdivision", "2": "Source of heading or term"})

# 651 - Subject Added Entry - Geographic Name
_reg("651", "Subject Added Entry - Geographic Name", repeatable=True, sfs={"a": "Geographic name", "v": "Form subdivision", "x": "General subdivision", "y": "Chronological subdivision", "z": "Geographic subdivision"})

# 700 - Added Entry - Personal Name
_reg("700", "Added Entry - Personal Name", repeatable=True, sfs={"a": "Personal name", "b": "Numeration", "c": "Titles and words associated with a name", "d": "Dates associated with a name", "e": "Relator term", "q": "Fuller form of name", "u": "Affiliation", "4": "Relationship code"})

# 710 - Added Entry - Corporate Name
_reg("710", "Added Entry - Corporate Name", repeatable=True, sfs={"a": "Corporate name", "b": "Subordinate unit", "c": "Location of meeting", "d": "Date of meeting", "e": "Relator term"})

# 856 - Electronic Location and Access
_reg("856", "Electronic Location and Access", repeatable=True, ind1={"4": "HTTP"}, ind2={"0": "Resource", "1": "Version of resource", "2": "Related resource"}, sfs={"u": "Uniform Resource Identifier", "y": "Link text", "z": "Public note", "3": "Materials specified", "q": "Electronic format type"})
