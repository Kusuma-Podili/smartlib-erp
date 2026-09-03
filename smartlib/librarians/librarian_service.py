"""
Business logic for managing librarian staff.
"""

from typing import Optional, List
from smartlib.librarians.models import Librarian
from smartlib.librarians.repository import LibrarianRepository
from smartlib.users.user_service import UserService
from smartlib.users.models import UserDTO
from smartlib.constants import UserRole

class LibrarianService:
    def __init__(self, repo: Optional[LibrarianRepository] = None, user_service: Optional[UserService] = None):
        self.repo = repo or LibrarianRepository()
        self.user_service = user_service or UserService()

    def register_librarian(
        self,
        username: str,
        email: str,
        password: str,
        employee_code: str,
        full_name: str,
        phone: Optional[str] = None,
        department: str = "Circulation Services",
        shift: str = "Morning",
        desk_location: str = "Circulation Desk 1",
        actor_username: str = "admin"
    ) -> Librarian:
        user_dto = UserDTO(
            username=username,
            email=email,
            password=password,
            role=UserRole.LIBRARIAN.value
        )
        user = self.user_service.register_user(user_dto, actor_username=actor_username)
        lib = Librarian(
            user_id=user.user_id,
            employee_code=employee_code,
            full_name=full_name,
            phone=phone,
            department=department,
            shift=shift,
            desk_location=desk_location
        )
        return self.repo.create(lib)

    def get_by_user_id(self, user_id: int) -> Optional[Librarian]:
        return self.repo.get_by_user_id(user_id)

    def list_librarians(self) -> List[Librarian]:
        return self.repo.list_all()
