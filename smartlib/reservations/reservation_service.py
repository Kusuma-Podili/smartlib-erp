"""Reservation hold queue coordinator. Assigns FIFO queue order and transitions holds on book return."""
import datetime
from typing import Optional, List
from smartlib.reservations.models import Reservation
from smartlib.reservations.repository import ReservationRepository
from smartlib.books.repository import BookRepository
from smartlib.members.repository import MemberRepository
from smartlib.audit.audit_service import AuditService
from smartlib.constants import ReservationStatus, AuditAction
from smartlib.errors import EntityNotFoundError, BusinessRuleViolationError, MembershipExpiredError
from smartlib.utilities.date_utils import add_days, today_iso

class ReservationService:
    def __init__(
        self,
        reserve_repo: Optional[ReservationRepository] = None,
        book_repo: Optional[BookRepository] = None,
        member_repo: Optional[MemberRepository] = None,
        audit_svc: Optional[AuditService] = None
    ):
        self.reserve_repo = reserve_repo or ReservationRepository()
        self.book_repo = book_repo or BookRepository()
        self.member_repo = member_repo or MemberRepository()
        self.audit_svc = audit_svc or AuditService()

    def reserve_book(self, member_id: int, book_id: int, actor_username: str = "member") -> Reservation:
        member = self.member_repo.get_by_id(member_id)
        if not member or not member.is_active():
            raise BusinessRuleViolationError("MEMBER_INACTIVE", "Inactive member cannot place reservations.")
        if member.is_expired():
            raise MembershipExpiredError(member.expiry_date)

        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise EntityNotFoundError("Book", book_id)

        # Rule 4: Prevent duplicate active reservations
        existing = self.reserve_repo.get_active_for_member_and_book(member_id, book_id)
        if existing:
            raise BusinessRuleViolationError(
                "DUPLICATE_RESERVATION",
                f"Member {member.member_code} already has an active reservation for '{book.title}' (Position #{existing.queue_position})."
            )

        # Assign FIFO queue position
        next_pos = self.reserve_repo.get_next_queue_position(book_id)
        res = Reservation(
            book_id=book_id,
            member_id=member_id,
            queue_position=next_pos,
            status=ReservationStatus.PENDING.value
        )
        created = self.reserve_repo.create(res)

        self.audit_svc.log(
            action=AuditAction.RESERVATION_CREATE.value,
            entity_type="Reservation",
            entity_id=created.reservation_id,
            username=actor_username,
            description=f"Patron {member.member_code} reserved '{book.title}'. Position: #{next_pos} in queue."
        )
        return self.reserve_repo.get_by_id(created.reservation_id)

    def cancel_reservation(self, reservation_id: int, member_id: int, actor_username: str = "member") -> Reservation:
        res = self.reserve_repo.get_by_id(reservation_id)
        if not res:
            raise EntityNotFoundError("Reservation", reservation_id)
        if res.member_id != member_id and actor_username != "librarian":
            raise BusinessRuleViolationError("UNAUTHORIZED", "Cannot cancel reservations of other patrons.")

        self.reserve_repo.update_status(reservation_id, ReservationStatus.CANCELLED.value)
        self.audit_svc.log(
            action=AuditAction.RESERVATION_CANCEL.value,
            entity_type="Reservation",
            entity_id=reservation_id,
            username=actor_username,
            description=f"Cancelled reservation #{reservation_id} for '{res.book_title}'."
        )
        return self.reserve_repo.get_by_id(reservation_id)

    def process_returned_book_holds(self, book_id: int, hold_days: int = 3) -> Optional[Reservation]:
        """Identify next waiting patron in queue, transition status to READY_FOR_PICKUP with hold expiry."""
        pending_queue = self.reserve_repo.list_pending_by_book(book_id)
        if not pending_queue:
            return None

        next_res = pending_queue[0]
        hold_expiry = add_days(today_iso(), hold_days)
        self.reserve_repo.update_status(
            next_res.reservation_id,
            ReservationStatus.READY_FOR_PICKUP.value,
            hold_expiry_date=hold_expiry
        )
        self.audit_svc.log(
            action="RESERVATION_READY",
            entity_type="Reservation",
            entity_id=next_res.reservation_id,
            username="SYSTEM",
            description=f"Copy arrived for reserved book '{next_res.book_title}'. Patron {next_res.member_code} notified. Hold valid until {hold_expiry}."
        )
        return self.reserve_repo.get_by_id(next_res.reservation_id)

    def list_member_reservations(self, member_id: int) -> List[Reservation]:
        return self.reserve_repo.list_by_member(member_id)
