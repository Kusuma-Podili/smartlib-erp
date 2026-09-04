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

    def test_admin_reports_and_analytics_views(self):
        """Verify rendering of all Reports & Analytics subtabs in web presentation layer."""
        from smartlib.web.admin_reports import render_admin_reports_and_analytics
        class DummyApp:
            def __init__(self, db, metrics):
                self.db_manager = db
                self.metrics = metrics

        dummy_app = DummyApp(self.db_manager, self.metrics)

        # 1. Analytics tab
        html_analytics = render_admin_reports_and_analytics(dummy_app, {"subtab": "analytics"})
        self.assertIn("Monthly Borrowing Trends", html_analytics)
        self.assertIn("Issue vs Return Comparison", html_analytics)
        self.assertIn("Most Borrowed Books", html_analytics)
        self.assertIn("Book Availability Analysis", html_analytics)
        self.assertIn("Member Activity", html_analytics)
        self.assertIn("Fine Collection Trends", html_analytics)
        self.assertIn("₹", html_analytics)

        # 2. Inventory tab
        html_inv = render_admin_reports_and_analytics(dummy_app, {"subtab": "inventory"})
        self.assertIn("Catalog Master Inventory", html_inv)
        self.assertIn("Books by Category", html_inv)
        self.assertIn("Books by Author", html_inv)
        self.assertIn("Books by Publisher", html_inv)
        self.assertIn("₹", html_inv)

        # 3. Overdue tab
        html_overdue = render_admin_reports_and_analytics(dummy_app, {"subtab": "overdue"})
        self.assertIn("Overdue Circulation Ledger", html_overdue)
        self.assertIn("Filter by Member", html_overdue)
        self.assertIn("₹", html_overdue)

        # 4. Financial tab
        html_fin = render_admin_reports_and_analytics(dummy_app, {"subtab": "financial"})
        self.assertIn("Fine Collections & Financial Ledger", html_fin)
        self.assertIn("Total Fines Generated", html_fin)
        self.assertIn("₹", html_fin)

if __name__ == "__main__":
    unittest.main()

