"""Automated Nightly Maintenance Jobs for Library ERP."""

import datetime


def run_overdue_fines_job(circulation_service=None, fines_service=None):
    """Calculates daily overdue fine accruals for checked out items past their due date."""
    print(f"[{datetime.datetime.now().isoformat()}] Running Nightly Overdue Fines Accrual Job...")


def sweep_expired_reservations_job(reservation_service=None):
    """Cancels hold reservations that were not picked up within the 5-day hold shelf window."""
    print(f"[{datetime.datetime.now().isoformat()}] Sweeping Expired Shelf Hold Reservations...")
