"""Library of Congress Classification (LCC) Complete Subclasses and Schedules.

Defines all official primary classes (A-Z) and standard subclasses across all 21 schedules,
with cutter ranges, scope descriptions, and subject indexing.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class LccSubclassDefinition:
    class_letter: str
    subclass_code: str
    title: str
    schedule_name: str
    call_number_range: str
    scope_notes: str
    primary_disciplines: List[str] = field(default_factory=list)


LCC_SUBCLASS_REGISTRY: Dict[str, LccSubclassDefinition] = {}


def _lcc(cls: str, sub: str, title: str, sched: str, rng: str, notes: str, disc: List[str]):
    LCC_SUBCLASS_REGISTRY[sub] = LccSubclassDefinition(
        class_letter=cls,
        subclass_code=sub,
        title=title,
        schedule_name=sched,
        call_number_range=rng,
        scope_notes=notes,
        primary_disciplines=disc
    )

_lcc(
    cls="A",
    sub="AC",
    title="Collections. Series. Collected works",
    sched="Class A - General Works",
    rng="AC1-999",
    notes="General collected works, monographs, series, and multi-subject miscellany",
    disc=['General', 'Polygraphy']
)
_lcc(
    cls="A",
    sub="AE",
    title="Encyclopedias",
    sched="Class A - General Works",
    rng="AE1-90",
    notes="General encyclopedias across languages and international traditions",
    disc=['Reference', 'Encyclopedias']
)
_lcc(
    cls="A",
    sub="AG",
    title="Dictionaries and other general reference books",
    sched="Class A - General Works",
    rng="AG1-600",
    notes="General fact handbooks, queries, and question-and-answer compendiums",
    disc=['Reference']
)
_lcc(
    cls="A",
    sub="AI",
    title="Indexes",
    sched="Class A - General Works",
    rng="AI1-21",
    notes="General periodical indexes, newspaper abstracts, and bibliography indexes",
    disc=['Indexes', 'Bibliographies']
)
_lcc(
    cls="A",
    sub="AM",
    title="Museums. Collectors and collecting",
    sched="Class A - General Works",
    rng="AM1-501",
    notes="Museology, museum governance, display techniques, and personal collecting",
    disc=['Museology']
)
_lcc(
    cls="A",
    sub="AN",
    title="Newspapers",
    sched="Class A - General Works",
    rng="AN",
    notes="General newspapers and broadsides arranged geographically",
    disc=['Journalism', 'Newspapers']
)
_lcc(
    cls="A",
    sub="AP",
    title="Periodicals",
    sched="Class A - General Works",
    rng="AP1-271",
    notes="General non-specialized periodicals, cultural revues, and illustrated magazines",
    disc=['Periodicals']
)
_lcc(
    cls="A",
    sub="AS",
    title="Academies and learned societies",
    sched="Class A - General Works",
    rng="AS1-945",
    notes="Proceedings, yearbooks, and governance of international learned academies",
    disc=['Learned Societies']
)
_lcc(
    cls="A",
    sub="AY",
    title="Yearbooks. Almanacs. Directories",
    sched="Class A - General Works",
    rng="AY1-2001",
    notes="General annuals, almanacs, directories, and statistical yearbooks",
    disc=['Almanacs', 'Yearbooks']
)
_lcc(
    cls="A",
    sub="AZ",
    title="History of scholarship and learning",
    sched="Class A - General Works",
    rng="AZ1-999",
    notes="History of humanistic disciplines, universities, and academic scholarship",
    disc=['Higher Education', 'Intellectual History']
)
_lcc(
    cls="B",
    sub="B",
    title="Philosophy (General)",
    sched="Class B - Philosophy, Psychology, Religion",
    rng="B1-5802",
    notes="General history of philosophical systems, schools, and canonical philosophers",
    disc=['Philosophy']
)
_lcc(
    cls="B",
    sub="BC",
    title="Logic",
    sched="Class B - Philosophy, Psychology, Religion",
    rng="BC1-199",
    notes="Formal logic, deductive reasoning, syllogisms, and symbolic logic",
    disc=['Logic', 'Philosophy']
)
_lcc(
    cls="B",
    sub="BD",
    title="Speculative philosophy",
    sched="Class B - Philosophy, Psychology, Religion",
    rng="BD10-701",
    notes="Metaphysics, epistemology, ontology, and philosophy of mind",
    disc=['Metaphysics', 'Epistemology']
)
_lcc(
    cls="B",
    sub="BF",
    title="Psychology",
    sched="Class B - Philosophy, Psychology, Religion",
    rng="BF1-990",
    notes="Developmental psychology, cognitive processes, sensation, and perception",
    disc=['Psychology', 'Cognitive Science']
)
_lcc(
    cls="B",
    sub="BH",
    title="Aesthetics",
    sched="Class B - Philosophy, Psychology, Religion",
    rng="BH1-301",
    notes="Philosophical aesthetics, theory of beauty, and artistic criticism",
    disc=['Aesthetics', 'Art Theory']
)
_lcc(
    cls="B",
    sub="BJ",
    title="Ethics",
    sched="Class B - Philosophy, Psychology, Religion",
    rng="BJ1-1725",
    notes="Moral philosophy, normative ethics, professional codes, and moral behavior",
    disc=['Ethics', 'Moral Philosophy']
)
_lcc(
    cls="B",
    sub="BL",
    title="Religions. Mythology. Rationalism",
    sched="Class B - Philosophy, Psychology, Religion",
    rng="BL1-2790",
    notes="Comparative religion, mythological traditions, and religious phenomena",
    disc=['Comparative Religion', 'Mythology']
)
_lcc(
    cls="B",
    sub="BM",
    title="Judaism",
    sched="Class B - Philosophy, Psychology, Religion",
    rng="BM1-990",
    notes="Rabbinic literature, Talmud, Jewish law, liturgy, and history",
    disc=['Judaism', 'Theology']
)
_lcc(
    cls="B",
    sub="BP",
    title="Islam. Bahaism. Theosophy",
    sched="Class B - Philosophy, Psychology, Religion",
    rng="BP1-610",
    notes="Quranic studies, hadith, Islamic jurisprudence, Sufism, and Baha'i faith",
    disc=['Islamic Studies', 'Theology']
)
_lcc(
    cls="B",
    sub="BQ",
    title="Buddhism",
    sched="Class B - Philosophy, Psychology, Religion",
    rng="BQ1-9800",
    notes="Theravada, Mahayana, Tibetan Vajrayana, Zen traditions and scriptures",
    disc=['Buddhist Studies']
)
_lcc(
    cls="B",
    sub="BR",
    title="Christianity",
    sched="Class B - Philosophy, Psychology, Religion",
    rng="BR1-1725",
    notes="Early Church fathers, patristics, ecclesiastical history, and denominations",
    disc=['Christian History', 'Patristics']
)
_lcc(
    cls="B",
    sub="BS",
    title="The Bible",
    sched="Class B - Philosophy, Psychology, Religion",
    rng="BS1-2970",
    notes="Old and New Testament texts, exegesis, hermeneutics, and biblical archaeology",
    disc=['Biblical Studies']
)
_lcc(
    cls="B",
    sub="BT",
    title="Doctrinal Theology",
    sched="Class B - Philosophy, Psychology, Religion",
    rng="BT10-1480",
    notes="Christology, soteriology, ecclesiology, and dogmatics",
    disc=['Systematic Theology']
)
_lcc(
    cls="B",
    sub="BV",
    title="Practical Theology",
    sched="Class B - Philosophy, Psychology, Religion",
    rng="BV1-5100",
    notes="Liturgy, homiletics, pastoral care, hymnology, and missions",
    disc=['Pastoral Ministry']
)
_lcc(
    cls="B",
    sub="BX",
    title="Christian Denominations",
    sched="Class B - Philosophy, Psychology, Religion",
    rng="BX1-9999",
    notes="Catholicism, Eastern Orthodoxy, Protestantism, and Anglicanism",
    disc=['Denominational Studies']
)
_lcc(
    cls="C",
    sub="CB",
    title="History of Civilization",
    sched="Class C - Auxiliary Sciences",
    rng="CB3-482",
    notes="Comparative cultural history and evolutionary development of human civilizations",
    disc=['Cultural History']
)
_lcc(
    cls="C",
    sub="CC",
    title="Archaeology",
    sched="Class C - Auxiliary Sciences",
    rng="CC1-960",
    notes="Archaeological methodology, excavation techniques, artifact preservation",
    disc=['Archaeology']
)
_lcc(
    cls="C",
    sub="CD",
    title="Diplomatics. Archives. Seals",
    sched="Class C - Auxiliary Sciences",
    rng="CD1-6471",
    notes="Archival administration, manuscript preservation, diplomatics, and sigillography",
    disc=['Archival Science']
)
_lcc(
    cls="C",
    sub="CE",
    title="Technical Chronology. Calendar",
    sched="Class C - Auxiliary Sciences",
    rng="CE1-97",
    notes="Systems of reckoning time, historical calendars, and astronomical eras",
    disc=['Chronology']
)
_lcc(
    cls="C",
    sub="CJ",
    title="Numismatics",
    sched="Class C - Auxiliary Sciences",
    rng="CJ1-6661",
    notes="Coinage, tokens, medals, paper currency, and monetary history",
    disc=['Numismatics']
)
_lcc(
    cls="C",
    sub="CN",
    title="Epigraphy. Inscriptions",
    sched="Class C - Auxiliary Sciences",
    rng="CN1-1355",
    notes="Inscriptions in stone, bronze, and classical epigraphic monuments",
    disc=['Epigraphy']
)
_lcc(
    cls="C",
    sub="CR",
    title="Heraldry",
    sched="Class C - Auxiliary Sciences",
    rng="CR1-6305",
    notes="Coats of arms, blazonry, heraldic law, and chivalric orders",
    disc=['Heraldry']
)
_lcc(
    cls="C",
    sub="CS",
    title="Genealogy",
    sched="Class C - Auxiliary Sciences",
    rng="CS1-3090",
    notes="Family histories, genealogical research, parish registers, and heraldic descent",
    disc=['Genealogy']
)
_lcc(
    cls="C",
    sub="CT",
    title="Biography",
    sched="Class C - Auxiliary Sciences",
    rng="CT21-9999",
    notes="Collective biography, biographical dictionaries, and biographical theory",
    disc=['Biography']
)
_lcc(
    cls="D",
    sub="D",
    title="History (General)",
    sched="Class D - World History",
    rng="D1-2027",
    notes="World historical overviews, major wars, historiography, and global eras",
    disc=['World History']
)
_lcc(
    cls="D",
    sub="DA",
    title="Great Britain",
    sched="Class D - World History",
    rng="DA1-995",
    notes="English, Scottish, Welsh, and Irish national history",
    disc=['British History']
)
_lcc(
    cls="D",
    sub="DAW",
    title="Central Europe",
    sched="Class D - World History",
    rng="DAW1001-1051",
    notes="Danubian basin, Habsburg Empire, and Central European historical development",
    disc=['European History']
)
_lcc(
    cls="D",
    sub="DB",
    title="Austria. Liechtenstein. Hungary. Czechia. Slovakia",
    sched="Class D - World History",
    rng="DB1-3150",
    notes="Austro-Hungarian and West Slavic regional history",
    disc=['European History']
)
_lcc(
    cls="D",
    sub="DC",
    title="France. Andorra. Monaco",
    sched="Class D - World History",
    rng="DC1-947",
    notes="French royal dynasties, French Revolution, Napoleon, and modern republics",
    disc=['French History']
)
_lcc(
    cls="D",
    sub="DD",
    title="Germany",
    sched="Class D - World History",
    rng="DD1-905",
    notes="Holy Roman Empire, Prussian kingdom, Weimar, and post-unification Germany",
    disc=['German History']
)
_lcc(
    cls="D",
    sub="DE",
    title="Greco-Roman World",
    sched="Class D - World History",
    rng="DE1-100",
    notes="Classical Mediterranean antiquity, Hellenistic world, and Roman civilization",
    disc=['Classical Studies']
)
_lcc(
    cls="D",
    sub="DF",
    title="Greece",
    sched="Class D - World History",
    rng="DF10-951",
    notes="Ancient Greek city-states, Byzantine Empire, and modern Greek history",
    disc=['Greek History']
)
_lcc(
    cls="D",
    sub="DG",
    title="Italy. Malta",
    sched="Class D - World History",
    rng="DG11-999",
    notes="Roman Republic and Empire, Italian Renaissance, Risorgimento, and modern Italy",
    disc=['Italian History']
)
_lcc(
    cls="D",
    sub="DH",
    title="Low Countries. Benelux",
    sched="Class D - World History",
    rng="DH1-925",
    notes="Flanders, Belgium, Netherlands, and Luxembourg historical development",
    disc=['Benelux History']
)
_lcc(
    cls="D",
    sub="DK",
    title="Russia. Soviet Union. Former Soviet Republics",
    sched="Class D - World History",
    rng="DK1-9495",
    notes="Russian Empire, Tsarist dynasties, USSR, and contemporary post-Soviet states",
    disc=['Russian History']
)
_lcc(
    cls="D",
    sub="DP",
    title="Spain. Portugal",
    sched="Class D - World History",
    rng="DP1-802",
    notes="Iberian Peninsula, Reconquista, Spanish Empire, and Lusophone history",
    disc=['Iberian History']
)
_lcc(
    cls="D",
    sub="DS",
    title="Asia",
    sched="Class D - World History",
    rng="DS1-937",
    notes="Middle East, South Asia, East Asia, and Southeast Asian historical developments",
    disc=['Asian History']
)
_lcc(
    cls="D",
    sub="DT",
    title="Africa",
    sched="Class D - World History",
    rng="DT1-3415",
    notes="North African antiquity, Saharan kingdoms, colonial period, and post-colonial nations",
    disc=['African History']
)
_lcc(
    cls="D",
    sub="DU",
    title="Oceania",
    sched="Class D - World History",
    rng="DU1-950",
    notes="Australia, New Zealand, Melanesia, Micronesia, and Polynesian histories",
    disc=['Pacific History']
)
_lcc(
    cls="E",
    sub="E",
    title="History of America (General and United States)",
    sched="Class E-F - The Americas",
    rng="E11-909",
    notes="North American indigenous peoples, colonial America, and US national history",
    disc=['American History']
)
_lcc(
    cls="F",
    sub="F",
    title="United States Local History and Latin America",
    sched="Class E-F - The Americas",
    rng="F1-3799",
    notes="US state and municipal histories, Canada, Mexico, Central and South America",
    disc=['Latin American Studies']
)
_lcc(
    cls="G",
    sub="G",
    title="Geography (General). Atlases. Maps",
    sched="Class G - Geography",
    rng="G1-922",
    notes="General geography, cartography, globes, and historical atlases",
    disc=['Geography', 'Cartography']
)
_lcc(
    cls="G",
    sub="GA",
    title="Mathematical geography. Cartography",
    sched="Class G - Geography",
    rng="GA1-1776",
    notes="Surveying, projection systems, GIS foundations, and map production",
    disc=['GIS', 'Geomatics']
)
_lcc(
    cls="G",
    sub="GB",
    title="Physical geography",
    sched="Class G - Geography",
    rng="GB400-5030",
    notes="Geomorphology, hydrologic regimes, glaciers, and terrain landforms",
    disc=['Geomorphology']
)
_lcc(
    cls="G",
    sub="GC",
    title="Oceanography",
    sched="Class G - Geography",
    rng="GC1-1581",
    notes="Marine physics, ocean currents, bathymetry, and benthic environments",
    disc=['Oceanography']
)
_lcc(
    cls="G",
    sub="GE",
    title="Environmental Sciences",
    sched="Class G - Geography",
    rng="GE1-350",
    notes="Environmental systems, ecosystem health, human environmental impact",
    disc=['Environmental Science']
)
_lcc(
    cls="G",
    sub="GF",
    title="Human ecology. Anthropogeography",
    sched="Class G - Geography",
    rng="GF1-900",
    notes="Settlement geography, spatial human organization, and regional cultures",
    disc=['Human Geography']
)
_lcc(
    cls="G",
    sub="GN",
    title="Anthropology",
    sched="Class G - Geography",
    rng="GN1-890",
    notes="Physical anthropology, ethnology, ethnography, and cultural anthropological theory",
    disc=['Anthropology']
)
_lcc(
    cls="G",
    sub="GR",
    title="Folklore",
    sched="Class G - Geography",
    rng="GR1-950",
    notes="Folk tales, mythical legends, oral traditions, and traditional customs",
    disc=['Folklore']
)
_lcc(
    cls="G",
    sub="GT",
    title="Manners and customs (General)",
    sched="Class G - Geography",
    rng="GT1-7070",
    notes="Costume, dress, dining customs, funerals, and daily domestic life",
    disc=['Cultural Studies']
)
_lcc(
    cls="G",
    sub="GV",
    title="Recreation. Leisure. Sports",
    sched="Class G - Geography",
    rng="GV1-1860",
    notes="Games, physical education, athletic competitions, and leisure activities",
    disc=['Sports Science']
)
_lcc(
    cls="H",
    sub="H",
    title="Social sciences (General)",
    sched="Class H - Social Sciences",
    rng="H1-99",
    notes="Comprehensive social science methodologies, institutes, and publications",
    disc=['Social Sciences']
)
_lcc(
    cls="H",
    sub="HA",
    title="Statistics",
    sched="Class H - Social Sciences",
    rng="HA1-4737",
    notes="Statistical theory, census compilations, and demographic yearbooks",
    disc=['Applied Statistics']
)
_lcc(
    cls="H",
    sub="HB",
    title="Economic theory. Demography",
    sched="Class H - Social Sciences",
    rng="HB1-3840",
    notes="Value and price theory, business cycles, demography, and macro-theories",
    disc=['Economics', 'Demography']
)
_lcc(
    cls="H",
    sub="HC",
    title="Economic history and conditions",
    sched="Class H - Social Sciences",
    rng="HC10-1085",
    notes="National and regional economic development, five-year plans, and GDP studies",
    disc=['Economic History']
)
_lcc(
    cls="H",
    sub="HD",
    title="Industries. Land use. Labor",
    sched="Class H - Social Sciences",
    rng="HD28-9999",
    notes="Industrial management, agriculture economics, labor unions, and corporations",
    disc=['Management', 'Labor']
)
_lcc(
    cls="H",
    sub="HE",
    title="Transportation and communications",
    sched="Class H - Social Sciences",
    rng="HE1-9900",
    notes="Railroads, shipping lines, aviation, postal systems, and telecommunications",
    disc=['Transportation']
)
_lcc(
    cls="H",
    sub="HF",
    title="Commerce",
    sched="Class H - Social Sciences",
    rng="HF1-6182",
    notes="International trade, marketing, accounting standards, and business logistics",
    disc=['Commerce', 'Marketing']
)
_lcc(
    cls="H",
    sub="HG",
    title="Finance",
    sched="Class H - Social Sciences",
    rng="HG1-9999",
    notes="Banking systems, investment securities, monetary policy, and insurance",
    disc=['Finance', 'Banking']
)
_lcc(
    cls="H",
    sub="HJ",
    title="Public finance",
    sched="Class H - Social Sciences",
    rng="HJ9-9940",
    notes="Government taxation, revenue, public debt, national budgeting, and audits",
    disc=['Public Finance']
)
_lcc(
    cls="H",
    sub="HM",
    title="Sociology (General)",
    sched="Class H - Social Sciences",
    rng="HM1-1281",
    notes="Sociological paradigms, social change, deviance, and collective action",
    disc=['Sociology']
)
_lcc(
    cls="H",
    sub="HN",
    title="Social history and conditions. Social problems",
    sched="Class H - Social Sciences",
    rng="HN1-995",
    notes="Social movements, public reform initiatives, and community welfare",
    disc=['Social Policy']
)
_lcc(
    cls="H",
    sub="HQ",
    title="The family. Marriage. Women",
    sched="Class H - Social Sciences",
    rng="HQ1-2044",
    notes="Family sociology, gender studies, marriage customs, and sexuality",
    disc=['Gender Studies', 'Family Sociology']
)
_lcc(
    cls="H",
    sub="HS",
    title="Societies: secret, benevolent, etc.",
    sched="Class H - Social Sciences",
    rng="HS1-3371",
    notes="Fraternal orders, service clubs, lodges, and mutual benefit societies",
    disc=['Sociology']
)
_lcc(
    cls="H",
    sub="HT",
    title="Communities. Classes. Races",
    sched="Class H - Social Sciences",
    rng="HT51-1595",
    notes="Urban sociology, rural communities, social classes, and race relations",
    disc=['Urban Sociology']
)
_lcc(
    cls="H",
    sub="HV",
    title="Social pathology. Social and public welfare. Criminology",
    sched="Class H - Social Sciences",
    rng="HV1-9960",
    notes="Charity work, social work, criminology, penology, and police administration",
    disc=['Criminology', 'Social Work']
)
_lcc(
    cls="H",
    sub="HX",
    title="Socialism. Communism. Anarchism",
    sched="Class H - Social Sciences",
    rng="HX1-970",
    notes="Socialist theory, communist political movements, and utopianism",
    disc=['Political Philosophy']
)
_lcc(
    cls="Q",
    sub="Q",
    title="Science (General)",
    sched="Class Q - Science",
    rng="Q1-390",
    notes="General scientific societies, scientific instruments, and philosophy of science",
    disc=['General Science']
)
_lcc(
    cls="Q",
    sub="QA",
    title="Mathematics. Computer Science",
    sched="Class Q - Science",
    rng="QA1-939",
    notes="Calculus, algebra, algorithms, numerical analysis, and machine learning",
    disc=['Mathematics', 'Computer Science']
)
_lcc(
    cls="Q",
    sub="QB",
    title="Astronomy",
    sched="Class Q - Science",
    rng="QB1-991",
    notes="Celestial mechanics, astrophysics, planetary science, and cosmology",
    disc=['Astronomy', 'Astrophysics']
)
_lcc(
    cls="Q",
    sub="QC",
    title="Physics",
    sched="Class Q - Science",
    rng="QC1-999",
    notes="Classical mechanics, electromagnetism, optics, acoustics, and quantum physics",
    disc=['Physics']
)
_lcc(
    cls="Q",
    sub="QD",
    title="Chemistry",
    sched="Class Q - Science",
    rng="QD1-999",
    notes="Analytical, organic, inorganic, and physical chemistry, and crystallography",
    disc=['Chemistry']
)
_lcc(
    cls="Q",
    sub="QE",
    title="Geology",
    sched="Class Q - Science",
    rng="QE1-996",
    notes="Stratigraphy, paleontology, petrology, mineralogy, and volcanology",
    disc=['Geology', 'Earth Sciences']
)
_lcc(
    cls="Q",
    sub="QH",
    title="Natural history. Biology",
    sched="Class Q - Science",
    rng="QH1-705",
    notes="General biology, ecology, genetics, microscopy, and evolution",
    disc=['Biology', 'Ecology']
)
_lcc(
    cls="Q",
    sub="QK",
    title="Botany",
    sched="Class Q - Science",
    rng="QK1-989",
    notes="Plant morphology, physiology, taxonomy, bryology, and pteridology",
    disc=['Botany']
)
_lcc(
    cls="Q",
    sub="QL",
    title="Zoology",
    sched="Class Q - Science",
    rng="QL1-991",
    notes="Invertebrate and vertebrate zoology, entomology, ornithology, mammalogy",
    disc=['Zoology']
)
_lcc(
    cls="Q",
    sub="QM",
    title="Human anatomy",
    sched="Class Q - Science",
    rng="QM1-695",
    notes="Gross human anatomy, histology, and human embryology",
    disc=['Human Anatomy']
)
_lcc(
    cls="Q",
    sub="QP",
    title="Physiology",
    sched="Class Q - Science",
    rng="QP1-981",
    notes="Cardiovascular, neurophysiology, endocrine, biochemical mechanisms",
    disc=['Physiology']
)
_lcc(
    cls="Q",
    sub="QR",
    title="Microbiology",
    sched="Class Q - Science",
    rng="QR1-502",
    notes="Bacteriology, virology, immunology, and microbial genetics",
    disc=['Microbiology']
)
_lcc(
    cls="R",
    sub="RA",
    title="Public aspects of medicine",
    sched="Class R - Medicine",
    rng="RA1-1270",
    notes="Public health, epidemiology, toxicology, hygiene, and hospital administration",
    disc=["Class R - Medicine"]
)
_lcc(
    cls="R",
    sub="RB",
    title="Pathology",
    sched="Class R - Medicine",
    rng="RB1-214",
    notes="Cellular pathology, histopathology, diagnostic clinical laboratories",
    disc=["Class R - Medicine"]
)
_lcc(
    cls="R",
    sub="RC",
    title="Internal medicine",
    sched="Class R - Medicine",
    rng="RC31-1245",
    notes="Cardiology, oncology, gastroenterology, infectious diseases, and psychiatry",
    disc=["Class R - Medicine"]
)
_lcc(
    cls="R",
    sub="RD",
    title="Surgery",
    sched="Class R - Medicine",
    rng="RD1-811",
    notes="General surgical operative techniques, orthopedic, and plastic surgery",
    disc=["Class R - Medicine"]
)
_lcc(
    cls="R",
    sub="RE",
    title="Ophthalmology",
    sched="Class R - Medicine",
    rng="RE1-992",
    notes="Diseases and refractive surgery of the eye and visual pathways",
    disc=["Class R - Medicine"]
)
_lcc(
    cls="R",
    sub="RF",
    title="Otorhinolaryngology",
    sched="Class R - Medicine",
    rng="RF1-547",
    notes="Ear, nose, throat, and head and neck surgical pathology",
    disc=["Class R - Medicine"]
)
_lcc(
    cls="R",
    sub="RG",
    title="Gynecology and Obstetrics",
    sched="Class R - Medicine",
    rng="RG1-991",
    notes="Maternal-fetal medicine, obstetrical care, and reproductive health",
    disc=["Class R - Medicine"]
)
_lcc(
    cls="R",
    sub="RJ",
    title="Pediatrics",
    sched="Class R - Medicine",
    rng="RJ1-570",
    notes="Pediatric medicine, neonatology, and adolescent health care",
    disc=["Class R - Medicine"]
)
_lcc(
    cls="R",
    sub="RK",
    title="Dentistry",
    sched="Class R - Medicine",
    rng="RK1-715",
    notes="Oral pathology, periodontics, orthodontics, and endodontics",
    disc=["Class R - Medicine"]
)
_lcc(
    cls="R",
    sub="RL",
    title="Dermatology",
    sched="Class R - Medicine",
    rng="RL1-801",
    notes="Integumentary medicine, cutaneous biology, and dermatopathology",
    disc=["Class R - Medicine"]
)
_lcc(
    cls="R",
    sub="RM",
    title="Therapeutics. Pharmacology",
    sched="Class R - Medicine",
    rng="RM1-950",
    notes="Pharmacotherapy, physical therapy, radiotherapy, and dietary regimens",
    disc=["Class R - Medicine"]
)
_lcc(
    cls="R",
    sub="RS",
    title="Pharmacy and materia medica",
    sched="Class R - Medicine",
    rng="RS1-441",
    notes="Formulation, pharmacognosy, and pharmaceutical dispensing regulations",
    disc=["Class R - Medicine"]
)
_lcc(
    cls="R",
    sub="RT",
    title="Nursing",
    sched="Class R - Medicine",
    rng="RT1-120",
    notes="Clinical nursing practice, geriatric nursing, and patient advocacy",
    disc=["Class R - Medicine"]
)
_lcc(
    cls="S",
    sub="S",
    title="Agriculture (General)",
    sched="Class S - Agriculture",
    rng="S1-972",
    notes="Agricultural extension, farm management, and soil conservation",
    disc=["Class S - Agriculture"]
)
_lcc(
    cls="S",
    sub="SB",
    title="Plant culture",
    sched="Class S - Agriculture",
    rng="SB1-1110",
    notes="Horticulture, agronomy, field crops, and arboriculture",
    disc=["Class S - Agriculture"]
)
_lcc(
    cls="S",
    sub="SD",
    title="Forestry",
    sched="Class S - Agriculture",
    rng="SD1-669",
    notes="Silviculture, timber management, wildland fires, and forest conservation",
    disc=["Class S - Agriculture"]
)
_lcc(
    cls="S",
    sub="SF",
    title="Animal culture",
    sched="Class S - Agriculture",
    rng="SF1-1100",
    notes="Veterinary medicine, livestock husbandry, breeding, and dairy farming",
    disc=["Class S - Agriculture"]
)
_lcc(
    cls="S",
    sub="SH",
    title="Aquaculture. Fisheries. Angling",
    sched="Class S - Agriculture",
    rng="SH1-691",
    notes="Commercial fishing, mariculture, fish hatcheries, and ocean fisheries",
    disc=["Class S - Agriculture"]
)
_lcc(
    cls="S",
    sub="SK",
    title="Hunting sports",
    sched="Class S - Agriculture",
    rng="SK1-665",
    notes="Wildlife management, game preserves, and trapping regulations",
    disc=["Class S - Agriculture"]
)
_lcc(
    cls="T",
    sub="T",
    title="Technology (General)",
    sched="Class T - Technology",
    rng="T1-995",
    notes="Industrial research, inventions, patents, and engineering drawing",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TA",
    title="Engineering (General). Civil engineering",
    sched="Class T - Technology",
    rng="TA1-2040",
    notes="Structural mechanics, materials testing, surveying, and foundational engineering",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TC",
    title="Hydraulic engineering",
    sched="Class T - Technology",
    rng="TC1-978",
    notes="Dams, canals, harbor works, irrigation, and river engineering",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TD",
    title="Environmental technology. Sanitary engineering",
    sched="Class T - Technology",
    rng="TD1-1066",
    notes="Water treatment, sewage disposal, municipal refuse, and air pollution control",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TE",
    title="Highway engineering. Roads and pavements",
    sched="Class T - Technology",
    rng="TE1-450",
    notes="Pavement design, asphalt engineering, highway geometries, and traffic control",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TF",
    title="Railroad engineering and operation",
    sched="Class T - Technology",
    rng="TF1-1620",
    notes="Locomotives, rolling stock, rail signaling, and high-speed rail networks",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TG",
    title="Bridge engineering",
    sched="Class T - Technology",
    rng="TG1-470",
    notes="Suspension, arch, truss, and cable-stayed bridge structural design",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TH",
    title="Building construction",
    sched="Class T - Technology",
    rng="TH1-9745",
    notes="Architectural engineering, HVAC systems, fire prevention, and masonry",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TJ",
    title="Mechanical engineering and machinery",
    sched="Class T - Technology",
    rng="TJ1-1570",
    notes="Turbines, robotics, machine tools, heat engines, and mechanical systems",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TK",
    title="Electrical engineering. Electronics. Nuclear engineering",
    sched="Class T - Technology",
    rng="TK1-9971",
    notes="Semiconductor circuits, power grids, telecommunications, and photonics",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TL",
    title="Motor vehicles. Aeronautics. Astronautics",
    sched="Class T - Technology",
    rng="TL1-4050",
    notes="Automotive engineering, aerospace propulsion, avionics, and space flight",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TN",
    title="Mining engineering. Metallurgy",
    sched="Class T - Technology",
    rng="TN1-997",
    notes="Mineral extraction, assaying, petroleum drilling, and metallurgy",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TP",
    title="Chemical technology",
    sched="Class T - Technology",
    rng="TP1-1185",
    notes="Industrial chemical manufacturing, fermentation, polymers, and fuels",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TR",
    title="Photography",
    sched="Class T - Technology",
    rng="TR1-1050",
    notes="Optics, cinematography, digital imaging sensors, and darkroom processes",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TS",
    title="Manufactures",
    sched="Class T - Technology",
    rng="TS1-2301",
    notes="Factory production systems, metalworking, textiles, and quality control",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TT",
    title="Handicrafts. Arts and crafts",
    sched="Class T - Technology",
    rng="TT1-999",
    notes="Woodworking, cabinetmaking, upholstery, and decorative crafts",
    disc=["Class T - Technology"]
)
_lcc(
    cls="T",
    sub="TX",
    title="Home economics",
    sched="Class T - Technology",
    rng="TX1-1110",
    notes="Culinary arts, institutional catering, hotel management, and consumer education",
    disc=["Class T - Technology"]
)
_lcc(
    cls="U",
    sub="U",
    title="Military science (General)",
    sched="Class U - Military Science",
    rng="U1-900",
    notes="Military strategy, command and control, operational doctrine, and tactics",
    disc=["Class U - Military Science"]
)
_lcc(
    cls="U",
    sub="UA",
    title="Armies: Organization, description, facilities",
    sched="Class U - Military Science",
    rng="UA10-997",
    notes="National armed forces, military bases, garrison strengths, and defense budgets",
    disc=["Class U - Military Science"]
)
_lcc(
    cls="U",
    sub="UB",
    title="Military administration",
    sched="Class U - Military Science",
    rng="UB1-900",
    notes="Personnel recruitment, military intelligence, and martial justice",
    disc=["Class U - Military Science"]
)
_lcc(
    cls="V",
    sub="V",
    title="Naval science (General)",
    sched="Class V - Naval Science",
    rng="V1-995",
    notes="Naval warfare theory, fleet operations, and maritime strategies",
    disc=["Class V - Naval Science"]
)
_lcc(
    cls="V",
    sub="VA",
    title="Navies: Organization, description, facilities",
    sched="Class V - Naval Science",
    rng="VA10-750",
    notes="Naval fleets, shipyard dock facilities, and naval bases",
    disc=["Class V - Naval Science"]
)
_lcc(
    cls="V",
    sub="VM",
    title="Naval architecture. Shipbuilding. Marine engineering",
    sched="Class V - Naval Science",
    rng="VM1-989",
    notes="Hull hydrodynamics, naval propulsion, vessel stability, and marine engines",
    disc=["Class V - Naval Science"]
)
_lcc(
    cls="Z",
    sub="Z",
    title="Books (General). Writing. Paleography. Libraries",
    sched="Class Z - Library Science",
    rng="Z4-8720",
    notes="Library management, typography, rare books, cataloging, and national bibliographies",
    disc=["Class Z - Library Science"]
)
_lcc(
    cls="Z",
    sub="ZA",
    title="Information resources (General)",
    sched="Class Z - Library Science",
    rng="ZA3038-5190",
    notes="Information literacy, electronic databases, and digital information management",
    disc=["Class Z - Library Science"]
)

def lookup_lcc_subclass(subclass_code: str) -> Optional[LccSubclassDefinition]:
    """Look up Library of Congress subclass definition by its 1-3 letter code."""
    return LCC_SUBCLASS_REGISTRY.get(subclass_code.strip().upper())


def get_subclasses_by_main_class(class_letter: str) -> List[LccSubclassDefinition]:
    """Retrieve all subclasses falling under a primary LCC single letter class."""
    clean = class_letter.strip().upper()
    return [s for s in LCC_SUBCLASS_REGISTRY.values() if s.class_letter == clean]
