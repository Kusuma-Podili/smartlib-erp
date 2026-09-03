"""
Publisher domain entities.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Publisher:
    publisher_id: Optional[int] = None
    name: str = ""
    contact_email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    country: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "publisher_id": self.publisher_id,
            "name": self.name,
            "contact_email": self.contact_email,
            "phone": self.phone,
            "address": self.address,
            "website": self.website,
            "country": self.country,
            "created_at": self.created_at
        }

@dataclass
class PublisherDTO:
    name: str
    contact_email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    country: Optional[str] = None
