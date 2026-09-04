"""Library Subject Thesaurus and Controlled Vocabulary Engine."""

from typing import Dict, List, Set, Optional


class SubjectThesaurus:
    """Provides synonym expansion, broader terms, and narrower terms."""

    def __init__(self):
        self.synonyms: Dict[str, Set[str]] = {
            "ai": {"artificial intelligence", "machine learning", "deep learning", "neural networks"},
            "programming": {"coding", "software engineering", "computer programming", "development"},
            "database": {"databases", "sql", "relational database", "nosql", "data storage"},
            "algorithms": {"data structures", "computational complexity", "algorithmic design"},
            "security": {"cybersecurity", "information security", "cryptography", "infosec"},
            "networking": {"computer networks", "telecommunications", "tcp/ip", "internet protocols"},
            "mathematics": {"math", "calculus", "linear algebra", "discrete math", "statistics"},
            "physics": {"classical mechanics", "quantum mechanics", "thermodynamics", "astrophysics"},
        }
        self.broader_terms: Dict[str, str] = {
            "machine learning": "artificial intelligence",
            "deep learning": "machine learning",
            "relational database": "database",
            "linear algebra": "mathematics",
            "quantum mechanics": "physics",
        }

    def expand_query(self, term: str) -> Set[str]:
        """Expand a term with its known synonyms and related terms."""
        clean = term.lower().strip()
        expanded = {clean}
        if clean in self.synonyms:
            expanded.update(self.synonyms[clean])
        # Reverse lookup
        for head, syns in self.synonyms.items():
            if clean in syns:
                expanded.add(head)
                expanded.update(syns)
        return expanded
