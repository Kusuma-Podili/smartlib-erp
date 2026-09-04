"""Standard Common Query Language (CQL) Context Sets and Index Aliases.

Defines Dublin Core (dc), Bath Profile (bath), Bib-1 (bib), and Record (rec) index sets.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CqlIndexDefinition:
    context_set: str
    index_name: str
    description: str
    supported_relations: List[str]
    sql_target_column: str


CQL_INDEX_REGISTRY: Dict[str, CqlIndexDefinition] = {}

def _cql_idx(ctx: str, idx: str, desc: str, rels: List[str], col: str):
    key = f"{ctx}.{idx}".lower()
    CQL_INDEX_REGISTRY[key] = CqlIndexDefinition(ctx, idx, desc, rels, col)

_cql_idx("dc", "title", "Title proper of work", ['=', 'exact', 'all', 'any'], "books.title")
_cql_idx("dc", "creator", "Primary author or creator", ['=', 'exact', 'all', 'any'], "authors.name")
_cql_idx("dc", "subject", "Topical subject heading", ['=', 'exact', 'all', 'any'], "categories.name")
_cql_idx("dc", "description", "Abstract or descriptive summary", ['=', 'all', 'any'], "books.summary")
_cql_idx("dc", "publisher", "Publishing agency or firm", ['=', 'exact', 'all', 'any'], "publishers.name")
_cql_idx("dc", "contributor", "Secondary contributor", ['=', 'all', 'any'], "authors.name")
_cql_idx("dc", "date", "Publication year or imprint date", ['=', '<', '<=', '>', '>='], "books.publication_year")
_cql_idx("dc", "type", "Material resource type", ['=', 'exact'], "'Monograph'")
_cql_idx("dc", "format", "Physical extent or carrier", ['=', 'exact'], "book_copies.status")
_cql_idx("dc", "identifier", "Standard identifier (ISBN, Barcode)", ['=', 'exact'], "books.isbn")
_cql_idx("dc", "source", "Bibliographic provenance", ['='], "'Library Catalog'")
_cql_idx("dc", "language", "Language code of text", ['=', 'exact'], "books.language")
_cql_idx("dc", "relation", "Related title or series", ['=', 'all'], "books.title")
_cql_idx("dc", "coverage", "Spatial or temporal scope", ['=', 'all'], "books.title")
_cql_idx("dc", "rights", "Copyright license terms", ['=', 'exact'], "'In Copyright'")
_cql_idx("bath", "personalAuthor", "Personal author main entry", ['=', 'exact', 'all'], "authors.name")
_cql_idx("bath", "corporateAuthor", "Corporate body author", ['=', 'exact', 'all'], "authors.name")
_cql_idx("bath", "meetingAuthor", "Conference or meeting name", ['=', 'all'], "books.title")
_cql_idx("bath", "uniformTitle", "Standardized uniform title", ['=', 'exact'], "books.title")
_cql_idx("bath", "keyTitle", "Continuing resource key title", ['=', 'exact'], "books.title")
_cql_idx("bath", "topicalSubject", "LCSH topical subject heading", ['=', 'all', 'any'], "categories.name")
_cql_idx("bath", "geographicSubject", "Geographic area name", ['=', 'all'], "categories.name")
_cql_idx("bath", "classification", "Dewey or LC classification mark", ['=', 'exact', '<='], "categories.name")

def lookup_cql_index(qualifier: str, index: str) -> Optional[CqlIndexDefinition]:
    key = f"{qualifier}.{index}".strip().lower()
    return CQL_INDEX_REGISTRY.get(key)
