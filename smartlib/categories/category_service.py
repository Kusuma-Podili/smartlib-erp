"""
Category management service.
"""

from typing import Optional, List
from smartlib.categories.models import Category, CategoryDTO
from smartlib.categories.repository import CategoryRepository
from smartlib.audit.audit_service import AuditService
from smartlib.errors import ValidationError, DuplicateEntityError, EntityNotFoundError

class CategoryService:
    def __init__(self, repo: Optional[CategoryRepository] = None, audit_svc: Optional[AuditService] = None):
        self.repo = repo or CategoryRepository()
        self.audit_svc = audit_svc or AuditService()

    def add_category(self, dto: CategoryDTO, actor_username: str = "librarian") -> Category:
        if not dto.code or not dto.code.strip():
            raise ValidationError("Category code is required.", {"code": "Required field."})
        if not dto.name or not dto.name.strip():
            raise ValidationError("Category name is required.", {"name": "Required field."})

        code_clean = dto.code.strip().upper()
        if self.repo.get_by_code(code_clean):
            raise DuplicateEntityError("Category", "code", code_clean)

        cat = Category(
            code=code_clean,
            name=dto.name.strip(),
            dewey_decimal_class=dto.dewey_decimal_class,
            parent_category_id=dto.parent_category_id,
            description=dto.description
        )
        created = self.repo.create(cat)
        self.audit_svc.log(
            action="CATEGORY_CREATE",
            entity_type="Category",
            entity_id=created.category_id,
            username=actor_username,
            description=f"Created category '{created.name}' ({created.code})."
        )
        return created

    def get_category(self, category_id: int) -> Category:
        c = self.repo.get_by_id(category_id)
        if not c:
            raise EntityNotFoundError("Category", category_id)
        return c

    def get_or_create(self, code: str, name: str, actor_username: str = "librarian") -> Category:
        existing = self.repo.get_by_code(code)
        if existing:
            return existing
        return self.add_category(CategoryDTO(code=code, name=name), actor_username=actor_username)

    def list_categories(self) -> List[Category]:
        return self.repo.list_all()
