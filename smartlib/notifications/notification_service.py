"""Notification dispatch service."""
from typing import Optional, List
from smartlib.notifications.models import Notification
from smartlib.notifications.repository import NotificationRepository
from smartlib.constants import NotificationType

class NotificationService:
    def __init__(self, repo: Optional[NotificationRepository] = None):
        self.repo = repo or NotificationRepository()

    def send_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: str = NotificationType.GENERAL_ANNOUNCEMENT.value
    ) -> Notification:
        n = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            is_read=False
        )
        return self.repo.create(n)

    def get_user_notifications(self, user_id: int, unread_only: bool = False) -> List[Notification]:
        return self.repo.list_by_user(user_id=user_id, unread_only=unread_only)

    def mark_read(self, notification_id: int, user_id: int) -> None:
        self.repo.mark_as_read(notification_id, user_id)
