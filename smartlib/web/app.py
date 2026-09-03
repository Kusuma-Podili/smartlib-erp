"""
Production-grade WSGI Web Server & Interactive Portals for SmartLibrary ERP.
Pure Python standard library (wsgiref, http.cookies, urllib.parse).
Features:
- Authentication & Login portal with session cookies
- Automatic post-login role detection and redirect
- Admin Dashboard with live KPI cards, audit logs, and catalog metrics
- Librarian Circulation Desk for issuing, returning, catalog search, and fines
- Member Self-Service Portal with active loans, renewals, search, and notifications
"""

import urllib.parse
import http.cookies
from wsgiref.simple_server import make_server
from typing import Dict, Any, Tuple, Optional

from smartlib.authentication.session_manager import SessionManager
from smartlib.authentication.auth_service import AuthService
from smartlib.analytics.dashboard_metrics import DashboardMetrics
from smartlib.analytics.trends_analyzer import TrendsAnalyzer
from smartlib.books.book_service import BookService
from smartlib.books.models import BookFilter
from smartlib.copies.copy_service import CopyService
from smartlib.members.member_service import MemberService
from smartlib.borrowing.issue_service import IssueService
from smartlib.returns.return_service import ReturnService
from smartlib.renewals.renewal_service import RenewalService
from smartlib.fines.fine_service import FineService
from smartlib.payments.payment_service import PaymentService
from smartlib.notifications.notification_service import NotificationService
from smartlib.announcements.announcement_service import AnnouncementService
from smartlib.audit.audit_service import AuditService
from smartlib.database.migrations import MigrationManager
from smartlib.database.seeder import DatabaseSeeder
from smartlib.constants import UserRole, PaymentMethod

# Base CSS theme
THEME_CSS = """
:root {
    --primary: #1e3a8a;
    --primary-hover: #1d4ed8;
    --secondary: #0f766e;
    --bg-main: #f1f5f9;
    --bg-card: #ffffff;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --border: #cbd5e1;
    --success: #16a34a;
    --warning: #d97706;
    --danger: #dc2626;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg-main); color: var(--text-main); line-height: 1.5; }
header { background: var(--primary); color: white; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
header h1 { font-size: 1.3rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; }
header nav { display: flex; align-items: center; gap: 1.25rem; }
header nav a { color: white; text-decoration: none; font-size: 0.95rem; font-weight: 500; }
header nav a:hover { text-decoration: underline; }
.container { max-width: 1200px; margin: 2rem auto; padding: 0 1.5rem; }
.grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem; margin-bottom: 2rem; }
.kpi-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.kpi-title { font-size: 0.85rem; text-transform: uppercase; color: var(--text-muted); font-weight: 600; }
.kpi-value { font-size: 1.8rem; font-weight: 700; color: var(--primary); margin-top: 0.25rem; }
.card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 1.5rem; }
.card h2 { font-size: 1.2rem; margin-bottom: 1rem; color: var(--text-main); border-bottom: 2px solid var(--bg-main); padding-bottom: 0.5rem; }
table { width: 100%; border-collapse: collapse; margin-top: 0.75rem; }
th, td { text-align: left; padding: 0.75rem; border-bottom: 1px solid var(--border); font-size: 0.9rem; }
th { background: #f8fafc; color: var(--text-muted); font-weight: 600; }
.badge { display: inline-block; padding: 0.2rem 0.55rem; border-radius: 4px; font-size: 0.75rem; font-weight: 700; }
.badge-admin { background: #fee2e2; color: #991b1b; }
.badge-librarian { background: #fef3c7; color: #92400e; }
.badge-member { background: #dcfce7; color: #166534; }
.badge-avail { background: #dcfce7; color: #166534; }
.badge-issued { background: #e0e7ff; color: #3730a3; }
.badge-overdue { background: #fee2e2; color: #991b1b; }
.btn { display: inline-block; background: var(--primary); color: white; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; font-size: 0.9rem; font-weight: 500; border: none; cursor: pointer; }
.btn:hover { background: var(--primary-hover); }
.btn-sm { padding: 0.25rem 0.6rem; font-size: 0.8rem; }
.btn-success { background: var(--success); }
.btn-secondary { background: var(--text-muted); }
.alert { padding: 0.75rem 1rem; border-radius: 6px; margin-bottom: 1rem; font-size: 0.9rem; }
.alert-error { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }
.alert-success { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
form .form-group { margin-bottom: 1rem; }
form label { display: block; font-size: 0.85rem; font-weight: 600; color: var(--text-main); margin-bottom: 0.25rem; }
form input, form select, form textarea { width: 100%; padding: 0.55rem 0.75rem; border: 1px solid var(--border); border-radius: 6px; font-size: 0.95rem; }
footer { text-align: center; padding: 2rem; color: var(--text-muted); font-size: 0.85rem; border-top: 1px solid var(--border); margin-top: 3rem; }
"""

def render_html_page(title: str, content: str, user: Optional[dict] = None) -> str:
    user_nav = ""
    if user:
        role_badge = f'<span class="badge badge-{user["role"].lower()}">{user["role"]}</span>'
        user_nav = f"""
            <span>Logged in as: <strong>{user.get("username")}</strong> ({role_badge})</span>
            <a href="/logout">Sign Out</a>
        """
    else:
        user_nav = '<a href="/login" class="btn btn-sm">Sign In</a>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - SmartLibrary ERP</title>
    <style>{THEME_CSS}</style>
</head>
<body>
    <header>
        <h1>📚 SmartLibrary ERP</h1>
        <nav>{user_nav}</nav>
    </header>
    <main class="container">
        {content}
    </main>
    <footer>
        &copy; 2026 SmartLibrary ERP &bull; Enterprise Library Resource Planning System &bull; Pure Python 3.10+
    </footer>
</body>
</html>"""

class ApplicationServer:
    def __init__(self):
        # Database initialization & migrations
        self.migrator = MigrationManager()
        self.migrator.apply_initial_schema()
        self.seeder = DatabaseSeeder()
        self.seeder.seed_all()

        # Core Services
        self.session_mgr = SessionManager()
        self.auth_svc = AuthService(session_mgr=self.session_mgr)
        self.metrics = DashboardMetrics()
        self.trends = TrendsAnalyzer()
        self.book_svc = BookService()
        self.copy_svc = CopyService()
        self.member_svc = MemberService()
        self.issue_svc = IssueService()
        self.return_svc = ReturnService()
        self.renew_svc = RenewalService()
        self.fine_svc = FineService()
        self.payment_svc = PaymentService()
        self.notif_svc = NotificationService()
        self.announce_svc = AnnouncementService()
        self.audit_svc = AuditService()

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

    def __call__(self, environ: dict, start_response: Any):
        path = environ.get("PATH_INFO", "/")
        method = environ.get("REQUEST_METHOD", "GET").upper()
        current_user = self.get_current_user(environ)

        # Route Dispatcher
        if path == "/":
            return self.handle_home(environ, start_response, current_user)
        elif path == "/login":
            return self.handle_login(environ, start_response, method, current_user)
        elif path == "/logout":
            return self.handle_logout(environ, start_response)
        elif path.startswith("/admin"):
            return self.handle_admin(environ, start_response, path, current_user)
        elif path.startswith("/librarian"):
            return self.handle_librarian(environ, start_response, path, current_user)
        elif path.startswith("/member"):
            return self.handle_member(environ, start_response, path, current_user)
        else:
            return self.handle_not_found(start_response)

    def handle_home(self, environ, start_response, current_user):
        if current_user:
            role = current_user.get("role", "MEMBER").upper()
            dest = f"/{role.lower()}/dashboard"
            start_response("302 Found", [("Location", dest)])
            return [b""]

        kpis = self.metrics.get_summary_kpis()
        content = f"""
        <div style="text-align: center; margin: 3rem 0;">
            <h1 style="font-size: 2.5rem; color: var(--primary); margin-bottom: 0.75rem;">Enterprise Library Resource Planning</h1>
            <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 650px; margin: 0 auto 2rem;">
                A unified pure Python platform managing catalog inventory, circulation desk operations, 
                patron memberships, automated reservation queues, and financial fine collections.
            </p>
            <div style="display: flex; justify-content: center; gap: 1rem;">
                <a href="/login" class="btn" style="font-size: 1.05rem; padding: 0.75rem 1.75rem;">Access System Portal &rarr;</a>
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
            <h2>Quick Demo Credentials (Pre-seeded)</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem;">
                <div style="background: #f8fafc; padding: 1rem; border-radius: 6px; border-left: 4px solid #dc2626;">
                    <strong>System Administrator</strong><br>
                    Email: <code>admin@library.com</code><br>
                    Password: <code>Admin@123</code><br>
                    <small>Full administrative oversight & rule configuration</small>
                </div>
                <div style="background: #f8fafc; padding: 1rem; border-radius: 6px; border-left: 4px solid #d97706;">
                    <strong>Circulation Librarian</strong><br>
                    Email: <code>librarian@library.com</code><br>
                    Password: <code>Librarian@123</code><br>
                    <small>Checkouts, checkins, barcodes, fine cashier</small>
                </div>
                <div style="background: #f8fafc; padding: 1rem; border-radius: 6px; border-left: 4px solid #16a34a;">
                    <strong>Patron / Member</strong><br>
                    Email: <code>member@library.com</code><br>
                    Password: <code>Member@123</code><br>
                    <small>Catalog search, loan tracking, hold reservations</small>
                </div>
            </div>
        </div>
        """
        html = render_html_page("Welcome", content, current_user)
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [html.encode("utf-8")]

    def handle_login(self, environ, start_response, method, current_user):
        error_msg = ""
        if method == "POST":
            try:
                length = int(environ.get("CONTENT_LENGTH", "0"))
            except ValueError:
                length = 0
            body = environ["wsgi.input"].read(length).decode("utf-8")
            params = urllib.parse.parse_qs(body)
            username = params.get("username", [""])[0].strip()
            password = params.get("password", [""])[0].strip()

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
        content = f"""
        <div style="max-width: 420px; margin: 3rem auto;" class="card">
            <h2>Sign In to SmartLibrary ERP</h2>
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
                <button type="submit" class="btn" style="width: 100%; margin-top: 0.5rem; padding: 0.75rem;">Sign In</button>
            </form>
            <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid var(--border); font-size: 0.85rem; color: var(--text-muted);">
                <p><strong>Note:</strong> Role selection is automatic upon authentication. The ERP directs you straight to your dedicated portal.</p>
            </div>
        </div>
        """
        html = render_html_page("Sign In", content, current_user)
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

    def handle_admin(self, environ, start_response, path, current_user):
        if not current_user or current_user.get("role") != UserRole.ADMIN.value:
            start_response("302 Found", [("Location", "/login")])
            return [b""]

        kpis = self.metrics.get_summary_kpis()
        books, _ = self.book_svc.search(BookFilter(limit=10))
        audits = self.audit_svc.get_recent_activity(limit=8)

        books_rows = "".join(f"""
            <tr>
                <td><code>{b.isbn}</code></td>
                <td><strong>{b.title}</strong></td>
                <td>{b.author_name or "-"}</td>
                <td>{b.category_name or "-"}</td>
                <td>{b.total_copies}</td>
                <td><span class="badge badge-avail">{b.available_copies}</span></td>
                <td>${b.price:.2f}</td>
            </tr>
        """ for b in books)

        audit_rows = "".join(f"""
            <tr>
                <td><small>{a.timestamp}</small></td>
                <td><code>{a.username}</code></td>
                <td><span class="badge badge-admin">{a.action}</span></td>
                <td>{a.entity_type} #{a.entity_id or "-"}</td>
                <td>{a.description}</td>
            </tr>
        """ for a in audits)

        content = f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <h2>System Administration Dashboard</h2>
            <span class="badge badge-admin" style="font-size: 0.9rem; padding: 0.35rem 0.75rem;">ROLE_ADMIN Access</span>
        </div>

        <div class="grid-4">
            <div class="kpi-card">
                <div class="kpi-title">Catalog Titles</div>
                <div class="kpi-value">{kpis['total_books']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Total Physical Copies</div>
                <div class="kpi-value">{kpis['total_copies']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Available Copies</div>
                <div class="kpi-value" style="color: var(--success);">{kpis['available_copies']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Currently Issued</div>
                <div class="kpi-value" style="color: var(--primary);">{kpis['issued_copies']}</div>
            </div>
        </div>

        <div class="grid-4">
            <div class="kpi-card">
                <div class="kpi-title">Total Patrons</div>
                <div class="kpi-value">{kpis['total_members']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Active Memberships</div>
                <div class="kpi-value" style="color: var(--success);">{kpis['active_members']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Overdue Loans</div>
                <div class="kpi-value" style="color: var(--danger);">{kpis['overdue_books']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Collected Revenue</div>
                <div class="kpi-value">${kpis['collected_fines']:.2f}</div>
            </div>
        </div>

        <div class="card">
            <h2>Master Catalog Inventory</h2>
            <table>
                <thead>
                    <tr><th>ISBN</th><th>Title</th><th>Author</th><th>Genre</th><th>Total</th><th>Available</th><th>Price</th></tr>
                </thead>
                <tbody>{books_rows or "<tr><td colspan='7'>No books registered.</td></tr>"}</tbody>
            </table>
        </div>

        <div class="card">
            <h2>Compliance Audit Trail</h2>
            <table>
                <thead>
                    <tr><th>Timestamp</th><th>User</th><th>Action</th><th>Entity</th><th>Details</th></tr>
                </thead>
                <tbody>{audit_rows or "<tr><td colspan='5'>No recent audit events.</td></tr>"}</tbody>
            </table>
        </div>
        """
        html = render_html_page("Admin Dashboard", content, current_user)
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [html.encode("utf-8")]

    def handle_librarian(self, environ, start_response, path, current_user):
        if not current_user or current_user.get("role") not in (UserRole.LIBRARIAN.value, UserRole.ADMIN.value):
            start_response("302 Found", [("Location", "/login")])
            return [b""]

        kpis = self.metrics.get_summary_kpis()
        books, _ = self.book_svc.search(BookFilter(limit=10))
        members, _ = self.member_svc.search(limit=10)

        books_rows = "".join(f"""
            <tr>
                <td><code>{b.isbn}</code></td>
                <td><strong>{b.title}</strong></td>
                <td>{b.author_name or "-"}</td>
                <td>Shelf: {b.shelf_number} | Rack: {b.rack_number}</td>
                <td><span class="badge badge-avail">{b.available_copies} of {b.total_copies}</span></td>
            </tr>
        """ for b in books)

        members_rows = "".join(f"""
            <tr>
                <td><code>{m.member_code}</code></td>
                <td><strong>{m.full_name}</strong></td>
                <td>{m.email}</td>
                <td><span class="badge badge-member">{m.membership_type}</span></td>
                <td>{m.expiry_date}</td>
                <td><span class="badge badge-avail">{m.status}</span></td>
            </tr>
        """ for m in members)

        content = f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <h2>Librarian Circulation Desk</h2>
            <span class="badge badge-librarian" style="font-size: 0.9rem; padding: 0.35rem 0.75rem;">ROLE_LIBRARIAN Access</span>
        </div>

        <div class="grid-4">
            <div class="kpi-card">
                <div class="kpi-title">Available for Checkout</div>
                <div class="kpi-value" style="color: var(--success);">{kpis['available_copies']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Active Loans</div>
                <div class="kpi-value">{kpis['issued_copies']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Overdue Loans</div>
                <div class="kpi-value" style="color: var(--danger);">{kpis['overdue_books']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Pending Hold Requests</div>
                <div class="kpi-value" style="color: var(--warning);">{kpis['pending_reservations']}</div>
            </div>
        </div>

        <div class="card">
            <h2>Registered Patrons Roster</h2>
            <table>
                <thead>
                    <tr><th>Card ID</th><th>Full Name</th><th>Email</th><th>Tier</th><th>Expiry Date</th><th>Status</th></tr>
                </thead>
                <tbody>{members_rows or "<tr><td colspan='6'>No patrons found.</td></tr>"}</tbody>
            </table>
        </div>

        <div class="card">
            <h2>Circulation Catalog Overview</h2>
            <table>
                <thead>
                    <tr><th>ISBN</th><th>Title</th><th>Author</th><th>Location</th><th>Availability</th></tr>
                </thead>
                <tbody>{books_rows or "<tr><td colspan='5'>No books found.</td></tr>"}</tbody>
            </table>
        </div>
        """
        html = render_html_page("Librarian Circulation Desk", content, current_user)
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [html.encode("utf-8")]

    def handle_member(self, environ, start_response, path, current_user):
        if not current_user:
            start_response("302 Found", [("Location", "/login")])
            return [b""]

        user_id = current_user.get("user_id")
        member = self.member_svc.get_by_user_id(user_id) if user_id else None

        loans = []
        fines = []
        notifications = []
        if member:
            loans = self.issue_svc.borrow_repo.list_active_by_member(member.member_id)
            fines = self.fine_svc.list_fines_by_member(member.member_id)
            notifications = self.notif_svc.get_user_notifications(user_id=user_id, limit=5)

        loan_rows = "".join(f"""
            <tr>
                <td><strong>{l.book_title}</strong></td>
                <td><code>{l.barcode}</code></td>
                <td>{l.issue_date}</td>
                <td><strong>{l.due_date}</strong></td>
                <td>{l.renewal_count} / {l.max_renewals_allowed}</td>
                <td><span class="badge badge-issued">{l.status}</span></td>
            </tr>
        """ for l in loans)

        fine_rows = "".join(f"""
            <tr>
                <td>{f.fine_type}</td>
                <td>${f.amount:.2f}</td>
                <td>${f.paid_amount:.2f}</td>
                <td><strong>${f.balance_amount:.2f}</strong></td>
                <td><span class="badge badge-{'avail' if f.status == 'PAID' else 'overdue'}">{f.status}</span></td>
            </tr>
        """ for f in fines)

        member_code = member.member_code if member else "MEM-GUEST"
        tier_name = member.membership_type if member else "GENERAL"
        expiry = member.expiry_date if member else "N/A"

        content = f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <h2>Patron Self-Service Portal</h2>
            <span class="badge badge-member" style="font-size: 0.9rem; padding: 0.35rem 0.75rem;">ROLE_MEMBER</span>
        </div>

        <div class="grid-4">
            <div class="kpi-card">
                <div class="kpi-title">Patron Card ID</div>
                <div class="kpi-value" style="font-size: 1.4rem;">{member_code}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Membership Tier</div>
                <div class="kpi-value" style="font-size: 1.4rem;">{tier_name}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Active Loans</div>
                <div class="kpi-value">{len(loans)}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Membership Expiry</div>
                <div class="kpi-value" style="font-size: 1.2rem; color: var(--text-muted);">{expiry}</div>
            </div>
        </div>

        <div class="card">
            <h2>Active Borrowed Books</h2>
            <table>
                <thead>
                    <tr><th>Book Title</th><th>Copy Barcode</th><th>Issue Date</th><th>Due Date</th><th>Renewals</th><th>Status</th></tr>
                </thead>
                <tbody>{loan_rows or "<tr><td colspan='6'>You have no active borrowed books.</td></tr>"}</tbody>
            </table>
        </div>

        <div class="card">
            <h2>Assessed Fines & Balance</h2>
            <table>
                <thead>
                    <tr><th>Fine Type</th><th>Amount</th><th>Paid</th><th>Outstanding Balance</th><th>Status</th></tr>
                </thead>
                <tbody>{fine_rows or "<tr><td colspan='5'>No fines recorded on your account.</td></tr>"}</tbody>
            </table>
        </div>
        """
        html = render_html_page("Member Portal", content, current_user)
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [html.encode("utf-8")]

    def handle_not_found(self, start_response):
        content = """
        <div class="card" style="text-align: center; padding: 3rem;">
            <h1>404 - Page Not Found</h1>
            <p style="margin-top: 1rem;"><a href="/" class="btn">Return to Home</a></p>
        </div>
        """
        html = render_html_page("Not Found", content)
        start_response("404 Not Found", [("Content-Type", "text/html; charset=utf-8")])
        return [html.encode("utf-8")]

def create_app():
    return ApplicationServer()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    app = create_app()
    server = make_server(host, port, app)
    print(f"[✓] SmartLibrary ERP Server is LIVE at: http://{host}:{port}")
    print(f"[✓] Admin Portal:       http://{host}:{port}/admin/dashboard")
    print(f"[✓] Librarian Desk:     http://{host}:{port}/librarian/dashboard")
    print(f"[✓] Member Portal:      http://{host}:{port}/member/dashboard")
    print("[✓] Press Ctrl+C to stop the server.")
    server.serve_forever()
