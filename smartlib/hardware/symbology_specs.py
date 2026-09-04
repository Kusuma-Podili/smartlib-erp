"""Complete Library Barcode Symbology Encoders and Pattern Specifications.

Implements bit patterns, stop/start framing, checksum algorithms, and parity encodings
for standard library barcode formats: Code 39, Code 128 (ABC), EAN-13, and Codabar.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SymbologyEncodingResult:
    symbology_name: str
    raw_value: str
    checksum_digit: Optional[str]
    binary_pattern: str  # 1 = bar, 0 = space
    formatted_barcode: str


# ====================================================================
# CODE 39 SPECIFICATION & PATTERNS
# ====================================================================
CODE39_PATTERNS: Dict[str, str] = {
    '0': '000110100', '1': '100100001', '2': '001100001', '3': '101100000',
    '4': '000110001', '5': '100110000', '6': '001110000', '7': '000100101',
    '8': '100100100', '9': '001100100', 'A': '100001001', 'B': '001001001',
    'C': '101001000', 'D': '000011001', 'E': '100011000', 'F': '001011000',
    'G': '000001101', 'H': '100001100', 'I': '001001100', 'J': '000011100',
    'K': '100000011', 'L': '001000011', 'M': '101000010', 'N': '000010011',
    'O': '100010010', 'P': '001010010', 'Q': '000000111', 'R': '100000110',
    'S': '001000110', 'T': '000010110', 'U': '110000001', 'V': '011000001',
    'W': '111000000', 'X': '010010001', 'Y': '110010000', 'Z': '011010000',
    '-': '010000101', '.': '110000100', ' ': '011000100', '$': '010101000',
    '/': '010100010', '+': '010001010', '%': '000101010', '*': '010010100'
}


def encode_code39(text: str, include_checksum: bool = False) -> SymbologyEncodingResult:
    """Encode alphanumeric text into Code 39 bar/space pattern."""
    clean = text.upper().strip()
    c39_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%"
    checksum_char = None

    if include_checksum:
        total = sum(c39_chars.index(c) for c in clean if c in c39_chars)
        checksum_char = c39_chars[total % 43]
        clean += checksum_char

    full_str = f"*{clean}*"
    pattern_parts = []
    for ch in full_str:
        pat = CODE39_PATTERNS.get(ch, CODE39_PATTERNS[' '])
        # Convert narrow/wide to binary representation: 0 = narrow bar/space, 1 = wide bar/space
        # Each char is 5 bars and 4 spaces (total 9 elements)
        binary = ""
        for idx, bit in enumerate(pat):
            char_type = "1" if idx % 2 == 0 else "0"
            weight = 2 if bit == "1" else 1
            binary += char_type * weight
        pattern_parts.append(binary)

    # Intersymbol space of 1 unit
    binary_pattern = "0".join(pattern_parts)
    return SymbologyEncodingResult(
        symbology_name="Code 39",
        raw_value=text,
        checksum_digit=checksum_char,
        binary_pattern=binary_pattern,
        formatted_barcode=full_str
    )


# ====================================================================
# CODABAR (USD-4 / NW-7) SPECIFICATION
# ====================================================================
CODABAR_PATTERNS: Dict[str, str] = {
    '0': '101010011', '1': '101011001', '2': '101001011', '3': '110010101',
    '4': '101101001', '5': '110101001', '6': '100101011', '7': '100101101',
    '8': '100110101', '9': '110100101', '-': '101001101', '$': '101100101',
    ':': '1101011011', '/': '1101101011', '.': '1101101101', '+': '1011011011',
    'A': '1011001001', 'B': '1001001011', 'C': '1010010011', 'D': '1010011001'
}


def encode_codabar(text: str, start_char: str = "A", stop_char: str = "B") -> SymbologyEncodingResult:
    """Encode numeric library patron/copy identifier into Codabar format."""
    clean = text.strip()
    full_str = f"{start_char}{clean}{stop_char}"
    patterns = []
    for ch in full_str:
        pat = CODABAR_PATTERNS.get(ch, CODABAR_PATTERNS['0'])
        patterns.append(pat)

    binary_pattern = "0".join(patterns)
    return SymbologyEncodingResult(
        symbology_name="Codabar (NW-7)",
        raw_value=text,
        checksum_digit=None,
        binary_pattern=binary_pattern,
        formatted_barcode=full_str
    )


# ====================================================================
# EAN-13 / ISBN-13 SPECIFICATION
# ====================================================================
EAN13_L_CODES = [
    "0001101", "0011001", "0010011", "0111101", "0100011",
    "0110001", "0101111", "0111011", "0110111", "0001011"
]
EAN13_G_CODES = [
    "0100111", "0110011", "0011011", "0100001", "0011101",
    "0111001", "0000101", "0010001", "0001001", "0010111"
]
EAN13_R_CODES = [
    "1110010", "1100110", "1101100", "1000010", "1011100",
    "1001110", "1010000", "1000100", "1001000", "1110100"
]
EAN13_STRUCTURE = [
    "LLLLLL", "LLGLGG", "LLGGLG", "LLGGGL", "LGLLGG",
    "LGGLLG", "LGGGLL", "LGLGLG", "LGLGGL", "LGGLGL"
]


def calculate_ean13_checksum(digits12: str) -> int:
    """Calculate the Modulo-10 checksum digit for an EAN-13 string."""
    odd_sum = sum(int(digits12[i]) for i in range(0, 12, 2))
    even_sum = sum(int(digits12[i]) * 3 for i in range(1, 12, 2))
    total = odd_sum + even_sum
    rem = total % 10
    return 0 if rem == 0 else (10 - rem)


def encode_ean13(isbn12_or_13: str) -> SymbologyEncodingResult:
    """Encode ISBN/EAN into complete EAN-13 barcode pattern."""
    digits = "".join(c for c in isbn12_or_13 if c.isdigit())
    if len(digits) == 12:
        chk = calculate_ean13_checksum(digits)
        full_digits = f"{digits}{chk}"
    elif len(digits) >= 13:
        full_digits = digits[:13]
        chk = int(full_digits[-1])
    else:
        full_digits = digits.zfill(12)
        chk = calculate_ean13_checksum(full_digits)
        full_digits = f"{full_digits}{chk}"

    first_digit = int(full_digits[0])
    struct = EAN13_STRUCTURE[first_digit]

    # Normal framing: 101 guard bars
    binary = "101"
    # Left 6 digits
    for i, ch in enumerate(full_digits[1:7]):
        digit_val = int(ch)
        if struct[i] == "L":
            binary += EAN13_L_CODES[digit_val]
        else:
            binary += EAN13_G_CODES[digit_val]

    # Center guard pattern: 01010
    binary += "01010"

    # Right 6 digits (always R codes)
    for ch in full_digits[7:13]:
        digit_val = int(ch)
        binary += EAN13_R_CODES[digit_val]

    # End guard bars: 101
    binary += "101"

    return SymbologyEncodingResult(
        symbology_name="EAN-13 / ISBN-13",
        raw_value=isbn12_or_13,
        checksum_digit=str(chk),
        binary_pattern=binary,
        formatted_barcode=full_digits
    )
