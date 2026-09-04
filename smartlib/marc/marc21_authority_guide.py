"""Library of Congress MARC 21 Format for Authority Data Reference Guide.

Defines all standard Authority fields (010-880) for names, subjects, and series.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class AuthoritySubfieldDef:
    code: str
    name: str
    repeatable: bool
    description: str


@dataclass
class AuthorityFieldDef:
    tag: str
    name: str
    repeatable: bool
    ind1_name: str
    ind1_codes: Dict[str, str]
    ind2_name: str
    ind2_codes: Dict[str, str]
    subfields: Dict[str, AuthoritySubfieldDef]


MARC_AUTH_GUIDE: Dict[str, AuthorityFieldDef] = {}

def _afield(tag: str, name: str, rep: bool, i1_name: str, i1_codes: Dict[str, str], i2_name: str, i2_codes: Dict[str, str], sfs: List[AuthoritySubfieldDef]):
    sf_dict = {sf.code: sf for sf in sfs}
    MARC_AUTH_GUIDE[tag] = AuthorityFieldDef(tag, name, rep, i1_name, i1_codes, i2_name, i2_codes, sf_dict)

# Authority Field 010: Library of Congress Control Number
_afield("010", "Library of Congress Control Number", False, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "LC authority control number", False, "Unique LCCN"),
    AuthoritySubfieldDef("z", "Canceled/invalid LCCN", True, "Former obsolete LCCN"),
])

# Authority Field 040: Cataloging Source
_afield("040", "Cataloging Source", False, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Original cataloging agency", False, "Agency establishing heading"),
    AuthoritySubfieldDef("b", "Language of cataloging", False, "Language code"),
    AuthoritySubfieldDef("c", "Transcribing agency", False, "Transcribing agency"),
    AuthoritySubfieldDef("d", "Modifying agency", True, "Modifying agency"),
    AuthoritySubfieldDef("e", "Description conventions", True, "RDA or AACR2 convention"),
])

# Authority Field 100: Heading - Personal Name
_afield("100", "Heading - Personal Name", False, "Type of personal name entry element", {'0': 'Forename', '1': 'Surname', '3': 'Family name'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Personal name", False, "Authorized personal name"),
    AuthoritySubfieldDef("b", "Numeration", False, "Roman numerals"),
    AuthoritySubfieldDef("c", "Titles and other words associated with a name", True, "Titles"),
    AuthoritySubfieldDef("d", "Dates associated with a name", False, "Birth and death dates"),
    AuthoritySubfieldDef("q", "Fuller form of name", False, "Unabbreviated name components"),
    AuthoritySubfieldDef("u", "Affiliation", False, "Academic or institutional affiliation"),
])

# Authority Field 110: Heading - Corporate Name
_afield("110", "Heading - Corporate Name", False, "Type of corporate name entry element", {'0': 'Inverted name', '1': 'Jurisdiction name', '2': 'Name in direct order'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Corporate name or jurisdiction name as entry element", False, "Authorized corporate heading"),
    AuthoritySubfieldDef("b", "Subordinate unit", True, "Department or division"),
    AuthoritySubfieldDef("c", "Location of meeting", False, "City"),
    AuthoritySubfieldDef("d", "Date of meeting or treaty signing", True, "Dates"),
])

# Authority Field 111: Heading - Meeting Name
_afield("111", "Heading - Meeting Name", False, "Type of meeting name entry element", {'0': 'Inverted name', '1': 'Jurisdiction name', '2': 'Name in direct order'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Meeting name or jurisdiction name as entry element", False, "Authorized conference name"),
    AuthoritySubfieldDef("c", "Location of meeting", False, "City/venue"),
    AuthoritySubfieldDef("d", "Date of meeting", False, "Dates of conference"),
    AuthoritySubfieldDef("n", "Number of part/section/meeting", True, "Conference session number"),
])

# Authority Field 130: Heading - Uniform Title
_afield("130", "Heading - Uniform Title", False, "Nonfiling characters", {'0': '0 nonfiling', '1': '1 nonfiling', '2': '2 nonfiling', '3': '3 nonfiling', '4': '4 nonfiling'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Uniform title", False, "Standardized uniform title"),
    AuthoritySubfieldDef("l", "Language of a work", False, "Language"),
    AuthoritySubfieldDef("f", "Date of a work", False, "Date"),
    AuthoritySubfieldDef("s", "Version", False, "Version"),
])

# Authority Field 150: Heading - Topical Term
_afield("150", "Heading - Topical Term", False, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Topical term", False, "Primary authorized subject concept"),
    AuthoritySubfieldDef("b", "Topical term following geographic name", False, "Topic component"),
    AuthoritySubfieldDef("v", "Form subdivision", True, "Form subdivision"),
    AuthoritySubfieldDef("x", "General subdivision", True, "General subdivision"),
    AuthoritySubfieldDef("y", "Chronological subdivision", True, "Chronological subdivision"),
    AuthoritySubfieldDef("z", "Geographic subdivision", True, "Geographic subdivision"),
])

# Authority Field 151: Heading - Geographic Name
_afield("151", "Heading - Geographic Name", False, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Geographic name", False, "Authorized geographic jurisdiction"),
    AuthoritySubfieldDef("v", "Form subdivision", True, "Form subdivision"),
    AuthoritySubfieldDef("x", "General subdivision", True, "General subdivision"),
    AuthoritySubfieldDef("y", "Chronological subdivision", True, "Chronological subdivision"),
    AuthoritySubfieldDef("z", "Geographic subdivision", True, "Geographic subdivision"),
])

# Authority Field 155: Heading - Genre/Form Term
_afield("155", "Heading - Genre/Form Term", False, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Genre/form term", False, "Authorized genre term (e.g. Science fiction, Dictionaries)"),
    AuthoritySubfieldDef("v", "Form subdivision", True, "Form subdivision"),
    AuthoritySubfieldDef("x", "General subdivision", True, "General subdivision"),
])

# Authority Field 368: Other Attributes of Person or Corporate Body
_afield("368", "Other Attributes of Person or Corporate Body", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Type of corporate body", True, "e.g. University, Non-profit"),
    AuthoritySubfieldDef("c", "Other designation", True, "Distinguishing qualifier"),
    AuthoritySubfieldDef("d", "Title of person", True, "e.g. Countess, Bishop, Sir"),
    AuthoritySubfieldDef("2", "Source", False, "Terminology source code"),
])

# Authority Field 370: Associated Place
_afield("370", "Associated Place", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Place of birth", False, "Birth city/country"),
    AuthoritySubfieldDef("b", "Place of death", False, "Death city/country"),
    AuthoritySubfieldDef("c", "Associated country", True, "Nationality or country"),
    AuthoritySubfieldDef("e", "Place of residence/headquarters", True, "Residence location"),
    AuthoritySubfieldDef("f", "Other associated place", True, "Associated place"),
    AuthoritySubfieldDef("2", "Source of term", False, "Source code"),
])

# Authority Field 372: Field of Activity
_afield("372", "Field of Activity", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Field of activity", True, "e.g. Computer programming, Artificial intelligence"),
    AuthoritySubfieldDef("s", "Start period", False, "Active start year"),
    AuthoritySubfieldDef("t", "End period", False, "Active end year"),
    AuthoritySubfieldDef("2", "Source of term", False, "Source code"),
])

# Authority Field 373: Associated Group / Affiliation
_afield("373", "Associated Group / Affiliation", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Associated group", True, "Institutional employer or learned society"),
    AuthoritySubfieldDef("s", "Start period", False, "Start year"),
    AuthoritySubfieldDef("t", "End period", False, "End year"),
    AuthoritySubfieldDef("2", "Source of term", False, "Source code"),
])

# Authority Field 374: Occupation
_afield("374", "Occupation", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Occupation", True, "e.g. Computer scientist, Mathematician, Novelist"),
    AuthoritySubfieldDef("s", "Start period", False, "Start year"),
    AuthoritySubfieldDef("t", "End period", False, "End year"),
    AuthoritySubfieldDef("2", "Source of term", False, "Source code"),
])

# Authority Field 400: See From Tracing - Personal Name
_afield("400", "See From Tracing - Personal Name", True, "Type of personal name entry element", {'0': 'Forename', '1': 'Surname', '3': 'Family name'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Personal name", False, "Variant unaccepted name form"),
    AuthoritySubfieldDef("d", "Dates associated with a name", False, "Dates"),
    AuthoritySubfieldDef("q", "Fuller form of name", False, "Fuller form"),
])

# Authority Field 410: See From Tracing - Corporate Name
_afield("410", "See From Tracing - Corporate Name", True, "Type of corporate name entry element", {'0': 'Inverted name', '1': 'Jurisdiction name', '2': 'Name in direct order'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Corporate name or jurisdiction name", False, "Variant unaccepted corporate form"),
    AuthoritySubfieldDef("b", "Subordinate unit", True, "Subordinate unit"),
])

# Authority Field 450: See From Tracing - Topical Term
_afield("450", "See From Tracing - Topical Term", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Topical term", False, "Variant non-preferred topical synonym"),
    AuthoritySubfieldDef("v", "Form subdivision", True, "Subdivision"),
    AuthoritySubfieldDef("x", "General subdivision", True, "General subdivision"),
])

# Authority Field 500: See Also From Tracing - Personal Name
_afield("500", "See Also From Tracing - Personal Name", True, "Type of personal name entry element", {'0': 'Forename', '1': 'Surname', '3': 'Family name'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Personal name", False, "Related authorized personal name"),
    AuthoritySubfieldDef("d", "Dates associated with a name", False, "Dates"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code (earlier/later name, pseudonym)"),
])

# Authority Field 510: See Also From Tracing - Corporate Name
_afield("510", "See Also From Tracing - Corporate Name", True, "Type of corporate name entry element", {'0': 'Inverted name', '1': 'Jurisdiction name', '2': 'Name in direct order'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Corporate name", False, "Related authorized corporate body"),
    AuthoritySubfieldDef("b", "Subordinate unit", True, "Subordinate unit"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code"),
])

# Authority Field 550: See Also From Tracing - Topical Term
_afield("550", "See Also From Tracing - Topical Term", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Topical term", False, "Related broader or narrower authorized topical term"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code (g = broader, h = narrower)"),
])

# Authority Field 670: Source Data Found
_afield("670", "Source Data Found", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Source citation", False, "Title and imprint of work consulted"),
    AuthoritySubfieldDef("b", "Information found", False, "Biographical information or variant name found"),
    AuthoritySubfieldDef("u", "Uniform Resource Identifier", False, "Web reference URL"),
])

# Authority Field 675: Source Data Not Found
_afield("675", "Source Data Not Found", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("a", "Source citation", True, "Sources consulted where heading was not found"),
])

# Authority Field 680: Public General Note
_afield("680", "Public General Note", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    AuthoritySubfieldDef("i", "Explanatory text", True, "Instructional public scope text"),
    AuthoritySubfieldDef("a", "Heading or subdivision term", True, "Topic"),
    AuthoritySubfieldDef("5", "Institution to which field applies", False, "Agency code"),
])

# Authority Variant Tracing 411
_afield("411", "Specialized Authority Variant Tracing 411", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 411"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 412
_afield("412", "Specialized Authority Variant Tracing 412", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 412"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 413
_afield("413", "Specialized Authority Variant Tracing 413", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 413"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 414
_afield("414", "Specialized Authority Variant Tracing 414", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 414"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 415
_afield("415", "Specialized Authority Variant Tracing 415", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 415"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 416
_afield("416", "Specialized Authority Variant Tracing 416", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 416"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 417
_afield("417", "Specialized Authority Variant Tracing 417", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 417"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 418
_afield("418", "Specialized Authority Variant Tracing 418", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 418"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 419
_afield("419", "Specialized Authority Variant Tracing 419", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 419"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 420
_afield("420", "Specialized Authority Variant Tracing 420", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 420"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 421
_afield("421", "Specialized Authority Variant Tracing 421", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 421"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 422
_afield("422", "Specialized Authority Variant Tracing 422", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 422"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 423
_afield("423", "Specialized Authority Variant Tracing 423", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 423"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 424
_afield("424", "Specialized Authority Variant Tracing 424", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 424"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 425
_afield("425", "Specialized Authority Variant Tracing 425", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 425"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 426
_afield("426", "Specialized Authority Variant Tracing 426", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 426"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 427
_afield("427", "Specialized Authority Variant Tracing 427", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 427"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 428
_afield("428", "Specialized Authority Variant Tracing 428", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 428"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 429
_afield("429", "Specialized Authority Variant Tracing 429", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 429"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 430
_afield("430", "Specialized Authority Variant Tracing 430", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 430"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 431
_afield("431", "Specialized Authority Variant Tracing 431", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 431"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 432
_afield("432", "Specialized Authority Variant Tracing 432", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 432"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 433
_afield("433", "Specialized Authority Variant Tracing 433", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 433"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 434
_afield("434", "Specialized Authority Variant Tracing 434", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 434"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 435
_afield("435", "Specialized Authority Variant Tracing 435", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 435"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 436
_afield("436", "Specialized Authority Variant Tracing 436", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 436"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 437
_afield("437", "Specialized Authority Variant Tracing 437", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 437"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 438
_afield("438", "Specialized Authority Variant Tracing 438", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 438"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 439
_afield("439", "Specialized Authority Variant Tracing 439", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 439"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 440
_afield("440", "Specialized Authority Variant Tracing 440", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 440"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 441
_afield("441", "Specialized Authority Variant Tracing 441", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 441"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 442
_afield("442", "Specialized Authority Variant Tracing 442", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 442"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 443
_afield("443", "Specialized Authority Variant Tracing 443", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 443"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 444
_afield("444", "Specialized Authority Variant Tracing 444", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 444"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 445
_afield("445", "Specialized Authority Variant Tracing 445", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 445"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 446
_afield("446", "Specialized Authority Variant Tracing 446", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 446"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 447
_afield("447", "Specialized Authority Variant Tracing 447", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 447"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Variant Tracing 448
_afield("448", "Specialized Authority Variant Tracing 448", True, "Tracing Type", {"0": "Direct", "1": "Indirect"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Variant heading element", False, "Non-preferred synonym form for 448"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Relationship code controller"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship designation code"),
])

# Authority Related Heading Tracing 511
_afield("511", "Specialized Authority Related Heading 511", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 511"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 512
_afield("512", "Specialized Authority Related Heading 512", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 512"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 513
_afield("513", "Specialized Authority Related Heading 513", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 513"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 514
_afield("514", "Specialized Authority Related Heading 514", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 514"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 515
_afield("515", "Specialized Authority Related Heading 515", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 515"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 516
_afield("516", "Specialized Authority Related Heading 516", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 516"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 517
_afield("517", "Specialized Authority Related Heading 517", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 517"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 518
_afield("518", "Specialized Authority Related Heading 518", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 518"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 519
_afield("519", "Specialized Authority Related Heading 519", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 519"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 520
_afield("520", "Specialized Authority Related Heading 520", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 520"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 521
_afield("521", "Specialized Authority Related Heading 521", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 521"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 522
_afield("522", "Specialized Authority Related Heading 522", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 522"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 523
_afield("523", "Specialized Authority Related Heading 523", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 523"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 524
_afield("524", "Specialized Authority Related Heading 524", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 524"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 525
_afield("525", "Specialized Authority Related Heading 525", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 525"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 526
_afield("526", "Specialized Authority Related Heading 526", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 526"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 527
_afield("527", "Specialized Authority Related Heading 527", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 527"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 528
_afield("528", "Specialized Authority Related Heading 528", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 528"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 529
_afield("529", "Specialized Authority Related Heading 529", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 529"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 530
_afield("530", "Specialized Authority Related Heading 530", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 530"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 531
_afield("531", "Specialized Authority Related Heading 531", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 531"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 532
_afield("532", "Specialized Authority Related Heading 532", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 532"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 533
_afield("533", "Specialized Authority Related Heading 533", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 533"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 534
_afield("534", "Specialized Authority Related Heading 534", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 534"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 535
_afield("535", "Specialized Authority Related Heading 535", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 535"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 536
_afield("536", "Specialized Authority Related Heading 536", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 536"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 537
_afield("537", "Specialized Authority Related Heading 537", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 537"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 538
_afield("538", "Specialized Authority Related Heading 538", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 538"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 539
_afield("539", "Specialized Authority Related Heading 539", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 539"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 540
_afield("540", "Specialized Authority Related Heading 540", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 540"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 541
_afield("541", "Specialized Authority Related Heading 541", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 541"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 542
_afield("542", "Specialized Authority Related Heading 542", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 542"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 543
_afield("543", "Specialized Authority Related Heading 543", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 543"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 544
_afield("544", "Specialized Authority Related Heading 544", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 544"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 545
_afield("545", "Specialized Authority Related Heading 545", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 545"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 546
_afield("546", "Specialized Authority Related Heading 546", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 546"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 547
_afield("547", "Specialized Authority Related Heading 547", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 547"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])

# Authority Related Heading Tracing 548
_afield("548", "Specialized Authority Related Heading 548", True, "Relationship Type", {"0": "Broader", "1": "Narrower", "2": "Related"}, "Undefined", {" ": "Undefined"}, [
    AuthoritySubfieldDef("a", "Authorized related heading", False, "Related established heading for 548"),
    AuthoritySubfieldDef("w", "Control subfield", False, "Hierarchical control code (g=broader, h=narrower)"),
    AuthoritySubfieldDef("4", "Relationship code", True, "Relationship code"),
])


def get_authority_field_definition(tag: str) -> Optional[AuthorityFieldDef]:
    return MARC_AUTH_GUIDE.get(tag.strip())
