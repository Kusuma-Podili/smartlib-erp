"""Attribute-Based Access Control (ABAC) Policy Engine."""

from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


class Role(Enum):
    ADMIN = "admin"
    LIBRARIAN = "librarian"
    CATALOGER = "cataloger"
    ACQUISITIONS = "acquisitions"
    MEMBER = "member"
    GUEST = "guest"


class AbacDecision(Enum):
    PERMIT = "permit"
    DENY = "deny"


@dataclass
class AbacRequest:
    subject_role: Role
    subject_id: str
    action: str
    resource_type: str
    resource_owner_id: Optional[str] = None


class AbacPolicyEngine:
    """Evaluates security access requests against granular role matrices."""

    ROLE_PERMISSIONS = {
        Role.ADMIN: ["*"],
        Role.LIBRARIAN: [
            "books:*", "copies:*", "loans:*", "returns:*", "renewals:*",
            "reservations:*", "fines:assess", "fines:collect", "fines:waive",
            "members:read", "members:create", "reports:read"
        ],
        Role.CATALOGER: [
            "books:*", "authors:*", "categories:*", "publishers:*", "copies:*"
        ],
        Role.ACQUISITIONS: [
            "acquisitions:*", "vendors:*", "funds:*", "purchase_orders:*"
        ],
        Role.MEMBER: [
            "books:read", "copies:read", "reservations:create", "renewals:create",
            "loans:read_self", "fines:read_self", "fines:pay_self"
        ],
        Role.GUEST: [
            "books:read", "copies:read"
        ]
    }

    @classmethod
    def evaluate(cls, req: AbacRequest) -> AbacDecision:
        if req.subject_role == Role.ADMIN:
            return AbacDecision.PERMIT

        allowed = cls.ROLE_PERMISSIONS.get(req.subject_role, [])
        action_key = f"{req.resource_type}:{req.action}"

        for perm in allowed:
            if perm == "*":
                return AbacDecision.PERMIT
            if perm == f"{req.resource_type}:*":
                return AbacDecision.PERMIT
            if perm == action_key:
                return AbacDecision.PERMIT

        # Self-ownership check for patron reading own loans or paying fines
        if req.action.endswith("_self"):
            if req.subject_id == req.resource_owner_id:
                return AbacDecision.PERMIT

        return AbacDecision.DENY
