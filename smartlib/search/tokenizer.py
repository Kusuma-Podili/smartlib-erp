"""Multilingual Text Tokenizer, Normalizer, and N-gram Generator."""

import re
import unicodedata
from typing import List, Tuple, Set


def remove_accents(input_str: str) -> str:
    """Normalize unicode and strip combining diacritical marks."""
    nfkd = unicodedata.normalize("NFKD", input_str)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_text(text: str) -> str:
    """Convert to lower case, strip accents, and normalize whitespace."""
    if not text:
        return ""
    text = remove_accents(text).lower()
    # Replace non-alphanumeric punctuation with spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


class Tokenizer:
    """Tokenizes text into terms, positions, and n-grams."""

    def __init__(self, min_token_len: int = 2, max_token_len: int = 40):
        self.min_token_len = min_token_len
        self.max_token_len = max_token_len

    def tokenize(self, text: str) -> List[str]:
        norm = normalize_text(text)
        tokens = norm.split()
        return [t for t in tokens if self.min_token_len <= len(t) <= self.max_token_len]

    def tokenize_with_positions(self, text: str) -> List[Tuple[str, int]]:
        norm = normalize_text(text)
        tokens = norm.split()
        result = []
        for pos, t in enumerate(tokens):
            if self.min_token_len <= len(t) <= self.max_token_len:
                result.append((t, pos))
        return result

    def generate_ngrams(self, tokens: List[str], n: int = 2) -> List[str]:
        if len(tokens) < n:
            return []
        return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
