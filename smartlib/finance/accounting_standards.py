"""GAAP and GASB Standard Financial Reporting Rules for Public & Academic Libraries.

Defines compliance formulas, ratio calculations, and fiscal year closeout policies.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class FinancialRatioMetric:
    name: str
    formula: str
    benchmark_minimum: float
    description: str


LIBRARY_FINANCIAL_RATIOS: Dict[str, FinancialRatioMetric] = {
    "current_ratio": FinancialRatioMetric("Current Ratio", "Total Current Assets / Total Current Liabilities", 1.5, "Measures short-term debt solvency"),
    "cash_ratio": FinancialRatioMetric("Cash Ratio", "Cash & Equivalents / Total Current Liabilities", 0.5, "Strict liquidity measure"),
    "acquisitions_ratio": FinancialRatioMetric("Acquisitions Spending Ratio", "Collection Expenditures / Total Operating Budget", 0.15, "Percentage of operating budget dedicated to books, serials, and digital resources"),
    "fine_collection_rate": FinancialRatioMetric("Fine Collection Realization Rate", "Collected Fines / Assessed Fines", 0.70, "Efficiency of overdue and lost book fine recovery"),
    "program_expense_ratio": FinancialRatioMetric("Patron Program Expense Ratio", "Public Program Expenses / Total Expenditures", 0.08, "Direct patron community service spend ratio")
}

def calculate_current_ratio(current_assets_cents: int, current_liabilities_cents: int) -> float:
    if current_liabilities_cents <= 0:
        return 999.99
    return round(current_assets_cents / current_liabilities_cents, 2)

def calculate_collection_realization(collected_cents: int, assessed_cents: int) -> float:
    if assessed_cents <= 0:
        return 1.0
    return round(collected_cents / assessed_cents, 4)
