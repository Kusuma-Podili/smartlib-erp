"""Soundex and Metaphone Phonetic Search Encoders."""

import re


class Soundex:
    """Standard American Soundex Algorithm (RFC 1888)."""

    CODE_MAP = {
        "b": "1", "f": "1", "p": "1", "v": "1",
        "c": "2", "g": "2", "j": "2", "k": "2", "q": "2", "s": "2", "x": "2", "z": "2",
        "d": "3", "t": "3",
        "l": "4",
        "m": "5", "n": "5",
        "r": "6"
    }

    @classmethod
    def encode(cls, word: str) -> str:
        word = re.sub(r"[^a-zA-Z]", "", word).lower()
        if not word:
            return "0000"

        first_char = word[0].upper()
        encoded = [first_char]
        prev_code = cls.CODE_MAP.get(word[0], "0")

        for c in word[1:]:
            code = cls.CODE_MAP.get(c, "0")
            if code != "0":
                if code != prev_code:
                    encoded.append(code)
                prev_code = code
            else:
                prev_code = "0"

        code_str = "".join(encoded).ljust(4, "0")[:4]
        return code_str


class Metaphone:
    """Basic English Metaphone phonetic transformation algorithm."""

    @classmethod
    def encode(cls, word: str) -> str:
        word = re.sub(r"[^a-zA-Z]", "", word).upper()
        if not word:
            return ""

        # Drop initial letters
        if word.startswith(("KN", "GN", "PN", "AE", "WR")):
            word = word[1:]
        elif word.startswith("X"):
            word = "S" + word[1:]
        elif word.startswith("WH"):
            word = "W" + word[2:]

        result = []
        i = 0
        length = len(word)

        while i < length and len(result) < 6:
            c = word[i]
            # Avoid duplicate adjacent consonants except C
            if c != "C" and i > 0 and c == word[i - 1]:
                i += 1
                continue

            if c in "AEIOU":
                if i == 0:
                    result.append(c)
            elif c == "B":
                if i == length - 1 and i > 0 and word[i - 1] == "M":
                    pass
                else:
                    result.append("B")
            elif c == "C":
                if i + 1 < length and word[i + 1] in "EIY":
                    result.append("S")
                elif i + 1 < length and word[i + 1] == "H":
                    result.append("X")
                    i += 1
                else:
                    result.append("K")
            elif c == "D":
                if i + 2 < length and word[i+1:i+3] in ["GE", "GY", "GI"]:
                    result.append("J")
                else:
                    result.append("T")
            elif c in "FJLMNR":
                result.append(c)
            elif c == "G":
                if i + 1 < length and word[i + 1] in "EIY":
                    result.append("J")
                else:
                    result.append("K")
            elif c == "H":
                if i + 1 < length and word[i + 1] in "AEIOU":
                    result.append("H")
            elif c == "K":
                result.append("K")
            elif c == "P":
                if i + 1 < length and word[i + 1] == "H":
                    result.append("F")
                    i += 1
                else:
                    result.append("P")
            elif c == "Q":
                result.append("K")
            elif c == "S":
                if i + 1 < length and word[i + 1] == "H":
                    result.append("X")
                    i += 1
                else:
                    result.append("S")
            elif c == "T":
                if i + 1 < length and word[i + 1] == "H":
                    result.append("0")
                    i += 1
                elif i + 2 < length and word[i+1:i+3] in ["IA", "IO"]:
                    result.append("X")
                else:
                    result.append("T")
            elif c == "V":
                result.append("F")
            elif c in "WY":
                if i + 1 < length and word[i + 1] in "AEIOU":
                    result.append(c)
            elif c == "X":
                result.extend(["K", "S"])
            elif c == "Z":
                result.append("S")

            i += 1

        return "".join(result)
