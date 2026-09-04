"""Publication Frequency Pattern Directory and Calculation Service."""

from typing import Dict, Optional, List
from .models import FrequencyPattern, FrequencyType


class PatternService:
    """Provides standard publication frequency definitions."""

    STANDARD_PATTERNS = {
        "m": FrequencyPattern("m", "Monthly", "12 issues/year", FrequencyType.MONTHLY, 12, 12, 1),
        "q": FrequencyPattern("q", "Quarterly", "4 issues/year", FrequencyType.QUARTERLY, 4, 4, 3),
        "w": FrequencyPattern("w", "Weekly", "52 issues/year", FrequencyType.WEEKLY, 52, 52, 0),
        "b": FrequencyPattern("b", "Bimonthly", "6 issues/year", FrequencyType.BIMONTHLY, 6, 6, 2),
        "a": FrequencyPattern("a", "Annual", "1 issue/year", FrequencyType.ANNUAL, 1, 1, 12),
        "s": FrequencyPattern("s", "Semiannual", "2 issues/year", FrequencyType.SEMIANNUAL, 2, 2, 6),
    }

    def get_pattern(self, code: str) -> Optional[FrequencyPattern]:
        return self.STANDARD_PATTERNS.get(code)
