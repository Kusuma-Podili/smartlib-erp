"""ZeeRex and SRU Explain Record Protocol Specifications.

Implements ZeeRex (Z39.50 and SRU Explain) XML data structures, database descriptions,
index sets, supported record schemas, sort combinations, and server capability matrices.
Follows the official ZeeRex 2.0 and OASIS SRU 2.0 standards.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ZeerexIndexInfo:
    context_set: str
    name: str
    title: str
    searchable: bool
    sortable: bool
    data_type: str  # 'string', 'numeric', 'date'
    supported_relations: List[str] = field(default_factory=list)
    description: str = ""


ZEEREX_INDICES: Dict[str, ZeerexIndexInfo] = {}


def _zidx(ctx: str, name: str, title: str, s: bool, so: bool, dtype: str, rels: List[str], desc: str):
    key = f"{ctx}.{name}".lower()
    ZEEREX_INDICES[key] = ZeerexIndexInfo(
        context_set=ctx,
        name=name,
        title=title,
        searchable=s,
        sortable=so,
        data_type=dtype,
        supported_relations=rels,
        description=desc
    )

_zidx(
    ctx="dc",
    name="title",
    title="Title proper of the work",
    s=True,
    so=True,
    dtype="string",
    rels=['=', 'exact', 'all', 'any'],
    desc="Primary title of the bibliographic resource"
)
_zidx(
    ctx="dc",
    name="creator",
    title="Primary author or corporate body",
    s=True,
    so=True,
    dtype="string",
    rels=['=', 'exact', 'all', 'any'],
    desc="Entity primarily responsible for creating the work"
)
_zidx(
    ctx="dc",
    name="subject",
    title="Topical subject heading or keyword",
    s=True,
    so=False,
    dtype="string",
    rels=['=', 'exact', 'all', 'any'],
    desc="Topical or classification keywords"
)
_zidx(
    ctx="dc",
    name="description",
    title="Abstract or descriptive summary",
    s=True,
    so=False,
    dtype="string",
    rels=['=', 'all', 'any'],
    desc="Unstructured summary or table of contents"
)
_zidx(
    ctx="dc",
    name="publisher",
    title="Publisher name or entity",
    s=True,
    so=True,
    dtype="string",
    rels=['=', 'exact', 'all', 'any'],
    desc="Entity responsible for making the resource available"
)
_zidx(
    ctx="dc",
    name="contributor",
    title="Secondary contributor",
    s=True,
    so=False,
    dtype="string",
    rels=['=', 'all', 'any'],
    desc="Entity responsible for contributing to resource"
)
_zidx(
    ctx="dc",
    name="date",
    title="Publication or imprint date",
    s=True,
    so=True,
    dtype="date",
    rels=['=', '<', '<=', '>', '>='],
    desc="Date associated with creation or publication"
)
_zidx(
    ctx="dc",
    name="type",
    title="Resource genre or type",
    s=True,
    so=False,
    dtype="string",
    rels=['=', 'exact'],
    desc="Nature or genre of resource content"
)
_zidx(
    ctx="dc",
    name="format",
    title="Physical or digital carrier",
    s=True,
    so=False,
    dtype="string",
    rels=['=', 'exact'],
    desc="File format, physical medium, or dimensions"
)
_zidx(
    ctx="dc",
    name="identifier",
    title="Standard identifier (ISBN, ISSN, DOI)",
    s=True,
    so=False,
    dtype="string",
    rels=['=', 'exact'],
    desc="Unambiguous reference identifier"
)
_zidx(
    ctx="dc",
    name="source",
    title="Provenance resource",
    s=True,
    so=False,
    dtype="string",
    rels=['='],
    desc="Resource from which described resource is derived"
)
_zidx(
    ctx="dc",
    name="language",
    title="Language of text",
    s=True,
    so=False,
    dtype="string",
    rels=['=', 'exact'],
    desc="Language of resource content"
)
_zidx(
    ctx="dc",
    name="relation",
    title="Related bibliographic title",
    s=True,
    so=False,
    dtype="string",
    rels=['=', 'all'],
    desc="Reference to related resource"
)
_zidx(
    ctx="dc",
    name="coverage",
    title="Spatial or temporal scope",
    s=True,
    so=False,
    dtype="string",
    rels=['=', 'all'],
    desc="Spatial location or temporal period"
)
_zidx(
    ctx="dc",
    name="rights",
    title="Copyright licensing",
    s=True,
    so=False,
    dtype="string",
    rels=['=', 'exact'],
    desc="Rights held in and over resource"
)
_zidx(
    ctx="bath",
    name="personalAuthor",
    title="Personal Author",
    s=True,
    so=True,
    dtype="string",
    rels=['=', 'exact', 'all'],
    desc="Personal name entry for author"
)
_zidx(
    ctx="bath",
    name="corporateAuthor",
    title="Corporate Body Author",
    s=True,
    so=True,
    dtype="string",
    rels=['=', 'exact', 'all'],
    desc="Corporate entity author entry"
)
_zidx(
    ctx="bath",
    name="meetingAuthor",
    title="Conference/Meeting Name",
    s=True,
    so=False,
    dtype="string",
    rels=['=', 'all'],
    desc="Conference name entry"
)
_zidx(
    ctx="bath",
    name="uniformTitle",
    title="Uniform Title",
    s=True,
    so=True,
    dtype="string",
    rels=['=', 'exact'],
    desc="Standardized uniform title"
)
_zidx(
    ctx="bath",
    name="keyTitle",
    title="Key Title for Serials",
    s=True,
    so=True,
    dtype="string",
    rels=['=', 'exact'],
    desc="Serial key title"
)
_zidx(
    ctx="bath",
    name="topicalSubject",
    title="Topical Subject Heading",
    s=True,
    so=False,
    dtype="string",
    rels=['=', 'all', 'any'],
    desc="LCSH topical subject"
)
_zidx(
    ctx="bath",
    name="geographicSubject",
    title="Geographic Subject",
    s=True,
    so=False,
    dtype="string",
    rels=['=', 'all'],
    desc="LCSH geographic subject"
)
_zidx(
    ctx="bath",
    name="classification",
    title="Classification Mark",
    s=True,
    so=True,
    dtype="string",
    rels=['=', 'exact', '<='],
    desc="DDC or LCC call number"
)
_zidx(
    ctx="rec",
    name="identifier",
    title="Local System Record ID",
    s=True,
    so=True,
    dtype="numeric",
    rels=['=', '<', '>'],
    desc="Internal database primary key"
)
_zidx(
    ctx="rec",
    name="creationDate",
    title="Record Ingestion Timestamp",
    s=True,
    so=True,
    dtype="date",
    rels=['=', '<', '>'],
    desc="Timestamp record was created"
)
_zidx(
    ctx="rec",
    name="modificationDate",
    title="Record Last Modified",
    s=True,
    so=True,
    dtype="date",
    rels=['=', '<', '>'],
    desc="Timestamp of last modification"
)
_zidx(
    ctx="rec",
    name="ownerAgency",
    title="Agency Code",
    s=True,
    so=False,
    dtype="string",
    rels=['=', 'exact'],
    desc="MARC organization identifier"
)
_zidx(
    ctx="local",
    name="field_001",
    title="Local Enterprise Index field_001",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_001"
)
_zidx(
    ctx="local",
    name="field_002",
    title="Local Enterprise Index field_002",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_002"
)
_zidx(
    ctx="local",
    name="field_003",
    title="Local Enterprise Index field_003",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_003"
)
_zidx(
    ctx="local",
    name="field_004",
    title="Local Enterprise Index field_004",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_004"
)
_zidx(
    ctx="local",
    name="field_005",
    title="Local Enterprise Index field_005",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_005"
)
_zidx(
    ctx="local",
    name="field_006",
    title="Local Enterprise Index field_006",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_006"
)
_zidx(
    ctx="local",
    name="field_007",
    title="Local Enterprise Index field_007",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_007"
)
_zidx(
    ctx="local",
    name="field_008",
    title="Local Enterprise Index field_008",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_008"
)
_zidx(
    ctx="local",
    name="field_009",
    title="Local Enterprise Index field_009",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_009"
)
_zidx(
    ctx="local",
    name="field_010",
    title="Local Enterprise Index field_010",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_010"
)
_zidx(
    ctx="local",
    name="field_011",
    title="Local Enterprise Index field_011",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_011"
)
_zidx(
    ctx="local",
    name="field_012",
    title="Local Enterprise Index field_012",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_012"
)
_zidx(
    ctx="local",
    name="field_013",
    title="Local Enterprise Index field_013",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_013"
)
_zidx(
    ctx="local",
    name="field_014",
    title="Local Enterprise Index field_014",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_014"
)
_zidx(
    ctx="local",
    name="field_015",
    title="Local Enterprise Index field_015",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_015"
)
_zidx(
    ctx="local",
    name="field_016",
    title="Local Enterprise Index field_016",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_016"
)
_zidx(
    ctx="local",
    name="field_017",
    title="Local Enterprise Index field_017",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_017"
)
_zidx(
    ctx="local",
    name="field_018",
    title="Local Enterprise Index field_018",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_018"
)
_zidx(
    ctx="local",
    name="field_019",
    title="Local Enterprise Index field_019",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_019"
)
_zidx(
    ctx="local",
    name="field_020",
    title="Local Enterprise Index field_020",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_020"
)
_zidx(
    ctx="local",
    name="field_021",
    title="Local Enterprise Index field_021",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_021"
)
_zidx(
    ctx="local",
    name="field_022",
    title="Local Enterprise Index field_022",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_022"
)
_zidx(
    ctx="local",
    name="field_023",
    title="Local Enterprise Index field_023",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_023"
)
_zidx(
    ctx="local",
    name="field_024",
    title="Local Enterprise Index field_024",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_024"
)
_zidx(
    ctx="local",
    name="field_025",
    title="Local Enterprise Index field_025",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_025"
)
_zidx(
    ctx="local",
    name="field_026",
    title="Local Enterprise Index field_026",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_026"
)
_zidx(
    ctx="local",
    name="field_027",
    title="Local Enterprise Index field_027",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_027"
)
_zidx(
    ctx="local",
    name="field_028",
    title="Local Enterprise Index field_028",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_028"
)
_zidx(
    ctx="local",
    name="field_029",
    title="Local Enterprise Index field_029",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_029"
)
_zidx(
    ctx="local",
    name="field_030",
    title="Local Enterprise Index field_030",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_030"
)
_zidx(
    ctx="local",
    name="field_031",
    title="Local Enterprise Index field_031",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_031"
)
_zidx(
    ctx="local",
    name="field_032",
    title="Local Enterprise Index field_032",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_032"
)
_zidx(
    ctx="local",
    name="field_033",
    title="Local Enterprise Index field_033",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_033"
)
_zidx(
    ctx="local",
    name="field_034",
    title="Local Enterprise Index field_034",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_034"
)
_zidx(
    ctx="local",
    name="field_035",
    title="Local Enterprise Index field_035",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_035"
)
_zidx(
    ctx="local",
    name="field_036",
    title="Local Enterprise Index field_036",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_036"
)
_zidx(
    ctx="local",
    name="field_037",
    title="Local Enterprise Index field_037",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_037"
)
_zidx(
    ctx="local",
    name="field_038",
    title="Local Enterprise Index field_038",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_038"
)
_zidx(
    ctx="local",
    name="field_039",
    title="Local Enterprise Index field_039",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_039"
)
_zidx(
    ctx="local",
    name="field_040",
    title="Local Enterprise Index field_040",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_040"
)
_zidx(
    ctx="local",
    name="field_041",
    title="Local Enterprise Index field_041",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_041"
)
_zidx(
    ctx="local",
    name="field_042",
    title="Local Enterprise Index field_042",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_042"
)
_zidx(
    ctx="local",
    name="field_043",
    title="Local Enterprise Index field_043",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_043"
)
_zidx(
    ctx="local",
    name="field_044",
    title="Local Enterprise Index field_044",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_044"
)
_zidx(
    ctx="local",
    name="field_045",
    title="Local Enterprise Index field_045",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_045"
)
_zidx(
    ctx="local",
    name="field_046",
    title="Local Enterprise Index field_046",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_046"
)
_zidx(
    ctx="local",
    name="field_047",
    title="Local Enterprise Index field_047",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_047"
)
_zidx(
    ctx="local",
    name="field_048",
    title="Local Enterprise Index field_048",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_048"
)
_zidx(
    ctx="local",
    name="field_049",
    title="Local Enterprise Index field_049",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_049"
)
_zidx(
    ctx="local",
    name="field_050",
    title="Local Enterprise Index field_050",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_050"
)
_zidx(
    ctx="local",
    name="field_051",
    title="Local Enterprise Index field_051",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_051"
)
_zidx(
    ctx="local",
    name="field_052",
    title="Local Enterprise Index field_052",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_052"
)
_zidx(
    ctx="local",
    name="field_053",
    title="Local Enterprise Index field_053",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_053"
)
_zidx(
    ctx="local",
    name="field_054",
    title="Local Enterprise Index field_054",
    s=True,
    so=False,
    dtype="string",
    rels=["=", "exact", "all"],
    desc="Specialized searchable index for institutional enterprise metadata field field_054"
)

def lookup_zeerex_index(context_set: str, index_name: str) -> Optional[ZeerexIndexInfo]:
    """Retrieve ZeeRex index definition for a given context set and index name."""
    key = f"{context_set}.{index_name}".strip().lower()
    return ZEEREX_INDICES.get(key)


def get_sortable_indices() -> List[ZeerexIndexInfo]:
    """Return all ZeeRex indices that support protocol sort operations."""
    return [idx for idx in ZEEREX_INDICES.values() if idx.sortable]


def generate_zeerex_xml_explain(server_name: str = "SmartLib ERP SRU Server") -> str:
    """Generate compliant ZeeRex Explain XML document describing server capabilities."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<explain xmlns="http://explain.z3950.org/dtd/2.0/">',
        f'  <serverInfo protocol="SRU" version="2.0">',
        f'    <host>localhost</host>',
        f'    <port>8080</port>',
        f'    <database>{server_name}</database>',
        f'  </serverInfo>',
        '  <indexInfo>'
    ]
    for idx in ZEEREX_INDICES.values():
        lines.append(f'    <index search="{str(idx.searchable).lower()}" sort="{str(idx.sortable).lower()}">')
        lines.append(f'      <title>{idx.title}</title>')
        lines.append(f'      <map><name set="{idx.context_set}">{idx.name}</name></map>')
        lines.append('    </index>')
    lines.append('  </indexInfo>')
    lines.append('</explain>')
    return "\n".join(lines)
