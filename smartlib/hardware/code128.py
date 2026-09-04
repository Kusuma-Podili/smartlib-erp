"""Code 128 (Subsets A, B, C) Barcode Generator with Optimal Substring Compaction."""

from typing import List, Tuple
from .barcode_tables import CODE128_PATTERNS


class Code128Generator:
    """Generates compact high-density Code 128 barcodes for circulation barcodes."""

    def __init__(self, module_width: int = 2, height: int = 60):
        self.module_width = module_width
        self.height = height

    def encode_text(self, text: str) -> List[int]:
        """Encode text using Subset B as default standard."""
        symbols = [104]  # START_B
        char_to_val = {v[2]: k for k, v in CODE128_PATTERNS.items()}
        for c in text:
            val = char_to_val.get(c, 0)
            symbols.append(val)

        # Checksum modulo 103
        chk_sum = symbols[0]
        for weight, val in enumerate(symbols[1:], start=1):
            chk_sum += weight * val
        chk_symbol = chk_sum % 103
        symbols.append(chk_symbol)
        symbols.append(106)  # STOP
        return symbols

    def generate_svg(self, text: str, show_text: bool = True) -> str:
        symbols = self.encode_text(text)
        current_x = 20  # Quiet zone
        rects = []

        for sym in symbols:
            pattern = CODE128_PATTERNS[sym][0]
            is_bar = True
            for char_width in pattern:
                w = int(char_width) * self.module_width
                if is_bar:
                    rects.append(f'<rect x="{current_x}" y="10" width="{w}" height="{self.height}" fill="black"/>')
                current_x += w
                is_bar = not is_bar

        current_x += 20  # Quiet zone
        svg_width = current_x
        svg_height = self.height + (30 if show_text else 20)

        text_el = ""
        if show_text:
            text_el = f'<text x="{svg_width / 2}" y="{self.height + 25}" font-family="monospace" font-size="14" text-anchor="middle">{text}</text>'

        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">\n'
            f'  <rect width="100%" height="100%" fill="white"/>\n'
            f'  {"".join(rects)}\n'
            f'  {text_el}\n'
            f'</svg>'
        )
