"""Physical condition inspection evaluator."""
from typing import Tuple
from smartlib.constants import BookCopyCondition, BookCopyStatus

class ConditionEvaluator:
    @staticmethod
    def evaluate_return_condition(condition: str) -> Tuple[str, bool]:
        c = condition.upper()
        if c in (BookCopyCondition.NEW.value, BookCopyCondition.EXCELLENT.value, BookCopyCondition.GOOD.value, BookCopyCondition.FAIR.value):
            return BookCopyStatus.AVAILABLE.value, False
        elif c == BookCopyCondition.POOR.value:
            return BookCopyStatus.IN_MAINTENANCE.value, True
        elif c == BookCopyCondition.DAMAGED.value:
            return BookCopyStatus.DAMAGED.value, True
        return BookCopyStatus.AVAILABLE.value, False
