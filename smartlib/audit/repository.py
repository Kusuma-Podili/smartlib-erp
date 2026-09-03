"""
Data repository for recording and querying audit trails.
"""

import json
from typing import List, Optional, Dict, Any
from smartlib.database.connection import DatabaseManager
from smartlib.audit.models import AuditLogEntry

class AuditRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def record(self, entry: AuditLogEntry) -> int:
        """Insert new audit log entry."""
        sql = """
        INSERT INTO audit_logs 
        (user_id, username, action, entity_type, entity_id, description, old_values, new_values, ip_address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(
            sql,
            (
                entry.user_id,
                entry.username,
                entry.action,
                entry.entity_type,
                str(entry.entity_id) if entry.entity_id is not None else None,
                entry.description,
                entry.old_values,
                entry.new_values,
                entry.ip_address
            )
        )
        self.db_manager.get_connection().commit()
        return cursor.lastrowid

    def list_recent(self, limit: int = 50, offset: int = 0) -> List[AuditLogEntry]:
        """Retrieve most recent audit entries."""
        sql = """
        SELECT log_id, user_id, username, action, entity_type, entity_id, description,
               old_values, new_values, ip_address, timestamp
        FROM audit_logs
        ORDER BY log_id DESC
        LIMIT ? OFFSET ?;
        """
        rows = self.db_manager.fetch_all(sql, (limit, offset))
        return [AuditLogEntry(**dict(r)) for r in rows]

    def filter_logs(
        self,
        username: Optional[str] = None,
        action: Optional[str] = None,
        entity_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[AuditLogEntry]:
        """Filter audit log records by criteria."""
        clauses = []
        params = []
        if username:
            clauses.append("username LIKE ?")
            params.append(f"%{username}%")
        if action:
            clauses.append("action = ?")
            params.append(action)
        if entity_type:
            clauses.append("entity_type = ?")
            params.append(entity_type)

        where_clause = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        sql = f"""
        SELECT log_id, user_id, username, action, entity_type, entity_id, description,
               old_values, new_values, ip_address, timestamp
        FROM audit_logs
        {where_clause}
        ORDER BY log_id DESC
        LIMIT ? OFFSET ?;
        """
        params.extend([limit, offset])
        rows = self.db_manager.fetch_all(sql, tuple(params))
        return [AuditLogEntry(**dict(r)) for r in rows]
