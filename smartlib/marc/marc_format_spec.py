"""MARC 21 Format for Bibliographic Data - Complete Tag Specifications.

Provides definitive validation metadata, indicator meanings, and subfield definitions
for MARC 21 variable control fields (00X) and data fields (01X-99X).
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class MarcSubfieldSpec:
    code: str
    name: str
    is_repeatable: bool
    description: str


@dataclass
class MarcFieldSpec:
    tag: str
    name: str
    is_repeatable: bool
    ind1_name: str
    ind2_name: str
    subfields: Dict[str, MarcSubfieldSpec] = field(default_factory=dict)
    indicator1_values: Dict[str, str] = field(default_factory=dict)
    indicator2_values: Dict[str, str] = field(default_factory=dict)


MARC_SPEC_CATALOG: Dict[str, MarcFieldSpec] = {}


def _fspec(tag: str, name: str, rep: bool, ind1_name: str, ind2_name: str,
           subfields: List[Tuple[str, str, bool, str]],
           ind1_vals: Optional[Dict[str, str]] = None,
           ind2_vals: Optional[Dict[str, str]] = None):
    sub_dict = {}
    for code, sname, srep, sdesc in subfields:
        sub_dict[code] = MarcSubfieldSpec(code, sname, srep, sdesc)
    MARC_SPEC_CATALOG[tag] = MarcFieldSpec(
        tag=tag,
        name=name,
        is_repeatable=rep,
        ind1_name=ind1_name,
        ind2_name=ind2_name,
        subfields=sub_dict,
        indicator1_values=ind1_vals or {},
        indicator2_values=ind2_vals or {}
    )

_fspec(
    tag="010",
    name="Library of Congress Control Number (LCCN)",
    rep=False,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
            ("a", "LC control number", False, "Standard LCCN identifier"),
            ("z", "Canceled or invalid LCCN", True, "Historical or duplicate LCCN")
        ]
)
_fspec(
    tag="020",
    name="International Standard Book Number (ISBN)",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
            ("a", "International Standard Book Number", False, "Valid 10 or 13-digit ISBN"),
            ("c", "Terms of availability", False, "Price or availability terms"),
            ("q", "Qualifying information", True, "Format qualifier e.g. pbk., hbk."),
            ("z", "Canceled/invalid ISBN", True, "Invalid or retired ISBN")
        ]
)
_fspec(
    tag="022",
    name="International Standard Serial Number (ISSN)",
    rep=True,
    ind1_name="Level of international scrutiny",
    ind2_name="Undefined",
    subfields=[
            ("a", "International Standard Serial Number", False, "Standard 8-character ISSN"),
            ("y", "Incorrect ISSN", True, "Erroneous ISSN appearing on item"),
            ("z", "Canceled ISSN", True, "Retired ISSN")
        ]
)
_fspec(
    tag="024",
    name="Other Standard Identifier (DOI, URN, ISMN)",
    rep=True,
    ind1_name="Type of identifier",
    ind2_name="Difference indicator",
    subfields=[
            ("a", "Standard number or code", False, "DOI, ISMN, or URI identifier"),
            ("c", "Terms of availability", False, "Access terms"),
            ("d", "Additional codes following the standard number", False, "Suffix modifier"),
            ("2", "Source of number or code", False, "Identifier agency authority code")
        ]
)
_fspec(
    tag="035",
    name="System Control Number (OCLC, Local ID)",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
            ("a", "System control number", False, "Prefix in parens followed by identifier"),
            ("z", "Canceled or invalid control number", True, "Previous identifier")
        ]
)
_fspec(
    tag="040",
    name="Cataloging Source",
    rep=False,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
            ("a", "Original cataloging agency", False, "MARC agency code of creator"),
            ("b", "Language of cataloging", False, "ISO 639-2 code of description language"),
            ("c", "Transcribing agency", False, "Agency that entered record"),
            ("d", "Modifying agency", True, "Agencies modifying the record"),
            ("e", "Description conventions", True, "RDA, AACR2, ISBD conventions")
        ]
)
_fspec(
    tag="041",
    name="Language Code",
    rep=True,
    ind1_name="Translation indication",
    ind2_name="Source of code",
    subfields=[
            ("a", "Language code of text/sound track", True, "3-letter language code"),
            ("b", "Language code of summary/abstract", True, "Summary language"),
            ("h", "Language code of original", True, "Original language if translated")
        ]
)
_fspec(
    tag="050",
    name="Library of Congress Call Number",
    rep=True,
    ind1_name="Existence in LC collection",
    ind2_name="Source of call number",
    subfields=[
            ("a", "Classification number", False, "LC class notation"),
            ("b", "Item number", False, "Cutter number and date"),
            ("3", "Materials specified", False, "Applicable volume cohort")
        ]
)
_fspec(
    tag="082",
    name="Dewey Decimal Classification Number",
    rep=True,
    ind1_name="Type of edition",
    ind2_name="Source of classification number",
    subfields=[
            ("a", "Classification number", True, "DDC class number with dot notation"),
            ("b", "Item number", False, "Cutter or author mark"),
            ("2", "Edition number", False, "DDC full or abridged edition e.g. 23")
        ]
)
_fspec(
    tag="100",
    name="Main Entry - Personal Name",
    rep=False,
    ind1_name="Type of personal name entry element",
    ind2_name="Undefined",
    subfields=[
            ("a", "Personal name", False, "Surname, Forename, or direct order"),
            ("b", "Numeration", False, "Roman numerals or ordinal titles"),
            ("c", "Titles and words associated with a name", True, "Sir, Lord, Ph.D."),
            ("d", "Dates associated with a name", False, "Birth and death years"),
            ("e", "Relator term", True, "Relationship designator e.g. author"),
            ("4", "Relator code", True, "Three-letter MARC relator code"),
            ("0", "Authority record control number", True, "URI or authority record ID"),
            ("1", "Real World Object URI", True, "Wikidata or ISNI URI")
        ]
)
_fspec(
    tag="110",
    name="Main Entry - Corporate Name",
    rep=False,
    ind1_name="Type of corporate name entry element",
    ind2_name="Undefined",
    subfields=[
            ("a", "Corporate name or jurisdiction name", False, "Primary organization name"),
            ("b", "Subordinate unit", True, "Department, division, or committee"),
            ("c", "Location of meeting", False, "Geographic seat"),
            ("d", "Date of meeting or treaty", True, "Inaugural or treaty date"),
            ("e", "Relator term", True, "Role of corporate body")
        ]
)
_fspec(
    tag="111",
    name="Main Entry - Meeting Name",
    rep=False,
    ind1_name="Type of meeting name entry element",
    ind2_name="Undefined",
    subfields=[
            ("a", "Meeting name or jurisdiction name", False, "Conference or congress name"),
            ("c", "Location of meeting", False, "City, conference center"),
            ("d", "Date of meeting", False, "Inclusive dates of conference"),
            ("e", "Subordinate unit", True, "Specialized section or committee"),
            ("n", "Number of part/section/meeting", True, "Conference session ordinal number")
        ]
)
_fspec(
    tag="130",
    name="Main Entry - Uniform Title",
    rep=False,
    ind1_name="Nonfiling characters",
    ind2_name="Undefined",
    subfields=[
            ("a", "Uniform title", False, "Standardized canonical title"),
            ("l", "Language of a work", False, "Language if translated"),
            ("f", "Date of a work", False, "Year of publication or composition")
        ]
)
_fspec(
    tag="240",
    name="Uniform Title (Linked to 1XX)",
    rep=False,
    ind1_name="Uniform title printed or displayed",
    ind2_name="Nonfiling characters",
    subfields=[
            ("a", "Uniform title", False, "Standardized canonical title"),
            ("l", "Language of a work", False, "Language if translated"),
            ("m", "Medium of performance for music", True, "Instruments and vocal scoring"),
            ("n", "Number of part/section of a work", True, "Opus, catalogue number"),
            ("p", "Name of part/section of a work", True, "Movement or section title")
        ]
)
_fspec(
    tag="245",
    name="Title Statement",
    rep=False,
    ind1_name="Title added entry",
    ind2_name="Nonfiling characters",
    subfields=[
            ("a", "Title proper", False, "Primary title text"),
            ("b", "Remainder of title", False, "Subtitle or parallel title"),
            ("c", "Statement of responsibility", False, "Author attribution as recorded on piece"),
            ("h", "Medium (GMD)", False, "General material designation [electronic resource]"),
            ("n", "Number of part/section of a work", True, "Volume or issue number"),
            ("p", "Name of part/section of a work", True, "Part title")
        ]
)
_fspec(
    tag="246",
    name="Varying Form of Title",
    rep=True,
    ind1_name="Note/added entry controller",
    ind2_name="Type of title",
    subfields=[
            ("a", "Title proper/short title", False, "Alternative, portion, or variant title"),
            ("b", "Remainder of title", False, "Subtitle of variant"),
            ("i", "Display text", False, "Prefatory note e.g. At head of title:")
        ]
)
_fspec(
    tag="250",
    name="Edition Statement",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
            ("a", "Edition statement", False, "1st ed., Rev. ed., 2nd international ed."),
            ("b", "Remainder of edition statement", False, "Editor or reviser attribution")
        ]
)
_fspec(
    tag="260",
    name="Publication, Distribution, etc. (Pre-RDA Imprint)",
    rep=True,
    ind1_name="Sequence of publishing statements",
    ind2_name="Undefined",
    subfields=[
            ("a", "Place of publication, distribution, etc.", True, "City of imprint"),
            ("b", "Name of publisher, distributor, etc.", True, "Firm name"),
            ("c", "Date of publication, distribution, etc.", True, "Calendar year")
        ]
)
_fspec(
    tag="264",
    name="Production, Publication, Distribution, Manufacture, and Copyright (RDA)",
    rep=True,
    ind1_name="Sequence of statements",
    ind2_name="Function of entity",
    subfields=[
            ("a", "Place of production, publication, etc.", True, "Geographic place name"),
            ("b", "Name of producer, publisher, etc.", True, "Corporate entity name"),
            ("c", "Date of production, publication, etc.", True, "Year or specific date")
        ]
)
_fspec(
    tag="300",
    name="Physical Description",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
            ("a", "Extent", True, "Pagination, number of volumes, discs, files"),
            ("b", "Other physical details", False, "Illustrations, maps, color, sound"),
            ("c", "Dimensions", True, "Height in cm, disc diameter in inches"),
            ("e", "Accompanying material", False, "Teacher's guide, CD-ROM supplement")
        ]
)
_fspec(
    tag="336",
    name="Content Type (RDA)",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
            ("a", "Content type term", False, "text, performed music, cartographic image"),
            ("b", "Content type code", False, "txt, prm, cri"),
            ("2", "Source", False, "rdacontent")
        ]
)
_fspec(
    tag="337",
    name="Media Type (RDA)",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
            ("a", "Media type term", False, "unmediated, computer, audio, video"),
            ("b", "Media type code", False, "n, c, s, v"),
            ("2", "Source", False, "rdamedia")
        ]
)
_fspec(
    tag="338",
    name="Carrier Type (RDA)",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
            ("a", "Carrier type term", False, "volume, online resource, computer disc"),
            ("b", "Carrier type code", False, "nc, cr, cd"),
            ("2", "Source", False, "rdacarrier")
        ]
)
_fspec(
    tag="490",
    name="Series Statement",
    rep=True,
    ind1_name="Specifies whether series is traced",
    ind2_name="Undefined",
    subfields=[
            ("a", "Series statement", True, "Series title as transcribed"),
            ("v", "Volume/sequential designation", True, "Volume number within series"),
            ("x", "International Standard Serial Number", True, "Series ISSN")
        ]
)
_fspec(
    tag="500",
    name="General Note",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
            ("a", "General note text", False, "Informal cataloger note on manifestation or item"),
            ("5", "Institution to which field applies", False, "Copy-specific MARC organization code")
        ]
)
_fspec(
    tag="504",
    name="Bibliography, etc. Note",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
            ("a", "Bibliography note text", False, "Includes bibliographical references and index"),
            ("b", "Number of references", False, "Quantification of citations")
        ]
)
_fspec(
    tag="505",
    name="Formatted Contents Note",
    rep=True,
    ind1_name="Display constant controller",
    ind2_name="Level of content designation",
    subfields=[
            ("a", "Formatted contents note", False, "Complete chapter and author listing"),
            ("t", "Title of component", True, "Discrete chapter or article title"),
            ("r", "Statement of responsibility", True, "Author of chapter or piece")
        ]
)
_fspec(
    tag="520",
    name="Summary, etc.",
    rep=True,
    ind1_name="Display constant controller",
    ind2_name="Undefined",
    subfields=[
            ("a", "Summary, abstract, or annotation", False, "Objective plot or academic abstract"),
            ("c", "Assigning agency", False, "Agency providing annotation"),
            ("u", "Uniform Resource Identifier", True, "Web link to external review or summary")
        ]
)
_fspec(
    tag="600",
    name="Subject Added Entry - Personal Name",
    rep=True,
    ind1_name="Type of personal name entry element",
    ind2_name="Thesaurus",
    subfields=[
            ("a", "Personal name", False, "Subject individual surname or forename"),
            ("b", "Numeration", False, "Roman numerals"),
            ("c", "Titles associated with name", True, "Ecclesiastical or noble titles"),
            ("d", "Dates associated with name", False, "Birth and death years"),
            ("v", "Form subdivision", True, "Biographies, correspondence, pictorial works"),
            ("x", "General subdivision", True, "Philosophy, political activity"),
            ("y", "Chronological subdivision", True, "19th century, Early life"),
            ("z", "Geographic subdivision", True, "England, Rome, United States"),
            ("2", "Source of heading or term", False, "lcsh, fast, mesh, rvm")
        ]
)
_fspec(
    tag="650",
    name="Subject Added Entry - Topical Term",
    rep=True,
    ind1_name="Level of subject",
    ind2_name="Thesaurus",
    subfields=[
            ("a", "Topical term or geographic name entry element", False, "Primary subject term"),
            ("v", "Form subdivision", True, "Encyclopedias, handbooks, manuals"),
            ("x", "General subdivision", True, "Technological innovations, moral aspects"),
            ("y", "Chronological subdivision", True, "21st century, 1945-1989"),
            ("z", "Geographic subdivision", True, "California, Developing countries"),
            ("2", "Source of heading or term", False, "lcsh, fast, mesh, sears")
        ]
)
_fspec(
    tag="651",
    name="Subject Added Entry - Geographic Name",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Thesaurus",
    subfields=[
            ("a", "Geographic name", False, "Country, city, region, or jurisdictional area"),
            ("v", "Form subdivision", True, "Maps, guidebooks, statistics"),
            ("x", "General subdivision", True, "Economic conditions, social life and customs"),
            ("y", "Chronological subdivision", True, "Civil War 1861-1865"),
            ("2", "Source of heading or term", False, "lcsh, fast")
        ]
)
_fspec(
    tag="700",
    name="Added Entry - Personal Name",
    rep=True,
    ind1_name="Type of personal name entry element",
    ind2_name="Type of added entry",
    subfields=[
            ("a", "Personal name", False, "Collaborator, co-author, illustrator, editor"),
            ("d", "Dates associated with name", False, "Birth and death years"),
            ("e", "Relator term", True, "Editor, translator, illustrator"),
            ("4", "Relator code", True, "MARC 3-letter relator code"),
            ("t", "Title of a work", False, "Analytic or included work title")
        ]
)
_fspec(
    tag="710",
    name="Added Entry - Corporate Name",
    rep=True,
    ind1_name="Type of corporate name entry element",
    ind2_name="Type of added entry",
    subfields=[
            ("a", "Corporate name or jurisdiction name", False, "Collaborating institution or sponsor"),
            ("b", "Subordinate unit", True, "Subdivision, office, or committee"),
            ("e", "Relator term", True, "Sponsor, issuing body"),
            ("4", "Relator code", True, "MARC relator code")
        ]
)
_fspec(
    tag="800",
    name="Series Added Entry - Personal Name",
    rep=True,
    ind1_name="Type of personal name entry element",
    ind2_name="Undefined",
    subfields=[
            ("a", "Personal name", False, "Author of the series"),
            ("t", "Title of a work", False, "Traced series uniform title"),
            ("v", "Volume/sequential designation", False, "Volume number within series")
        ]
)
_fspec(
    tag="830",
    name="Series Added Entry - Uniform Title",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Nonfiling characters",
    subfields=[
            ("a", "Uniform title", False, "Traced series uniform title proper"),
            ("v", "Volume/sequential designation", False, "Volume numbering designation"),
            ("w", "Bibliographic record control number", True, "Control number of series authority")
        ]
)
_fspec(
    tag="856",
    name="Electronic Location and Access",
    rep=True,
    ind1_name="Access method",
    ind2_name="Relationship",
    subfields=[
            ("u", "Uniform Resource Identifier", True, "Full web URL to electronic resource"),
            ("y", "Link text", True, "Display text for web link in OPAC"),
            ("z", "Public note", True, "Terms of electronic access or subscription requirement"),
            ("3", "Materials specified", False, "Table of contents, full text, publisher description")
        ]
)
_fspec(
    tag="037",
    name="Source of Acquisition",
    rep=True,
    ind1_name="Stock number source",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Source of Acquisition"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="043",
    name="Geographic Area Code",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Geographic Area Code"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="044",
    name="Country of Publishing/Producing Entity Code",
    rep=False,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Country of Publishing/Producing Entity Code"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="060",
    name="National Library of Medicine Call Number",
    rep=True,
    ind1_name="Existence in NLM",
    ind2_name="Source",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for National Library of Medicine Call Number"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="072",
    name="Subject Category Code",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Source of code",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Subject Category Code"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="080",
    name="Universal Decimal Classification Number",
    rep=True,
    ind1_name="Type of edition",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Universal Decimal Classification Number"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="210",
    name="Abbreviated Title",
    rep=True,
    ind1_name="Title added entry",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Abbreviated Title"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="222",
    name="Key Title",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Nonfiling characters",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Key Title"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="242",
    name="Translation of Title by Cataloging Agency",
    rep=True,
    ind1_name="Title added entry",
    ind2_name="Nonfiling characters",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Translation of Title by Cataloging Agency"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="243",
    name="Collective Uniform Title",
    rep=False,
    ind1_name="Uniform title printed",
    ind2_name="Nonfiling characters",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Collective Uniform Title"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="247",
    name="Former Title",
    rep=True,
    ind1_name="Title added entry",
    ind2_name="Note controller",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Former Title"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="254",
    name="Musical Presentation Statement",
    rep=False,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Musical Presentation Statement"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="255",
    name="Cartographic Mathematical Data",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Cartographic Mathematical Data"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="256",
    name="Computer File Characteristics",
    rep=False,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Computer File Characteristics"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="263",
    name="Projected Publication Date",
    rep=False,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Projected Publication Date"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="310",
    name="Current Publication Frequency",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Current Publication Frequency"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="321",
    name="Former Publication Frequency",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Former Publication Frequency"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="340",
    name="Physical Medium",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Physical Medium"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="347",
    name="Digital File Characteristics",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Digital File Characteristics"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="351",
    name="Organization and Arrangement of Materials",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Organization and Arrangement of Materials"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="362",
    name="Dates of Publication and/or Sequential Designation",
    rep=True,
    ind1_name="Format",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Dates of Publication and/or Sequential Designation"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="501",
    name="With Note",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for With Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="502",
    name="Dissertation Note",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Dissertation Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="506",
    name="Restrictions on Access Note",
    rep=True,
    ind1_name="Display controller",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Restrictions on Access Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="508",
    name="Creation/Production Credits Note",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Creation/Production Credits Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="510",
    name="Citation/References Note",
    rep=True,
    ind1_name="Coverage/location",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Citation/References Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="511",
    name="Participant or Performer Note",
    rep=True,
    ind1_name="Display constant",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Participant or Performer Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="515",
    name="Numbering Peculiarities Note",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Numbering Peculiarities Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="516",
    name="Type of Computer File or Data Note",
    rep=True,
    ind1_name="Display controller",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Type of Computer File or Data Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="518",
    name="Date/Time and Place of an Event Note",
    rep=True,
    ind1_name="Display controller",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Date/Time and Place of an Event Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="521",
    name="Target Audience Note",
    rep=True,
    ind1_name="Display controller",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Target Audience Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="522",
    name="Geographic Coverage Note",
    rep=True,
    ind1_name="Display controller",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Geographic Coverage Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="524",
    name="Preferred Citation of Described Materials Note",
    rep=True,
    ind1_name="Display controller",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Preferred Citation of Described Materials Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="525",
    name="Supplement Note",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Supplement Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="530",
    name="Additional Physical Form Available Note",
    rep=True,
    ind1_name="Display controller",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Additional Physical Form Available Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="533",
    name="Reproduction Note",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Reproduction Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="534",
    name="Original Version Note",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Original Version Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="538",
    name="System Details Note",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for System Details Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="540",
    name="Terms Governing Use and Reproduction Note",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Terms Governing Use and Reproduction Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="541",
    name="Immediate Source of Acquisition Note",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Immediate Source of Acquisition Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="545",
    name="Biographical or Historical Data",
    rep=True,
    ind1_name="Type of data",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Biographical or Historical Data"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="546",
    name="Language Note",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Language Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="555",
    name="Cumulative Index/Finding Aids Note",
    rep=True,
    ind1_name="Display controller",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Cumulative Index/Finding Aids Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="561",
    name="Ownership and Custodial History",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Ownership and Custodial History"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="563",
    name="Binding Information",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Binding Information"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="583",
    name="Action Note",
    rep=True,
    ind1_name="Privacy",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Action Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="586",
    name="Awards Note",
    rep=True,
    ind1_name="Display controller",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Awards Note"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="610",
    name="Subject Added Entry - Corporate Name",
    rep=True,
    ind1_name="Type of corporate name",
    ind2_name="Thesaurus",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Subject Added Entry - Corporate Name"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="611",
    name="Subject Added Entry - Meeting Name",
    rep=True,
    ind1_name="Type of meeting name",
    ind2_name="Thesaurus",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Subject Added Entry - Meeting Name"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="630",
    name="Subject Added Entry - Uniform Title",
    rep=True,
    ind1_name="Nonfiling characters",
    ind2_name="Thesaurus",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Subject Added Entry - Uniform Title"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="648",
    name="Subject Added Entry - Chronological Term",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Thesaurus",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Subject Added Entry - Chronological Term"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="653",
    name="Index Term - Uncontrolled",
    rep=True,
    ind1_name="Level of index term",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Index Term - Uncontrolled"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="655",
    name="Index Term - Genre/Form",
    rep=True,
    ind1_name="Type of heading",
    ind2_name="Thesaurus",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Index Term - Genre/Form"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="656",
    name="Index Term - Occupation",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Source of term",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Index Term - Occupation"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="657",
    name="Index Term - Function",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Source of term",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Index Term - Function"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="711",
    name="Added Entry - Meeting Name",
    rep=True,
    ind1_name="Type of meeting name",
    ind2_name="Type of added entry",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Added Entry - Meeting Name"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="720",
    name="Added Entry - Uncontrolled Name",
    rep=True,
    ind1_name="Type of name",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Added Entry - Uncontrolled Name"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="730",
    name="Added Entry - Uniform Title",
    rep=True,
    ind1_name="Nonfiling characters",
    ind2_name="Type of added entry",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Added Entry - Uniform Title"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="740",
    name="Added Entry - Uncontrolled Related/Analytical Title",
    rep=True,
    ind1_name="Nonfiling characters",
    ind2_name="Type of added entry",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Added Entry - Uncontrolled Related/Analytical Title"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="760",
    name="Main Series Entry",
    rep=True,
    ind1_name="Note controller",
    ind2_name="Display constant",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Main Series Entry"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="762",
    name="Subseries Entry",
    rep=True,
    ind1_name="Note controller",
    ind2_name="Display constant",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Subseries Entry"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="765",
    name="Original Language Entry",
    rep=True,
    ind1_name="Note controller",
    ind2_name="Display constant",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Original Language Entry"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="767",
    name="Translation Entry",
    rep=True,
    ind1_name="Note controller",
    ind2_name="Display constant",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Translation Entry"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="770",
    name="Supplement/Special Issue Entry",
    rep=True,
    ind1_name="Note controller",
    ind2_name="Display constant",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Supplement/Special Issue Entry"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="772",
    name="Supplement Parent Entry",
    rep=True,
    ind1_name="Note controller",
    ind2_name="Display constant",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Supplement Parent Entry"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="773",
    name="Host Item Entry",
    rep=True,
    ind1_name="Note controller",
    ind2_name="Display constant",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Host Item Entry"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="775",
    name="Other Edition Entry",
    rep=True,
    ind1_name="Note controller",
    ind2_name="Display constant",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Other Edition Entry"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="776",
    name="Additional Physical Form Entry",
    rep=True,
    ind1_name="Note controller",
    ind2_name="Display constant",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Additional Physical Form Entry"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="777",
    name="Issued With Entry",
    rep=True,
    ind1_name="Note controller",
    ind2_name="Display constant",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Issued With Entry"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="780",
    name="Preceding Entry",
    rep=True,
    ind1_name="Note controller",
    ind2_name="Type of relationship",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Preceding Entry"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="785",
    name="Succeeding Entry",
    rep=True,
    ind1_name="Note controller",
    ind2_name="Type of relationship",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Succeeding Entry"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="786",
    name="Data Source Entry",
    rep=True,
    ind1_name="Note controller",
    ind2_name="Display constant",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Data Source Entry"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="787",
    name="Other Relationship Entry",
    rep=True,
    ind1_name="Note controller",
    ind2_name="Display constant",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Other Relationship Entry"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="810",
    name="Series Added Entry - Corporate Name",
    rep=True,
    ind1_name="Type of corporate name",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Series Added Entry - Corporate Name"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="811",
    name="Series Added Entry - Meeting Name",
    rep=True,
    ind1_name="Type of meeting name",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Series Added Entry - Meeting Name"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="852",
    name="Location / Call Number",
    rep=True,
    ind1_name="Shelving scheme",
    ind2_name="Shelving order",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Location / Call Number"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="863",
    name="Enumeration and Chronology - Basic Holdings",
    rep=True,
    ind1_name="Field encoding level",
    ind2_name="Form of numbering",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Enumeration and Chronology - Basic Holdings"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="864",
    name="Enumeration and Chronology - Supplementary Material",
    rep=True,
    ind1_name="Field encoding level",
    ind2_name="Form of numbering",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Enumeration and Chronology - Supplementary Material"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="865",
    name="Enumeration and Chronology - Indexes",
    rep=True,
    ind1_name="Field encoding level",
    ind2_name="Form of numbering",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Enumeration and Chronology - Indexes"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="866",
    name="Textual Holdings - Basic Holdings",
    rep=True,
    ind1_name="Field encoding level",
    ind2_name="Type of notation",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Textual Holdings - Basic Holdings"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="867",
    name="Textual Holdings - Supplementary Material",
    rep=True,
    ind1_name="Field encoding level",
    ind2_name="Type of notation",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Textual Holdings - Supplementary Material"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="868",
    name="Textual Holdings - Indexes",
    rep=True,
    ind1_name="Field encoding level",
    ind2_name="Type of notation",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Textual Holdings - Indexes"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="876",
    name="Item Information - Basic Holdings",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Item Information - Basic Holdings"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="877",
    name="Item Information - Supplementary Material",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Item Information - Supplementary Material"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)
_fspec(
    tag="878",
    name="Item Information - Indexes",
    rep=True,
    ind1_name="Undefined",
    ind2_name="Undefined",
    subfields=[
        ("a", "Primary data element", False, "Main descriptive text for Item Information - Indexes"),
        ("x", "Nonpublic note", True, "Internal administrative note"),
        ("z", "Public note", True, "Publicly visible note"),
        ("3", "Materials specified", False, "Specified part of resource"),
        ("6", "Linkage", False, "Multiscript linkage data")
    ]
)

def lookup_marc_field_spec(tag: str) -> Optional[MarcFieldSpec]:
    """Retrieve official MARC 21 specification rules for a 3-digit tag."""
    return MARC_SPEC_CATALOG.get(tag.strip())


def validate_marc_field(tag: str, ind1: str, ind2: str, subfields: List[Tuple[str, str]]) -> Tuple[bool, List[str]]:
    """Validate a parsed field against official MARC 21 rules."""
    spec = lookup_marc_field_spec(tag)
    if not spec:
        return True, []  # Allow unrecognized local fields without error

    errors: List[str] = []
    seen_subs = set()
    for code, _ in subfields:
        sub_spec = spec.subfields.get(code)
        if sub_spec and not sub_spec.is_repeatable and code in seen_subs:
            errors.append(f"Field {tag} has non-repeatable subfield ${code} repeated.")
        seen_subs.add(code)

    return len(errors) == 0, errors
