"""Fund Accounting and Budget Allocation Service."""

from typing import Dict, List, Optional
from .models import Fund, FiscalYear


class BudgetService:
    """Tracks fund allocations, encumbrances, and expenditures."""

    def __init__(self):
        self.funds: Dict[str, Fund] = {}

    def create_fund(self, code: str, name: str, fiscal_year: str, allocation_cents: int) -> Fund:
        fund_id = f"FUND-{code}"
        fund = Fund(id=fund_id, code=code, name=name, fiscal_year_code=fiscal_year, allocated_amount_cents=allocation_cents)
        self.funds[fund_id] = fund
        return fund

    def encumber(self, fund_id: str, amount_cents: int) -> bool:
        fund = self.funds.get(fund_id)
        if not fund or fund.available_cents < amount_cents:
            return False
        fund.encumbered_cents += amount_cents
        return True

    def expend(self, fund_id: str, amount_cents: int) -> bool:
        fund = self.funds.get(fund_id)
        if not fund:
            return False
        # Release encumbrance and record expenditure
        fund.encumbered_cents = max(0, fund.encumbered_cents - amount_cents)
        fund.expended_cents += amount_cents
        return True

    def release_encumbrance(self, fund_id: str, amount_cents: int):
        fund = self.funds.get(fund_id)
        if fund:
            fund.encumbered_cents = max(0, fund.encumbered_cents - amount_cents)
