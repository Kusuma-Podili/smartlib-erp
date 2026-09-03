"""Notification domain entity."""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from smartlib.constants import NotificationType

@dataclass
class Notification:
    notification_id: Optional[int] = None
    user_id: int = 0
    title: str = ""
    message: str = ""
    type: str = NotificationType.GENERAL_ANNOUNCEMENT.value
    is_read: bool = False
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "title": self.title,
            "message": self.message,
            "type": self.type,
            "is_read": self.is_read,
            "created_at": self.created_at
        }
