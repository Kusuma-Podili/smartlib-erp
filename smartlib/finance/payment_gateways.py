"""Payment Gateway Adapters for online fine settlement."""

from typing import Dict, Any, Optional
import uuid
import datetime


class MockStripeGateway:
    """Simulates Stripe Charges and Webhooks."""

    @staticmethod
    def process_charge(amount_cents: int, currency: str = "INR", token: str = "tok_visa") -> Dict[str, Any]:
        charge_id = f"ch_{uuid.uuid4().hex[:24]}"
        return {
            "id": charge_id,
            "status": "succeeded",
            "amount": amount_cents,
            "currency": currency,
            "paid": True,
            "created": int(datetime.datetime.now().timestamp())
        }


class MockCashierTill:
    """Simulates physical cashier drawer receipt."""

    @staticmethod
    def record_cash(amount_cents: int, patron_id: str) -> Dict[str, Any]:
        receipt_num = f"RCPT-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        return {
            "receipt_number": receipt_num,
            "amount_cents": amount_cents,
            "patron_id": patron_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "PAID_CASH"
        }


class PaymentGatewayRegistry:
    """Central registry of active library payment gateways."""

    def __init__(self):
        self.gateways = {
            "stripe": MockStripeGateway,
            "cash": MockCashierTill
        }

    def get_gateway(self, name: str):
        return self.gateways.get(name.lower())
