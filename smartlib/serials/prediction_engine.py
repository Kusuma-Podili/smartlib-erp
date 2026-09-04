"""Serials Prediction Engine for computing expected future issue instances."""

from typing import List
import datetime
from .models import Subscription, IssueInstance, IssueStatus, FrequencyType
from .pattern_service import PatternService


class SerialsPredictionEngine:
    """Calculates upcoming issue arrivals and enumerations."""

    def __init__(self, pattern_service: PatternService):
        self.pattern_service = pattern_service

    def predict_next_issues(self, subscription: Subscription, frequency_code: str,
                            current_volume: int, current_issue: int, count: int = 12) -> List[IssueInstance]:
        pattern = self.pattern_service.get_pattern(frequency_code)
        if not pattern:
            return []

        predicted: List[IssueInstance] = []
        vol = current_volume
        iss = current_issue
        current_date = subscription.start_date

        for i in range(count):
            iss += 1
            if iss > pattern.issues_per_volume:
                vol += 1
                iss = 1

            if pattern.frequency_type == FrequencyType.MONTHLY:
                # Add 1 month
                month = (current_date.month % 12) + 1
                year = current_date.year + (1 if current_date.month == 12 else 0)
                current_date = datetime.date(year, month, min(current_date.day, 28))
            elif pattern.frequency_type == FrequencyType.QUARTERLY:
                month = current_date.month + 3
                year = current_date.year
                if month > 12:
                    month -= 12
                    year += 1
                current_date = datetime.date(year, month, min(current_date.day, 28))
            elif pattern.frequency_type == FrequencyType.WEEKLY:
                current_date = current_date + datetime.timedelta(days=7)
            else:
                current_date = current_date + datetime.timedelta(days=30)

            issue_id = f"ISS-{subscription.id}-V{vol:02d}N{iss:02d}"
            inst = IssueInstance(
                id=issue_id,
                subscription_id=subscription.id,
                volume_number=str(vol),
                issue_number=str(iss),
                enumeration=f"Vol. {vol}, No. {iss}",
                chronology=current_date.strftime("%B %Y"),
                expected_date=current_date,
                status=IssueStatus.EXPECTED
            )
            predicted.append(inst)

        return predicted
