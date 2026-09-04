"""
Production-grade WSGI Web Application & Interactive Portals for SmartLibrary ERP.
Pure Python standard library (wsgiref, http.cookies, urllib.parse).
"""

import json
import urllib.parse
import http.cookies
import datetime
from wsgiref.simple_server import make_server
from typing import Dict, Any, Tuple, Optional, List

from smartlib.database.connection import DatabaseManager
from smartlib.database.migrations import MigrationManager
from smartlib.database.seeder import DatabaseSeeder

from smartlib.authentication.session_manager import SessionManager
from smartlib.authentication.auth_service import AuthService
from smartlib.users.user_service import UserService
from smartlib.analytics.dashboard_metrics import DashboardMetrics
from smartlib.analytics.trends_analyzer import TrendsAnalyzer
from smartlib.reports.report_service import ReportService
from smartlib.books.book_service import BookService
from smartlib.copies.copy_service import CopyService
from smartlib.authors.author_service import AuthorService
from smartlib.categories.category_service import CategoryService
from smartlib.publishers.publisher_service import PublisherService
from smartlib.members.member_service import MemberService
from smartlib.memberships.tier_service import MembershipTierService
from smartlib.borrowing.issue_service import IssueService
from smartlib.returns.return_service import ReturnService
from smartlib.renewals.renewal_service import RenewalService
from smartlib.reservations.reservation_service import ReservationService
from smartlib.fines.fine_service import FineService
from smartlib.payments.payment_service import PaymentService
from smartlib.notifications.notification_service import NotificationService
from smartlib.announcements.announcement_service import AnnouncementService
from smartlib.audit.audit_service import AuditService
from smartlib.settings.settings_service import SettingsService

from smartlib.constants import UserRole
from smartlib.web.css import APP_CSS
from smartlib.web.admin_views import AdminViews
from smartlib.web.librarian_views import LibrarianViews
from smartlib.web.member_views import MemberViews

class ApplicationServer:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.migrator = MigrationManager(self.db_manager)
        self.migrator.apply_initial_schema()
        self.seeder = DatabaseSeeder(self.db_manager)
        self.seeder.seed_all(include_demo=True)

        self.session_mgr = SessionManager()
        self.auth_svc = AuthService(session_mgr=self.session_mgr)
        self.user_svc = UserService()
        self.metrics = DashboardMetrics()
        self.trends = TrendsAnalyzer()
        self.reports = ReportService()
        self.book_svc = BookService()
        self.copy_svc = CopyService()
        self.author_svc = AuthorService()
        self.category_svc = CategoryService()
        self.publisher_svc = PublisherService()
        self.member_svc = MemberService()
        self.tier_svc = MembershipTierService()
        self.issue_svc = IssueService()
        self.return_svc = ReturnService()
        self.renew_svc = RenewalService()
        self.reserve_svc = ReservationService()
        self.fine_svc = FineService()
        self.payment_svc = PaymentService()
        self.notif_svc = NotificationService()
        self.announce_svc = AnnouncementService()
        self.audit_svc = AuditService()
        self.settings_svc = SettingsService()

        # View Controllers
        self.admin_views = AdminViews(self)
        self.librarian_views = LibrarianViews(self)
        self.member_views = MemberViews(self)

    def get_current_user(self, environ: dict) -> Optional[dict]:
        cookie_header = environ.get("HTTP_COOKIE", "")
        if not cookie_header:
            return None
        cookie = http.cookies.SimpleCookie(cookie_header)
        session_cookie = cookie.get("smartlib_session")
        if not session_cookie:
            return None
        try:
            return self.session_mgr.validate_session(session_cookie.value)
        except Exception:
            return None

    def parse_body(self, environ: dict) -> dict:
        try:
            length = int(environ.get("CONTENT_LENGTH", "0"))
        except ValueError:
            length = 0
        if length <= 0:
            return {}
        raw = environ["wsgi.input"].read(length).decode("utf-8")
        parsed = urllib.parse.parse_qs(raw)
        return {k: v[0].strip() for k, v in parsed.items()}

    def parse_query(self, environ: dict) -> dict:
        qs = environ.get("QUERY_STRING", "")
        parsed = urllib.parse.parse_qs(qs)
        return {k: v[0].strip() for k, v in parsed.items()}

    def redirect(self, start_response, path: str, msg: str = "", msg_type: str = "success"):
        query = ""
        if msg:
            query = f"?msg={urllib.parse.quote(msg)}&msg_type={msg_type}"
        start_response("302 Found", [("Location", path + query)])
        return [b""]

    def __call__(self, environ: dict, start_response: Any):
        path = environ.get("PATH_INFO", "/")
        method = environ.get("REQUEST_METHOD", "GET").upper()
        current_user = self.get_current_user(environ)

        # Public routes
        if path == "/":
            return self.handle_home(environ, start_response, current_user)
        elif path == "/login":
            return self.handle_login(environ, start_response, method, current_user)
        elif path == "/logout":
            return self.handle_logout(environ, start_response)

        # Auth Guard
        if not current_user:
            return self.redirect(start_response, "/login")

        role = current_user.get("role")

        # Admin Portal
        if path.startswith("/admin"):
            if role != UserRole.ADMIN.value:
                return self.redirect(start_response, f"/{role.lower()}/dashboard", "Access denied. Admin portal restricted.", "error")
            return self.admin_views.handle_request(environ, start_response, path, method, current_user)

        # Librarian Portal
        elif path.startswith("/librarian"):
            if role not in (UserRole.LIBRARIAN.value, UserRole.ADMIN.value):
                return self.redirect(start_response, f"/{role.lower()}/dashboard", "Access denied. Librarian portal restricted.", "error")
            return self.librarian_views.handle_request(environ, start_response, path, method, current_user)

        # Member Portal
        elif path.startswith("/member"):
            return self.member_views.handle_request(environ, start_response, path, method, current_user)

        # 404
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"404 Not Found"]

    def handle_home(self, environ, start_response, current_user):
        if current_user:
            role = current_user.get("role", "MEMBER").lower()
            return self.redirect(start_response, f"/{role}/dashboard")

        kpis = self.metrics.get_summary_kpis()
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SmartLibrary ERP - Enterprise Library Portal</title>
    <style>{APP_CSS}</style>
</head>
<body>
    <header class="navbar">
        <a href="/" class="navbar-brand">&#128218; SmartLibrary ERP</a>
        <div class="navbar-user">
            <a href="/login" class="btn btn-sm">Sign In to Portal</a>
        </div>
    </header>
    <main class="main-content" style="max-width: 1200px; margin: 0 auto;">
        <div style="text-align: center; margin: 3rem 0;">
            <h1 style="font-size: 2.6rem; color: var(--primary); margin-bottom: 0.75rem;">SmartLibrary ERP System</h1>
            <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 650px; margin: 0 auto 2rem;">
                Enterprise Library Resource Planning System in Pure Python.
            </p>
            <div style="display: flex; justify-content: center; gap: 1rem;">
                <a href="/login" class="btn" style="font-size: 1.1rem; padding: 0.85rem 2rem;">Access System Portal &rarr;</a>
            </div>
        </div>

        <div class="grid-4">
            <div class="kpi-card">
                <div class="kpi-title">Catalog Titles</div>
                <div class="kpi-value">{kpis['total_books']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Physical Copies</div>
                <div class="kpi-value">{kpis['total_copies']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Available Copies</div>
                <div class="kpi-value" style="color: var(--success);">{kpis['available_copies']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Active Patrons</div>
                <div class="kpi-value">{kpis['total_members']}</div>
            </div>
        </div>

        <div class="card">
            <h2>Unified Role-Based Architecture</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.25rem;">
                <div style="background: #f8fafc; padding: 1.25rem; border-radius: 8px; border-left: 4px solid #dc2626;">
                    <h3 style="color: #991b1b; font-size: 1.1rem; margin-bottom: 0.5rem;">&#128104;&#8205;&#128188; ADMIN DASHBOARD</h3>
                    <p style="font-size: 0.88rem; color: #475569; margin-bottom: 0.75rem;">
                        <strong>Controls the entire library:</strong> Users + Books + Employees + Reports + Settings + Audits.
                    </p>
                    <div style="font-size: 0.85rem; background: white; padding: 0.6rem; border-radius: 4px; border: 1px solid var(--border);">
                        <strong>Credentials:</strong><br>
                        Email: <code>admin@library.com</code><br>
                        Password: <code>Admin@123</code>
                    </div>
                </div>

                <div style="background: #f8fafc; padding: 1.25rem; border-radius: 8px; border-left: 4px solid #d97706;">
                    <h3 style="color: #92400e; font-size: 1.1rem; margin-bottom: 0.5rem;">&#128105;&#8205;&#128188; EMPLOYEE / LIBRARIAN DASHBOARD</h3>
                    <p style="font-size: 0.88rem; color: #475569; margin-bottom: 0.75rem;">
                        <strong>Runs daily operations:</strong> Members + Books + Issues + Returns + Renewals + Fines + Cashier.
                    </p>
                    <div style="font-size: 0.85rem; background: white; padding: 0.6rem; border-radius: 4px; border: 1px solid var(--border);">
                        <strong>Credentials:</strong><br>
                        Email: <code>librarian@library.com</code><br>
                        Password: <code>Librarian@123</code>
                    </div>
                </div>

                <div style="background: #f8fafc; padding: 1.25rem; border-radius: 8px; border-left: 4px solid #16a34a;">
                    <h3 style="color: #166534; font-size: 1.1rem; margin-bottom: 0.5rem;">&#128104;&#8205;&#127891; MEMBER DASHBOARD</h3>
                    <p style="font-size: 0.88rem; color: #475569; margin-bottom: 0.75rem;">
                        <strong>Uses the library:</strong> Search + Borrow + Reserve Holds + Self-Renew + Pay Fines Online.
                    </p>
                    <div style="font-size: 0.85rem; background: white; padding: 0.6rem; border-radius: 4px; border: 1px solid var(--border);">
                        <strong>Credentials:</strong><br>
                        Email: <code>member@library.com</code><br>
                        Password: <code>Member@123</code>
                    </div>
                </div>
            </div>
        </div>
    </main>
</body>
</html>'''
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [html.encode("utf-8")]

    def handle_login(self, environ, start_response, method, current_user):
        error_msg = ""
        if method == "POST":
            params = self.parse_body(environ)
            username = params.get("username", "")
            password = params.get("password", "")
            try:
                auth_result = self.auth_svc.authenticate(
                    username_or_email=username,
                    password=password,
                    ip_address=environ.get("REMOTE_ADDR")
                )
                token = auth_result["session_token"]
                redirect_url = auth_result["redirect_url"]

                cookie = http.cookies.SimpleCookie()
                cookie["smartlib_session"] = token
                cookie["smartlib_session"]["path"] = "/"
                cookie["smartlib_session"]["httponly"] = True

                headers = [
                    ("Location", redirect_url),
                    ("Set-Cookie", cookie.output(header=""))
                ]
                start_response("302 Found", headers)
                return [b""]
            except Exception as e:
                error_msg = str(e)

        error_html = f'<div class="alert alert-error">{error_msg}</div>' if error_msg else ""
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sign In - SmartLibrary ERP</title>
    <style>{APP_CSS}</style>
</head>
<body style="display: flex; align-items: center; justify-content: center; height: 100vh;">
    <div style="width: 100%; max-width: 440px; padding: 2rem;" class="card">
        <h1 style="font-size: 1.5rem; color: var(--primary); text-align: center; margin-bottom: 0.35rem;">&#128218; SmartLibrary ERP</h1>
        <p style="text-align: center; font-size: 0.88rem; color: var(--text-muted); margin-bottom: 1.5rem;">Sign In to your role portal</p>
        {error_html}
        <form method="POST" action="/login">
            <div class="form-group">
                <label for="username">Username or Email</label>
                <input type="text" id="username" name="username" required autofocus placeholder="admin@library.com">
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required placeholder="••••••••">
            </div>
            <button type="submit" class="btn" style="width: 100%; margin-top: 0.75rem; padding: 0.75rem; font-size: 1rem;">Sign In</button>
        </form>
        <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid var(--border); font-size: 0.82rem; color: var(--text-muted);">
            <strong>Demo Accounts:</strong><br>
            - Admin: <code>admin@library.com</code> / <code>Admin@123</code><br>
            - Librarian: <code>librarian@library.com</code> / <code>Librarian@123</code><br>
            - Member: <code>member@library.com</code> / <code>Member@123</code>
        </div>
    </div>
</body>
</html>'''
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [html.encode("utf-8")]

    def handle_logout(self, environ, start_response):
        cookie_header = environ.get("HTTP_COOKIE", "")
        if cookie_header:
            cookie = http.cookies.SimpleCookie(cookie_header)
            session_cookie = cookie.get("smartlib_session")
            if session_cookie:
                self.auth_svc.logout(session_cookie.value)

        cookie = http.cookies.SimpleCookie()
        cookie["smartlib_session"] = ""
        cookie["smartlib_session"]["path"] = "/"
        cookie["smartlib_session"]["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"

        headers = [
            ("Location", "/login"),
            ("Set-Cookie", cookie.output(header=""))
        ]
        start_response("302 Found", headers)
        return [b""]


def create_app():
    return ApplicationServer()
