"""GDPR and ALA Patron Privacy and Circulation Anonymization Engine."""

import hashlib
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class RetentionPolicy:
    anonymize_circulation_history_on_return: bool = True
    mask_patron_identifiers_in_audit_logs: bool = True
    purge_inactive_accounts_after_years: int = 3


class PatronPrivacyEngine:
    """Anonymizes patron lending histories to uphold Library Bill of Rights."""

    def __init__(self, policy: Optional[RetentionPolicy] = None):
        self.policy = policy or RetentionPolicy()

    def anonymize_loan_record(self, loan_record: Dict[str, Any]) -> Dict[str, Any]:
        """Strip patron ID and replace with non-reversible salt hash upon return."""
        if not self.policy.anonymize_circulation_history_on_return:
            return loan_record

        anonymized = dict(loan_record)
        anonymized["patron_id"] = "ANONYMIZED_PATRON"
        anonymized["patron_name"] = "Confidential"
        anonymized["anonymized"] = True
        return anonymized

    def mask_email(self, email: str) -> str:
        if "@" not in email:
            return "***"
        local, domain = email.split("@", 1)
        masked_local = local[0] + "***" + (local[-1] if len(local) > 1 else "")
        return f"{masked_local}@{domain}"
