"""Data repository for membership tier definitions."""
from typing import Optional, List
from smartlib.database.connection import DatabaseManager
from smartlib.memberships.models import MembershipTier

class MembershipTierRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def get_by_type(self, tier_type: str) -> Optional[MembershipTier]:
        sql = """
        SELECT tier_id, tier_type, name, max_borrow_limit, loan_duration_days,
               grace_period_days, max_renewals, daily_fine_rate, description, created_at
        FROM membership_tiers WHERE UPPER(tier_type) = UPPER(?);
        """
        row = self.db_manager.fetch_one(sql, (tier_type.strip(),))
        return MembershipTier(**dict(row)) if row else None

    def list_all(self) -> List[MembershipTier]:
        sql = """
        SELECT tier_id, tier_type, name, max_borrow_limit, loan_duration_days,
               grace_period_days, max_renewals, daily_fine_rate, description, created_at
        FROM membership_tiers ORDER BY tier_id ASC;
        """
        rows = self.db_manager.fetch_all(sql)
        return [MembershipTier(**dict(r)) for r in rows]

    def update_tier(self, tier: MembershipTier) -> None:
        sql = """
        UPDATE membership_tiers
        SET max_borrow_limit = ?, loan_duration_days = ?, grace_period_days = ?,
            max_renewals = ?, daily_fine_rate = ?, description = ?
        WHERE tier_id = ?;
        """
        self.db_manager.execute(
            sql,
            (
                tier.max_borrow_limit, tier.loan_duration_days, tier.grace_period_days,
                tier.max_renewals, tier.daily_fine_rate, tier.description, tier.tier_id
            )
        )
        self.db_manager.get_connection().commit()
