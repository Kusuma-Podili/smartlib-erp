"""Fine assessment orchestrator."""
from typing import Optional, List
from smartlib.fines.models import Fine
from smartlib.fines.repository import FineRepository
from smartlib.fines.fine_calculator import FineCalculator
from smartlib.members.repository import MemberRepository
from smartlib.audit.audit_service import AuditService
from smartlib.constants import FineType, FineStatus, AuditAction
from smartlib.errors import EntityNotFoundError, ValidationError

class FineService:
    def __init__(
        self,
        fine_repo: Optional[FineRepository] = None,
        member_repo: Optional[MemberRepository] = None,
        audit_svc: Optional[AuditService] = None
    ):
        self.fine_repo = fine_repo or FineRepository()
        self.member_repo = member_repo or MemberRepository()
        self.audit_svc = audit_svc or AuditService()

    def assess_fine(
        self,
        member_id: int,
        amount: float,
        fine_type: str = FineType.OVERDUE.value,
        borrowing_id: Optional[int] = None,
        reason: Optional[str] = None,
        actor_username: str = "librarian"
    ) -> Fine:
        if amount <= 0:
            raise ValidationError("Fine amount must be greater than 0.", {"amount": "Positive value required."})

        member = self.member_repo.get_by_id(member_id)
        if not member:
            raise EntityNotFoundError("Member", member_id)

        fine = Fine(
            member_id=member_id,
            borrowing_id=borrowing_id,
            fine_type=fine_type,
            amount=amount,
            paid_amount=0.00,
            balance_amount=amount,
            status=FineStatus.UNPAID.value,
            reason=reason or f"Assessed {fine_type} penalty."
        )
        created = self.fine_repo.create(fine)

        self.audit_svc.log(
            action=AuditAction.FINE_CREATE.value,
            entity_type="Fine",
            entity_id=created.fine_id,
            username=actor_username,
            description=f"Assessed fine of ${amount:.2f} ({fine_type}) to patron {member.member_code}."
        )
        return self.fine_repo.get_by_id(created.fine_id)

    def waive_fine(self, fine_id: int, actor_username: str = "admin", reason: str = "Administrative waiver") -> Fine:
        fine = self.fine_repo.get_by_id(fine_id)
        if not fine:
            raise EntityNotFoundError("Fine", fine_id)

        self.fine_repo.update_balance_and_status(fine_id, fine.paid_amount, 0.00, FineStatus.WAIVED.value)
        self.audit_svc.log(
            action=AuditAction.FINE_WAIVE.value,
            entity_type="Fine",
            entity_id=fine_id,
            username=actor_username,
            description=f"Waived outstanding balance of ${fine.balance_amount:.2f} on fine #{fine_id}. Reason: {reason}."
        )
        return self.fine_repo.get_by_id(fine_id)

    def list_fines_by_member(self, member_id: int) -> List[Fine]:
        return self.fine_repo.list_by_member(member_id)

    def get_outstanding_balance(self, member_id: int) -> float:
        return self.fine_repo.get_total_outstanding_by_member(member_id)
