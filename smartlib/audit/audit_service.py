"""
Audit service orchestrator and change-differential generator.
"""

import json
from typing import Optional, Dict, Any, List
from smartlib.audit.models import AuditLogEntry
from smartlib.audit.repository import AuditRepository

class AuditService:
    def __init__(self, repo: Optional[AuditRepository] = None):
        self.repo = repo or AuditRepository()

    def log(
        self,
        action: str,
        entity_type: str,
        entity_id: Optional[Any] = None,
        username: str = "SYSTEM",
        user_id: Optional[int] = None,
        description: Optional[str] = None,
        old_data: Optional[Dict[str, Any]] = None,
        new_data: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None
    ) -> int:
        """Record high-fidelity operational audit trail with state diffs."""
        old_json = json.dumps(old_data, default=str) if old_data else None
        new_json = json.dumps(new_data, default=str) if new_data else None

        entry = AuditLogEntry(
            user_id=user_id,
            username=username,
            action=action,
            entity_type=entity_type,
            entity_id=str(entity_id) if entity_id is not None else None,
            description=description,
            old_values=old_json,
            new_values=new_json,
            ip_address=ip_address
        )
        return self.repo.record(entry)

    def get_recent_activity(self, limit: int = 50) -> List[AuditLogEntry]:
        return self.repo.list_recent(limit=limit)
