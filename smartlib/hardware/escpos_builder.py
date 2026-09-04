"""ESC/POS Thermal Receipt Printer Command Stream Generator."""

import datetime
from typing import List


class EscPosReceiptBuilder:
    """Builds binary and text ESC/POS command sequences for patron checkout receipts."""

    ESC = "\x1b"
    GS = "\x1d"

    def __init__(self):
        self.stream: List[str] = [f"{self.ESC}@", f"{self.ESC}a\x01"]  # Init and align center

    def header(self, library_name: str, address: str):
        self.stream.append(f"{self.ESC}!\x38{library_name}\n")  # Double height/width
        self.stream.append(f"{self.ESC}!\x00{address}\n")
        self.stream.append("------------------------------------------------\n")

    def align_left(self):
        self.stream.append(f"{self.ESC}a\x00")

    def align_center(self):
        self.stream.append(f"{self.ESC}a\x01")

    def add_line(self, left_text: str, right_text: str = ""):
        if not right_text:
            self.stream.append(f"{left_text}\n")
        else:
            spacing = 48 - len(left_text) - len(right_text)
            self.stream.append(f"{left_text}{' ' * max(1, spacing)}{right_text}\n")

    def cut_paper(self):
        self.stream.append(f"\n\n\n{self.GS}V\x41\x00")  # Feed and cut

    def kick_cash_drawer(self):
        self.stream.append(f"{self.ESC}p\x00\x19\xfa")  # Pulse pin 2

    def to_bytes(self) -> bytes:
        return "".join(self.stream).encode("latin-1", errors="replace")
