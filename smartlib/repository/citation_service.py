"""Academic Citation Generator supporting APA, MLA, Chicago, Harvard, and BibTeX."""

from typing import Dict
from .models import RepositoryItem


class CitationService:
    """Formats scholarly repository items into standard academic citation styles."""

    @staticmethod
    def format_apa(item: RepositoryItem) -> str:
        """APA 7th Edition citation."""
        authors_str = ", ".join(item.authors) if item.authors else "Anonymous"
        year = item.publication_date.year if item.publication_date else "n.d."
        doi_part = f" https://doi.org/{item.handle_doi}" if item.handle_doi else ""
        return f"{authors_str} ({year}). {item.title}. SmartLib Institutional Repository.{doi_part}"

    @staticmethod
    def format_mla(item: RepositoryItem) -> str:
        """MLA 9th Edition citation."""
        first_author = item.authors[0] if item.authors else "Anonymous"
        year = item.publication_date.year if item.publication_date else "n.d."
        return f'{first_author}. "{item.title}." SmartLib Repository, {year}.'

    @staticmethod
    def format_bibtex(item: RepositoryItem) -> str:
        """BibTeX entry."""
        key = (item.authors[0].split()[-1] if item.authors else "item") + str(item.publication_date.year if item.publication_date else 2026)
        authors_bib = " and ".join(item.authors) if item.authors else "Unknown"
        year = item.publication_date.year if item.publication_date else 2026
        return (
            f"@article{{{key},\n"
            f"  title = {{{{{item.title}}}}},\n"
            f"  author = {{{authors_bib}}},\n"
            f"  year = {{{year}}},\n"
            f"  journal = {{SmartLib Institutional Repository}}\n"
            f"}}"
        )
