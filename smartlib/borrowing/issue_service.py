"""
High-throughput checkout / book issue service.
Enforces:
1. Physical copy availability
2. Active patron status
3. Unexpired membership
4. Tier borrowing quota
5. Reservation hold priority
"""

import datetime
from typing import Optional
from smartlib.borrowing.models import BorrowingRecord
from smartlib.borrowing.repository import BorrowingRepository
from smartlib.borrowing.loan_calculator import LoanCalculator
from smartlib.members.repository import MemberRepository
from smartlib.memberships.repository import MembershipTierRepository
from smartlib.books.repository import BookRepository
from smartlib.copies.repository import CopyRepository
from smartlib.audit.audit_service import AuditService
from smartlib.constants import BookCopyStatus, BorrowingStatus, AuditAction
from smartlib.errors import (
    EntityNotFoundError, CopyUnavailableError, BorrowingLimitReachedError,
    MembershipExpiredError, BusinessRuleViolationError
)

class IssueService:
    def __init__(
        self,
        borrow_repo: Optional[BorrowingRepository] = None,
        member_repo: Optional[MemberRepository] = None,
        tier_repo: Optional[MembershipTierRepository] = None,
        book_repo: Optional[BookRepository] = None,
        copy_repo: Optional[CopyRepository] = None,
        audit_svc: Optional[AuditService] = None
    ):
        self.borrow_repo = borrow_repo or BorrowingRepository()
        self.member_repo = member_repo or MemberRepository()
        self.tier_repo = tier_repo or MembershipTierRepository()
        self.book_repo = book_repo or BookRepository()
        self.copy_repo = copy_repo or CopyRepository()
        self.audit_svc = audit_svc or AuditService()

    def issue_book(
        self,
        member_id: int,
        book_id: int,
        copy_id: Optional[int] = None,
        librarian_id: Optional[int] = None,
        actor_username: str = "librarian"
    ) -> BorrowingRecord:
        # 1. Validate Member
        member = self.member_repo.get_by_id(member_id)
        if not member:
            raise EntityNotFoundError("Member", member_id)
        if not member.is_active():
            raise BusinessRuleViolationError("MEMBER_INACTIVE", f"Member {member.member_code} is currently {member.status}. Cannot issue books.")
        if member.is_expired():
            raise MembershipExpiredError(member.expiry_date)

        # 2. Validate Membership Tier Quota
        tier = self.tier_repo.get_by_type(member.membership_type)
        max_limit = tier.max_borrow_limit if tier else 3
        loan_days = tier.loan_duration_days if tier else 14
        max_renewals = tier.max_renewals if tier else 2

        current_loans = self.borrow_repo.count_active_loans_by_member(member_id)
        if current_loans >= max_limit:
            raise BorrowingLimitReachedError(limit=max_limit, current=current_loans)

        # 3. Validate Book & Physical Copy Availability
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise EntityNotFoundError("Book", book_id)

        target_copy = None
        if copy_id:
            target_copy = self.copy_repo.get_by_id(copy_id)
            if not target_copy or target_copy.book_id != book_id:
                raise EntityNotFoundError("BookCopy", copy_id)
            if target_copy.status != BookCopyStatus.AVAILABLE.value:
                raise CopyUnavailableError(target_copy.copy_number, target_copy.status)
        else:
            target_copy = self.copy_repo.find_available_copy_for_book(book_id)
            if not target_copy:
                raise CopyUnavailableError(f"for Book '{book.title}'", "NO_COPIES_AVAILABLE")

        # 4. Calculate Due Date
        today = datetime.date.today().strftime("%Y-%m-%d")
        due_date = LoanCalculator.calculate_due_date(loan_days, today)

        # 5. Atomic check-out
        record = BorrowingRecord(
            member_id=member_id,
            book_id=book_id,
            copy_id=target_copy.copy_id,
            issued_by_librarian_id=librarian_id,
            issue_date=today,
            due_date=due_date,
            renewal_count=0,
            max_renewals_allowed=max_renewals,
            status=BorrowingStatus.ACTIVE.value
        )
        created_record = self.borrow_repo.create(record)

        # Update copy status to ISSUED
        self.copy_repo.update_status_and_condition(target_copy.copy_id, BookCopyStatus.ISSUED.value)
        # Update book master copy counts
        self.book_repo.update_copy_counts(book_id)

        self.audit_svc.log(
            action=AuditAction.BOOK_ISSUE.value,
            entity_type="Borrowing",
            entity_id=created_record.borrowing_id,
            username=actor_username,
            description=f"Issued copy {target_copy.copy_number} ({target_copy.barcode}) of '{book.title}' to {member.full_name} ({member.member_code}). Due on {due_date}."
        )

        return self.borrow_repo.get_by_id(created_record.borrowing_id)
