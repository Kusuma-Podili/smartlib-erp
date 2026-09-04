"""Financial Report Generator: Balance Sheet, Trial Balance, and Profit & Loss."""

from typing import Dict, Any, List
from .models import AccountType, NormalBalance
from .ledger_service import GeneralLedgerService


class FinancialReportGenerator:
    """Generates standard accounting statements from the General Ledger."""

    def __init__(self, ledger: GeneralLedgerService):
        self.ledger = ledger

    def generate_trial_balance(self) -> Dict[str, Any]:
        rows = []
        tot_deb = 0
        tot_cred = 0
        for code, acct in sorted(self.ledger.accounts.items()):
            if acct.balance_cents == 0:
                continue
            deb = acct.balance_cents if acct.normal_balance == NormalBalance.DEBIT else 0
            cred = acct.balance_cents if acct.normal_balance == NormalBalance.CREDIT else 0
            tot_deb += deb
            tot_cred += cred
            rows.append({
                "code": code,
                "name": acct.name,
                "type": acct.account_type.value,
                "debit_cents": deb,
                "credit_cents": cred
            })
        return {
            "report_name": "Trial Balance",
            "is_balanced": tot_deb == tot_cred,
            "total_debit_cents": tot_deb,
            "total_credit_cents": tot_cred,
            "rows": rows
        }

    def generate_income_statement(self) -> Dict[str, Any]:
        """Profit & Loss Statement (Revenue - Expenses)."""
        revenues = []
        expenses = []
        tot_rev = 0
        tot_exp = 0

        for code, acct in sorted(self.ledger.accounts.items()):
            if acct.account_type == AccountType.REVENUE:
                tot_rev += acct.balance_cents
                revenues.append({"code": code, "name": acct.name, "amount_cents": acct.balance_cents})
            elif acct.account_type == AccountType.EXPENSE:
                tot_exp += acct.balance_cents
                expenses.append({"code": code, "name": acct.name, "amount_cents": acct.balance_cents})

        net_surplus = tot_rev - tot_exp
        return {
            "report_name": "Statement of Revenues and Expenses (Income Statement)",
            "total_revenue_cents": tot_rev,
            "total_expense_cents": tot_exp,
            "net_surplus_deficit_cents": net_surplus,
            "revenues": revenues,
            "expenses": expenses
        }

    def generate_balance_sheet(self) -> Dict[str, Any]:
        """Balance Sheet (Assets = Liabilities + Fund Balances)."""
        assets = []
        liabilities = []
        equity = []
        tot_assets = 0
        tot_liabilities = 0
        tot_equity = 0

        for code, acct in sorted(self.ledger.accounts.items()):
            if acct.account_type == AccountType.ASSET:
                tot_assets += acct.balance_cents
                assets.append({"code": code, "name": acct.name, "amount_cents": acct.balance_cents})
            elif acct.account_type == AccountType.LIABILITY:
                tot_liabilities += acct.balance_cents
                liabilities.append({"code": code, "name": acct.name, "amount_cents": acct.balance_cents})
            elif acct.account_type == AccountType.EQUITY:
                tot_equity += acct.balance_cents
                equity.append({"code": code, "name": acct.name, "amount_cents": acct.balance_cents})

        return {
            "report_name": "Balance Sheet",
            "total_assets_cents": tot_assets,
            "total_liabilities_cents": tot_liabilities,
            "total_equity_cents": tot_equity,
            "assets": assets,
            "liabilities": liabilities,
            "equity": equity
        }
