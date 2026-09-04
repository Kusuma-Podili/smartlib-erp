"""Cashier desk cashiering and receipt issuance service."""
from typing import Optional, List
from smartlib.payments.models import PaymentTransaction
from smartlib.payments.repository import PaymentRepository
from smartlib.payments.receipt_generator import ReceiptGenerator
from smartlib.fines.repository import FineRepository
from smartlib.audit.audit_service import AuditService
from smartlib.constants import FineStatus, PaymentMethod, AuditAction
from smartlib.errors import EntityNotFoundError, ValidationError

class PaymentService:
    def __init__(
        self,
        payment_repo: Optional[PaymentRepository] = None,
        fine_repo: Optional[FineRepository] = None,
        audit_svc: Optional[AuditService] = None
    ):
        self.payment_repo = payment_repo or PaymentRepository()
        self.repo = self.payment_repo
        self.fine_repo = fine_repo or FineRepository()
        self.audit_svc = audit_svc or AuditService()

    def process_payment(
        self,
        fine_id: int,
        amount: float,
        payment_method: str = PaymentMethod.CASH.value,
        librarian_id: Optional[int] = None,
        transaction_reference: Optional[str] = None,
        actor_username: str = "librarian"
    ) -> PaymentTransaction:
        fine = self.fine_repo.get_by_id(fine_id)
        if not fine:
            raise EntityNotFoundError("Fine", fine_id)
        if amount <= 0:
            raise ValidationError("Payment amount must be greater than 0.", {"amount": "Positive amount required."})
        if amount > fine.balance_amount:
            raise ValidationError(
                f"Payment amount (${amount:.2f}) exceeds outstanding balance (${fine.balance_amount:.2f}).",
                {"amount": "Overpayment not allowed."}
            )

        new_paid = round(fine.paid_amount + amount, 2)
        new_balance = round(fine.balance_amount - amount, 2)
        new_status = FineStatus.PAID.value if new_balance == 0 else FineStatus.PARTIALLY_PAID.value

        receipt_no = ReceiptGenerator.generate_receipt_number()

        payment = PaymentTransaction(
            fine_id=fine_id,
            member_id=fine.member_id,
            processed_by_librarian_id=librarian_id,
            amount=amount,
            payment_method=payment_method,
            receipt_number=receipt_no,
            transaction_reference=transaction_reference
        )
        created_payment = self.payment_repo.create(payment)

        # Update fine ledger balance
        self.fine_repo.update_balance_and_status(fine_id, new_paid, new_balance, new_status)

        self.audit_svc.log(
            action=AuditAction.FINE_PAYMENT.value,
            entity_type="Payment",
            entity_id=created_payment.payment_id,
            username=actor_username,
            description=f"Recorded payment of ${amount:.2f} ({payment_method}) for fine #{fine_id}. Receipt: {receipt_no}. Remaining balance: ${new_balance:.2f}."
        )

        return created_payment

    def list_member_payments(self, member_id: int) -> List[PaymentTransaction]:
        return self.payment_repo.list_by_member(member_id)
