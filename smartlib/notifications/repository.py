"""Data repository for notifications."""
from typing import Optional, List
from smartlib.database.connection import DatabaseManager
from smartlib.notifications.models import Notification

class NotificationRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def create(self, n: Notification) -> Notification:
        sql = """
        INSERT INTO notifications (user_id, title, message, type, is_read)
        VALUES (?, ?, ?, ?, ?);
        """
        cursor = self.db_manager.execute(sql, (n.user_id, n.title, n.message, n.type, int(n.is_read)))
        self.db_manager.get_connection().commit()
        n.notification_id = cursor.lastrowid
        return n

    def list_by_user(self, user_id: int, unread_only: bool = False, limit: int = 50) -> List[Notification]:
        where = "WHERE user_id = ?" + (" AND is_read = 0" if unread_only else "")
        sql = f"""
        SELECT notification_id, user_id, title, message, type, is_read, created_at
        FROM notifications
        {where}
        ORDER BY notification_id DESC
        LIMIT ?;
        """
        rows = self.db_manager.fetch_all(sql, (user_id, limit))
        return [Notification(**dict(r)) for r in rows]

    def mark_as_read(self, notification_id: int, user_id: int) -> None:
        self.db_manager.execute(
            "UPDATE notifications SET is_read = 1 WHERE notification_id = ? AND user_id = ?;",
            (notification_id, user_id)
        )
        self.db_manager.get_connection().commit()

    def mark_all_as_read(self, user_id: int) -> None:
        self.db_manager.execute(
            "UPDATE notifications SET is_read = 1 WHERE user_id = ?;",
            (user_id,)
        )
        self.db_manager.get_connection().commit()
