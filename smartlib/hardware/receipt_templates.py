"""Circulation Receipt, Hold Slip, Transit Label, and Due Date Slips Formatter."""

import datetime
from typing import Dict, Any, List


class CirculationReceiptFormatter:
    """Generates ASCII and ESC/POS thermal receipts for circulation desk workflows."""

    LIBRARY_NAME = "SMARTLIB CENTRAL LIBRARY"
    LIBRARY_ADDRESS = "100 University Avenue, Academic Square"
    PHONE = "+1-555-0199"

    @classmethod
    def format_checkout_receipt(cls, member_name: str, member_number: str,
                                loans: List[Dict[str, Any]]) -> str:
        lines = [
            "================================================",
            f"{cls.LIBRARY_NAME:^48}",
            f"{cls.LIBRARY_ADDRESS:^48}",
            f"Tel: {cls.PHONE:^43}",
            "================================================",
            f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<20} Cashier: Self-Check 01",
            f"Patron: {member_name} ({member_number})",
            "------------------------------------------------",
            "ITEM CHECKOUT SUMMARY",
            "------------------------------------------------",
        ]
        for l in loans:
            title = l.get("title", "Book Title")[:35]
            barcode = l.get("barcode", "BC-000000")
            due = l.get("due_date", "2026-09-18")
            lines.append(f"Title: {title}")
            lines.append(f"Barcode: {barcode:<20} DUE: {due:>15}")
            lines.append("")

        lines.extend([
            "------------------------------------------------",
            f"Total Items Checked Out: {len(loans)}",
            "Please return or renew items before due date.",
            "Online renewal available at: http://localhost:8000",
            "================================================",
            f"{'THANK YOU FOR VISITING!':^48}",
            "================================================"
        ])
        return "\n".join(lines)

    @classmethod
    def format_return_receipt(cls, member_name: str, returns: List[Dict[str, Any]]) -> str:
        lines = [
            "================================================",
            f"{cls.LIBRARY_NAME:^48}",
            "               CHECKIN RECEIPT                  ",
            "================================================",
            f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Patron: {member_name}",
            "------------------------------------------------",
            "RETURNED ITEMS:",
        ]
        for r in returns:
            title = r.get("title", "Item Title")[:35]
            barcode = r.get("barcode", "BC-000000")
            status = r.get("status", "Returned - On Time")
            lines.append(f"Title: {title}")
            lines.append(f"Barcode: {barcode:<20} Status: {status}")
        lines.extend([
            "------------------------------------------------",
            f"Total Returned: {len(returns)}",
            "All returned items cleared from active borrowing.",
            "================================================"
        ])
        return "\n".join(lines)

    @classmethod
    def format_fine_payment_receipt(cls, receipt_number: str, member_name: str,
                                    amount_cents: int, payment_method: str) -> str:
        amount_fmt = f"₹{amount_cents / 100:.2f}"
        lines = [
            "================================================",
            f"{cls.LIBRARY_NAME:^48}",
            "            OFFICIAL PAYMENT RECEIPT            ",
            "================================================",
            f"Receipt No: {receipt_number}",
            f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Patron: {member_name}",
            f"Payment Method: {payment_method.upper()}",
            "------------------------------------------------",
            f"Amount Paid: {amount_fmt:>34}",
            f"Remaining Outstanding Dues: {'₹0.00':>19}",
            "------------------------------------------------",
            "Payment Status: CLEARED AND RECORDED",
            "Thank you for clearing your library dues.",
            "================================================"
        ]
        return "\n".join(lines)

    @classmethod
    def format_hold_pickup_slip(cls, patron_name: str, patron_card: str,
                                title: str, barcode: str, expire_date: str) -> str:
        lines = [
            "************************************************",
            "          HOLD SHELF PICKUP SLIP                ",
            "************************************************",
            f"Hold Recipient: {patron_name}",
            f"Card Number: {patron_card}",
            "------------------------------------------------",
            f"Title: {title}",
            f"Item Barcode: {barcode}",
            "------------------------------------------------",
            f"HOLD EXPIRES ON: {expire_date}",
            "Item will be released to next patron if not",
            "collected by the expiration date.",
            "************************************************"
        ]
        return "\n".join(lines)
