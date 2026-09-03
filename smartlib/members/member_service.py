"""Business logic orchestrating patron registration, profile maintenance, and eligibility."""
import datetime
from typing import Optional, List, Tuple
from smartlib.members.models import Member, MemberDTO
from smartlib.members.repository import MemberRepository
from smartlib.members.id_generator import MemberIdGenerator
from smartlib.users.user_service import UserService
from smartlib.users.models import UserDTO
from smartlib.validation.validators import validate_email, validate_phone
from smartlib.audit.audit_service import AuditService
from smartlib.constants import UserRole, MembershipStatus, MembershipType, AuditAction
from smartlib.errors import ValidationError, DuplicateEntityError, EntityNotFoundError

class MemberService:
    def __init__(
        self,
        member_repo: Optional[MemberRepository] = None,
        user_service: Optional[UserService] = None,
        audit_svc: Optional[AuditService] = None
    ):
        self.member_repo = member_repo or MemberRepository()
        self.user_service = user_service or UserService()
        self.audit_svc = audit_svc or AuditService()

    def register_member(self, dto: MemberDTO, actor_username: str = "librarian") -> Member:
        clean_email = validate_email(dto.email)
        clean_phone = validate_phone(dto.phone)
        if not dto.first_name or not dto.first_name.strip():
            raise ValidationError("First name is required.", {"first_name": "Required."})
        if not dto.last_name or not dto.last_name.strip():
            raise ValidationError("Last name is required.", {"last_name": "Required."})

        if self.member_repo.get_by_email(clean_email):
            raise DuplicateEntityError("Member", "email", clean_email)

        # Create or link user account for Member portal login
        user_password = dto.password or "Member@123"
        username = clean_email.split("@")[0].lower()
        if len(username) < 3:
            username = f"user_{username}"
        # Guarantee unique username
        existing_user = self.user_service.repo.get_by_username(username)
        if existing_user:
            username = f"{username}_{datetime.date.today().year}"

        user = self.user_service.register_user(
            UserDTO(
                username=username,
                email=clean_email,
                password=user_password,
                role=UserRole.MEMBER.value
            ),
            actor_username=actor_username
        )

        member_code = MemberIdGenerator.generate_next_code()
        today = datetime.date.today()
        expiry = today + datetime.timedelta(days=dto.duration_days)

        member = Member(
            user_id=user.user_id,
            member_code=member_code,
            first_name=dto.first_name.strip(),
            last_name=dto.last_name.strip(),
            email=clean_email,
            phone=clean_phone,
            address=dto.address,
            membership_type=dto.membership_type.upper(),
            registration_date=today.strftime("%Y-%m-%d"),
            expiry_date=expiry.strftime("%Y-%m-%d"),
            status=MembershipStatus.ACTIVE.value,
            notes=dto.notes
        )
        created = self.member_repo.create(member)

        self.audit_svc.log(
            action="MEMBER_REGISTER",
            entity_type="Member",
            entity_id=created.member_id,
            username=actor_username,
            description=f"Registered patron '{created.full_name}' ({member_code})."
        )
        return created

    def get_member(self, member_id: int) -> Member:
        m = self.member_repo.get_by_id(member_id)
        if not m:
            raise EntityNotFoundError("Member", member_id)
        return m

    def get_by_user_id(self, user_id: int) -> Member:
        m = self.member_repo.get_by_user_id(user_id)
        if not m:
            raise EntityNotFoundError("Member for User ID", user_id)
        return m

    def get_by_code(self, member_code: str) -> Member:
        m = self.member_repo.get_by_member_code(member_code)
        if not m:
            raise EntityNotFoundError("Member with code", member_code)
        return m

    def set_member_status(self, member_id: int, status: str, actor_username: str = "librarian") -> Member:
        m = self.get_member(member_id)
        old_status = m.status
        self.member_repo.update_status(member_id, status.upper())
        self.audit_svc.log(
            action=AuditAction.USER_STATUS_CHANGE.value,
            entity_type="Member",
            entity_id=member_id,
            username=actor_username,
            description=f"Changed member {m.member_code} status from {old_status} to {status.upper()}."
        )
        return self.get_member(member_id)

    def search(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        membership_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[Member], int]:
        return self.member_repo.search_members(query, status, membership_type, limit, offset)
