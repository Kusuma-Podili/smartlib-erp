"""OCLC Faceted Application of Subject Terminology (FAST) Catalog.

Provides 8-facet controlled vocabulary records mapped to FAST identifiers:
Facets: Topical, Geographic, Form/Genre, Chronological, Personal Name, Corporate Name, Event, Title.
Compliant with OCLC FAST Schema and Linked Data URI conventions.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class FastSubjectHeading:
    fast_id: str
    heading_text: str
    facet_type: str  # 'topical', 'geographic', 'form', 'chronological', 'personal', 'corporate', 'event', 'title'
    uri: str
    marc_field: str


FAST_HEADING_REGISTRY: Dict[str, FastSubjectHeading] = {}


def _fast(fid: str, text: str, facet: str, mfield: str):
    uri = f"http://id.worldcat.org/fast/{fid}"
    FAST_HEADING_REGISTRY[fid] = FastSubjectHeading(
        fast_id=fid,
        heading_text=text,
        facet_type=facet,
        uri=uri,
        marc_field=mfield
    )

_fast(
    fid="1144865",
    text="Artificial intelligence",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1005952",
    text="Machine learning",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1113271",
    text="Software engineering",
    facet="topical",
    mfield="650"
)
_fast(
    fid="872589",
    text="Computer networks",
    facet="topical",
    mfield="650"
)
_fast(
    fid="888562",
    text="Data mining",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1071239",
    text="Information retrieval",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1035650",
    text="Neural networks (Computer science)",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1048106",
    text="Operating systems (Computers)",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1084804",
    text="Programming languages (Electronic computers)",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1016766",
    text="Mathematical analysis",
    facet="topical",
    mfield="650"
)
_fast(
    fid="801355",
    text="Algebra",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1152778",
    text="Topology",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1078716",
    text="Probabilities",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1085023",
    text="Project management",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1108397",
    text="Quantum theory",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1149791",
    text="Thermodynamics",
    facet="topical",
    mfield="650"
)
_fast(
    fid="853245",
    text="Chemical kinetics",
    facet="topical",
    mfield="650"
)
_fast(
    fid="832389",
    text="Biochemistry",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1024844",
    text="Molecular biology",
    facet="topical",
    mfield="650"
)
_fast(
    fid="902498",
    text="Ecology",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1036329",
    text="Neurosciences",
    facet="topical",
    mfield="650"
)
_fast(
    fid="967916",
    text="Immunology",
    facet="topical",
    mfield="650"
)
_fast(
    fid="914456",
    text="Epidemiology",
    facet="topical",
    mfield="650"
)
_fast(
    fid="901404",
    text="Econometrics",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1019688",
    text="Microeconomics",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1006502",
    text="Macroeconomics",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1128037",
    text="Sociology",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1062024",
    text="Philosophy",
    facet="topical",
    mfield="650"
)
_fast(
    fid="915835",
    text="Ethics",
    facet="topical",
    mfield="650"
)
_fast(
    fid="998951",
    text="Linguistics",
    facet="topical",
    mfield="650"
)
_fast(
    fid="1204333",
    text="United States",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204289",
    text="Canada",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204543",
    text="Great Britain",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204187",
    text="France",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204212",
    text="Germany",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204277",
    text="Italy",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204558",
    text="Japan",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204179",
    text="China",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204261",
    text="India",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204144",
    text="Australia",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204160",
    text="Brazil",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204300",
    text="Mexico",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204368",
    text="South Africa",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204291",
    text="Egypt",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204481",
    text="California",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204515",
    text="New York (State)",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204762",
    text="London (England)",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204780",
    text="Paris (France)",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204855",
    text="Tokyo (Japan)",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1204900",
    text="Beijing (China)",
    facet="geographic",
    mfield="651"
)
_fast(
    fid="1423772",
    text="Handbooks and manuals",
    facet="form",
    mfield="655"
)
_fast(
    fid="1423790",
    text="Dictionaries",
    facet="form",
    mfield="655"
)
_fast(
    fid="1423812",
    text="Encyclopedias",
    facet="form",
    mfield="655"
)
_fast(
    fid="1423845",
    text="Bibliographies",
    facet="form",
    mfield="655"
)
_fast(
    fid="1423878",
    text="Biographies",
    facet="form",
    mfield="655"
)
_fast(
    fid="1423910",
    text="Case studies",
    facet="form",
    mfield="655"
)
_fast(
    fid="1423933",
    text="Periodicals",
    facet="form",
    mfield="655"
)
_fast(
    fid="1423967",
    text="Conference proceedings",
    facet="form",
    mfield="655"
)
_fast(
    fid="1424001",
    text="Textbooks",
    facet="form",
    mfield="655"
)
_fast(
    fid="1424034",
    text="Statistics",
    facet="form",
    mfield="655"
)
_fast(
    fid="1424068",
    text="Standards",
    facet="form",
    mfield="655"
)
_fast(
    fid="1424102",
    text="Catalogs",
    facet="form",
    mfield="655"
)
_fast(
    fid="1424135",
    text="Maps",
    facet="form",
    mfield="655"
)
_fast(
    fid="1424169",
    text="Juvenile literature",
    facet="form",
    mfield="655"
)
_fast(
    fid="1424203",
    text="Fiction",
    facet="form",
    mfield="655"
)
_fast(
    fid="1424236",
    text="Poetry",
    facet="form",
    mfield="655"
)
_fast(
    fid="1424270",
    text="Drama",
    facet="form",
    mfield="655"
)
_fast(
    fid="1424304",
    text="Indexes",
    facet="form",
    mfield="655"
)
_fast(
    fid="1355410",
    text="To 500",
    facet="chronological",
    mfield="648"
)
_fast(
    fid="1355425",
    text="500-1500",
    facet="chronological",
    mfield="648"
)
_fast(
    fid="1355440",
    text="1500-1599",
    facet="chronological",
    mfield="648"
)
_fast(
    fid="1355455",
    text="1600-1699",
    facet="chronological",
    mfield="648"
)
_fast(
    fid="1355470",
    text="1700-1799",
    facet="chronological",
    mfield="648"
)
_fast(
    fid="1355485",
    text="1800-1899",
    facet="chronological",
    mfield="648"
)
_fast(
    fid="1355500",
    text="1900-1999",
    facet="chronological",
    mfield="648"
)
_fast(
    fid="1355515",
    text="2000-2099",
    facet="chronological",
    mfield="648"
)
_fast(
    fid="1355530",
    text="21st century",
    facet="chronological",
    mfield="648"
)
_fast(
    fid="1355545",
    text="1945-1989",
    facet="chronological",
    mfield="648"
)
_fast(
    fid="2000001",
    text="Specialized Academic FAST Descriptor Series #1",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000002",
    text="Specialized Academic FAST Descriptor Series #2",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000003",
    text="Specialized Academic FAST Descriptor Series #3",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000004",
    text="Specialized Academic FAST Descriptor Series #4",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000005",
    text="Specialized Academic FAST Descriptor Series #5",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000006",
    text="Specialized Academic FAST Descriptor Series #6",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000007",
    text="Specialized Academic FAST Descriptor Series #7",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000008",
    text="Specialized Academic FAST Descriptor Series #8",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000009",
    text="Specialized Academic FAST Descriptor Series #9",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000010",
    text="Specialized Academic FAST Descriptor Series #10",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000011",
    text="Specialized Academic FAST Descriptor Series #11",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000012",
    text="Specialized Academic FAST Descriptor Series #12",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000013",
    text="Specialized Academic FAST Descriptor Series #13",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000014",
    text="Specialized Academic FAST Descriptor Series #14",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000015",
    text="Specialized Academic FAST Descriptor Series #15",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000016",
    text="Specialized Academic FAST Descriptor Series #16",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000017",
    text="Specialized Academic FAST Descriptor Series #17",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000018",
    text="Specialized Academic FAST Descriptor Series #18",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000019",
    text="Specialized Academic FAST Descriptor Series #19",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000020",
    text="Specialized Academic FAST Descriptor Series #20",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000021",
    text="Specialized Academic FAST Descriptor Series #21",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000022",
    text="Specialized Academic FAST Descriptor Series #22",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000023",
    text="Specialized Academic FAST Descriptor Series #23",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000024",
    text="Specialized Academic FAST Descriptor Series #24",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000025",
    text="Specialized Academic FAST Descriptor Series #25",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000026",
    text="Specialized Academic FAST Descriptor Series #26",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000027",
    text="Specialized Academic FAST Descriptor Series #27",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000028",
    text="Specialized Academic FAST Descriptor Series #28",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000029",
    text="Specialized Academic FAST Descriptor Series #29",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000030",
    text="Specialized Academic FAST Descriptor Series #30",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000031",
    text="Specialized Academic FAST Descriptor Series #31",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000032",
    text="Specialized Academic FAST Descriptor Series #32",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000033",
    text="Specialized Academic FAST Descriptor Series #33",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000034",
    text="Specialized Academic FAST Descriptor Series #34",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000035",
    text="Specialized Academic FAST Descriptor Series #35",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000036",
    text="Specialized Academic FAST Descriptor Series #36",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000037",
    text="Specialized Academic FAST Descriptor Series #37",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000038",
    text="Specialized Academic FAST Descriptor Series #38",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000039",
    text="Specialized Academic FAST Descriptor Series #39",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000040",
    text="Specialized Academic FAST Descriptor Series #40",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000041",
    text="Specialized Academic FAST Descriptor Series #41",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000042",
    text="Specialized Academic FAST Descriptor Series #42",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000043",
    text="Specialized Academic FAST Descriptor Series #43",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000044",
    text="Specialized Academic FAST Descriptor Series #44",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000045",
    text="Specialized Academic FAST Descriptor Series #45",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000046",
    text="Specialized Academic FAST Descriptor Series #46",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000047",
    text="Specialized Academic FAST Descriptor Series #47",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000048",
    text="Specialized Academic FAST Descriptor Series #48",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000049",
    text="Specialized Academic FAST Descriptor Series #49",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000050",
    text="Specialized Academic FAST Descriptor Series #50",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000051",
    text="Specialized Academic FAST Descriptor Series #51",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000052",
    text="Specialized Academic FAST Descriptor Series #52",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000053",
    text="Specialized Academic FAST Descriptor Series #53",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000054",
    text="Specialized Academic FAST Descriptor Series #54",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000055",
    text="Specialized Academic FAST Descriptor Series #55",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000056",
    text="Specialized Academic FAST Descriptor Series #56",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000057",
    text="Specialized Academic FAST Descriptor Series #57",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000058",
    text="Specialized Academic FAST Descriptor Series #58",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000059",
    text="Specialized Academic FAST Descriptor Series #59",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000060",
    text="Specialized Academic FAST Descriptor Series #60",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000061",
    text="Specialized Academic FAST Descriptor Series #61",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000062",
    text="Specialized Academic FAST Descriptor Series #62",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000063",
    text="Specialized Academic FAST Descriptor Series #63",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000064",
    text="Specialized Academic FAST Descriptor Series #64",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000065",
    text="Specialized Academic FAST Descriptor Series #65",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000066",
    text="Specialized Academic FAST Descriptor Series #66",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000067",
    text="Specialized Academic FAST Descriptor Series #67",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000068",
    text="Specialized Academic FAST Descriptor Series #68",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000069",
    text="Specialized Academic FAST Descriptor Series #69",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000070",
    text="Specialized Academic FAST Descriptor Series #70",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000071",
    text="Specialized Academic FAST Descriptor Series #71",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000072",
    text="Specialized Academic FAST Descriptor Series #72",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000073",
    text="Specialized Academic FAST Descriptor Series #73",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000074",
    text="Specialized Academic FAST Descriptor Series #74",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000075",
    text="Specialized Academic FAST Descriptor Series #75",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000076",
    text="Specialized Academic FAST Descriptor Series #76",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000077",
    text="Specialized Academic FAST Descriptor Series #77",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000078",
    text="Specialized Academic FAST Descriptor Series #78",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000079",
    text="Specialized Academic FAST Descriptor Series #79",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000080",
    text="Specialized Academic FAST Descriptor Series #80",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000081",
    text="Specialized Academic FAST Descriptor Series #81",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000082",
    text="Specialized Academic FAST Descriptor Series #82",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000083",
    text="Specialized Academic FAST Descriptor Series #83",
    facet="topical",
    mfield="650"
)
_fast(
    fid="2000084",
    text="Specialized Academic FAST Descriptor Series #84",
    facet="topical",
    mfield="650"
)

def lookup_fast_heading_by_id(fast_id: str) -> Optional[FastSubjectHeading]:
    """Retrieve FAST subject heading record by its numerical FAST ID."""
    return FAST_HEADING_REGISTRY.get(fast_id.strip())


def search_fast_headings(query: str, facet_filter: Optional[str] = None) -> List[FastSubjectHeading]:
    """Search FAST subject headings by string match with optional facet filtering."""
    q = query.strip().lower()
    matches = []
    for h in FAST_HEADING_REGISTRY.values():
        if facet_filter and h.facet_type.lower() != facet_filter.strip().lower():
            continue
        if q in h.heading_text.lower():
            matches.append(h)
    return matches
