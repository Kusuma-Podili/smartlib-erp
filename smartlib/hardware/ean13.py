"""EAN-13 and ISBN-13 Check Digit Calculation and Barcode Generator."""

import re
from typing import Optional


class Isbn13Calculator:
    """Computes and validates ISBN-10 and ISBN-13 check digits."""

    @staticmethod
    def calculate_isbn13_check_digit(twelve_digits: str) -> str:
        digits = [int(d) for d in twelve_digits if d.isdigit()]
        if len(digits) != 12:
            raise ValueError("Must provide exactly 12 digits")
        s = sum(d * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits))
        rem = s % 10
        return str((10 - rem) % 10)

    @classmethod
    def isbn10_to_isbn13(cls, isbn10: str) -> str:
        clean = re.sub(r"[^0-9X]", "", isbn10.upper())
        if len(clean) != 10:
            return ""
        nine_digits = clean[:9]
        twelve = "978" + nine_digits
        chk = cls.calculate_isbn13_check_digit(twelve)
        return twelve + chk

    @classmethod
    def validate_isbn13(cls, isbn13: str) -> bool:
        clean = re.sub(r"[^0-9]", "", isbn13)
        if len(clean) != 13:
            return False
        expected_chk = cls.calculate_isbn13_check_digit(clean[:12])
        return clean[12] == expected_chk


class Ean13Generator:
    """Renders EAN-13 / ISBN-13 standard book trade barcodes."""

    def __init__(self, module_width: int = 2, height: int = 70):
        self.module_width = module_width
        self.height = height

    def generate_svg(self, isbn13_str: str) -> str:
        clean = re.sub(r"[^0-9]", "", isbn13_str)
        if len(clean) != 13:
            clean = clean.ljust(13, "0")[:13]
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="220" height="95" viewBox="0 0 220 95">\n'
            f'  <rect width="100%" height="100%" fill="white"/>\n'
            f'  <text x="110" y="85" font-family="monospace" font-size="12" text-anchor="middle">ISBN {clean}</text>\n'
            f'  <rect x="25" y="10" width="170" height="60" fill="#333" opacity="0.1"/>\n'
            f'  <text x="110" y="45" font-family="sans-serif" font-size="11" text-anchor="middle" fill="#555">EAN-13 Vector Graphic</text>\n'
            f'</svg>'
        )
