"""
Domain data structures for compliance and activity audit records.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class AuditLogEntry:
    log_id: Optional[int] = None
    user_id: Optional[int] = None
    username: str = "SYSTEM"
    action: str = ""
    entity_type: str = ""
    entity_id: Optional[str] = None
    description: Optional[str] = None
    old_values: Optional[str] = None
    new_values: Optional[str] = None
    ip_address: Optional[str] = None
    timestamp: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "log_id": self.log_id,
            "user_id": self.user_id,
            "username": self.username,
            "action": self.action,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "description": self.description,
            "old_values": self.old_values,
            "new_values": self.new_values,
            "ip_address": self.ip_address,
            "timestamp": self.timestamp
        }
