"""
Author domain model and data structures.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Author:
    author_id: Optional[int] = None
    name: str = ""
    biography: Optional[str] = None
    nationality: Optional[str] = None
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    website: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "author_id": self.author_id,
            "name": self.name,
            "biography": self.biography,
            "nationality": self.nationality,
            "birth_year": self.birth_year,
            "death_year": self.death_year,
            "website": self.website,
            "created_at": self.created_at
        }

@dataclass
class AuthorDTO:
    name: str
    biography: Optional[str] = None
    nationality: Optional[str] = None
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    website: Optional[str] = None
