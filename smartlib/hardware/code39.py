"""Code 39 Barcode Generator producing vector SVG output."""

from typing import Optional
from .barcode_tables import CODE39_PATTERNS


class Code39Generator:
    """Renders standard Code 39 barcodes for library book copies and patron ID cards."""

    def __init__(self, narrow_width: int = 2, wide_width: int = 5, height: int = 60):
        self.narrow = narrow_width
        self.wide = wide_width
        self.height = height

    def calculate_checksum(self, text: str) -> str:
        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%"
        val_sum = sum(chars.index(c) for c in text.upper() if c in chars)
        return chars[val_sum % 43]

    def generate_svg(self, data: str, include_checksum: bool = False, show_text: bool = True) -> str:
        clean = data.upper()
        if include_checksum:
            clean += self.calculate_checksum(clean)

        full_text = f"*{clean}*"
        rects = []
        current_x = 20  # Quiet zone

        for char in full_text:
            pattern = CODE39_PATTERNS.get(char)
            if not pattern:
                continue

            for idx, bit in enumerate(pattern):
                is_bar = (idx % 2 == 0)
                width = self.wide if bit == "1" else self.narrow
                if is_bar:
                    rects.append(f'<rect x="{current_x}" y="10" width="{width}" height="{self.height}" fill="black"/>')
                current_x += width

            # Inter-character gap (narrow space)
            current_x += self.narrow

        current_x += 20  # Trailing quiet zone
        svg_width = current_x
        svg_height = self.height + (30 if show_text else 20)

        text_el = ""
        if show_text:
            text_el = f'<text x="{svg_width / 2}" y="{self.height + 25}" font-family="monospace" font-size="14" text-anchor="middle">{data}</text>'

        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">\n'
            f'  <rect width="100%" height="100%" fill="white"/>\n'
            f'  {"".join(rects)}\n'
            f'  {text_el}\n'
            f'</svg>'
        )
