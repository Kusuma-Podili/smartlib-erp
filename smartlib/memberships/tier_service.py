"""Service managing membership tiers and privilege lookups."""
from typing import Optional, List
from smartlib.memberships.models import MembershipTier
from smartlib.memberships.repository import MembershipTierRepository
from smartlib.memberships.policies import DEFAULT_POLICIES
from smartlib.errors import EntityNotFoundError

class MembershipTierService:
    def __init__(self, repo: Optional[MembershipTierRepository] = None):
        self.repo = repo or MembershipTierRepository()

    def get_tier(self, tier_type: str) -> MembershipTier:
        tier = self.repo.get_by_type(tier_type)
        if not tier:
            raise EntityNotFoundError("MembershipTier", tier_type)
        return tier

    def list_tiers(self) -> List[MembershipTier]:
        return self.repo.list_all()

    def update_limits(
        self,
        tier_type: str,
        max_borrow_limit: int,
        loan_duration_days: int,
        grace_period_days: int,
        daily_fine_rate: float
    ) -> MembershipTier:
        tier = self.get_tier(tier_type)
        tier.max_borrow_limit = max_borrow_limit
        tier.loan_duration_days = loan_duration_days
        tier.grace_period_days = grace_period_days
        tier.daily_fine_rate = daily_fine_rate
        self.repo.update_tier(tier)
        return tier
