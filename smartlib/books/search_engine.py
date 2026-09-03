"""High-performance faceted catalog search engine."""
from typing import Dict, Any
from smartlib.books.models import BookFilter
from smartlib.books.repository import BookRepository

class BookSearchEngine:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def search(
        self,
        keyword: str = "",
        category_id: int = None,
        author_id: int = None,
        available_only: bool = False,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        offset = max(0, (page - 1) * page_size)
        spec = BookFilter(
            query=keyword if keyword else None,
            category_id=category_id,
            author_id=author_id,
            available_only=available_only,
            limit=page_size,
            offset=offset
        )
        books, total = self.repo.search_books(spec)
        total_pages = max(1, (total + page_size - 1) // page_size)

        return {
            "items": [b.to_dict() for b in books],
            "total_items": total,
            "current_page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
