"""Extended Barcode Symbology Engine (Code 93, Data Matrix ECC 200, PDF417).

Provides mathematical encoding tables, Reed-Solomon polynomial math, and bit patterns.
"""

from typing import Dict, List, Tuple


# Code 93 Pattern Table (Character -> 9-module bit pattern: 3 bars and 3 spaces)
CODE93_PATTERNS: Dict[str, str] = {
    "0": "100010100", "1": "101001000", "2": "101000100", "3": "101000010",
    "4": "100101000", "5": "100100100", "6": "100100010", "7": "101010000",
    "8": "100010010", "9": "100001010", "A": "110101000", "B": "110100100",
    "C": "110100010", "D": "110010100", "E": "110010010", "F": "110001010",
    "G": "101101000", "H": "101100100", "I": "101100010", "J": "100110100",
    "K": "100011010", "L": "101011000", "M": "101001100", "N": "101000110",
    "O": "100101100", "P": "100010110", "Q": "110110100", "R": "110110010",
    "S": "110101100", "T": "110100110", "U": "110010110", "V": "110011010",
    "W": "101101100", "X": "101100110", "Y": "100110110", "Z": "100111010",
    "-": "100101110", ".": "111010100", " ": "111010010", "$": "111001010",
    "/": "101101110", "+": "101110110", "%": "110101110", "*": "101011110"
}

# Galois Field GF(256) Log and Anti-Log Tables for Reed-Solomon ECC Math
GF256_EXP: List[int] = [0] * 512
GF256_LOG: List[int] = [0] * 256

def _init_gf256():
    x = 1
    for i in range(255):
        GF256_EXP[i] = x
        GF256_EXP[i + 255] = x
        GF256_LOG[x] = i
        x <<= 1
        if x & 0x100:
            x ^= 0x12D  # Primitive polynomial x^8 + x^5 + x^3 + x^2 + 1

_init_gf256()

def gf_multiply(x: int, y: int) -> int:
    if x == 0 or y == 0:
        return 0
    return GF256_EXP[GF256_LOG[x] + GF256_LOG[y]]

def gf_poly_multiply(p1: List[int], p2: List[int]) -> List[int]:
    result = [0] * (len(p1) + len(p2) - 1)
    for j, c2 in enumerate(p2):
        for i, c1 in enumerate(p1):
            result[i + j] ^= gf_multiply(c1, c2)
    return result

def gf_poly_div(dividend: List[int], divisor: List[int]) -> List[int]:
    out = list(dividend)
    for i in range(len(dividend) - len(divisor) + 1):
        coef = out[i]
        if coef != 0:
            for j in range(1, len(divisor)):
                if divisor[j] != 0:
                    out[i + j] ^= gf_multiply(divisor[j], coef)
    separator = -(len(divisor) - 1)
    return out[separator:]
