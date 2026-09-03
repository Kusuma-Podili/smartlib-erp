"""Announcement domain entity."""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from smartlib.constants import AnnouncementPriority

@dataclass
class Announcement:
    announcement_id: Optional[int] = None
    created_by_user_id: int = 0
    title: str = ""
    content: str = ""
    priority: str = AnnouncementPriority.NORMAL.value
    is_published: bool = True
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "announcement_id": self.announcement_id,
            "created_by_user_id": self.created_by_user_id,
            "title": self.title,
            "content": self.content,
            "priority": self.priority,
            "is_published": self.is_published,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "created_at": self.created_at
        }
