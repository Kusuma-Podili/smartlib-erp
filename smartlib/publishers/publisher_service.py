"""
Publisher management service.
"""

from typing import Optional, List
from smartlib.publishers.models import Publisher, PublisherDTO
from smartlib.publishers.repository import PublisherRepository
from smartlib.audit.audit_service import AuditService
from smartlib.errors import ValidationError, DuplicateEntityError, EntityNotFoundError

class PublisherService:
    def __init__(self, repo: Optional[PublisherRepository] = None, audit_svc: Optional[AuditService] = None):
        self.repo = repo or PublisherRepository()
        self.audit_svc = audit_svc or AuditService()

    def add_publisher(self, dto: PublisherDTO, actor_username: str = "librarian") -> Publisher:
        if not dto.name or not dto.name.strip():
            raise ValidationError("Publisher name is required.", {"name": "Required field."})
        clean_name = dto.name.strip()
        if self.repo.get_by_name(clean_name):
            raise DuplicateEntityError("Publisher", "name", clean_name)

        pub = Publisher(
            name=clean_name,
            contact_email=dto.contact_email,
            phone=dto.phone,
            address=dto.address,
            website=dto.website,
            country=dto.country
        )
        created = self.repo.create(pub)
        self.audit_svc.log(
            action="PUBLISHER_CREATE",
            entity_type="Publisher",
            entity_id=created.publisher_id,
            username=actor_username,
            description=f"Created publisher '{created.name}'."
        )
        return created

    def get_publisher(self, publisher_id: int) -> Publisher:
        p = self.repo.get_by_id(publisher_id)
        if not p:
            raise EntityNotFoundError("Publisher", publisher_id)
        return p

    def get_or_create(self, name: str, actor_username: str = "librarian") -> Publisher:
        existing = self.repo.get_by_name(name)
        if existing:
            return existing
        return self.add_publisher(PublisherDTO(name=name), actor_username=actor_username)

    def list_publishers(self) -> List[Publisher]:
        return self.repo.list_all()
