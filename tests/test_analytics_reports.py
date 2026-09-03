"""
Comprehensive Test Suite 5 (Part A): Executive Analytics, Reports,
Notifications, Announcements & Settings.
"""

import unittest
from tests.conftest import BaseTestCase
from smartlib.analytics.dashboard_metrics import DashboardMetrics
from smartlib.analytics.trends_analyzer import TrendsAnalyzer
from smartlib.reports.report_service import ReportService
from smartlib.notifications.notification_service import NotificationService
from smartlib.announcements.announcement_service import AnnouncementService
from smartlib.settings.settings_service import SettingsService
from smartlib.constants import AnnouncementPriority

class TestAnalyticsAndReports(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.metrics = DashboardMetrics()
        self.trends = TrendsAnalyzer()
        self.report_svc = ReportService()
        self.notif_svc = NotificationService()
        self.announce_svc = AnnouncementService()
        self.settings_svc = SettingsService()

    def test_dashboard_kpi_summary_generation(self):
        """Verify KPI aggregation from live database records."""
        kpis = self.metrics.get_summary_kpis()
        self.assertIn("total_books", kpis)
        self.assertIn("total_members", kpis)
        self.assertIn("available_copies", kpis)
        self.assertIn("total_fines", kpis)
        self.assertIn("collected_fines", kpis)
        # Default seeded data has 1 member
        self.assertTrue(kpis["total_members"] >= 1)

    def test_report_service_csv_exports(self):
        """Verify CSV export generation for inventory, overdue loans, and financial ledger."""
        # Inventory Report
        inv = self.report_svc.generate_books_inventory_report()
        self.assertIn("ISBN", inv["headers"])
        self.assertIn("csv", inv)

        # Overdue Report
        od = self.report_svc.generate_overdue_report()
        self.assertIn("Due Date", od["headers"])

        # Financial Ledger Report
        fin = self.report_svc.generate_financial_ledger_report()
        self.assertIn("Assessed", fin["headers"])

    def test_notification_delivery_and_read_state(self):
        """Verify notification creation, retrieval, and read state transition."""
        n = self.notif_svc.send_notification(
            user_id=1,
            title="Book Due Reminder",
            message="Your book is due tomorrow."
        )
        self.assertIsNotNone(n.notification_id)
        self.assertFalse(n.is_read)

        # List unread
        unread = self.notif_svc.get_user_notifications(user_id=1, unread_only=True)
        self.assertTrue(any(item.notification_id == n.notification_id for item in unread))

        # Mark read
        self.notif_svc.mark_read(n.notification_id, user_id=1)
        unread_after = self.notif_svc.get_user_notifications(user_id=1, unread_only=True)
        self.assertFalse(any(item.notification_id == n.notification_id for item in unread_after))

    def test_announcement_publishing_and_priority(self):
        """Verify announcement publishing and ordering by priority."""
        self.announce_svc.publish_announcement(
            creator_user_id=1,
            title="Library Holiday Notice",
            content="The library will be closed on Monday for Labor Day.",
            priority=AnnouncementPriority.HIGH.value
        )
        active = self.announce_svc.list_active_announcements()
        self.assertTrue(len(active) >= 1)
        self.assertEqual(active[0].title, "Library Holiday Notice")

    def test_system_settings_runtime_configuration(self):
        """Verify dynamic retrieval and modification of system rules and policies."""
        val = self.settings_svc.get_setting_value("default_fine_per_day")
        self.assertEqual(val, "10.00")

        # Update setting
        self.settings_svc.update_setting("default_fine_per_day", "15.00")
        updated_val = self.settings_svc.get_setting_value("default_fine_per_day")
        self.assertEqual(updated_val, "15.00")

if __name__ == "__main__":
    unittest.main()
