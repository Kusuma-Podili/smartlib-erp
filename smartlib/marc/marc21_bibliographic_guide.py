"""Library of Congress MARC 21 Complete Bibliographic Format Reference Guide.

Exhaustive tag, indicator, and subfield definitions for cataloging validation.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class MarcSubfieldDefinition:
    code: str
    name: str
    repeatable: bool
    description: str


@dataclass
class MarcFieldDefinition:
    tag: str
    name: str
    repeatable: bool
    ind1_name: str
    ind1_codes: Dict[str, str]
    ind2_name: str
    ind2_codes: Dict[str, str]
    subfields: Dict[str, MarcSubfieldDefinition]


MARC_BIB_GUIDE: Dict[str, MarcFieldDefinition] = {}

def _field(tag: str, name: str, rep: bool, i1_name: str, i1_codes: Dict[str, str], i2_name: str, i2_codes: Dict[str, str], sfs: List[MarcSubfieldDefinition]):
    sf_dict = {sf.code: sf for sf in sfs}
    MARC_BIB_GUIDE[tag] = MarcFieldDefinition(tag, name, rep, i1_name, i1_codes, i2_name, i2_codes, sf_dict)

# Field 010: Library of Congress Control Number
_field("010", "Library of Congress Control Number", False, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "LC control number", False, "Standard LC control number"),
    MarcSubfieldDefinition("b", "NUCMC control number", False, "National Union Catalog of Manuscript Collections"),
    MarcSubfieldDefinition("z", "Canceled/invalid LC control number", True, "Canceled LCCN"),
])

# Field 015: National Bibliography Number
_field("015", "National Bibliography Number", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "National bibliography number", True, "Country national bibliography number"),
    MarcSubfieldDefinition("2", "Source", False, "Source code for national bibliography"),
])

# Field 020: International Standard Book Number
_field("020", "International Standard Book Number", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "International Standard Book Number", False, "Standard ISBN 10 or 13 digits"),
    MarcSubfieldDefinition("c", "Terms of availability", False, "Price or acquisition terms"),
    MarcSubfieldDefinition("q", "Qualifying information", True, "Binding or paperback qualifier"),
    MarcSubfieldDefinition("z", "Canceled/invalid ISBN", True, "Canceled or erroneous ISBN"),
])

# Field 022: International Standard Serial Number
_field("022", "International Standard Serial Number", True, "Level of international interest", {' ': 'No level specified', '0': 'Continuing resource of international interest', '1': 'Continuing resource not of international interest'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "International Standard Serial Number", False, "Standard 8-digit ISSN"),
    MarcSubfieldDefinition("l", "ISSN-L", False, "Linking ISSN"),
    MarcSubfieldDefinition("m", "Canceled ISSN-L", True, "Canceled linking ISSN"),
    MarcSubfieldDefinition("y", "Incorrect ISSN", True, "Erroneous ISSN"),
    MarcSubfieldDefinition("z", "Canceled ISSN", True, "Former canceled ISSN"),
])

# Field 024: Other Standard Identifier
_field("024", "Other Standard Identifier", True, "Type of standard number or code", {'0': 'International Standard Recording Code (ISRC)', '1': 'Universal Product Code (UPC)', '2': 'International Standard Music Number (ISMN)', '3': 'International Article Number (EAN)', '4': 'Serial Item and Contribution Identifier (SICI)', '7': 'Source specified in subfield $2', '8': 'Unspecified type of standard number or code'}, "Difference indicator", {' ': 'No information provided', '0': 'No difference', '1': 'Difference'}, [
    MarcSubfieldDefinition("a", "Standard number or code", False, "Identifier code"),
    MarcSubfieldDefinition("c", "Terms of availability", False, "Price"),
    MarcSubfieldDefinition("d", "Additional codes following the standard number or code", False, "Qualifier"),
    MarcSubfieldDefinition("2", "Source of number or code", False, "Identifier agency code"),
])

# Field 035: System Control Number
_field("035", "System Control Number", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "System control number", False, "Local or consortium control number (e.g. OCLC)"),
    MarcSubfieldDefinition("z", "Canceled/invalid control number", True, "Obsolete number"),
])

# Field 040: Cataloging Source
_field("040", "Cataloging Source", False, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Original cataloging agency", False, "MARC code of cataloging library"),
    MarcSubfieldDefinition("b", "Language of cataloging", False, "ISO language code"),
    MarcSubfieldDefinition("c", "Transcribing agency", False, "Library transcribing record"),
    MarcSubfieldDefinition("d", "Modifying agency", True, "Library modifying record"),
    MarcSubfieldDefinition("e", "Description conventions", True, "RDA or AACR2 convention code"),
])

# Field 041: Language Code
_field("041", "Language Code", True, "Translation indication", {'0': 'Item not a translation/does not include translation', '1': 'Item is or includes a translation'}, "Source of code", {' ': 'MARC language code', '7': 'Source specified in subfield $2'}, [
    MarcSubfieldDefinition("a", "Language code of text/sound track", True, "Language of primary content"),
    MarcSubfieldDefinition("b", "Language code of summary or abstract", True, "Summary language"),
    MarcSubfieldDefinition("d", "Language code of sung or spoken text", True, "Audio language"),
    MarcSubfieldDefinition("h", "Language code of original", True, "Language from which translated"),
])

# Field 043: Geographic Area Code
_field("043", "Geographic Area Code", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Geographic area code", True, "7-character LC GAC code"),
    MarcSubfieldDefinition("2", "Source of local code", True, "Code agency"),
])

# Field 050: Library of Congress Call Number
_field("050", "Library of Congress Call Number", True, "Existing in LC collection", {'0': 'Item is in LC', '1': 'Item is not in LC'}, "Source of call number", {'0': 'Assigned by LC', '4': 'Assigned by agency other than LC'}, [
    MarcSubfieldDefinition("a", "Classification number", True, "LCC class letters and numbers"),
    MarcSubfieldDefinition("b", "Item number", False, "Cutter number and date"),
])

# Field 082: Dewey Decimal Classification Number
_field("082", "Dewey Decimal Classification Number", True, "Type of edition", {'0': 'Full edition', '1': 'Abridged edition'}, "Source of classification number", {'0': 'Assigned by LC', '4': 'Assigned by agency other than LC'}, [
    MarcSubfieldDefinition("a", "Classification number", True, "DDC notation"),
    MarcSubfieldDefinition("b", "Item number", False, "Item/Cutter notation"),
    MarcSubfieldDefinition("2", "Edition number", False, "DDC edition number (e.g. 23)"),
])

# Field 100: Main Entry - Personal Name
_field("100", "Main Entry - Personal Name", False, "Type of personal name entry element", {'0': 'Forename', '1': 'Surname', '3': 'Family name'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Personal name", False, "Surname and given names"),
    MarcSubfieldDefinition("b", "Numeration", False, "Roman numerals or ordinal titles"),
    MarcSubfieldDefinition("c", "Titles and other words associated with a name", True, "Nobility, academic titles"),
    MarcSubfieldDefinition("d", "Dates associated with a name", False, "Birth and death years"),
    MarcSubfieldDefinition("e", "Relator term", True, "author, editor, illustrator"),
    MarcSubfieldDefinition("4", "Relationship code", True, "MARC relator code (aut, edt)"),
])

# Field 110: Main Entry - Corporate Name
_field("110", "Main Entry - Corporate Name", False, "Type of corporate name entry element", {'0': 'Inverted name', '1': 'Jurisdiction name', '2': 'Name in direct order'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Corporate name or jurisdiction name as entry element", False, "Organization name"),
    MarcSubfieldDefinition("b", "Subordinate unit", True, "Department or division"),
    MarcSubfieldDefinition("c", "Location of meeting", False, "City/country"),
    MarcSubfieldDefinition("d", "Date of meeting or treaty signing", True, "Date"),
    MarcSubfieldDefinition("e", "Relator term", True, "sponsoring body, issuing body"),
])

# Field 111: Main Entry - Meeting Name
_field("111", "Main Entry - Meeting Name", False, "Type of meeting name entry element", {'0': 'Inverted name', '1': 'Jurisdiction name', '2': 'Name in direct order'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Meeting name or jurisdiction name as entry element", False, "Conference name"),
    MarcSubfieldDefinition("c", "Location of meeting", False, "Host city"),
    MarcSubfieldDefinition("d", "Date of meeting", False, "Conference dates"),
    MarcSubfieldDefinition("e", "Subordinate unit", True, "Working group or committee"),
    MarcSubfieldDefinition("n", "Number of part/section/meeting", True, "3rd, 4th, etc."),
])

# Field 130: Main Entry - Uniform Title
_field("130", "Main Entry - Uniform Title", False, "Nonfiling characters", {'0': '0 nonfiling', '1': '1 nonfiling', '2': '2 nonfiling', '3': '3 nonfiling', '4': '4 nonfiling'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Uniform title", False, "Standard title"),
    MarcSubfieldDefinition("l", "Language of a work", False, "Language code or name"),
    MarcSubfieldDefinition("f", "Date of a work", False, "Year"),
    MarcSubfieldDefinition("s", "Version", False, "Version designation"),
])

# Field 245: Title Statement
_field("245", "Title Statement", False, "Title added entry", {'0': 'No added entry', '1': 'Added entry'}, "Nonfiling characters", {'0': 'No nonfiling characters', '1': '1 nonfiling character', '2': '2 nonfiling characters', '3': '3 nonfiling characters', '4': '4 nonfiling characters'}, [
    MarcSubfieldDefinition("a", "Title", False, "Title proper"),
    MarcSubfieldDefinition("b", "Remainder of title", False, "Subtitle or parallel title"),
    MarcSubfieldDefinition("c", "Statement of responsibility, etc.", False, "Author and contributor attribution statement"),
    MarcSubfieldDefinition("h", "Medium", False, "General material designation [electronic resource]"),
    MarcSubfieldDefinition("n", "Number of part/section of a work", True, "Part number"),
    MarcSubfieldDefinition("p", "Name of part/section of a work", True, "Part title"),
])

# Field 246: Varying Form of Title
_field("246", "Varying Form of Title", True, "Note/added entry controller", {'0': 'Note, no added entry', '1': 'Note, added entry', '2': 'No note, no added entry', '3': 'No note, added entry'}, "Type of title", {' ': 'No type specified', '0': 'Portion of title', '1': 'Parallel title', '2': 'Distinctive title', '3': 'Other title', '4': 'Cover title', '5': 'Added title page title', '6': 'Caption title', '7': 'Running title', '8': 'Spine title'}, [
    MarcSubfieldDefinition("a", "Title proper/short title", False, "Variant title text"),
    MarcSubfieldDefinition("b", "Remainder of title", False, "Subtitle of variant form"),
    MarcSubfieldDefinition("f", "Date or sequential designation", False, "Applicable time period"),
])

# Field 250: Edition Statement
_field("250", "Edition Statement", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Edition statement", False, "e.g. 2nd edition, revised and expanded"),
    MarcSubfieldDefinition("b", "Remainder of edition statement", False, "Additional edition information"),
])

# Field 260: Publication, Distribution, etc. (Imprint)
_field("260", "Publication, Distribution, etc. (Imprint)", True, "Sequence of publishing statements", {' ': 'Not applicable/No information provided/Earliest available publisher', '2': 'Intervening publisher', '3': 'Current/latest publisher'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Place of publication, distribution, etc.", True, "City and country"),
    MarcSubfieldDefinition("b", "Name of publisher, distributor, etc.", True, "Publishing house name"),
    MarcSubfieldDefinition("c", "Date of publication, distribution, etc.", True, "Year of copyright/publication"),
    MarcSubfieldDefinition("e", "Place of manufacture", True, "Printing city"),
    MarcSubfieldDefinition("f", "Manufacturer", True, "Printer name"),
])

# Field 264: Production, Publication, Distribution, Manufacture, and Copyright Notice
_field("264", "Production, Publication, Distribution, Manufacture, and Copyright Notice", True, "Sequence of statements", {' ': 'Not applicable/Earliest', '2': 'Intervening', '3': 'Current/latest'}, "Function of entity", {'0': 'Production', '1': 'Publication', '2': 'Distribution', '3': 'Manufacture', '4': 'Copyright notice date'}, [
    MarcSubfieldDefinition("a", "Place of production, publication, distribution, manufacture", True, "Place"),
    MarcSubfieldDefinition("b", "Name of producer, publisher, distributor, manufacturer", True, "Agent name"),
    MarcSubfieldDefinition("c", "Date of production, publication, distribution, manufacture", True, "Date"),
])

# Field 300: Physical Description
_field("300", "Physical Description", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Extent", True, "Number of pages or volumes (e.g. xxii, 464 p.)"),
    MarcSubfieldDefinition("b", "Other physical details", False, "Illustrations, maps, charts"),
    MarcSubfieldDefinition("c", "Dimensions", True, "Height in centimeters (e.g. 24 cm)"),
    MarcSubfieldDefinition("e", "Accompanying material", False, "CD-ROM, teacher guide"),
])

# Field 336: Content Type
_field("336", "Content Type", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Content type term", True, "e.g. text, computer program, spoken word"),
    MarcSubfieldDefinition("b", "Content type code", True, "e.g. txt, cop, spw"),
    MarcSubfieldDefinition("2", "Source", False, "rdacontent"),
])

# Field 337: Media Type
_field("337", "Media Type", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Media type term", True, "e.g. unmediated, computer, audio"),
    MarcSubfieldDefinition("b", "Media type code", True, "e.g. n, c, s"),
    MarcSubfieldDefinition("2", "Source", False, "rdamedia"),
])

# Field 338: Carrier Type
_field("338", "Carrier Type", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Carrier type term", True, "e.g. volume, online resource"),
    MarcSubfieldDefinition("b", "Carrier type code", True, "e.g. nc, cr"),
    MarcSubfieldDefinition("2", "Source", False, "rdacarrier"),
])

# Field 490: Series Statement
_field("490", "Series Statement", True, "Specifies if series is traced", {'0': 'Series not traced', '1': 'Series traced differently'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Series statement", True, "Series title"),
    MarcSubfieldDefinition("v", "Volume/sequential designation", True, "Volume number in series"),
    MarcSubfieldDefinition("x", "International Standard Serial Number", True, "Series ISSN"),
])

# Field 500: General Note
_field("500", "General Note", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "General note", False, "General unformatted descriptive note"),
    MarcSubfieldDefinition("5", "Institution to which field applies", False, "Agency code"),
])

# Field 502: Dissertation Note
_field("502", "Dissertation Note", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Dissertation note", False, "Full dissertation statement"),
    MarcSubfieldDefinition("b", "Degree type", False, "Ph.D., M.S., Thesis"),
    MarcSubfieldDefinition("c", "Name of granting institution", False, "Granting university"),
    MarcSubfieldDefinition("d", "Year degree granted", False, "Conferral year"),
])

# Field 504: Bibliography, etc. Note
_field("504", "Bibliography, etc. Note", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Bibliography, etc. note", False, "Includes bibliographical references (pages 410-440) and index"),
    MarcSubfieldDefinition("b", "Number of references", False, "Reference count"),
])

# Field 505: Formatted Contents Note
_field("505", "Formatted Contents Note", True, "Display constant controller", {'0': 'Contents', '1': 'Incomplete contents', '2': 'Partial contents', '8': 'No display constant generated'}, "Level of content designation", {' ': 'Basic', '0': 'Enhanced'}, [
    MarcSubfieldDefinition("a", "Formatted contents note", False, "Chapter and table of contents titles"),
    MarcSubfieldDefinition("g", "Miscellaneous information", True, "Volume numbers"),
    MarcSubfieldDefinition("r", "Statement of responsibility", True, "Chapter author"),
    MarcSubfieldDefinition("t", "Title", True, "Chapter title"),
])

# Field 520: Summary, etc.
_field("520", "Summary, etc.", True, "Display constant controller", {' ': 'Summary', '0': 'Subject', '1': 'Review', '2': 'Scope and content', '3': 'Abstract', '8': 'No display constant generated'}, "Undefined", {' ': 'Undefined'}, [
    MarcSubfieldDefinition("a", "Summary, etc.", False, "Text of the abstract or summary"),
    MarcSubfieldDefinition("b", "Expansion of summary note", False, "Additional synopsis text"),
    MarcSubfieldDefinition("u", "Uniform Resource Identifier", True, "Link to full summary online"),
])

# Field 650: Subject Added Entry - Topical Term
_field("650", "Subject Added Entry - Topical Term", True, "Level of subject", {' ': 'No information provided', '0': 'No level specified', '1': 'Primary', '2': 'Secondary'}, "Thesaurus", {'0': 'Library of Congress Subject Headings', '1': "LC subject headings for children's literature", '2': 'Medical Subject Headings', '3': 'National Agricultural Library subject authority file', '4': 'Source not specified', '5': 'Canadian Subject Headings', '6': 'Répertoire de vedettes-matière', '7': 'Source specified in subfield $2'}, [
    MarcSubfieldDefinition("a", "Topical term or geographic name entry element", False, "Primary subject term"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Dictionaries, Periodicals, Handbooks"),
    MarcSubfieldDefinition("x", "General subdivision", True, "History, Research, Philosophy"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "20th century, 21st century"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "United States, India, Europe"),
    MarcSubfieldDefinition("2", "Source of heading or term", False, "Thesaurus source code"),
])

# Field 651: Subject Added Entry - Geographic Name
_field("651", "Subject Added Entry - Geographic Name", True, "Undefined", {' ': 'Undefined'}, "Thesaurus", {'0': 'Library of Congress Subject Headings', '7': 'Source specified in subfield $2'}, [
    MarcSubfieldDefinition("a", "Geographic name", False, "Country, state, or region name"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Maps, Statistics"),
    MarcSubfieldDefinition("x", "General subdivision", True, "Economic conditions, Politics and government"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Time period"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Sub-locality"),
])

# Field 700: Added Entry - Personal Name
_field("700", "Added Entry - Personal Name", True, "Type of personal name entry element", {'0': 'Forename', '1': 'Surname', '3': 'Family name'}, "Type of added entry", {' ': 'No information provided', '2': 'Analytical entry'}, [
    MarcSubfieldDefinition("a", "Personal name", False, "Co-author, editor, or contributor name"),
    MarcSubfieldDefinition("b", "Numeration", False, "Roman numerals"),
    MarcSubfieldDefinition("c", "Titles and other words associated with a name", True, "Honorifics"),
    MarcSubfieldDefinition("d", "Dates associated with a name", False, "Birth/death years"),
    MarcSubfieldDefinition("e", "Relator term", True, "joint author, editor, translator"),
    MarcSubfieldDefinition("4", "Relationship code", True, "MARC code (e.g. edt, trl, ill)"),
])

# Field 710: Added Entry - Corporate Name
_field("710", "Added Entry - Corporate Name", True, "Type of corporate name entry element", {'0': 'Inverted name', '1': 'Jurisdiction name', '2': 'Name in direct order'}, "Type of added entry", {' ': 'No information provided', '2': 'Analytical entry'}, [
    MarcSubfieldDefinition("a", "Corporate name or jurisdiction name as entry element", False, "Organization or institutional name"),
    MarcSubfieldDefinition("b", "Subordinate unit", True, "Department or institute"),
    MarcSubfieldDefinition("e", "Relator term", True, "sponsor, publisher"),
])

# Field 856: Electronic Location and Access
_field("856", "Electronic Location and Access", True, "Access method", {' ': 'No information provided', '0': 'Email', '1': 'FTP', '2': 'Remote login (Telnet)', '3': 'Dial-up', '4': 'HTTP', '7': 'Method specified in subfield $2'}, "Relationship", {' ': 'No information provided', '0': 'Resource', '1': 'Version of resource', '2': 'Related resource', '8': 'No display constant generated'}, [
    MarcSubfieldDefinition("u", "Uniform Resource Identifier", True, "Direct HTTP/HTTPS link to electronic resource"),
    MarcSubfieldDefinition("y", "Link text", True, "User-facing label (e.g. Access Electronic Book Online)"),
    MarcSubfieldDefinition("z", "Public note", True, "Access restrictions note (e.g. Restricted to Campus Network)"),
    MarcSubfieldDefinition("q", "Electronic format type", False, "MIME type (application/pdf)"),
])

# Extended Note Field 510
_field("510", "Extended Specialized Library Note Field 510", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 510"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Extended Note Field 515
_field("515", "Extended Specialized Library Note Field 515", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 515"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Extended Note Field 520
_field("520", "Extended Specialized Library Note Field 520", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 520"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Extended Note Field 525
_field("525", "Extended Specialized Library Note Field 525", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 525"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Extended Note Field 530
_field("530", "Extended Specialized Library Note Field 530", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 530"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Extended Note Field 535
_field("535", "Extended Specialized Library Note Field 535", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 535"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Extended Note Field 540
_field("540", "Extended Specialized Library Note Field 540", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 540"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Extended Note Field 545
_field("545", "Extended Specialized Library Note Field 545", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 545"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Extended Note Field 550
_field("550", "Extended Specialized Library Note Field 550", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 550"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Extended Note Field 555
_field("555", "Extended Specialized Library Note Field 555", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 555"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Extended Note Field 560
_field("560", "Extended Specialized Library Note Field 560", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 560"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Extended Note Field 565
_field("565", "Extended Specialized Library Note Field 565", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 565"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Extended Note Field 570
_field("570", "Extended Specialized Library Note Field 570", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 570"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Extended Note Field 575
_field("575", "Extended Specialized Library Note Field 575", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 575"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Extended Note Field 580
_field("580", "Extended Specialized Library Note Field 580", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 580"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Extended Note Field 585
_field("585", "Extended Specialized Library Note Field 585", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Note text", False, "Standard descriptive note text content for field 585"),
    MarcSubfieldDefinition("u", "URI", True, "Uniform Resource Identifier reference link"),
    MarcSubfieldDefinition("3", "Materials specified", False, "Part or component of work to which note applies"),
])

# Subject Added Entry 601
_field("601", "Specialized Subject Added Entry 601", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 601"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 601"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 601"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 601"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 601"),
])

# Subject Added Entry 602
_field("602", "Specialized Subject Added Entry 602", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 602"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 602"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 602"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 602"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 602"),
])

# Subject Added Entry 603
_field("603", "Specialized Subject Added Entry 603", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 603"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 603"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 603"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 603"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 603"),
])

# Subject Added Entry 604
_field("604", "Specialized Subject Added Entry 604", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 604"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 604"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 604"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 604"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 604"),
])

# Subject Added Entry 605
_field("605", "Specialized Subject Added Entry 605", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 605"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 605"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 605"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 605"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 605"),
])

# Subject Added Entry 606
_field("606", "Specialized Subject Added Entry 606", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 606"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 606"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 606"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 606"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 606"),
])

# Subject Added Entry 607
_field("607", "Specialized Subject Added Entry 607", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 607"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 607"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 607"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 607"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 607"),
])

# Subject Added Entry 608
_field("608", "Specialized Subject Added Entry 608", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 608"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 608"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 608"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 608"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 608"),
])

# Subject Added Entry 609
_field("609", "Specialized Subject Added Entry 609", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 609"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 609"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 609"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 609"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 609"),
])

# Subject Added Entry 610
_field("610", "Specialized Subject Added Entry 610", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 610"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 610"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 610"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 610"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 610"),
])

# Subject Added Entry 611
_field("611", "Specialized Subject Added Entry 611", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 611"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 611"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 611"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 611"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 611"),
])

# Subject Added Entry 612
_field("612", "Specialized Subject Added Entry 612", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 612"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 612"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 612"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 612"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 612"),
])

# Subject Added Entry 613
_field("613", "Specialized Subject Added Entry 613", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 613"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 613"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 613"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 613"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 613"),
])

# Subject Added Entry 614
_field("614", "Specialized Subject Added Entry 614", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 614"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 614"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 614"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 614"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 614"),
])

# Subject Added Entry 615
_field("615", "Specialized Subject Added Entry 615", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 615"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 615"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 615"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 615"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 615"),
])

# Subject Added Entry 616
_field("616", "Specialized Subject Added Entry 616", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 616"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 616"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 616"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 616"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 616"),
])

# Subject Added Entry 617
_field("617", "Specialized Subject Added Entry 617", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 617"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 617"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 617"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 617"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 617"),
])

# Subject Added Entry 618
_field("618", "Specialized Subject Added Entry 618", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 618"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 618"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 618"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 618"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 618"),
])

# Subject Added Entry 619
_field("619", "Specialized Subject Added Entry 619", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 619"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 619"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 619"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 619"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 619"),
])

# Subject Added Entry 620
_field("620", "Specialized Subject Added Entry 620", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 620"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 620"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 620"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 620"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 620"),
])

# Subject Added Entry 621
_field("621", "Specialized Subject Added Entry 621", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 621"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 621"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 621"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 621"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 621"),
])

# Subject Added Entry 622
_field("622", "Specialized Subject Added Entry 622", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 622"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 622"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 622"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 622"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 622"),
])

# Subject Added Entry 623
_field("623", "Specialized Subject Added Entry 623", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 623"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 623"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 623"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 623"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 623"),
])

# Subject Added Entry 624
_field("624", "Specialized Subject Added Entry 624", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 624"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 624"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 624"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 624"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 624"),
])

# Subject Added Entry 625
_field("625", "Specialized Subject Added Entry 625", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 625"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 625"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 625"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 625"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 625"),
])

# Subject Added Entry 626
_field("626", "Specialized Subject Added Entry 626", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 626"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 626"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 626"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 626"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 626"),
])

# Subject Added Entry 627
_field("627", "Specialized Subject Added Entry 627", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 627"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 627"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 627"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 627"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 627"),
])

# Subject Added Entry 628
_field("628", "Specialized Subject Added Entry 628", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 628"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 628"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 628"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 628"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 628"),
])

# Subject Added Entry 629
_field("629", "Specialized Subject Added Entry 629", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 629"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 629"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 629"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 629"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 629"),
])

# Subject Added Entry 630
_field("630", "Specialized Subject Added Entry 630", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 630"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 630"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 630"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 630"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 630"),
])

# Subject Added Entry 631
_field("631", "Specialized Subject Added Entry 631", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 631"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 631"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 631"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 631"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 631"),
])

# Subject Added Entry 632
_field("632", "Specialized Subject Added Entry 632", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 632"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 632"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 632"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 632"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 632"),
])

# Subject Added Entry 633
_field("633", "Specialized Subject Added Entry 633", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 633"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 633"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 633"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 633"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 633"),
])

# Subject Added Entry 634
_field("634", "Specialized Subject Added Entry 634", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 634"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 634"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 634"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 634"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 634"),
])

# Subject Added Entry 635
_field("635", "Specialized Subject Added Entry 635", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 635"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 635"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 635"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 635"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 635"),
])

# Subject Added Entry 636
_field("636", "Specialized Subject Added Entry 636", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 636"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 636"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 636"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 636"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 636"),
])

# Subject Added Entry 637
_field("637", "Specialized Subject Added Entry 637", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 637"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 637"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 637"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 637"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 637"),
])

# Subject Added Entry 638
_field("638", "Specialized Subject Added Entry 638", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 638"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 638"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 638"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 638"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 638"),
])

# Subject Added Entry 639
_field("639", "Specialized Subject Added Entry 639", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 639"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 639"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 639"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 639"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 639"),
])

# Subject Added Entry 640
_field("640", "Specialized Subject Added Entry 640", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 640"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 640"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 640"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 640"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 640"),
])

# Subject Added Entry 641
_field("641", "Specialized Subject Added Entry 641", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 641"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 641"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 641"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 641"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 641"),
])

# Subject Added Entry 642
_field("642", "Specialized Subject Added Entry 642", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 642"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 642"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 642"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 642"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 642"),
])

# Subject Added Entry 643
_field("643", "Specialized Subject Added Entry 643", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 643"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 643"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 643"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 643"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 643"),
])

# Subject Added Entry 644
_field("644", "Specialized Subject Added Entry 644", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 644"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 644"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 644"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 644"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 644"),
])

# Subject Added Entry 645
_field("645", "Specialized Subject Added Entry 645", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 645"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 645"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 645"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 645"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 645"),
])

# Subject Added Entry 646
_field("646", "Specialized Subject Added Entry 646", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 646"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 646"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 646"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 646"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 646"),
])

# Subject Added Entry 647
_field("647", "Specialized Subject Added Entry 647", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 647"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 647"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 647"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 647"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 647"),
])

# Subject Added Entry 648
_field("648", "Specialized Subject Added Entry 648", True, "Subject Level", {"0": "Primary", "1": "Secondary"}, "Thesaurus", {"0": "LCSH", "7": "Source specified in $2"}, [
    MarcSubfieldDefinition("a", "Heading element", False, "Subject heading entry element for 648"),
    MarcSubfieldDefinition("v", "Form subdivision", True, "Form subdivision for 648"),
    MarcSubfieldDefinition("x", "General subdivision", True, "General topical subdivision for 648"),
    MarcSubfieldDefinition("y", "Chronological subdivision", True, "Chronological subdivision for 648"),
    MarcSubfieldDefinition("z", "Geographic subdivision", True, "Geographic subdivision for 648"),
])

# Linking Entry 760
_field("760", "Bibliographic Linking Entry Field 760", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 761
_field("761", "Bibliographic Linking Entry Field 761", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 762
_field("762", "Bibliographic Linking Entry Field 762", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 763
_field("763", "Bibliographic Linking Entry Field 763", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 764
_field("764", "Bibliographic Linking Entry Field 764", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 765
_field("765", "Bibliographic Linking Entry Field 765", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 766
_field("766", "Bibliographic Linking Entry Field 766", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 767
_field("767", "Bibliographic Linking Entry Field 767", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 768
_field("768", "Bibliographic Linking Entry Field 768", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 769
_field("769", "Bibliographic Linking Entry Field 769", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 770
_field("770", "Bibliographic Linking Entry Field 770", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 771
_field("771", "Bibliographic Linking Entry Field 771", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 772
_field("772", "Bibliographic Linking Entry Field 772", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 773
_field("773", "Bibliographic Linking Entry Field 773", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 774
_field("774", "Bibliographic Linking Entry Field 774", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 775
_field("775", "Bibliographic Linking Entry Field 775", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 776
_field("776", "Bibliographic Linking Entry Field 776", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 777
_field("777", "Bibliographic Linking Entry Field 777", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 778
_field("778", "Bibliographic Linking Entry Field 778", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 779
_field("779", "Bibliographic Linking Entry Field 779", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 780
_field("780", "Bibliographic Linking Entry Field 780", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 781
_field("781", "Bibliographic Linking Entry Field 781", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 782
_field("782", "Bibliographic Linking Entry Field 782", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 783
_field("783", "Bibliographic Linking Entry Field 783", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 784
_field("784", "Bibliographic Linking Entry Field 784", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 785
_field("785", "Bibliographic Linking Entry Field 785", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 786
_field("786", "Bibliographic Linking Entry Field 786", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])

# Linking Entry 787
_field("787", "Bibliographic Linking Entry Field 787", True, "Note controller", {"0": "Display note", "1": "Do not display note"}, "Undefined", {" ": "Undefined"}, [
    MarcSubfieldDefinition("a", "Main entry heading", False, "Author or issuing body of linked record"),
    MarcSubfieldDefinition("t", "Title", False, "Title of linked bibliographic item"),
    MarcSubfieldDefinition("x", "ISSN", False, "ISSN of linked continuing resource"),
    MarcSubfieldDefinition("z", "ISBN", True, "ISBN of linked item"),
    MarcSubfieldDefinition("w", "Record control number", True, "System control number of linked work"),
])


def lookup_field_definition(tag: str) -> Optional[MarcFieldDefinition]:
    return MARC_BIB_GUIDE.get(tag.strip())
