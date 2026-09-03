"""
Comprehensive Test Suite 4 (Part C): Fine Engine & Cashier Payments
Assessment of overdue fines, lost/damage fees, payment processing, and serialized receipt numbering.
"""

import unittest
from tests.conftest import BaseTestCase
from smartlib.members.member_service import MemberService
from smartlib.members.models import MemberDTO
from smartlib.fines.fine_service import FineService
from smartlib.fines.fine_calculator import FineCalculator
from smartlib.payments.payment_service import PaymentService
from smartlib.constants import FineType, FineStatus, PaymentMethod
from smartlib.errors import ValidationError

class TestFinesAndPayments(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.member_svc = MemberService()
        self.fine_svc = FineService()
        self.payment_svc = PaymentService()

        self.member = self.member_svc.register_member(
            MemberDTO(first_name="Charles", last_name="Babbage", email="babbage@engine.org")
        )

    def test_fine_calculation_formulas(self):
        """Verify overdue penalty, lost replacement multiplier, and damage assessment formulas."""
        # 5 overdue days * $10/day = $50.00
        late_fine = FineCalculator.calculate_overdue_fine(5, 10.00)
        self.assertEqual(late_fine, 50.00)

        # $60 book * 1.5 multiplier = $90.00
        lost_charge = FineCalculator.calculate_lost_book_charge(60.00, multiplier=1.5)
        self.assertEqual(lost_charge, 90.00)

        # $80 book * 50% damage fee = $40.00
        damaged_charge = FineCalculator.calculate_damaged_book_charge(80.00, damage_percentage=0.50)
        self.assertEqual(damaged_charge, 40.00)

    def test_fine_assessment_and_payment_receipt_issuance(self):
        """Verify fine creation, partial payment, full payment, and serialized receipt numbering."""
        # 1. Assess $50 fine
        fine = self.fine_svc.assess_fine(
            member_id=self.member.member_id,
            amount=50.00,
            fine_type=FineType.OVERDUE.value,
            reason="5 days overdue on textbook"
        )
        self.assertEqual(fine.amount, 50.00)
        self.assertEqual(fine.balance_amount, 50.00)
        self.assertEqual(fine.status, FineStatus.UNPAID.value)

        # 2. Check member total outstanding
        outstanding = self.fine_svc.get_outstanding_balance(self.member.member_id)
        self.assertEqual(outstanding, 50.00)

        # 3. Process partial payment ($20 via CASH)
        p1 = self.payment_svc.process_payment(
            fine_id=fine.fine_id,
            amount=20.00,
            payment_method=PaymentMethod.CASH.value
        )
        self.assertTrue(p1.receipt_number.startswith("REC-"))
        self.assertEqual(p1.amount, 20.00)

        # Check updated fine balance ($30 remaining, PARTIALLY_PAID)
        updated_fine1 = self.fine_svc.fine_repo.get_by_id(fine.fine_id)
        self.assertEqual(updated_fine1.balance_amount, 30.00)
        self.assertEqual(updated_fine1.status, FineStatus.PARTIALLY_PAID.value)

        # 4. Overpayment rejection
        with self.assertRaises(ValidationError):
            self.payment_svc.process_payment(fine_id=fine.fine_id, amount=40.00)

        # 5. Settle remaining $30 via UPI
        p2 = self.payment_svc.process_payment(
            fine_id=fine.fine_id,
            amount=30.00,
            payment_method=PaymentMethod.UPI.value
        )
        self.assertNotEqual(p1.receipt_number, p2.receipt_number)

        # Check final fine balance ($0, PAID)
        final_fine = self.fine_svc.fine_repo.get_by_id(fine.fine_id)
        self.assertEqual(final_fine.balance_amount, 0.00)
        self.assertEqual(final_fine.status, FineStatus.PAID.value)
        self.assertEqual(self.fine_svc.get_outstanding_balance(self.member.member_id), 0.00)

    def test_fine_waiver(self):
        """Verify administrative fine waiver zeroes balance and marks status WAIVED."""
        fine = self.fine_svc.assess_fine(self.member.member_id, amount=25.00)
        waived = self.fine_svc.waive_fine(fine.fine_id, actor_username="admin", reason="Good patron standing waiver")
        self.assertEqual(waived.status, FineStatus.WAIVED.value)
        self.assertEqual(waived.balance_amount, 0.00)

if __name__ == "__main__":
    unittest.main()
