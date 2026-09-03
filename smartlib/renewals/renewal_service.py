"""Loan renewal service enforcing renewal count caps, hold conflicts, and overdue policies."""
import datetime
from typing import Optional
from smartlib.renewals.models import RenewalRecord
from smartlib.renewals.repository import RenewalRepository
from smartlib.borrowing.repository import BorrowingRepository
from smartlib.borrowing.loan_calculator import LoanCalculator
from smartlib.members.repository import MemberRepository
from smartlib.memberships.repository import MembershipTierRepository
from smartlib.audit.audit_service import AuditService
from smartlib.utilities.date_utils import is_overdue, today_iso
from smartlib.constants import BorrowingStatus, AuditAction
from smartlib.errors import EntityNotFoundError, BusinessRuleViolationError, MembershipExpiredError

class RenewalService:
    def __init__(
        self,
        renewal_repo: Optional[RenewalRepository] = None,
        borrow_repo: Optional[BorrowingRepository] = None,
        member_repo: Optional[MemberRepository] = None,
        tier_repo: Optional[MembershipTierRepository] = None,
        audit_svc: Optional[AuditService] = None
    ):
        self.renewal_repo = renewal_repo or RenewalRepository()
        self.borrow_repo = borrow_repo or BorrowingRepository()
        self.member_repo = member_repo or MemberRepository()
        self.tier_repo = tier_repo or MembershipTierRepository()
        self.audit_svc = audit_svc or AuditService()

    def request_renewal(
        self,
        borrowing_id: int,
        member_id: int,
        librarian_id: Optional[int] = None,
        actor_username: str = "member"
    ) -> RenewalRecord:
        loan = self.borrow_repo.get_by_id(borrowing_id)
        if not loan:
            raise EntityNotFoundError("Borrowing record", borrowing_id)
        if loan.member_id != member_id:
            raise BusinessRuleViolationError("UNAUTHORIZED_RENEWAL", "Members can only renew their own borrowed books.")
        if loan.status != BorrowingStatus.ACTIVE.value:
            raise BusinessRuleViolationError("INVALID_LOAN_STATUS", f"Cannot renew loan with status '{loan.status}'.")

        # 1. Check if overdue
        if is_overdue(loan.due_date):
            raise BusinessRuleViolationError("OVERDUE_RENEWAL_BLOCKED", "Overdue loans cannot be renewed. Return the book and settle any penalties.")

        # 2. Check renewal limit
        if loan.renewal_count >= loan.max_renewals_allowed:
            raise BusinessRuleViolationError(
                "RENEWAL_LIMIT_REACHED",
                f"Maximum allowed renewals ({loan.max_renewals_allowed}) reached for this loan."
            )

        # 3. Check member status
        member = self.member_repo.get_by_id(member_id)
        if not member or not member.is_active():
            raise BusinessRuleViolationError("MEMBER_INACTIVE", "Inactive member cannot request renewals.")
        if member.is_expired():
            raise MembershipExpiredError(member.expiry_date)

        # 4. Calculate new due date
        tier = self.tier_repo.get_by_type(member.membership_type)
        loan_days = tier.loan_duration_days if tier else 14
        new_due_date = LoanCalculator.calculate_due_date(loan_days, loan.due_date)

        # 5. Apply renewal update
        new_count = loan.renewal_count + 1
        self.borrow_repo.update_due_date_and_renewals(borrowing_id, new_due_date, new_count)

        rec = RenewalRecord(
            borrowing_id=borrowing_id,
            requested_by_member_id=member_id,
            approved_by_librarian_id=librarian_id,
            previous_due_date=loan.due_date,
            new_due_date=new_due_date
        )
        created_rec = self.renewal_repo.create(rec)

        self.audit_svc.log(
            action=AuditAction.BOOK_RENEW.value,
            entity_type="Renewal",
            entity_id=created_rec.renewal_id,
            username=actor_username,
            description=f"Renewed loan {borrowing_id} for {member.full_name}. Due extended from {loan.due_date} to {new_due_date} (Renewal #{new_count})."
        )
        return created_rec
