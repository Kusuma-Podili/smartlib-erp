"""
Author cataloging service.
"""

from typing import Optional, List
from smartlib.authors.models import Author, AuthorDTO
from smartlib.authors.repository import AuthorRepository
from smartlib.audit.audit_service import AuditService
from smartlib.errors import ValidationError, EntityNotFoundError
from smartlib.constants import AuditAction

class AuthorService:
    def __init__(self, repo: Optional[AuthorRepository] = None, audit_svc: Optional[AuditService] = None):
        self.repo = repo or AuthorRepository()
        self.audit_svc = audit_svc or AuditService()

    def add_author(self, dto: AuthorDTO, actor_username: str = "librarian") -> Author:
        if not dto.name or not dto.name.strip():
            raise ValidationError("Author name is required.", {"name": "Required field."})
        author = Author(
            name=dto.name.strip(),
            biography=dto.biography,
            nationality=dto.nationality,
            birth_year=dto.birth_year,
            death_year=dto.death_year,
            website=dto.website
        )
        created = self.repo.create(author)
        self.audit_svc.log(
            action=AuditAction.BOOK_CREATE.value,
            entity_type="Author",
            entity_id=created.author_id,
            username=actor_username,
            description=f"Added author '{created.name}'."
        )
        return created

    def get_author(self, author_id: int) -> Author:
        a = self.repo.get_by_id(author_id)
        if not a:
            raise EntityNotFoundError("Author", author_id)
        return a

    def get_or_create(self, name: str, actor_username: str = "librarian") -> Author:
        existing = self.repo.get_by_name(name)
        if existing:
            return existing
        return self.add_author(AuthorDTO(name=name), actor_username=actor_username)

    def list_authors(self, search: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[Author]:
        return self.repo.list_all(search=search, limit=limit, offset=offset)
