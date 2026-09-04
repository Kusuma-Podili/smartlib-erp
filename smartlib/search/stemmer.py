"""Martin Porter Stemming Algorithm Implementation (Porter 1 & 2 rules)."""


class PorterStemmer:
    """Pure-Python implementation of the standard Porter Stemmer."""

    @staticmethod
    def _is_consonant(word: str, i: int) -> bool:
        c = word[i]
        if c in "aeiou":
            return False
        if c == "y":
            if i == 0:
                return True
            return not PorterStemmer._is_consonant(word, i - 1)
        return True

    @classmethod
    def _measure(cls, stem: str) -> int:
        """Measure m of a stem [C](VC)^m[V]."""
        m = 0
        i = 0
        n = len(stem)
        while i < n and cls._is_consonant(stem, i):
            i += 1
        while i < n:
            while i < n and not cls._is_consonant(stem, i):
                i += 1
            if i < n:
                m += 1
                while i < n and cls._is_consonant(stem, i):
                    i += 1
        return m

    @classmethod
    def _has_vowel(cls, stem: str) -> bool:
        for i in range(len(stem)):
            if not cls._is_consonant(stem, i):
                return True
        return False

    @classmethod
    def _ends_double_consonant(cls, stem: str) -> bool:
        if len(stem) < 2:
            return False
        return stem[-1] == stem[-2] and cls._is_consonant(stem, len(stem) - 1)

    @classmethod
    def _cvc(cls, stem: str) -> bool:
        if len(stem) < 3:
            return False
        i = len(stem) - 1
        if not cls._is_consonant(stem, i):
            return False
        if cls._is_consonant(stem, i - 1):
            return False
        if not cls._is_consonant(stem, i - 2):
            return False
        c = stem[i]
        if c in "wxy":
            return False
        return True

    @classmethod
    def stem(cls, word: str) -> str:
        word = word.lower()
        if len(word) <= 2:
            return word

        # Step 1a
        if word.endswith("sses"):
            word = word[:-2]
        elif word.endswith("ies"):
            word = word[:-2]
        elif not word.endswith("ss") and word.endswith("s"):
            word = word[:-1]

        # Step 1b
        extra_flag = False
        if word.endswith("eed"):
            stem = word[:-3]
            if cls._measure(stem) > 0:
                word = stem + "ee"
        elif word.endswith("ed"):
            stem = word[:-2]
            if cls._has_vowel(stem):
                word = stem
                extra_flag = True
        elif word.endswith("ing"):
            stem = word[:-3]
            if cls._has_vowel(stem):
                word = stem
                extra_flag = True

        if extra_flag:
            if word.endswith("at") or word.endswith("bl") or word.endswith("iz"):
                word += "e"
            elif cls._ends_double_consonant(word) and not word.endswith("l") and not word.endswith("s") and not word.endswith("z"):
                word = word[:-1]
            elif cls._measure(word) == 1 and cls._cvc(word):
                word += "e"

        # Step 1c
        if word.endswith("y"):
            stem = word[:-1]
            if cls._has_vowel(stem):
                word = stem + "i"

        # Step 2
        step2_suffixes = {
            "ational": "ate", "tional": "tion", "enci": "ence", "anci": "ance",
            "izer": "ize", "bli": "ble", "alli": "al", "entli": "ent", "eli": "e",
            "ousli": "ous", "ization": "ize", "ation": "ate", "ator": "ate",
            "alism": "al", "iveness": "ive", "fulness": "ful", "ousness": "ous",
            "aliti": "al", "iviti": "ive", "biliti": "ble"
        }
        for sfx, rep in step2_suffixes.items():
            if word.endswith(sfx):
                stem = word[:-len(sfx)]
                if cls._measure(stem) > 0:
                    word = stem + rep
                break

        # Step 3
        step3_suffixes = {
            "icate": "ic", "ative": "", "alize": "al", "iciti": "ic",
            "ical": "ic", "ful": "", "ness": ""
        }
        for sfx, rep in step3_suffixes.items():
            if word.endswith(sfx):
                stem = word[:-len(sfx)]
                if cls._measure(stem) > 0:
                    word = stem + rep
                break

        # Step 4
        step4_suffixes = ["al", "ance", "ence", "er", "ic", "able", "ible", "ant", "ement",
                          "ment", "ent", "sion", "tion", "ou", "ism", "ate", "iti", "ous", "ive", "ize"]
        for sfx in step4_suffixes:
            if word.endswith(sfx):
                stem = word[:-len(sfx)]
                if cls._measure(stem) > 1:
                    word = stem
                break

        # Step 5a
        if word.endswith("e"):
            stem = word[:-1]
            m = cls._measure(stem)
            if m > 1 or (m == 1 and not cls._cvc(stem)):
                word = stem

        # Step 5b
        if cls._measure(word) > 1 and cls._ends_double_consonant(word) and word.endswith("l"):
            word = word[:-1]

        return word
