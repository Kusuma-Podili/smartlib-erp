"""Spelling Correction and Query Suggestion Engine."""

from typing import Dict, List, Set, Optional


class SpellCorrector:
    """Damerau-Levenshtein distance spell corrector using catalog vocabulary."""

    def __init__(self):
        self.vocab: Dict[str, int] = {}

    def add_word(self, word: str, count: int = 1):
        clean = word.lower().strip()
        self.vocab[clean] = self.vocab.get(clean, 0) + count

    def train_from_text(self, text: str):
        import re
        words = re.findall(r"[a-zA-Z]{3,}", text.lower())
        for w in words:
            self.add_word(w)

    def _edits1(self, word: str) -> Set[str]:
        letters = "abcdefghijklmnopqrstuvwxyz"
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def suggest(self, word: str) -> Optional[str]:
        clean = word.lower().strip()
        if clean in self.vocab:
            return clean

        candidates = self._edits1(clean)
        valid_candidates = [c for c in candidates if c in self.vocab]
        if not valid_candidates:
            return None

        # Return candidate with highest frequency
        return max(valid_candidates, key=lambda c: self.vocab[c])
