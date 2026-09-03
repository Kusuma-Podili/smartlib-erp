"""
Category domain model and classification structures.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Category:
    category_id: Optional[int] = None
    code: str = ""
    name: str = ""
    dewey_decimal_class: Optional[str] = None
    parent_category_id: Optional[int] = None
    description: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category_id": self.category_id,
            "code": self.code,
            "name": self.name,
            "dewey_decimal_class": self.dewey_decimal_class,
            "parent_category_id": self.parent_category_id,
            "description": self.description,
            "created_at": self.created_at
        }

@dataclass
class CategoryDTO:
    code: str
    name: str
    dewey_decimal_class: Optional[str] = None
    parent_category_id: Optional[int] = None
    description: Optional[str] = None
