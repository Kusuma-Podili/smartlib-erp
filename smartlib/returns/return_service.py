"""Circulation desk check-in / return orchestrator."""
import datetime
from typing import Optional, Tuple
from smartlib.returns.models import ReturnRecord
from smartlib.returns.repository import ReturnRepository
from smartlib.returns.overdue_checker import OverdueChecker
from smartlib.borrowing.repository import BorrowingRepository
from smartlib.copies.repository import CopyRepository
from smartlib.copies.condition_evaluator import ConditionEvaluator
from smartlib.books.repository import BookRepository
from smartlib.members.repository import MemberRepository
from smartlib.memberships.repository import MembershipTierRepository
from smartlib.audit.audit_service import AuditService
from smartlib.constants import BorrowingStatus, BookCopyStatus, BookCopyCondition, AuditAction
from smartlib.errors import EntityNotFoundError, BusinessRuleViolationError

class ReturnService:
    def __init__(
        self,
        return_repo: Optional[ReturnRepository] = None,
        borrow_repo: Optional[BorrowingRepository] = None,
        copy_repo: Optional[CopyRepository] = None,
        book_repo: Optional[BookRepository] = None,
        member_repo: Optional[MemberRepository] = None,
        tier_repo: Optional[MembershipTierRepository] = None,
        audit_svc: Optional[AuditService] = None
    ):
        self.return_repo = return_repo or ReturnRepository()
        self.repo = self.return_repo
        self.borrow_repo = borrow_repo or BorrowingRepository()
        self.copy_repo = copy_repo or CopyRepository()
        self.book_repo = book_repo or BookRepository()
        self.member_repo = member_repo or MemberRepository()
        self.tier_repo = tier_repo or MembershipTierRepository()
        self.audit_svc = audit_svc or AuditService()

    def process_return(
        self,
        borrowing_id: int,
        return_date: Optional[str] = None,
        condition_on_return: str = BookCopyCondition.GOOD.value,
        librarian_id: Optional[int] = None,
        actor_username: str = "librarian"
    ) -> Tuple[ReturnRecord, float]:
        # 1. Retrieve loan record
        loan = self.borrow_repo.get_by_id(borrowing_id)
        if not loan:
            raise EntityNotFoundError("Borrowing record", borrowing_id)
        if loan.status == BorrowingStatus.RETURNED.value:
            raise BusinessRuleViolationError("ALREADY_RETURNED", f"Loan ID {borrowing_id} has already been returned.")

        ret_date = return_date or datetime.date.today().strftime("%Y-%m-%d")

        # 2. Member & Tier policy
        member = self.member_repo.get_by_id(loan.member_id)
        tier = self.tier_repo.get_by_type(member.membership_type) if member else None
        daily_rate = tier.daily_fine_rate if tier else 10.0
        grace_days = tier.grace_period_days if tier else 1

        # 3. Calculate overdue penalty
        late_days, has_fine = OverdueChecker.assess_overdue(loan.due_date, ret_date, grace_days)
        overdue_fine = (late_days * daily_rate) if has_fine else 0.0

        # 4. Physical condition & copy status routing
        copy_status, needs_maint = ConditionEvaluator.evaluate_return_condition(condition_on_return)
        self.copy_repo.update_status_and_condition(loan.copy_id, copy_status, condition_on_return)

        # 5. Update loan status to RETURNED
        self.borrow_repo.update_status(borrowing_id, BorrowingStatus.RETURNED.value)

        # 6. Recalculate book totals
        self.book_repo.update_copy_counts(loan.book_id)

        # 7. Record return transaction
        rec = ReturnRecord(
            borrowing_id=borrowing_id,
            returned_date=ret_date,
            received_by_librarian_id=librarian_id,
            overdue_days=late_days,
            fine_amount=overdue_fine,
            condition_on_return=condition_on_return
        )
        created_ret = self.return_repo.create(rec)

        self.audit_svc.log(
            action=AuditAction.BOOK_RETURN.value,
            entity_type="Return",
            entity_id=created_ret.return_id,
            username=actor_username,
            description=f"Returned copy {loan.copy_number} of '{loan.book_title}'. Overdue days: {late_days}, Fine: ${overdue_fine:.2f}."
        )

        return created_ret, overdue_fine
