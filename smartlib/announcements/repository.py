"""Data repository for library announcements."""
from typing import Optional, List
from smartlib.database.connection import DatabaseManager
from smartlib.announcements.models import Announcement

class AnnouncementRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, a: Announcement) -> Announcement:
        sql = """
        INSERT INTO announcements (created_by_user_id, title, content, priority, is_published, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(
            sql,
            (a.created_by_user_id, a.title, a.content, a.priority, int(a.is_published), a.start_date, a.end_date)
        )
        self.db_manager.get_connection().commit()
        a.announcement_id = cursor.lastrowid
        return a

    def list_active(self) -> List[Announcement]:
        sql = """
        SELECT announcement_id, created_by_user_id, title, content, priority, is_published, start_date, end_date, created_at
        FROM announcements
        WHERE is_published = 1 AND (end_date IS NULL OR end_date >= DATE('now'))
        ORDER BY 
            CASE priority 
                WHEN 'CRITICAL' THEN 1 
                WHEN 'HIGH' THEN 2 
                WHEN 'NORMAL' THEN 3 
                ELSE 4 
            END ASC, announcement_id DESC;
        """
        rows = self.db_manager.fetch_all(sql)
        return [Announcement(**dict(r)) for r in rows]
