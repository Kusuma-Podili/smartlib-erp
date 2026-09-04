"""Zebra Programming Language (ZPL II) Label Formatter."""

from typing import List


class ZplLabelBuilder:
    """Generates ZPL II commands for industrial thermal spine and barcode printers."""

    def __init__(self, label_width_dots: int = 812, label_height_dots: int = 1218):
        self.width = label_width_dots
        self.height = label_height_dots
        self.commands: List[str] = ["^XA"]  # Start Format

    def add_text(self, x: int, y: int, text: str, font_size_dots: int = 30):
        self.commands.append(f"^FO{x},{y}^A0N,{font_size_dots},{font_size_dots}^FD{text}^FS")

    def add_barcode_code128(self, x: int, y: int, data: str, height_dots: int = 100, show_text: bool = True):
        line_opt = "Y" if show_text else "N"
        self.commands.append(f"^FO{x},{y}^BCN,{height_dots},{line_opt},N,N^FD{data}^FS")

    def add_box(self, x: int, y: int, width: int, height: int, border_thickness: int = 2):
        self.commands.append(f"^FO{x},{y}^GB{width},{height},{border_thickness}^FS")

    def render(self) -> str:
        self.commands.append("^XZ")  # End Format
        return "\n".join(self.commands)

    @classmethod
    def create_spine_label(cls, call_number: str, author_cutter: str, year: str) -> str:
        b = cls(label_width_dots=400, label_height_dots=300)
        b.add_box(10, 10, 380, 280, 3)
        b.add_text(30, 40, "SMARTLIB CENTRAL", font_size_dots=22)
        b.add_text(30, 90, call_number, font_size_dots=32)
        b.add_text(30, 140, author_cutter, font_size_dots=32)
        b.add_text(30, 190, year, font_size_dots=28)
        return b.render()
