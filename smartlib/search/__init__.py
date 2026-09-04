"""Search Engine, Natural Language Processing, and Catalog Indexer Package.

Implements Okapi BM25 & TF-IDF ranking, inverted index, Porter stemmer,
phonetic search (Soundex & Metaphone), multi-field faceted search, and spell check.
"""
from .tokenizer import Tokenizer, normalize_text
from .stemmer import PorterStemmer
from .stopwords import get_stopwords, is_stopword
from .phonetics import Soundex, Metaphone
from .thesaurus import SubjectThesaurus
from .inverted_index import InvertedIndex, SearchResult
from .faceted_search import FacetEngine, FacetResult
from .spell_corrector import SpellCorrector
