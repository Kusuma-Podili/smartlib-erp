"""Broadcast announcement publishing service."""
import datetime
from typing import Optional, List
from smartlib.announcements.models import Announcement
from smartlib.announcements.repository import AnnouncementRepository
from smartlib.audit.audit_service import AuditService
from smartlib.constants import AnnouncementPriority, AuditAction
from smartlib.errors import ValidationError

class AnnouncementService:
    def __init__(self, repo: Optional[AnnouncementRepository] = None, audit_svc: Optional[AuditService] = None):
        self.repo = repo or AnnouncementRepository()
        self.audit_svc = audit_svc or AuditService()

    def publish_announcement(
        self,
        creator_user_id: int,
        title: str,
        content: str,
        priority: str = AnnouncementPriority.NORMAL.value,
        end_date: Optional[str] = None,
        actor_username: str = "admin"
    ) -> Announcement:
        if not title or not title.strip():
            raise ValidationError("Title is required.", {"title": "Required."})
        if not content or not content.strip():
            raise ValidationError("Content is required.", {"content": "Required."})

        today = datetime.date.today().strftime("%Y-%m-%d")
        a = Announcement(
            created_by_user_id=creator_user_id,
            title=title.strip(),
            content=content.strip(),
            priority=priority,
            is_published=True,
            start_date=today,
            end_date=end_date
        )
        created = self.repo.create(a)

        self.audit_svc.log(
            action=AuditAction.ANNOUNCEMENT_CREATE.value,
            entity_type="Announcement",
            entity_id=created.announcement_id,
            username=actor_username,
            description=f"Published announcement '{created.title}' (Priority: {priority})."
        )
        return created

    def list_active_announcements(self) -> List[Announcement]:
        return self.repo.list_active()
