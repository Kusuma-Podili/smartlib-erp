"""Barcode and serialized accession tag generator."""
import re

class BarcodeGenerator:
    @staticmethod
    def generate_barcode(isbn: str, copy_index: int) -> str:
        clean_isbn = re.sub(r"\D", "", isbn)
        return f"BC-{clean_isbn}-{copy_index:03d}"

    @staticmethod
    def generate_copy_number(copy_index: int) -> str:
        return f"COPY-{copy_index:03d}"
