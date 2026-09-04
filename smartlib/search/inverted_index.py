"""Inverted Index with Okapi BM25 and TF-IDF Ranking."""

import math
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass
from .tokenizer import Tokenizer
from .stemmer import PorterStemmer
from .stopwords import is_stopword


@dataclass
class SearchResult:
    doc_id: str
    score: float
    matched_terms: List[str]


class InvertedIndex:
    """In-memory positional inverted index with BM25 scoring."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.tokenizer = Tokenizer()
        # term -> doc_id -> list of positions
        self.index: Dict[str, Dict[str, List[int]]] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.doc_metadata: Dict[str, Dict[str, Any]] = {}
        self.total_docs: int = 0

    def add_document(self, doc_id: str, text: str, metadata: Optional[Dict[str, Any]] = None):
        tokens_with_pos = self.tokenizer.tokenize_with_positions(text)
        filtered_terms = []
        doc_term_positions: Dict[str, List[int]] = {}

        for token, pos in tokens_with_pos:
            if not is_stopword(token):
                stemmed = PorterStemmer.stem(token)
                filtered_terms.append(stemmed)
                if stemmed not in doc_term_positions:
                    doc_term_positions[stemmed] = []
                doc_term_positions[stemmed].append(pos)

        self.doc_lengths[doc_id] = len(filtered_terms)
        self.doc_metadata[doc_id] = metadata or {}
        self.total_docs += 1

        for term, positions in doc_term_positions.items():
            if term not in self.index:
                self.index[term] = {}
            self.index[term][doc_id] = positions

    def search(self, query: str, top_k: int = 20) -> List[SearchResult]:
        query_tokens = self.tokenizer.tokenize(query)
        stemmed_query = [PorterStemmer.stem(t) for t in query_tokens if not is_stopword(t)]
        if not stemmed_query or self.total_docs == 0:
            return []

        avg_doc_len = sum(self.doc_lengths.values()) / max(1, self.total_docs)
        doc_scores: Dict[str, float] = {}
        doc_matched_terms: Dict[str, List[str]] = {}

        for term in stemmed_query:
            if term not in self.index:
                continue

            posting = self.index[term]
            doc_freq = len(posting)
            # IDF formula with smoothing
            idf = math.log(1.0 + (self.total_docs - doc_freq + 0.5) / (doc_freq + 0.5))

            for doc_id, positions in posting.items():
                tf = len(positions)
                doc_len = self.doc_lengths.get(doc_id, avg_doc_len)
                # BM25 term frequency saturation
                denom = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / avg_doc_len))
                term_score = idf * (tf * (self.k1 + 1.0)) / max(0.001, denom)

                doc_scores[doc_id] = doc_scores.get(doc_id, 0.0) + term_score
                if doc_id not in doc_matched_terms:
                    doc_matched_terms[doc_id] = []
                doc_matched_terms[doc_id].append(term)

        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [
            SearchResult(doc_id=d, score=s, matched_terms=doc_matched_terms.get(d, []))
            for d, s in sorted_docs
        ]
