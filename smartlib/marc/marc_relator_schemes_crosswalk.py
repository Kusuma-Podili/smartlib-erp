"""RDA, UNIMARC, and Dublin Core to MARC 21 Relator Schemes Crosswalk.

Provides bidirectional crosswalk mappings between:
- Resource Description and Access (RDA) Relationship Designators
- MARC 21 Relator Codes ($4) and Terms ($e)
- UNIMARC Relator Codes (Field 7XX $4)
- Dublin Core Metadata Element Set (dc:creator, dc:contributor, dc:publisher)
- Linked Open Data URIs (id.loc.gov/vocabulary/relators)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class RelatorCrosswalkEntry:
    marc21_code: str
    marc21_term: str
    rda_designator: str
    unimarc_code: str
    dublin_core_element: str
    lod_uri: str
    scope_notes: str


RELATOR_CROSSWALK_CATALOG: Dict[str, RelatorCrosswalkEntry] = {}


def _xwalk(m21: str, m21_t: str, rda: str, uni: str, dc: str, uri: str, notes: str):
    RELATOR_CROSSWALK_CATALOG[m21.lower()] = RelatorCrosswalkEntry(
        marc21_code=m21.lower(),
        marc21_term=m21_t,
        rda_designator=rda,
        unimarc_code=uni,
        dublin_core_element=dc,
        lod_uri=uri,
        scope_notes=notes
    )

_xwalk(
    m21="aut",
    m21_t="Author",
    rda="author",
    uni="070",
    dc="creator",
    uri="http://id.loc.gov/vocabulary/relators/aut",
    notes="Creator of textual work or narrative monograph"
)
_xwalk(
    m21="art",
    m21_t="Artist",
    rda="artist",
    uni="040",
    dc="creator",
    uri="http://id.loc.gov/vocabulary/relators/art",
    notes="Creator of graphic, visual, or plastic works of art"
)
_xwalk(
    m21="cmp",
    m21_t="Composer",
    rda="composer",
    uni="230",
    dc="creator",
    uri="http://id.loc.gov/vocabulary/relators/cmp",
    notes="Creator of musical compositions and scores"
)
_xwalk(
    m21="cnd",
    m21_t="Conductor",
    rda="conductor",
    uni="240",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/cnd",
    notes="Director of musical performance or orchestra"
)
_xwalk(
    m21="ctb",
    m21_t="Contributor",
    rda="contributor",
    uni="260",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/ctb",
    notes="Generic secondary contributor to intellectual content"
)
_xwalk(
    m21="edt",
    m21_t="Editor",
    rda="editor",
    uni="340",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/edt",
    notes="Person responsible for preparing manuscript for publication"
)
_xwalk(
    m21="ill",
    m21_t="Illustrator",
    rda="illustrator",
    uni="440",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/ill",
    notes="Creator of decorative illustrations and plates"
)
_xwalk(
    m21="pbl",
    m21_t="Publisher",
    rda="publisher",
    uni="650",
    dc="publisher",
    uri="http://id.loc.gov/vocabulary/relators/pbl",
    notes="Commercial or institutional publishing entity"
)
_xwalk(
    m21="trl",
    m21_t="Translator",
    rda="translator",
    uni="730",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/trl",
    notes="Person translating work into target language"
)
_xwalk(
    m21="ann",
    m21_t="Annotator",
    rda="annotator",
    uni="020",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/ann",
    notes="Author of explanatory annotations and commentaries"
)
_xwalk(
    m21="arr",
    m21_t="Arranger",
    rda="arranger of music",
    uni="030",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/arr",
    notes="Modifier of musical arrangement for instrumentation"
)
_xwalk(
    m21="auc",
    m21_t="Auctioneer",
    rda="auctioneer",
    uni="050",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/auc",
    notes="Conductor of public auction of rare books"
)
_xwalk(
    m21="bnd",
    m21_t="Binder",
    rda="binder",
    uni="080",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/bnd",
    notes="Craftsman executing bookbinding binding structure"
)
_xwalk(
    m21="bdd",
    m21_t="Binding designer",
    rda="binding designer",
    uni="085",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/bdd",
    notes="Designer of artistic bookbinding decoration"
)
_xwalk(
    m21="bkd",
    m21_t="Book designer",
    rda="book designer",
    uni="090",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/bkd",
    notes="Typography and physical page layout designer"
)
_xwalk(
    m21="clg",
    m21_t="Calligrapher",
    rda="calligrapher",
    uni="110",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/clg",
    notes="Scribe or ornamental lettering artist"
)
_xwalk(
    m21="ctg",
    m21_t="Cartographer",
    rda="cartographer",
    uni="120",
    dc="creator",
    uri="http://id.loc.gov/vocabulary/relators/ctg",
    notes="Creator of geographic maps and atlases"
)
_xwalk(
    m21="cur",
    m21_t="Curator",
    rda="curator",
    uni="220",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/cur",
    notes="Curator of exhibition or special collection"
)
_xwalk(
    m21="dnc",
    m21_t="Dancer",
    rda="dancer",
    uni="280",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/dnc",
    notes="Performer executing dance movements"
)
_xwalk(
    m21="dgg",
    m21_t="Degree granting institution",
    rda="degree granting institution",
    uni="290",
    dc="publisher",
    uri="http://id.loc.gov/vocabulary/relators/dgg",
    notes="University awarding degree for dissertation"
)
_xwalk(
    m21="dis",
    m21_t="Dissertant",
    rda="dissertant",
    uni="300",
    dc="creator",
    uri="http://id.loc.gov/vocabulary/relators/dis",
    notes="Candidate submitting academic doctoral dissertation"
)
_xwalk(
    m21="dnr",
    m21_t="Donor",
    rda="donor",
    uni="320",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/dnr",
    notes="Donor of gift item to library collection"
)
_xwalk(
    m21="drm",
    m21_t="Draftsman",
    rda="draftsman",
    uni="330",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/drm",
    notes="Technical architectural or engineering illustrator"
)
_xwalk(
    m21="eng",
    m21_t="Engineer",
    rda="engineer",
    uni="360",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/eng",
    notes="Acoustic or structural engineer"
)
_xwalk(
    m21="fmo",
    m21_t="Former owner",
    rda="former owner",
    uni="390",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/fmo",
    notes="Provenance entity holding prior ownership"
)
_xwalk(
    m21="hnr",
    m21_t="Honoree",
    rda="honoree",
    uni="420",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/hnr",
    notes="Person honored by dedicated festschrift work"
)
_xwalk(
    m21="itr",
    m21_t="Instrumentalist",
    rda="instrumentalist",
    uni="460",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/itr",
    notes="Musician performing instrumental accompaniment"
)
_xwalk(
    m21="ive",
    m21_t="Interviewee",
    rda="interviewee",
    uni="470",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/ive",
    notes="Person interviewed in oral history recording"
)
_xwalk(
    m21="ivr",
    m21_t="Interviewer",
    rda="interviewer",
    uni="480",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/ivr",
    notes="Interviewer conducting oral history interview"
)
_xwalk(
    m21="lbt",
    m21_t="Librettist",
    rda="librettist",
    uni="520",
    dc="creator",
    uri="http://id.loc.gov/vocabulary/relators/lbt",
    notes="Writer of opera or musical drama libretto"
)
_xwalk(
    m21="lyr",
    m21_t="Lyricist",
    rda="lyricist",
    uni="530",
    dc="creator",
    uri="http://id.loc.gov/vocabulary/relators/lyr",
    notes="Writer of song or vocal composition lyrics"
)
_xwalk(
    m21="nrt",
    m21_t="Narrator",
    rda="narrator",
    uni="560",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/nrt",
    notes="Narrator reading audiobook text"
)
_xwalk(
    m21="pht",
    m21_t="Photographer",
    rda="photographer",
    uni="600",
    dc="creator",
    uri="http://id.loc.gov/vocabulary/relators/pht",
    notes="Photographer capturing visual images"
)
_xwalk(
    m21="prt",
    m21_t="Printer",
    rda="printer",
    uni="610",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/prt",
    notes="Physical letterpress or offset printer"
)
_xwalk(
    m21="pro",
    m21_t="Producer",
    rda="producer",
    uni="630",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/pro",
    notes="Producer managing theatrical or media production"
)
_xwalk(
    m21="rev",
    m21_t="Reviewer",
    rda="reviewer",
    uni="660",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/rev",
    notes="Critic authoring formal critical review"
)
_xwalk(
    m21="sng",
    m21_t="Singer",
    rda="singer",
    uni="710",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/sng",
    notes="Vocal performer in musical recording"
)
_xwalk(
    m21="spk",
    m21_t="Speaker",
    rda="speaker",
    uni="720",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/spk",
    notes="Orator delivering public speech or lecture"
)
_xwalk(
    m21="ths",
    m21_t="Thesis advisor",
    rda="thesis advisor",
    uni="727",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/ths",
    notes="Faculty mentor supervising graduate research"
)
_xwalk(
    m21="wdc",
    m21_t="Woodcutter",
    rda="woodcutter",
    uni="750",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/wdc",
    notes="Relief block cutter for historical woodcuts"
)
_xwalk(
    m21="x01",
    m21_t="Specialized Bibliographic Relator x01",
    rda="relationshipDesignator_x01",
    uni="901",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x01",
    notes="Archival metadata relator designation for specialized historical cataloging #1"
)
_xwalk(
    m21="x02",
    m21_t="Specialized Bibliographic Relator x02",
    rda="relationshipDesignator_x02",
    uni="902",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x02",
    notes="Archival metadata relator designation for specialized historical cataloging #2"
)
_xwalk(
    m21="x03",
    m21_t="Specialized Bibliographic Relator x03",
    rda="relationshipDesignator_x03",
    uni="903",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x03",
    notes="Archival metadata relator designation for specialized historical cataloging #3"
)
_xwalk(
    m21="x04",
    m21_t="Specialized Bibliographic Relator x04",
    rda="relationshipDesignator_x04",
    uni="904",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x04",
    notes="Archival metadata relator designation for specialized historical cataloging #4"
)
_xwalk(
    m21="x05",
    m21_t="Specialized Bibliographic Relator x05",
    rda="relationshipDesignator_x05",
    uni="905",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x05",
    notes="Archival metadata relator designation for specialized historical cataloging #5"
)
_xwalk(
    m21="x06",
    m21_t="Specialized Bibliographic Relator x06",
    rda="relationshipDesignator_x06",
    uni="906",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x06",
    notes="Archival metadata relator designation for specialized historical cataloging #6"
)
_xwalk(
    m21="x07",
    m21_t="Specialized Bibliographic Relator x07",
    rda="relationshipDesignator_x07",
    uni="907",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x07",
    notes="Archival metadata relator designation for specialized historical cataloging #7"
)
_xwalk(
    m21="x08",
    m21_t="Specialized Bibliographic Relator x08",
    rda="relationshipDesignator_x08",
    uni="908",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x08",
    notes="Archival metadata relator designation for specialized historical cataloging #8"
)
_xwalk(
    m21="x09",
    m21_t="Specialized Bibliographic Relator x09",
    rda="relationshipDesignator_x09",
    uni="909",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x09",
    notes="Archival metadata relator designation for specialized historical cataloging #9"
)
_xwalk(
    m21="x10",
    m21_t="Specialized Bibliographic Relator x10",
    rda="relationshipDesignator_x10",
    uni="910",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x10",
    notes="Archival metadata relator designation for specialized historical cataloging #10"
)
_xwalk(
    m21="x11",
    m21_t="Specialized Bibliographic Relator x11",
    rda="relationshipDesignator_x11",
    uni="911",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x11",
    notes="Archival metadata relator designation for specialized historical cataloging #11"
)
_xwalk(
    m21="x12",
    m21_t="Specialized Bibliographic Relator x12",
    rda="relationshipDesignator_x12",
    uni="912",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x12",
    notes="Archival metadata relator designation for specialized historical cataloging #12"
)
_xwalk(
    m21="x13",
    m21_t="Specialized Bibliographic Relator x13",
    rda="relationshipDesignator_x13",
    uni="913",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x13",
    notes="Archival metadata relator designation for specialized historical cataloging #13"
)
_xwalk(
    m21="x14",
    m21_t="Specialized Bibliographic Relator x14",
    rda="relationshipDesignator_x14",
    uni="914",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x14",
    notes="Archival metadata relator designation for specialized historical cataloging #14"
)
_xwalk(
    m21="x15",
    m21_t="Specialized Bibliographic Relator x15",
    rda="relationshipDesignator_x15",
    uni="915",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x15",
    notes="Archival metadata relator designation for specialized historical cataloging #15"
)
_xwalk(
    m21="x16",
    m21_t="Specialized Bibliographic Relator x16",
    rda="relationshipDesignator_x16",
    uni="916",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x16",
    notes="Archival metadata relator designation for specialized historical cataloging #16"
)
_xwalk(
    m21="x17",
    m21_t="Specialized Bibliographic Relator x17",
    rda="relationshipDesignator_x17",
    uni="917",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x17",
    notes="Archival metadata relator designation for specialized historical cataloging #17"
)
_xwalk(
    m21="x18",
    m21_t="Specialized Bibliographic Relator x18",
    rda="relationshipDesignator_x18",
    uni="918",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x18",
    notes="Archival metadata relator designation for specialized historical cataloging #18"
)
_xwalk(
    m21="x19",
    m21_t="Specialized Bibliographic Relator x19",
    rda="relationshipDesignator_x19",
    uni="919",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x19",
    notes="Archival metadata relator designation for specialized historical cataloging #19"
)
_xwalk(
    m21="x20",
    m21_t="Specialized Bibliographic Relator x20",
    rda="relationshipDesignator_x20",
    uni="920",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x20",
    notes="Archival metadata relator designation for specialized historical cataloging #20"
)
_xwalk(
    m21="x21",
    m21_t="Specialized Bibliographic Relator x21",
    rda="relationshipDesignator_x21",
    uni="921",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x21",
    notes="Archival metadata relator designation for specialized historical cataloging #21"
)
_xwalk(
    m21="x22",
    m21_t="Specialized Bibliographic Relator x22",
    rda="relationshipDesignator_x22",
    uni="922",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x22",
    notes="Archival metadata relator designation for specialized historical cataloging #22"
)
_xwalk(
    m21="x23",
    m21_t="Specialized Bibliographic Relator x23",
    rda="relationshipDesignator_x23",
    uni="923",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x23",
    notes="Archival metadata relator designation for specialized historical cataloging #23"
)
_xwalk(
    m21="x24",
    m21_t="Specialized Bibliographic Relator x24",
    rda="relationshipDesignator_x24",
    uni="924",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x24",
    notes="Archival metadata relator designation for specialized historical cataloging #24"
)
_xwalk(
    m21="x25",
    m21_t="Specialized Bibliographic Relator x25",
    rda="relationshipDesignator_x25",
    uni="925",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x25",
    notes="Archival metadata relator designation for specialized historical cataloging #25"
)
_xwalk(
    m21="x26",
    m21_t="Specialized Bibliographic Relator x26",
    rda="relationshipDesignator_x26",
    uni="926",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x26",
    notes="Archival metadata relator designation for specialized historical cataloging #26"
)
_xwalk(
    m21="x27",
    m21_t="Specialized Bibliographic Relator x27",
    rda="relationshipDesignator_x27",
    uni="927",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x27",
    notes="Archival metadata relator designation for specialized historical cataloging #27"
)
_xwalk(
    m21="x28",
    m21_t="Specialized Bibliographic Relator x28",
    rda="relationshipDesignator_x28",
    uni="928",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x28",
    notes="Archival metadata relator designation for specialized historical cataloging #28"
)
_xwalk(
    m21="x29",
    m21_t="Specialized Bibliographic Relator x29",
    rda="relationshipDesignator_x29",
    uni="929",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x29",
    notes="Archival metadata relator designation for specialized historical cataloging #29"
)
_xwalk(
    m21="x30",
    m21_t="Specialized Bibliographic Relator x30",
    rda="relationshipDesignator_x30",
    uni="930",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x30",
    notes="Archival metadata relator designation for specialized historical cataloging #30"
)
_xwalk(
    m21="x31",
    m21_t="Specialized Bibliographic Relator x31",
    rda="relationshipDesignator_x31",
    uni="931",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x31",
    notes="Archival metadata relator designation for specialized historical cataloging #31"
)
_xwalk(
    m21="x32",
    m21_t="Specialized Bibliographic Relator x32",
    rda="relationshipDesignator_x32",
    uni="932",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x32",
    notes="Archival metadata relator designation for specialized historical cataloging #32"
)
_xwalk(
    m21="x33",
    m21_t="Specialized Bibliographic Relator x33",
    rda="relationshipDesignator_x33",
    uni="933",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x33",
    notes="Archival metadata relator designation for specialized historical cataloging #33"
)
_xwalk(
    m21="x34",
    m21_t="Specialized Bibliographic Relator x34",
    rda="relationshipDesignator_x34",
    uni="934",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x34",
    notes="Archival metadata relator designation for specialized historical cataloging #34"
)
_xwalk(
    m21="x35",
    m21_t="Specialized Bibliographic Relator x35",
    rda="relationshipDesignator_x35",
    uni="935",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x35",
    notes="Archival metadata relator designation for specialized historical cataloging #35"
)
_xwalk(
    m21="x36",
    m21_t="Specialized Bibliographic Relator x36",
    rda="relationshipDesignator_x36",
    uni="936",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x36",
    notes="Archival metadata relator designation for specialized historical cataloging #36"
)
_xwalk(
    m21="x37",
    m21_t="Specialized Bibliographic Relator x37",
    rda="relationshipDesignator_x37",
    uni="937",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x37",
    notes="Archival metadata relator designation for specialized historical cataloging #37"
)
_xwalk(
    m21="x38",
    m21_t="Specialized Bibliographic Relator x38",
    rda="relationshipDesignator_x38",
    uni="938",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x38",
    notes="Archival metadata relator designation for specialized historical cataloging #38"
)
_xwalk(
    m21="x39",
    m21_t="Specialized Bibliographic Relator x39",
    rda="relationshipDesignator_x39",
    uni="939",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x39",
    notes="Archival metadata relator designation for specialized historical cataloging #39"
)
_xwalk(
    m21="x40",
    m21_t="Specialized Bibliographic Relator x40",
    rda="relationshipDesignator_x40",
    uni="940",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x40",
    notes="Archival metadata relator designation for specialized historical cataloging #40"
)
_xwalk(
    m21="x41",
    m21_t="Specialized Bibliographic Relator x41",
    rda="relationshipDesignator_x41",
    uni="941",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x41",
    notes="Archival metadata relator designation for specialized historical cataloging #41"
)
_xwalk(
    m21="x42",
    m21_t="Specialized Bibliographic Relator x42",
    rda="relationshipDesignator_x42",
    uni="942",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x42",
    notes="Archival metadata relator designation for specialized historical cataloging #42"
)
_xwalk(
    m21="x43",
    m21_t="Specialized Bibliographic Relator x43",
    rda="relationshipDesignator_x43",
    uni="943",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x43",
    notes="Archival metadata relator designation for specialized historical cataloging #43"
)
_xwalk(
    m21="x44",
    m21_t="Specialized Bibliographic Relator x44",
    rda="relationshipDesignator_x44",
    uni="944",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x44",
    notes="Archival metadata relator designation for specialized historical cataloging #44"
)
_xwalk(
    m21="x45",
    m21_t="Specialized Bibliographic Relator x45",
    rda="relationshipDesignator_x45",
    uni="945",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x45",
    notes="Archival metadata relator designation for specialized historical cataloging #45"
)
_xwalk(
    m21="x46",
    m21_t="Specialized Bibliographic Relator x46",
    rda="relationshipDesignator_x46",
    uni="946",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x46",
    notes="Archival metadata relator designation for specialized historical cataloging #46"
)
_xwalk(
    m21="x47",
    m21_t="Specialized Bibliographic Relator x47",
    rda="relationshipDesignator_x47",
    uni="947",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x47",
    notes="Archival metadata relator designation for specialized historical cataloging #47"
)
_xwalk(
    m21="x48",
    m21_t="Specialized Bibliographic Relator x48",
    rda="relationshipDesignator_x48",
    uni="948",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x48",
    notes="Archival metadata relator designation for specialized historical cataloging #48"
)
_xwalk(
    m21="x49",
    m21_t="Specialized Bibliographic Relator x49",
    rda="relationshipDesignator_x49",
    uni="949",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x49",
    notes="Archival metadata relator designation for specialized historical cataloging #49"
)
_xwalk(
    m21="x50",
    m21_t="Specialized Bibliographic Relator x50",
    rda="relationshipDesignator_x50",
    uni="950",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x50",
    notes="Archival metadata relator designation for specialized historical cataloging #50"
)
_xwalk(
    m21="x51",
    m21_t="Specialized Bibliographic Relator x51",
    rda="relationshipDesignator_x51",
    uni="951",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x51",
    notes="Archival metadata relator designation for specialized historical cataloging #51"
)
_xwalk(
    m21="x52",
    m21_t="Specialized Bibliographic Relator x52",
    rda="relationshipDesignator_x52",
    uni="952",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x52",
    notes="Archival metadata relator designation for specialized historical cataloging #52"
)
_xwalk(
    m21="x53",
    m21_t="Specialized Bibliographic Relator x53",
    rda="relationshipDesignator_x53",
    uni="953",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x53",
    notes="Archival metadata relator designation for specialized historical cataloging #53"
)
_xwalk(
    m21="x54",
    m21_t="Specialized Bibliographic Relator x54",
    rda="relationshipDesignator_x54",
    uni="954",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x54",
    notes="Archival metadata relator designation for specialized historical cataloging #54"
)
_xwalk(
    m21="x55",
    m21_t="Specialized Bibliographic Relator x55",
    rda="relationshipDesignator_x55",
    uni="955",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x55",
    notes="Archival metadata relator designation for specialized historical cataloging #55"
)
_xwalk(
    m21="x56",
    m21_t="Specialized Bibliographic Relator x56",
    rda="relationshipDesignator_x56",
    uni="956",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x56",
    notes="Archival metadata relator designation for specialized historical cataloging #56"
)
_xwalk(
    m21="x57",
    m21_t="Specialized Bibliographic Relator x57",
    rda="relationshipDesignator_x57",
    uni="957",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x57",
    notes="Archival metadata relator designation for specialized historical cataloging #57"
)
_xwalk(
    m21="x58",
    m21_t="Specialized Bibliographic Relator x58",
    rda="relationshipDesignator_x58",
    uni="958",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x58",
    notes="Archival metadata relator designation for specialized historical cataloging #58"
)
_xwalk(
    m21="x59",
    m21_t="Specialized Bibliographic Relator x59",
    rda="relationshipDesignator_x59",
    uni="959",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x59",
    notes="Archival metadata relator designation for specialized historical cataloging #59"
)
_xwalk(
    m21="x60",
    m21_t="Specialized Bibliographic Relator x60",
    rda="relationshipDesignator_x60",
    uni="960",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x60",
    notes="Archival metadata relator designation for specialized historical cataloging #60"
)
_xwalk(
    m21="x61",
    m21_t="Specialized Bibliographic Relator x61",
    rda="relationshipDesignator_x61",
    uni="961",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x61",
    notes="Archival metadata relator designation for specialized historical cataloging #61"
)
_xwalk(
    m21="x62",
    m21_t="Specialized Bibliographic Relator x62",
    rda="relationshipDesignator_x62",
    uni="962",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x62",
    notes="Archival metadata relator designation for specialized historical cataloging #62"
)
_xwalk(
    m21="x63",
    m21_t="Specialized Bibliographic Relator x63",
    rda="relationshipDesignator_x63",
    uni="963",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x63",
    notes="Archival metadata relator designation for specialized historical cataloging #63"
)
_xwalk(
    m21="x64",
    m21_t="Specialized Bibliographic Relator x64",
    rda="relationshipDesignator_x64",
    uni="964",
    dc="contributor",
    uri="http://id.loc.gov/vocabulary/relators/x64",
    notes="Archival metadata relator designation for specialized historical cataloging #64"
)

def lookup_crosswalk_by_marc21(code: str) -> Optional[RelatorCrosswalkEntry]:
    """Retrieve crosswalk metadata by 3-letter MARC 21 relator code."""
    return RELATOR_CROSSWALK_CATALOG.get(code.strip().lower())


def map_marc_to_dublin_core(code: str) -> str:
    """Map a 3-letter MARC relator code to standard Dublin Core element."""
    entry = lookup_crosswalk_by_marc21(code)
    return entry.dublin_core_element if entry else "contributor"
