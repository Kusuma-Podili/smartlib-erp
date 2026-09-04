"""Library of Congress MARC 21 Format for Community Information Reference Guide.

Defines public library community programs, workshops, social agencies, and services.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CommunitySubfieldDef:
    code: str
    name: str
    repeatable: bool
    description: str


@dataclass
class CommunityFieldDef:
    tag: str
    name: str
    repeatable: bool
    ind1_name: str
    ind1_codes: Dict[str, str]
    ind2_name: str
    ind2_codes: Dict[str, str]
    subfields: Dict[str, CommunitySubfieldDef]


MARC_COMMUNITY_GUIDE: Dict[str, CommunityFieldDef] = {}

def _cfield(tag: str, name: str, rep: bool, i1_name: str, i1_codes: Dict[str, str], i2_name: str, i2_codes: Dict[str, str], sfs: List[CommunitySubfieldDef]):
    sf_dict = {sf.code: sf for sf in sfs}
    MARC_COMMUNITY_GUIDE[tag] = CommunityFieldDef(tag, name, rep, i1_name, i1_codes, i2_name, i2_codes, sf_dict)

# Community Field 001: Community Record Control Number
_cfield("001", "Community Record Control Number", False, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    CommunitySubfieldDef("a", "Control number", False, "Unique agency record identifier"),
])

# Community Field 110: Main Entry - Corporate Name / Agency
_cfield("110", "Main Entry - Corporate Name / Agency", False, "Type of entry", {'1': 'Jurisdiction', '2': 'Direct order'}, "Undefined", {' ': 'Undefined'}, [
    CommunitySubfieldDef("a", "Corporate name", False, "Name of community service or library agency"),
    CommunitySubfieldDef("b", "Subordinate unit", True, "Division or program committee"),
])

# Community Field 245: Title of Program or Service
_cfield("245", "Title of Program or Service", False, "Added entry", {'0': 'No added entry', '1': 'Added entry'}, "Nonfiling", {'0': '0 nonfiling'}, [
    CommunitySubfieldDef("a", "Title of program", False, "e.g. Summer Reading Club, Digital Literacy Workshop"),
    CommunitySubfieldDef("b", "Subtitle", False, "Program subtitle"),
    CommunitySubfieldDef("c", "Statement of responsibility", False, "Sponsoring library branch"),
])

# Community Field 270: Address
_cfield("270", "Address", True, "Type of address", {' ': 'No level specified', '1': 'Primary', '2': 'Secondary'}, "Undefined", {' ': 'Undefined'}, [
    CommunitySubfieldDef("a", "Address", True, "Street address"),
    CommunitySubfieldDef("b", "City", False, "Municipality"),
    CommunitySubfieldDef("c", "State or province", False, "State"),
    CommunitySubfieldDef("d", "Country", False, "Country"),
    CommunitySubfieldDef("e", "Postal code", False, "ZIP/Postal code"),
    CommunitySubfieldDef("k", "Telephone number", True, "Contact phone"),
    CommunitySubfieldDef("m", "Email address", True, "Contact email"),
    CommunitySubfieldDef("p", "Contact person", True, "Program coordinator"),
])

# Community Field 301: Hours of Service
_cfield("301", "Hours of Service", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    CommunitySubfieldDef("a", "Hours", False, "e.g. Mon-Fri 9am-8pm, Sat 10am-5pm"),
    CommunitySubfieldDef("b", "Days of week", True, "Operating days"),
])

# Community Field 307: Times of Program or Event
_cfield("307", "Times of Program or Event", True, "Display constant", {' ': 'Hours', '8': 'No display constant'}, "Undefined", {' ': 'Undefined'}, [
    CommunitySubfieldDef("a", "Event schedule", False, "Specific workshop meeting times"),
])

# Community Field 520: Summary of Program or Service
_cfield("520", "Summary of Program or Service", True, "Display constant", {' ': 'Summary', '3': 'Abstract'}, "Undefined", {' ': 'Undefined'}, [
    CommunitySubfieldDef("a", "Summary text", False, "Comprehensive description of public service offerings"),
    CommunitySubfieldDef("b", "Expansion of note", False, "Target audience and registration requirements"),
])

# Community Field 650: Subject Heading - Community Topic
_cfield("650", "Subject Heading - Community Topic", True, "Subject level", {'0': 'Primary'}, "Thesaurus", {'0': 'LCSH', '7': 'Source in $2'}, [
    CommunitySubfieldDef("a", "Topical term", False, "e.g. Adult education, Children's literacy, Job search assistance"),
    CommunitySubfieldDef("x", "General subdivision", True, "Subdivision"),
])

# Extended Community Note 530
_cfield("530", "Specialized Community Service Note 530", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    CommunitySubfieldDef("a", "Community note", False, "Service description for 530"),
    CommunitySubfieldDef("u", "Web resource link", True, "Online registration URL"),
])

# Extended Community Note 535
_cfield("535", "Specialized Community Service Note 535", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    CommunitySubfieldDef("a", "Community note", False, "Service description for 535"),
    CommunitySubfieldDef("u", "Web resource link", True, "Online registration URL"),
])

# Extended Community Note 540
_cfield("540", "Specialized Community Service Note 540", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    CommunitySubfieldDef("a", "Community note", False, "Service description for 540"),
    CommunitySubfieldDef("u", "Web resource link", True, "Online registration URL"),
])

# Extended Community Note 545
_cfield("545", "Specialized Community Service Note 545", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    CommunitySubfieldDef("a", "Community note", False, "Service description for 545"),
    CommunitySubfieldDef("u", "Web resource link", True, "Online registration URL"),
])

# Extended Community Note 550
_cfield("550", "Specialized Community Service Note 550", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    CommunitySubfieldDef("a", "Community note", False, "Service description for 550"),
    CommunitySubfieldDef("u", "Web resource link", True, "Online registration URL"),
])

# Extended Community Note 555
_cfield("555", "Specialized Community Service Note 555", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    CommunitySubfieldDef("a", "Community note", False, "Service description for 555"),
    CommunitySubfieldDef("u", "Web resource link", True, "Online registration URL"),
])

# Extended Community Note 560
_cfield("560", "Specialized Community Service Note 560", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    CommunitySubfieldDef("a", "Community note", False, "Service description for 560"),
    CommunitySubfieldDef("u", "Web resource link", True, "Online registration URL"),
])

# Extended Community Note 565
_cfield("565", "Specialized Community Service Note 565", True, "Undefined", {" ": "Undefined"}, "Undefined", {" ": "Undefined"}, [
    CommunitySubfieldDef("a", "Community note", False, "Service description for 565"),
    CommunitySubfieldDef("u", "Web resource link", True, "Online registration URL"),
])


def get_community_field_definition(tag: str) -> Optional[CommunityFieldDef]:
    return MARC_COMMUNITY_GUIDE.get(tag.strip())
