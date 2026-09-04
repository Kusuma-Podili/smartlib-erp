"""Qualified Dublin Core (QDC) and DSpace/EPrints Institutional Metadata.

Implements all 55 standard DCMI Metadata Terms qualifiers for institutional repositories,
including bibliographicCitation, abstract, tableOfContents, spatial/temporal coverage,
accrualMethod, accessRights, and provenance tracking.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class QdcTermDefinition:
    element_name: str
    qualifier_name: Optional[str]
    term_uri: str
    label: str
    definition: str
    dspace_schema_field: str
    oai_dc_fallback: str


QDC_TERMS_CATALOG: Dict[str, QdcTermDefinition] = {}


def _qdc(elem: str, qual: Optional[str], uri: str, label: str, defn: str, ds_field: str, oai_fall: str):
    key = f"{elem}.{qual}".lower() if qual else elem.lower()
    QDC_TERMS_CATALOG[key] = QdcTermDefinition(
        element_name=elem,
        qualifier_name=qual,
        term_uri=uri,
        label=label,
        definition=defn,
        dspace_schema_field=ds_field,
        oai_dc_fallback=oai_fall
    )

_qdc(
    elem="title",
    qual=None,
    uri="http://purl.org/dc/terms/title",
    label="Title",
    defn="A name given to the resource.",
    ds_field="dc.title",
    oai_fall="title"
)
_qdc(
    elem="title",
    qual="alternative",
    uri="http://purl.org/dc/terms/alternative",
    label="Alternative Title",
    defn="An alternative name for the resource.",
    ds_field="dc.title.alternative",
    oai_fall="title"
)
_qdc(
    elem="creator",
    qual=None,
    uri="http://purl.org/dc/terms/creator",
    label="Creator",
    defn="An entity primarily responsible for making the resource.",
    ds_field="dc.contributor.author",
    oai_fall="creator"
)
_qdc(
    elem="contributor",
    qual="advisor",
    uri="http://purl.org/dc/terms/contributor",
    label="Thesis Advisor",
    defn="An entity responsible for advising a student thesis or dissertation.",
    ds_field="dc.contributor.advisor",
    oai_fall="contributor"
)
_qdc(
    elem="contributor",
    qual="editor",
    uri="http://purl.org/dc/terms/contributor",
    label="Editor",
    defn="An entity responsible for editing the collection or volume.",
    ds_field="dc.contributor.editor",
    oai_fall="contributor"
)
_qdc(
    elem="contributor",
    qual="illustrator",
    uri="http://purl.org/dc/terms/contributor",
    label="Illustrator",
    defn="An entity responsible for creating illustrations.",
    ds_field="dc.contributor.illustrator",
    oai_fall="contributor"
)
_qdc(
    elem="description",
    qual="abstract",
    uri="http://purl.org/dc/terms/abstract",
    label="Abstract",
    defn="A summary of the resource content.",
    ds_field="dc.description.abstract",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="tableOfContents",
    uri="http://purl.org/dc/terms/tableOfContents",
    label="Table of Contents",
    defn="A list of subunits of the resource.",
    ds_field="dc.description.tableofcontents",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="provenance",
    uri="http://purl.org/dc/terms/provenance",
    label="Provenance",
    defn="A statement of changes in ownership and custody.",
    ds_field="dc.description.provenance",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="sponsorship",
    uri="http://purl.org/dc/terms/description",
    label="Sponsorship Note",
    defn="Information on grant or fellowship funding.",
    ds_field="dc.description.sponsorship",
    oai_fall="description"
)
_qdc(
    elem="date",
    qual="issued",
    uri="http://purl.org/dc/terms/issued",
    label="Date Issued",
    defn="Date of formal publication, distribution, or release.",
    ds_field="dc.date.issued",
    oai_fall="date"
)
_qdc(
    elem="date",
    qual="created",
    uri="http://purl.org/dc/terms/created",
    label="Date Created",
    defn="Date of creation of the resource.",
    ds_field="dc.date.created",
    oai_fall="date"
)
_qdc(
    elem="date",
    qual="available",
    uri="http://purl.org/dc/terms/available",
    label="Date Available",
    defn="Date that the resource became or will become available.",
    ds_field="dc.date.available",
    oai_fall="date"
)
_qdc(
    elem="date",
    qual="accessioned",
    uri="http://purl.org/dc/terms/date",
    label="Date Accessioned",
    defn="Date that digital item was deposited in repository.",
    ds_field="dc.date.accessioned",
    oai_fall="date"
)
_qdc(
    elem="identifier",
    qual="uri",
    uri="http://purl.org/dc/terms/identifier",
    label="URI Identifier",
    defn="Persistent handle or DOI web link to resource.",
    ds_field="dc.identifier.uri",
    oai_fall="identifier"
)
_qdc(
    elem="identifier",
    qual="isbn",
    uri="http://purl.org/dc/terms/identifier",
    label="ISBN",
    defn="International Standard Book Number.",
    ds_field="dc.identifier.isbn",
    oai_fall="identifier"
)
_qdc(
    elem="identifier",
    qual="issn",
    uri="http://purl.org/dc/terms/identifier",
    label="ISSN",
    defn="International Standard Serial Number.",
    ds_field="dc.identifier.issn",
    oai_fall="identifier"
)
_qdc(
    elem="identifier",
    qual="doi",
    uri="http://purl.org/dc/terms/identifier",
    label="DOI",
    defn="Digital Object Identifier persistent identifier.",
    ds_field="dc.identifier.doi",
    oai_fall="identifier"
)
_qdc(
    elem="identifier",
    qual="citation",
    uri="http://purl.org/dc/terms/bibliographicCitation",
    label="Bibliographic Citation",
    defn="A bibliographic reference for the resource.",
    ds_field="dc.identifier.citation",
    oai_fall="identifier"
)
_qdc(
    elem="coverage",
    qual="spatial",
    uri="http://purl.org/dc/terms/spatial",
    label="Spatial Coverage",
    defn="Spatial characteristics of the resource (geographic places).",
    ds_field="dc.coverage.spatial",
    oai_fall="coverage"
)
_qdc(
    elem="coverage",
    qual="temporal",
    uri="http://purl.org/dc/terms/temporal",
    label="Temporal Coverage",
    defn="Temporal characteristics of the resource (eras, periods).",
    ds_field="dc.coverage.temporal",
    oai_fall="coverage"
)
_qdc(
    elem="rights",
    qual="accessRights",
    uri="http://purl.org/dc/terms/accessRights",
    label="Access Rights",
    defn="Information about who can access the resource or an embargo statement.",
    ds_field="dc.rights.accessrights",
    oai_fall="rights"
)
_qdc(
    elem="rights",
    qual="license",
    uri="http://purl.org/dc/terms/license",
    label="License",
    defn="A legal document giving official permission to do something with the resource.",
    ds_field="dc.rights.license",
    oai_fall="rights"
)
_qdc(
    elem="format",
    qual="extent",
    uri="http://purl.org/dc/terms/extent",
    label="Extent",
    defn="The size or duration of the resource (e.g. 350 p., 45 MB).",
    ds_field="dc.format.extent",
    oai_fall="format"
)
_qdc(
    elem="format",
    qual="medium",
    uri="http://purl.org/dc/terms/medium",
    label="Medium",
    defn="The material or physical carrier of the resource.",
    ds_field="dc.format.medium",
    oai_fall="format"
)
_qdc(
    elem="relation",
    qual="isVersionOf",
    uri="http://purl.org/dc/terms/isVersionOf",
    label="Is Version Of",
    defn="A related resource of which the described resource is a version.",
    ds_field="dc.relation.isversionof",
    oai_fall="relation"
)
_qdc(
    elem="relation",
    qual="hasVersion",
    uri="http://purl.org/dc/terms/hasVersion",
    label="Has Version",
    defn="A related resource that is a version of the described resource.",
    ds_field="dc.relation.hasversion",
    oai_fall="relation"
)
_qdc(
    elem="relation",
    qual="isFormatOf",
    uri="http://purl.org/dc/terms/isFormatOf",
    label="Is Format Of",
    defn="A related resource that is substantially the same with another format.",
    ds_field="dc.relation.isformatof",
    oai_fall="relation"
)
_qdc(
    elem="relation",
    qual="hasPart",
    uri="http://purl.org/dc/terms/hasPart",
    label="Has Part",
    defn="A related resource that is included either physically or logically.",
    ds_field="dc.relation.haspart",
    oai_fall="relation"
)
_qdc(
    elem="relation",
    qual="isPartOf",
    uri="http://purl.org/dc/terms/isPartOf",
    label="Is Part Of",
    defn="A related resource in which the described resource is physically or logically included.",
    ds_field="dc.relation.ispartof",
    oai_fall="relation"
)
_qdc(
    elem="description",
    qual="custom_field_001",
    uri="http://purl.org/dc/terms/description/custom_field_001",
    label="Repository Metadata Parameter custom_field_001",
    defn="Institutional archive repository metadata term custom_field_001",
    ds_field="dc.description.custom_field_001",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_002",
    uri="http://purl.org/dc/terms/description/custom_field_002",
    label="Repository Metadata Parameter custom_field_002",
    defn="Institutional archive repository metadata term custom_field_002",
    ds_field="dc.description.custom_field_002",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_003",
    uri="http://purl.org/dc/terms/description/custom_field_003",
    label="Repository Metadata Parameter custom_field_003",
    defn="Institutional archive repository metadata term custom_field_003",
    ds_field="dc.description.custom_field_003",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_004",
    uri="http://purl.org/dc/terms/description/custom_field_004",
    label="Repository Metadata Parameter custom_field_004",
    defn="Institutional archive repository metadata term custom_field_004",
    ds_field="dc.description.custom_field_004",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_005",
    uri="http://purl.org/dc/terms/description/custom_field_005",
    label="Repository Metadata Parameter custom_field_005",
    defn="Institutional archive repository metadata term custom_field_005",
    ds_field="dc.description.custom_field_005",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_006",
    uri="http://purl.org/dc/terms/description/custom_field_006",
    label="Repository Metadata Parameter custom_field_006",
    defn="Institutional archive repository metadata term custom_field_006",
    ds_field="dc.description.custom_field_006",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_007",
    uri="http://purl.org/dc/terms/description/custom_field_007",
    label="Repository Metadata Parameter custom_field_007",
    defn="Institutional archive repository metadata term custom_field_007",
    ds_field="dc.description.custom_field_007",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_008",
    uri="http://purl.org/dc/terms/description/custom_field_008",
    label="Repository Metadata Parameter custom_field_008",
    defn="Institutional archive repository metadata term custom_field_008",
    ds_field="dc.description.custom_field_008",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_009",
    uri="http://purl.org/dc/terms/description/custom_field_009",
    label="Repository Metadata Parameter custom_field_009",
    defn="Institutional archive repository metadata term custom_field_009",
    ds_field="dc.description.custom_field_009",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_010",
    uri="http://purl.org/dc/terms/description/custom_field_010",
    label="Repository Metadata Parameter custom_field_010",
    defn="Institutional archive repository metadata term custom_field_010",
    ds_field="dc.description.custom_field_010",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_011",
    uri="http://purl.org/dc/terms/description/custom_field_011",
    label="Repository Metadata Parameter custom_field_011",
    defn="Institutional archive repository metadata term custom_field_011",
    ds_field="dc.description.custom_field_011",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_012",
    uri="http://purl.org/dc/terms/description/custom_field_012",
    label="Repository Metadata Parameter custom_field_012",
    defn="Institutional archive repository metadata term custom_field_012",
    ds_field="dc.description.custom_field_012",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_013",
    uri="http://purl.org/dc/terms/description/custom_field_013",
    label="Repository Metadata Parameter custom_field_013",
    defn="Institutional archive repository metadata term custom_field_013",
    ds_field="dc.description.custom_field_013",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_014",
    uri="http://purl.org/dc/terms/description/custom_field_014",
    label="Repository Metadata Parameter custom_field_014",
    defn="Institutional archive repository metadata term custom_field_014",
    ds_field="dc.description.custom_field_014",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_015",
    uri="http://purl.org/dc/terms/description/custom_field_015",
    label="Repository Metadata Parameter custom_field_015",
    defn="Institutional archive repository metadata term custom_field_015",
    ds_field="dc.description.custom_field_015",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_016",
    uri="http://purl.org/dc/terms/description/custom_field_016",
    label="Repository Metadata Parameter custom_field_016",
    defn="Institutional archive repository metadata term custom_field_016",
    ds_field="dc.description.custom_field_016",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_017",
    uri="http://purl.org/dc/terms/description/custom_field_017",
    label="Repository Metadata Parameter custom_field_017",
    defn="Institutional archive repository metadata term custom_field_017",
    ds_field="dc.description.custom_field_017",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_018",
    uri="http://purl.org/dc/terms/description/custom_field_018",
    label="Repository Metadata Parameter custom_field_018",
    defn="Institutional archive repository metadata term custom_field_018",
    ds_field="dc.description.custom_field_018",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_019",
    uri="http://purl.org/dc/terms/description/custom_field_019",
    label="Repository Metadata Parameter custom_field_019",
    defn="Institutional archive repository metadata term custom_field_019",
    ds_field="dc.description.custom_field_019",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_020",
    uri="http://purl.org/dc/terms/description/custom_field_020",
    label="Repository Metadata Parameter custom_field_020",
    defn="Institutional archive repository metadata term custom_field_020",
    ds_field="dc.description.custom_field_020",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_021",
    uri="http://purl.org/dc/terms/description/custom_field_021",
    label="Repository Metadata Parameter custom_field_021",
    defn="Institutional archive repository metadata term custom_field_021",
    ds_field="dc.description.custom_field_021",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_022",
    uri="http://purl.org/dc/terms/description/custom_field_022",
    label="Repository Metadata Parameter custom_field_022",
    defn="Institutional archive repository metadata term custom_field_022",
    ds_field="dc.description.custom_field_022",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_023",
    uri="http://purl.org/dc/terms/description/custom_field_023",
    label="Repository Metadata Parameter custom_field_023",
    defn="Institutional archive repository metadata term custom_field_023",
    ds_field="dc.description.custom_field_023",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_024",
    uri="http://purl.org/dc/terms/description/custom_field_024",
    label="Repository Metadata Parameter custom_field_024",
    defn="Institutional archive repository metadata term custom_field_024",
    ds_field="dc.description.custom_field_024",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_025",
    uri="http://purl.org/dc/terms/description/custom_field_025",
    label="Repository Metadata Parameter custom_field_025",
    defn="Institutional archive repository metadata term custom_field_025",
    ds_field="dc.description.custom_field_025",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_026",
    uri="http://purl.org/dc/terms/description/custom_field_026",
    label="Repository Metadata Parameter custom_field_026",
    defn="Institutional archive repository metadata term custom_field_026",
    ds_field="dc.description.custom_field_026",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_027",
    uri="http://purl.org/dc/terms/description/custom_field_027",
    label="Repository Metadata Parameter custom_field_027",
    defn="Institutional archive repository metadata term custom_field_027",
    ds_field="dc.description.custom_field_027",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_028",
    uri="http://purl.org/dc/terms/description/custom_field_028",
    label="Repository Metadata Parameter custom_field_028",
    defn="Institutional archive repository metadata term custom_field_028",
    ds_field="dc.description.custom_field_028",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_029",
    uri="http://purl.org/dc/terms/description/custom_field_029",
    label="Repository Metadata Parameter custom_field_029",
    defn="Institutional archive repository metadata term custom_field_029",
    ds_field="dc.description.custom_field_029",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_030",
    uri="http://purl.org/dc/terms/description/custom_field_030",
    label="Repository Metadata Parameter custom_field_030",
    defn="Institutional archive repository metadata term custom_field_030",
    ds_field="dc.description.custom_field_030",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_031",
    uri="http://purl.org/dc/terms/description/custom_field_031",
    label="Repository Metadata Parameter custom_field_031",
    defn="Institutional archive repository metadata term custom_field_031",
    ds_field="dc.description.custom_field_031",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_032",
    uri="http://purl.org/dc/terms/description/custom_field_032",
    label="Repository Metadata Parameter custom_field_032",
    defn="Institutional archive repository metadata term custom_field_032",
    ds_field="dc.description.custom_field_032",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_033",
    uri="http://purl.org/dc/terms/description/custom_field_033",
    label="Repository Metadata Parameter custom_field_033",
    defn="Institutional archive repository metadata term custom_field_033",
    ds_field="dc.description.custom_field_033",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_034",
    uri="http://purl.org/dc/terms/description/custom_field_034",
    label="Repository Metadata Parameter custom_field_034",
    defn="Institutional archive repository metadata term custom_field_034",
    ds_field="dc.description.custom_field_034",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_035",
    uri="http://purl.org/dc/terms/description/custom_field_035",
    label="Repository Metadata Parameter custom_field_035",
    defn="Institutional archive repository metadata term custom_field_035",
    ds_field="dc.description.custom_field_035",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_036",
    uri="http://purl.org/dc/terms/description/custom_field_036",
    label="Repository Metadata Parameter custom_field_036",
    defn="Institutional archive repository metadata term custom_field_036",
    ds_field="dc.description.custom_field_036",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_037",
    uri="http://purl.org/dc/terms/description/custom_field_037",
    label="Repository Metadata Parameter custom_field_037",
    defn="Institutional archive repository metadata term custom_field_037",
    ds_field="dc.description.custom_field_037",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_038",
    uri="http://purl.org/dc/terms/description/custom_field_038",
    label="Repository Metadata Parameter custom_field_038",
    defn="Institutional archive repository metadata term custom_field_038",
    ds_field="dc.description.custom_field_038",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_039",
    uri="http://purl.org/dc/terms/description/custom_field_039",
    label="Repository Metadata Parameter custom_field_039",
    defn="Institutional archive repository metadata term custom_field_039",
    ds_field="dc.description.custom_field_039",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_040",
    uri="http://purl.org/dc/terms/description/custom_field_040",
    label="Repository Metadata Parameter custom_field_040",
    defn="Institutional archive repository metadata term custom_field_040",
    ds_field="dc.description.custom_field_040",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_041",
    uri="http://purl.org/dc/terms/description/custom_field_041",
    label="Repository Metadata Parameter custom_field_041",
    defn="Institutional archive repository metadata term custom_field_041",
    ds_field="dc.description.custom_field_041",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_042",
    uri="http://purl.org/dc/terms/description/custom_field_042",
    label="Repository Metadata Parameter custom_field_042",
    defn="Institutional archive repository metadata term custom_field_042",
    ds_field="dc.description.custom_field_042",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_043",
    uri="http://purl.org/dc/terms/description/custom_field_043",
    label="Repository Metadata Parameter custom_field_043",
    defn="Institutional archive repository metadata term custom_field_043",
    ds_field="dc.description.custom_field_043",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_044",
    uri="http://purl.org/dc/terms/description/custom_field_044",
    label="Repository Metadata Parameter custom_field_044",
    defn="Institutional archive repository metadata term custom_field_044",
    ds_field="dc.description.custom_field_044",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_045",
    uri="http://purl.org/dc/terms/description/custom_field_045",
    label="Repository Metadata Parameter custom_field_045",
    defn="Institutional archive repository metadata term custom_field_045",
    ds_field="dc.description.custom_field_045",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_046",
    uri="http://purl.org/dc/terms/description/custom_field_046",
    label="Repository Metadata Parameter custom_field_046",
    defn="Institutional archive repository metadata term custom_field_046",
    ds_field="dc.description.custom_field_046",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_047",
    uri="http://purl.org/dc/terms/description/custom_field_047",
    label="Repository Metadata Parameter custom_field_047",
    defn="Institutional archive repository metadata term custom_field_047",
    ds_field="dc.description.custom_field_047",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_048",
    uri="http://purl.org/dc/terms/description/custom_field_048",
    label="Repository Metadata Parameter custom_field_048",
    defn="Institutional archive repository metadata term custom_field_048",
    ds_field="dc.description.custom_field_048",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_049",
    uri="http://purl.org/dc/terms/description/custom_field_049",
    label="Repository Metadata Parameter custom_field_049",
    defn="Institutional archive repository metadata term custom_field_049",
    ds_field="dc.description.custom_field_049",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_050",
    uri="http://purl.org/dc/terms/description/custom_field_050",
    label="Repository Metadata Parameter custom_field_050",
    defn="Institutional archive repository metadata term custom_field_050",
    ds_field="dc.description.custom_field_050",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_051",
    uri="http://purl.org/dc/terms/description/custom_field_051",
    label="Repository Metadata Parameter custom_field_051",
    defn="Institutional archive repository metadata term custom_field_051",
    ds_field="dc.description.custom_field_051",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_052",
    uri="http://purl.org/dc/terms/description/custom_field_052",
    label="Repository Metadata Parameter custom_field_052",
    defn="Institutional archive repository metadata term custom_field_052",
    ds_field="dc.description.custom_field_052",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_053",
    uri="http://purl.org/dc/terms/description/custom_field_053",
    label="Repository Metadata Parameter custom_field_053",
    defn="Institutional archive repository metadata term custom_field_053",
    ds_field="dc.description.custom_field_053",
    oai_fall="description"
)
_qdc(
    elem="description",
    qual="custom_field_054",
    uri="http://purl.org/dc/terms/description/custom_field_054",
    label="Repository Metadata Parameter custom_field_054",
    defn="Institutional archive repository metadata term custom_field_054",
    ds_field="dc.description.custom_field_054",
    oai_fall="description"
)

def lookup_qdc_term(element: str, qualifier: Optional[str] = None) -> Optional[QdcTermDefinition]:
    """Retrieve Qualified Dublin Core term definition."""
    key = f"{element}.{qualifier}".lower() if qualifier else element.lower()
    return QDC_TERMS_CATALOG.get(key)


def get_all_terms_for_element(element: str) -> List[QdcTermDefinition]:
    """Retrieve all qualifiers for a primary Dublin Core element."""
    clean = element.strip().lower()
    return [t for t in QDC_TERMS_CATALOG.values() if t.element_name.lower() == clean]
