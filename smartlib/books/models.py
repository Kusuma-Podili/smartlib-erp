"""Book master domain entities and query specification filters."""
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from smartlib.constants import BookCopyStatus

@dataclass
class Book:
    book_id: Optional[int] = None
    isbn: str = ""
    title: str = ""
    subtitle: Optional[str] = None
    author_id: int = 0
    publisher_id: int = 0
    category_id: int = 0
    edition: str = "1st Edition"
    publication_year: Optional[int] = None
    language: str = "English"
    description: Optional[str] = None
    shelf_number: str = "A1"
    rack_number: str = "R1"
    price: float = 0.00
    total_copies: int = 0
    available_copies: int = 0
    issued_copies: int = 0
    lost_copies: int = 0
    damaged_copies: int = 0
    status: str = BookCopyStatus.AVAILABLE.value
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    author_name: Optional[str] = None
    category_name: Optional[str] = None
    publisher_name: Optional[str] = None

    def is_available(self) -> bool:
        return self.available_copies > 0 and self.status == BookCopyStatus.AVAILABLE.value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "book_id": self.book_id,
            "isbn": self.isbn,
            "title": self.title,
            "subtitle": self.subtitle,
            "author_id": self.author_id,
            "author_name": self.author_name,
            "publisher_id": self.publisher_id,
            "publisher_name": self.publisher_name,
            "category_id": self.category_id,
            "category_name": self.category_name,
            "edition": self.edition,
            "publication_year": self.publication_year,
            "language": self.language,
            "description": self.description,
            "shelf_number": self.shelf_number,
            "rack_number": self.rack_number,
            "price": self.price,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies,
            "issued_copies": self.issued_copies,
            "lost_copies": self.lost_copies,
            "damaged_copies": self.damaged_copies,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

@dataclass
class BookDTO:
    isbn: str
    title: str
    author_id: int
    publisher_id: int
    category_id: int
    subtitle: Optional[str] = None
    edition: str = "1st Edition"
    publication_year: Optional[int] = None
    language: str = "English"
    description: Optional[str] = None
    shelf_number: str = "A1"
    rack_number: str = "R1"
    price: float = 0.00

@dataclass
class BookFilter:
    query: Optional[str] = None
    isbn: Optional[str] = None
    author_id: Optional[int] = None
    category_id: Optional[int] = None
    publisher_id: Optional[int] = None
    language: Optional[str] = None
    available_only: bool = False
    shelf_number: Optional[str] = None
    rack_number: Optional[str] = None
    sort_by: str = "title"
    sort_dir: str = "ASC"
    limit: int = 20
    offset: int = 0
