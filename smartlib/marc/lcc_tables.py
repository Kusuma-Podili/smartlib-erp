"""Library of Congress Classification (LCC) Outline and Subclass Table.

Provides standard LCC letter-based classifications and subject descriptions.
"""

from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class LccSubclass:
    code: str
    main_class: str
    description: str


LCC_SUBCLASSES: Dict[str, LccSubclass] = {}

# Class A - General Works
LCC_SUBCLASSES["A"] = LccSubclass("A", "General Works", "General Works (Collections, Polygraphy)")
LCC_SUBCLASSES["AC"] = LccSubclass("AC", "General Works", "Collections, Series, Collected works")
LCC_SUBCLASSES["AE"] = LccSubclass("AE", "General Works", "Encyclopedias")
LCC_SUBCLASSES["AG"] = LccSubclass("AG", "General Works", "Dictionaries and other general reference works")
LCC_SUBCLASSES["AI"] = LccSubclass("AI", "General Works", "Indexes")
LCC_SUBCLASSES["AM"] = LccSubclass("AM", "General Works", "Museums, Collectors and collecting")
LCC_SUBCLASSES["AN"] = LccSubclass("AN", "General Works", "Newspapers")
LCC_SUBCLASSES["AP"] = LccSubclass("AP", "General Works", "Periodicals")
LCC_SUBCLASSES["AS"] = LccSubclass("AS", "General Works", "Academies and learned societies")
LCC_SUBCLASSES["AY"] = LccSubclass("AY", "General Works", "Yearbooks, Almanacs, Directories")
LCC_SUBCLASSES["AZ"] = LccSubclass("AZ", "General Works", "History of scholarship and learning, The humanities")

# Class B - Philosophy, Psychology, Religion
LCC_SUBCLASSES["B"] = LccSubclass("B", "Philosophy, Psychology, Religion", "Philosophy (General)")
LCC_SUBCLASSES["BC"] = LccSubclass("BC", "Philosophy, Psychology, Religion", "Logic")
LCC_SUBCLASSES["BD"] = LccSubclass("BD", "Philosophy, Psychology, Religion", "Speculative philosophy")
LCC_SUBCLASSES["BF"] = LccSubclass("BF", "Philosophy, Psychology, Religion", "Psychology")
LCC_SUBCLASSES["BH"] = LccSubclass("BH", "Philosophy, Psychology, Religion", "Aesthetics")
LCC_SUBCLASSES["BJ"] = LccSubclass("BJ", "Philosophy, Psychology, Religion", "Ethics")
LCC_SUBCLASSES["BL"] = LccSubclass("BL", "Philosophy, Psychology, Religion", "Religions, Mythology, Rationalism")
LCC_SUBCLASSES["BM"] = LccSubclass("BM", "Philosophy, Psychology, Religion", "Judaism")
LCC_SUBCLASSES["BP"] = LccSubclass("BP", "Philosophy, Psychology, Religion", "Islam, Bahaism, Theosophy")
LCC_SUBCLASSES["BQ"] = LccSubclass("BQ", "Philosophy, Psychology, Religion", "Buddhism")
LCC_SUBCLASSES["BR"] = LccSubclass("BR", "Philosophy, Psychology, Religion", "Christianity, Church history")
LCC_SUBCLASSES["BS"] = LccSubclass("BS", "Philosophy, Psychology, Religion", "The Bible")
LCC_SUBCLASSES["BT"] = LccSubclass("BT", "Philosophy, Psychology, Religion", "Doctrinal Theology")
LCC_SUBCLASSES["BV"] = LccSubclass("BV", "Philosophy, Psychology, Religion", "Practical Theology")
LCC_SUBCLASSES["BX"] = LccSubclass("BX", "Philosophy, Psychology, Religion", "Christian Denominations")

# Class C - Auxiliary Sciences of History
LCC_SUBCLASSES["C"] = LccSubclass("C", "Auxiliary Sciences of History", "Auxiliary Sciences of History (General)")
LCC_SUBCLASSES["CB"] = LccSubclass("CB", "Auxiliary Sciences of History", "History of Civilization")
LCC_SUBCLASSES["CC"] = LccSubclass("CC", "Auxiliary Sciences of History", "Archaeology")
LCC_SUBCLASSES["CD"] = LccSubclass("CD", "Auxiliary Sciences of History", "Diplomatics, Archives, Seals")
LCC_SUBCLASSES["CE"] = LccSubclass("CE", "Auxiliary Sciences of History", "Technical Chronology, Calendar")
LCC_SUBCLASSES["CJ"] = LccSubclass("CJ", "Auxiliary Sciences of History", "Numismatics")
LCC_SUBCLASSES["CN"] = LccSubclass("CN", "Auxiliary Sciences of History", "Epigraphy, Inscriptions")
LCC_SUBCLASSES["CR"] = LccSubclass("CR", "Auxiliary Sciences of History", "Heraldry")
LCC_SUBCLASSES["CS"] = LccSubclass("CS", "Auxiliary Sciences of History", "Genealogy")
LCC_SUBCLASSES["CT"] = LccSubclass("CT", "Auxiliary Sciences of History", "Biography")

# Class D - World History
LCC_SUBCLASSES["D"] = LccSubclass("D", "World History", "History (General)")
LCC_SUBCLASSES["DA"] = LccSubclass("DA", "World History", "Great Britain")
LCC_SUBCLASSES["DAW"] = LccSubclass("DAW", "World History", "Central Europe")
LCC_SUBCLASSES["DB"] = LccSubclass("DB", "World History", "Austria, Liechtenstein, Hungary, Czechoslovakia")
LCC_SUBCLASSES["DC"] = LccSubclass("DC", "World History", "France, Andorra, Monaco")
LCC_SUBCLASSES["DD"] = LccSubclass("DD", "World History", "Germany")
LCC_SUBCLASSES["DE"] = LccSubclass("DE", "World History", "Greco-Roman World")
LCC_SUBCLASSES["DF"] = LccSubclass("DF", "World History", "Greece")
LCC_SUBCLASSES["DG"] = LccSubclass("DG", "World History", "Italy, Malta")
LCC_SUBCLASSES["DH"] = LccSubclass("DH", "World History", "Low Countries, Benelux Countries")
LCC_SUBCLASSES["DJ"] = LccSubclass("DJ", "World History", "Netherlands (Holland)")
LCC_SUBCLASSES["DJK"] = LccSubclass("DJK", "World History", "Eastern Europe (General)")
LCC_SUBCLASSES["DK"] = LccSubclass("DK", "World History", "Russia, Soviet Union, Former Soviet Republics, Poland")
LCC_SUBCLASSES["DL"] = LccSubclass("DL", "World History", "Northern Europe, Scandinavia")
LCC_SUBCLASSES["DP"] = LccSubclass("DP", "World History", "Spain, Portugal")
LCC_SUBCLASSES["DQ"] = LccSubclass("DQ", "World History", "Switzerland")
LCC_SUBCLASSES["DR"] = LccSubclass("DR", "World History", "Balkan Peninsula")
LCC_SUBCLASSES["DS"] = LccSubclass("DS", "World History", "Asia")
LCC_SUBCLASSES["DT"] = LccSubclass("DT", "World History", "Africa")
LCC_SUBCLASSES["DU"] = LccSubclass("DU", "World History", "Oceania (South Seas)")
LCC_SUBCLASSES["DX"] = LccSubclass("DX", "World History", "Romanies")

# Class G - Geography, Anthropology, Recreation
LCC_SUBCLASSES["G"] = LccSubclass("G", "Geography, Anthropology, Recreation", "Geography (General), Atlases, Maps")
LCC_SUBCLASSES["GA"] = LccSubclass("GA", "Geography, Anthropology, Recreation", "Mathematical geography, Cartography")
LCC_SUBCLASSES["GB"] = LccSubclass("GB", "Geography, Anthropology, Recreation", "Physical geography")
LCC_SUBCLASSES["GC"] = LccSubclass("GC", "Geography, Anthropology, Recreation", "Oceanography")
LCC_SUBCLASSES["GE"] = LccSubclass("GE", "Geography, Anthropology, Recreation", "Environmental Sciences")
LCC_SUBCLASSES["GF"] = LccSubclass("GF", "Geography, Anthropology, Recreation", "Human ecology, Anthropogeography")
LCC_SUBCLASSES["GN"] = LccSubclass("GN", "Geography, Anthropology, Recreation", "Anthropology")
LCC_SUBCLASSES["GR"] = LccSubclass("GR", "Geography, Anthropology, Recreation", "Folklore")
LCC_SUBCLASSES["GT"] = LccSubclass("GT", "Geography, Anthropology, Recreation", "Manners and customs (General)")
LCC_SUBCLASSES["GV"] = LccSubclass("GV", "Geography, Anthropology, Recreation", "Recreation, Leisure, Sports, Games")

# Class H - Social Sciences
LCC_SUBCLASSES["H"] = LccSubclass("H", "Social Sciences", "Social sciences (General)")
LCC_SUBCLASSES["HA"] = LccSubclass("HA", "Social Sciences", "Statistics")
LCC_SUBCLASSES["HB"] = LccSubclass("HB", "Social Sciences", "Economic theory, Demography")
LCC_SUBCLASSES["HC"] = LccSubclass("HC", "Social Sciences", "Economic history and conditions")
LCC_SUBCLASSES["HD"] = LccSubclass("HD", "Social Sciences", "Industries, Land use, Labor")
LCC_SUBCLASSES["HE"] = LccSubclass("HE", "Social Sciences", "Transportation and communications")
LCC_SUBCLASSES["HF"] = LccSubclass("HF", "Social Sciences", "Commerce")
LCC_SUBCLASSES["HG"] = LccSubclass("HG", "Social Sciences", "Finance")
LCC_SUBCLASSES["HJ"] = LccSubclass("HJ", "Social Sciences", "Public finance")
LCC_SUBCLASSES["HM"] = LccSubclass("HM", "Social Sciences", "Sociology (General)")
LCC_SUBCLASSES["HN"] = LccSubclass("HN", "Social Sciences", "Social history and conditions, Social problems, Social reform")
LCC_SUBCLASSES["HQ"] = LccSubclass("HQ", "Social Sciences", "The family, Marriage, Women")
LCC_SUBCLASSES["HS"] = LccSubclass("HS", "Social Sciences", "Societies: secret, benevolent, etc.")
LCC_SUBCLASSES["HT"] = LccSubclass("HT", "Social Sciences", "Communities, Classes, Races")
LCC_SUBCLASSES["HV"] = LccSubclass("HV", "Social Sciences", "Social pathology, Social and public welfare, Criminology")
LCC_SUBCLASSES["HX"] = LccSubclass("HX", "Social Sciences", "Socialism, Communism, Anarchism")

# Class Q - Science
LCC_SUBCLASSES["Q"] = LccSubclass("Q", "Science", "Science (General)")
LCC_SUBCLASSES["QA"] = LccSubclass("QA", "Science", "Mathematics, Computer Science")
LCC_SUBCLASSES["QB"] = LccSubclass("QB", "Science", "Astronomy")
LCC_SUBCLASSES["QC"] = LccSubclass("QC", "Science", "Physics")
LCC_SUBCLASSES["QD"] = LccSubclass("QD", "Science", "Chemistry")
LCC_SUBCLASSES["QE"] = LccSubclass("QE", "Science", "Geology")
LCC_SUBCLASSES["QH"] = LccSubclass("QH", "Science", "Natural history, Biology")
LCC_SUBCLASSES["QK"] = LccSubclass("QK", "Science", "Botany")
LCC_SUBCLASSES["QL"] = LccSubclass("QL", "Science", "Zoology")
LCC_SUBCLASSES["QM"] = LccSubclass("QM", "Science", "Human anatomy")
LCC_SUBCLASSES["QP"] = LccSubclass("QP", "Science", "Physiology")
LCC_SUBCLASSES["QR"] = LccSubclass("QR", "Science", "Microbiology")

# Class T - Technology
LCC_SUBCLASSES["T"] = LccSubclass("T", "Technology", "Technology (General)")
LCC_SUBCLASSES["TA"] = LccSubclass("TA", "Technology", "Engineering (General), Civil engineering")
LCC_SUBCLASSES["TC"] = LccSubclass("TC", "Technology", "Hydraulic engineering, Ocean engineering")
LCC_SUBCLASSES["TD"] = LccSubclass("TD", "Technology", "Environmental technology, Sanitary engineering")
LCC_SUBCLASSES["TE"] = LccSubclass("TE", "Technology", "Highway engineering, Roads and pavements")
LCC_SUBCLASSES["TF"] = LccSubclass("TF", "Technology", "Railroad engineering and operation")
LCC_SUBCLASSES["TG"] = LccSubclass("TG", "Technology", "Bridge engineering")
LCC_SUBCLASSES["TH"] = LccSubclass("TH", "Technology", "Building construction")
LCC_SUBCLASSES["TJ"] = LccSubclass("TJ", "Technology", "Mechanical engineering and machinery")
LCC_SUBCLASSES["TK"] = LccSubclass("TK", "Technology", "Electrical engineering, Electronics, Nuclear engineering")
LCC_SUBCLASSES["TL"] = LccSubclass("TL", "Technology", "Motor vehicles, Aeronautics, Astronautics")
LCC_SUBCLASSES["TN"] = LccSubclass("TN", "Technology", "Mining engineering, Metallurgy")
LCC_SUBCLASSES["TP"] = LccSubclass("TP", "Technology", "Chemical technology")
LCC_SUBCLASSES["TR"] = LccSubclass("TR", "Technology", "Photography")
LCC_SUBCLASSES["TS"] = LccSubclass("TS", "Technology", "Manufactures")
LCC_SUBCLASSES["TT"] = LccSubclass("TT", "Technology", "Handicrafts, Arts and crafts")
LCC_SUBCLASSES["TX"] = LccSubclass("TX", "Technology", "Home economics")

# Class Z - Bibliography, Library Science
LCC_SUBCLASSES["Z"] = LccSubclass("Z", "Bibliography, Library Science", "Books (General), Writing, Paleography, Book industries and trade, Libraries, Information science")
LCC_SUBCLASSES["ZA"] = LccSubclass("ZA", "Bibliography, Library Science", "Information resources (General)")

def lookup_lcc(call_number: str) -> Optional[LccSubclass]:
    """Look up LCC subclass from call number prefix."""
    clean = call_number.strip().upper()
    # Try 3 letters, then 2 letters, then 1 letter
    for length in [3, 2, 1]:
        prefix = clean[:length]
        if prefix in LCC_SUBCLASSES:
            return LCC_SUBCLASSES[prefix]
    return None
