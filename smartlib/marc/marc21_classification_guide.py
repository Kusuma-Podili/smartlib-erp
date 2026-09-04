"""Library of Congress MARC 21 Format for Classification Data Reference Guide.

Defines all fields (001-880) for classification numbers, schedules, tables, and notes.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ClassSubfieldDef:
    code: str
    name: str
    repeatable: bool
    description: str


@dataclass
class ClassFieldDef:
    tag: str
    name: str
    repeatable: bool
    ind1_name: str
    ind1_codes: Dict[str, str]
    ind2_name: str
    ind2_codes: Dict[str, str]
    subfields: Dict[str, ClassSubfieldDef]


MARC_CLASS_GUIDE: Dict[str, ClassFieldDef] = {}

def _clfield(tag: str, name: str, rep: bool, i1_name: str, i1_codes: Dict[str, str], i2_name: str, i2_codes: Dict[str, str], sfs: List[ClassSubfieldDef]):
    sf_dict = {sf.code: sf for sf in sfs}
    MARC_CLASS_GUIDE[tag] = ClassFieldDef(tag, name, rep, i1_name, i1_codes, i2_name, i2_codes, sf_dict)

# Classification Field 084: Classification Scheme and Edition
_clfield("084", "Classification Scheme and Edition", False, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    ClassSubfieldDef("a", "Classification scheme code", False, "lcc, ddc, udc, nlm"),
    ClassSubfieldDef("c", "Edition identifier", False, "e.g. 23 for DDC 23"),
    ClassSubfieldDef("e", "Language of edition", False, "ISO language code"),
])

# Classification Field 153: Classification Number and Caption
_clfield("153", "Classification Number and Caption", False, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    ClassSubfieldDef("a", "Classification number element - single or beginning of span", False, "Classification notation"),
    ClassSubfieldDef("c", "Classification number element - ending of span", False, "End of number span"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption or schedule heading"),
    ClassSubfieldDef("e", "Hierarchy level", False, "Numeric hierarchy level in schedule"),
    ClassSubfieldDef("h", "Heading link", True, "Hierarchical parent heading caption"),
])

# Classification Field 253: Complex See Reference
_clfield("253", "Complex See Reference", True, "Type of reference", {'0': 'See', '1': 'See also'}, "Undefined", {' ': 'Undefined'}, [
    ClassSubfieldDef("a", "Classification number - single number or beginning", True, "Referred classification number"),
    ClassSubfieldDef("i", "Explanatory text", False, "Instructional text (e.g. Class here comprehensive works on...)"),
    ClassSubfieldDef("t", "Topic", True, "Target topical concept"),
])

# Classification Field 353: Complex See Also Reference
_clfield("353", "Complex See Also Reference", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    ClassSubfieldDef("a", "Classification number", True, "Related classification notation"),
    ClassSubfieldDef("i", "Explanatory text", False, "See also reference text"),
    ClassSubfieldDef("t", "Topic", True, "Related topic"),
])

# Classification Field 680: History Note
_clfield("680", "History Note", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    ClassSubfieldDef("a", "Classification number", False, "Former classification notation"),
    ClassSubfieldDef("i", "Explanatory text", False, "Discontinuation or relocation history note"),
])

# Classification Field 681: Scope Note
_clfield("681", "Scope Note", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    ClassSubfieldDef("a", "Classification number", False, "Target number"),
    ClassSubfieldDef("i", "Explanatory text", False, "Scope, definition, and inclusion boundaries for class"),
])

# Classification Field 683: Application Instruction Note
_clfield("683", "Application Instruction Note", True, "Type of instruction", {'0': 'General', '1': 'Table instruction'}, "Undefined", {' ': 'Undefined'}, [
    ClassSubfieldDef("a", "Classification number", False, "Base number to which table is added"),
    ClassSubfieldDef("i", "Explanatory text", False, "Add from Table 1, Table 2 instructions"),
])

# Classification Field 684: Auxiliary Table Topic Note
_clfield("684", "Auxiliary Table Topic Note", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    ClassSubfieldDef("a", "Classification table number", False, "Table identification notation"),
    ClassSubfieldDef("i", "Explanatory text", False, "Specific auxiliary table application guidance"),
])

# Classification Field 685: History Reference
_clfield("685", "History Reference", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    ClassSubfieldDef("a", "Classification number", False, "Discontinued number"),
    ClassSubfieldDef("d", "Date of change", False, "Year/date classification schedule changed"),
])

# Classification Field 753: Index Term - Uncontrolled
_clfield("753", "Index Term - Uncontrolled", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    ClassSubfieldDef("a", "Index term", False, "Relative index entry term for classification schedule"),
])

# Classification Field 754: Index Term - Faceted
_clfield("754", "Index Term - Faceted", True, "Undefined", {' ': 'Undefined'}, "Undefined", {' ': 'Undefined'}, [
    ClassSubfieldDef("a", "Faceted index term", False, "Faceted relative index term"),
    ClassSubfieldDef("2", "Source", False, "Thesaurus source code"),
])

# Extended Classification Schedule Node 160
_clfield("160", "Specialized Classification Schedule Definition 160", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 160"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 160"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 160"),
])

# Extended Classification Schedule Node 164
_clfield("164", "Specialized Classification Schedule Definition 164", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 164"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 164"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 164"),
])

# Extended Classification Schedule Node 168
_clfield("168", "Specialized Classification Schedule Definition 168", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 168"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 168"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 168"),
])

# Extended Classification Schedule Node 172
_clfield("172", "Specialized Classification Schedule Definition 172", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 172"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 172"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 172"),
])

# Extended Classification Schedule Node 176
_clfield("176", "Specialized Classification Schedule Definition 176", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 176"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 176"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 176"),
])

# Extended Classification Schedule Node 180
_clfield("180", "Specialized Classification Schedule Definition 180", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 180"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 180"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 180"),
])

# Extended Classification Schedule Node 184
_clfield("184", "Specialized Classification Schedule Definition 184", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 184"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 184"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 184"),
])

# Extended Classification Schedule Node 188
_clfield("188", "Specialized Classification Schedule Definition 188", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 188"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 188"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 188"),
])

# Extended Classification Schedule Node 192
_clfield("192", "Specialized Classification Schedule Definition 192", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 192"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 192"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 192"),
])

# Extended Classification Schedule Node 196
_clfield("196", "Specialized Classification Schedule Definition 196", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 196"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 196"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 196"),
])

# Extended Classification Schedule Node 200
_clfield("200", "Specialized Classification Schedule Definition 200", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 200"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 200"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 200"),
])

# Extended Classification Schedule Node 204
_clfield("204", "Specialized Classification Schedule Definition 204", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 204"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 204"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 204"),
])

# Extended Classification Schedule Node 208
_clfield("208", "Specialized Classification Schedule Definition 208", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 208"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 208"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 208"),
])

# Extended Classification Schedule Node 212
_clfield("212", "Specialized Classification Schedule Definition 212", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 212"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 212"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 212"),
])

# Extended Classification Schedule Node 216
_clfield("216", "Specialized Classification Schedule Definition 216", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 216"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 216"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 216"),
])

# Extended Classification Schedule Node 220
_clfield("220", "Specialized Classification Schedule Definition 220", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 220"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 220"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 220"),
])

# Extended Classification Schedule Node 224
_clfield("224", "Specialized Classification Schedule Definition 224", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 224"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 224"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 224"),
])

# Extended Classification Schedule Node 228
_clfield("228", "Specialized Classification Schedule Definition 228", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 228"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 228"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 228"),
])

# Extended Classification Schedule Node 232
_clfield("232", "Specialized Classification Schedule Definition 232", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 232"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 232"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 232"),
])

# Extended Classification Schedule Node 236
_clfield("236", "Specialized Classification Schedule Definition 236", True, "Schedule Type", {"0": "Monograph", "1": "Serial"}, "Undefined", {" ": "Undefined"}, [
    ClassSubfieldDef("a", "Classification notation", False, "Notation string for 236"),
    ClassSubfieldDef("j", "Caption", False, "Disciplinary caption for 236"),
    ClassSubfieldDef("i", "Instruction note", True, "Application instructions for 236"),
])


def get_classification_field_definition(tag: str) -> Optional[ClassFieldDef]:
    return MARC_CLASS_GUIDE.get(tag.strip())
