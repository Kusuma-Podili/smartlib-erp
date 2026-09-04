"""Library of Congress MARC Code List for Relators and RDA Relationship Designators.

Defines all standard 3-letter relator codes ($4) and relationship designator terms ($e).
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class MarcRelatorTerm:
    code: str
    term: str
    definition: str
    inverse_term: Optional[str] = None


MARC_RELATORS_FULL: Dict[str, MarcRelatorTerm] = {}

def _rel(code: str, term: str, defn: str, inv: Optional[str] = None):
    MARC_RELATORS_FULL[code] = MarcRelatorTerm(code, term, defn, inv)

_rel("aut", "Author", "Person, family, or organization responsible for creating a work", "Author of")
_rel("art", "Artist", "Person, family, or organization responsible for creating a work of art", "Artist of")
_rel("cmp", "Composer", "Person or organization responsible for creating musical works", "Composer of")
_rel("cnd", "Conductor", "Person who directs a musical performance", "Conductor of")
_rel("ctb", "Contributor", "Person or organization responsible for contributing to a work", "Contributor to")
_rel("edt", "Editor", "Person or organization responsible for preparing a work for publication", "Editor of")
_rel("ill", "Illustrator", "Person or organization responsible for contributing illustrations to a work", "Illustrator of")
_rel("pbl", "Publisher", "Person or organization responsible for publishing, releasing, or issuing a work", "Publisher of")
_rel("trl", "Translator", "Person or organization responsible for translating a work from one language into another", "Translator of")
_rel("ann", "Annotator", "Person who writes formal explanatory notes for a text", "Annotator of")
_rel("arr", "Arranger", "Person or organization who modifies a musical work for different instrumentation", "Arranger of")
_rel("auc", "Auctioneer", "Person or organization responsible for conducting an auction of books", "Auctioneer of")
_rel("bnd", "Binder", "Person or organization responsible for the binding of a book", "Binder of")
_rel("bdd", "Binding designer", "Person or organization responsible for the binding design of a book", "Binding designer of")
_rel("bkd", "Book designer", "Person or organization responsible for the total typography and layout of a book", "Book designer of")
_rel("clg", "Calligrapher", "Person who designs and writes ornamental lettering", "Calligrapher of")
_rel("ctg", "Cartographer", "Person or organization responsible for the creation of maps and cartographic resources", "Cartographer of")
_rel("cur", "Curator", "Person or organization responsible for conceiving, organizing, and supervising an exhibition", "Curator of")
_rel("dnc", "Dancer", "Person who performs movements in dance", "Dancer in")
_rel("dgg", "Degree granting institution", "Organization granting an academic degree for which a thesis was presented", "Degree granted for")
_rel("dis", "Dissertant", "Person presenting a thesis or dissertation in partial fulfillment of a degree", "Dissertant of")
_rel("dnr", "Donor", "Person or organization who donates a book or collection to a library", "Donor of")
_rel("drm", "Draftsman", "Person who creates technical architectural or engineering drawings", "Draftsman of")
_rel("eng", "Engineer", "Person or organization responsible for engineering design or sound recording", "Engineer of")
_rel("fmo", "Former owner", "Person or organization that formerly owned an item in a library collection", "Former owner of")
_rel("hnr", "Honoree", "Person or organization in whose honor a festschrift or book is presented", "Honoree of")
_rel("itr", "Instrumentalist", "Person who plays a musical instrument in a performance", "Instrumentalist in")
_rel("ive", "Interviewee", "Person who is interviewed in a recorded broadcast or transcript", "Interviewee in")
_rel("ivr", "Interviewer", "Person who conducts an interview in a recorded work", "Interviewer of")
_rel("lbt", "Librettist", "Person who writes the text of an opera, oratorio, or musical", "Librettist of")
_rel("lyr", "Lyricist", "Person who writes the lyrics for a musical song or composition", "Lyricist of")
_rel("nrt", "Narrator", "Person who reads spoken text or provides spoken commentary", "Narrator of")
_rel("org", "Originator", "Person or organization performing the work that gave rise to a publication", "Originator of")
_rel("oth", "Other", "Entity whose role is not defined by any specific standard relator code", None)
_rel("pht", "Photographer", "Person or organization responsible for taking photographic images", "Photographer of")
_rel("prt", "Printer", "Person or organization responsible for printing a book or physical item", "Printer of")
_rel("pro", "Producer", "Person or organization responsible for the overall management of a production", "Producer of")
_rel("red", "Redactor", "Person who edits or prepares a text for publication", "Redactor of")
_rel("rev", "Reviewer", "Person who prepares a formal review or critique of a work", "Reviewer of")
_rel("sng", "Singer", "Person who sings musical text or vocal compositions", "Singer in")
_rel("spk", "Speaker", "Person who delivers a speech, lecture, or formal address", "Speaker in")
_rel("spn", "Sponsor", "Person or organization that provides financial or institutional sponsorship", "Sponsor of")
_rel("ths", "Thesis advisor", "Person who supervises an academic graduate dissertation", "Thesis advisor to")
_rel("voc", "Vocalist", "Person performing vocal accompaniment in a musical work", "Vocalist in")
_rel("wdc", "Woodcutter", "Person who cuts relief images into a wood block for printing", "Woodcutter of")
_rel("wde", "Wood engraver", "Person who engraves relief images into end-grain wood for printing", "Wood engraver of")
_rel("abr", "Abridger", "Person who shortens or condenses a work without loss of sense", None)
_rel("acp", "Art copyist", "Person who creates a copy of a work of art", None)
_rel("act", "Actor", "Person who acts in a theatrical, film, or broadcast production", None)
_rel("adi", "Art director", "Person responsible for visual art design in film or theatre", None)
_rel("anm", "Animator", "Person who creates animations or moving cartoon sequences", None)
_rel("app", "Applicant", "Person or organization that files an application for copyright or patent", None)
_rel("arc", "Architect", "Person or organization that designs buildings and physical structures", None)
_rel("aud", "Author of dialog", "Person who writes spoken dialog for a play or film", None)
_rel("aui", "Author of introduction", "Person who writes an introductory essay for a work", None)
_rel("aus", "Screenwriter", "Person who authors the screenplay for a film or television work", None)
_rel("blw", "Blurb writer", "Person who writes promotional review blurbs for book jackets", None)
_rel("brd", "Broadcaster", "Organization responsible for broadcast transmission", None)
_rel("cas", "Caster", "Person or foundry responsible for type casting or sculpture casting", None)
_rel("cns", "Censor", "Official who reviews and authorizes publication under censorship laws", None)
_rel("coe", "Contestant-appellee", "Party against whom an appellate contest is brought", None)
_rel("col", "Collector", "Person or organization that curated and assembled a collection", None)
_rel("com", "Compiler", "Person or organization that gathers diverse writings into a composite work", None)
_rel("cos", "Costume designer", "Person who designs costumes for dramatic productions", None)
_rel("cpc", "Copyright claimant", "Person or organization that legally claims copyright ownership", None)
_rel("cpe", "Complainant-appellee", "Party in whose favor a lower court decree was rendered", None)
_rel("cpr", "Copyright representative", "Legal agent authorized to manage copyright licensings", None)
_rel("cst", "Costume supervisor", "Person responsible for executing wardrobe and costume fabrication", None)
_rel("cov", "Cover designer", "Graphic designer responsible for book cover typography and jacket artwork", None)

def lookup_relator(code_or_term: str) -> Optional[MarcRelatorTerm]:
    clean = code_or_term.strip().lower()
    for rel in MARC_RELATORS_FULL.values():
        if rel.code.lower() == clean or rel.term.lower() == clean:
            return rel
    return None
