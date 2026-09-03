"""Notification message formatter templates."""

class NotificationTemplateEngine:
    @staticmethod
    def book_due_reminder(title: str, due_date: str) -> str:
        return f"Reminder: Your borrowed book '{title}' is due for return on {due_date}."

    @staticmethod
    def overdue_alert(title: str, overdue_days: int, current_fine: float) -> str:
        return f"OVERDUE NOTICE: '{title}' is {overdue_days} days overdue. Accumulated fine: ${current_fine:.2f}."

    @staticmethod
    def reservation_available(title: str, hold_expiry_date: str) -> str:
        return f"Hold Ready: '{title}' is now available for pick-up at Circulation Desk 1 until {hold_expiry_date}."

    @staticmethod
    def membership_expiring(expiry_date: str) -> str:
        return f"Your library membership will expire on {expiry_date}. Please visit the circulation desk to renew."

    @staticmethod
    def fine_generated(amount: float, reason: str) -> str:
        return f"A fine of ${amount:.2f} was assessed to your account. Reason: {reason}."

    @staticmethod
    def payment_confirmation(amount: float, receipt_no: str) -> str:
        return f"Payment confirmation: Received ${amount:.2f}. Receipt #{receipt_no}."
