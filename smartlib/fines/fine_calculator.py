"""Automated fine calculation formulas."""

class FineCalculator:
    @staticmethod
    def calculate_overdue_fine(overdue_days: int, daily_rate: float) -> float:
        """Multiply late days by daily fine rate."""
        if overdue_days <= 0:
            return 0.00
        return round(float(overdue_days * daily_rate), 2)

    @staticmethod
    def calculate_lost_book_charge(replacement_price: float, multiplier: float = 1.5) -> float:
        """Charge book replacement price with institutional procurement multiplier."""
        return round(float(replacement_price * multiplier), 2)

    @staticmethod
    def calculate_damaged_book_charge(replacement_price: float, damage_percentage: float = 0.50) -> float:
        """Assess repair charge based on percentage of catalog replacement cost."""
        return round(float(replacement_price * damage_percentage), 2)
