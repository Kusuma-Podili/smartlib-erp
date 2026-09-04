"""Member Portal Views and Handlers for SmartLibrary ERP."""
import datetime
from smartlib.web.css import render_shell
from smartlib.books.models import BookFilter
from smartlib.constants import PaymentMethod

MEMBER_MENU = [
    ("overview", "Overview", "&#128202;", "/member/dashboard?tab=overview"),
    ("search", "Search Books", "&#128269;", "/member/dashboard?tab=search"),
    ("my_books", "My Books", "&#128214;", "/member/dashboard?tab=my_books"),
    ("reservations", "My Reservations", "&#128278;", "/member/dashboard?tab=reservations"),
    ("fines", "My Fines", "&#128176;", "/member/dashboard?tab=fines"),
    ("notifications", "Notifications", "&#128276;", "/member/dashboard?tab=notifications"),
    ("profile", "My Profile", "&#128100;", "/member/dashboard?tab=profile"),
    ("announcements", "Announcements", "&#128227;", "/member/dashboard?tab=announcements"),
]

class MemberViews:
    def __init__(self, app):
        self.app = app

    def get_member_profile(self, user):
        res = self.app.db_manager.fetch_one("SELECT * FROM members WHERE user_id = ?;", (user["user_id"],))
        if not res:
            # Fallback for admin previewing member portal
            res = self.app.db_manager.fetch_one("SELECT * FROM members LIMIT 1;")
        return res

    def handle_request(self, environ, start_response, path, method, user):
        query = self.app.parse_query(environ)
        tab = query.get("tab", "overview")
        msg = query.get("msg", "")
        msg_type = query.get("msg_type", "success")

        member = self.get_member_profile(user)
        if not member:
            return self.app.redirect(start_response, "/login", "Member record not found.", "error")

        member_id = member["member_id"]

        if method == "POST":
            params = self.app.parse_body(environ)
            action = params.get("action", "")

            # 1. Self-Renewal
            if action == "renew_book":
                try:
                    borrowing_id = int(params.get("borrowing_id"))
                    loan = self.app.renew_svc.renew_loan(borrowing_id=borrowing_id, actor_username=user["username"])
                    return self.app.redirect(start_response, "/member/dashboard?tab=my_books", f"Renewal successful! New due date: {loan.new_due_date}")
                except Exception as e:
                    return self.app.redirect(start_response, "/member/dashboard?tab=my_books", str(e), "error")

            # 2. Reserve / Hold Book
            elif action == "reserve_book":
                try:
                    book_id = int(params.get("book_id"))
                    hold = self.app.reserve_svc.create_reservation(book_id=book_id, member_id=member_id, actor_username=user["username"])
                    return self.app.redirect(start_response, "/member/dashboard?tab=reservations", f"Hold placed! Position #{hold.queue_position}")
                except Exception as e:
                    return self.app.redirect(start_response, "/member/dashboard?tab=reservations", str(e), "error")

            # 3. Cancel Reservation
            elif action == "cancel_reservation":
                try:
                    res_id = int(params.get("reservation_id"))
                    self.app.reserve_svc.cancel_reservation(reservation_id=res_id, actor_username=user["username"])
                    return self.app.redirect(start_response, "/member/dashboard?tab=reservations", "Reservation cancelled successfully.")
                except Exception as e:
                    return self.app.redirect(start_response, "/member/dashboard?tab=reservations", str(e), "error")

            # 4. Pay Fine Online
            elif action == "pay_fine_online":
                try:
                    fine_id = int(params.get("fine_id"))
                    amount = float(params.get("amount"))
                    pm = params.get("payment_method", "UPI")
                    method_enum = PaymentMethod[pm]
                    receipt = self.app.payment_svc.process_payment(
                        fine_id=fine_id, amount=amount, payment_method=method_enum,
                        cashier_username="ONLINE_PORTAL", actor_username=user["username"]
                    )
                    return self.app.redirect(start_response, "/member/dashboard?tab=fines", f"Fine payment of ${amount:.2f} confirmed! Receipt #{receipt.receipt_number}")
                except Exception as e:
                    return self.app.redirect(start_response, "/member/dashboard?tab=fines", str(e), "error")

        content = ""
        if tab == "overview": content = self.render_overview(member)
        elif tab == "search": content = self.render_search(query)
        elif tab == "my_books": content = self.render_my_books(member)
        elif tab == "reservations": content = self.render_reservations(member)
        elif tab == "fines": content = self.render_fines(member)
        elif tab == "notifications": content = self.render_notifications(user)
        elif tab == "profile": content = self.render_profile(member, user)
        elif tab == "announcements": content = self.render_announcements()
        else: content = self.render_overview(member)

        html = render_shell("Member Portal", user, MEMBER_MENU, tab, content, msg, msg_type)
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [html.encode("utf-8")]

    def render_overview(self, member):
        mid = member["member_id"]
        today = datetime.date.today().isoformat()
        
        loans = self.app.db_manager.fetch_all("""
            SELECT b.*, bk.title, bk.isbn, c.barcode 
            FROM borrowings b 
            JOIN book_copies c ON b.copy_id = c.copy_id 
            JOIN books bk ON c.book_id = bk.book_id 
            WHERE b.member_id = ? AND b.status IN ('ISSUED', 'EXTENDED');
        """, (mid,))

        due_soon = [l for l in loans if l['due_date'] >= today]
        overdue = [l for l in loans if l['due_date'] < today]

        holds = self.app.db_manager.fetch_all("""
            SELECT r.*, b.title 
            FROM reservations r JOIN books b ON r.book_id = b.book_id 
            WHERE r.member_id = ? AND r.status IN ('PENDING', 'READY');
        """, (mid,))

        fines = self.app.db_manager.fetch_all("SELECT SUM(balance_amount) as total FROM fines WHERE member_id = ? AND status != 'PAID';", (mid,))
        outstanding_fine = fines[0]['total'] if fines and fines[0]['total'] else 0.0

        loan_rows = "".join(f'''
            <tr>
                <td><strong>{l['title']}</strong></td>
                <td><code>{l['barcode']}</code></td>
                <td>{l['issue_date']}</td>
                <td><strong>{l['due_date']}</strong></td>
                <td><span class="badge badge-{'overdue' if l['due_date'] < today else 'issued'}">{'OVERDUE' if l['due_date'] < today else 'ACTIVE'}</span></td>
            </tr>
        ''' for l in loans)

        return f'''
        <div class="header-row">
            <h1>Welcome, {member['first_name']}!</h1>
            <div>
                <a href="/member/dashboard?tab=search" class="btn btn-sm">Search Books</a>
                <a href="/member/dashboard?tab=my_books" class="btn btn-sm btn-secondary">My Checkouts</a>
            </div>
        </div>

        <div class="grid-4">
            <div class="kpi-card"><div class="kpi-title">Currently Borrowed</div><div class="kpi-value">{len(loans)}</div></div>
            <div class="kpi-card"><div class="kpi-title">Due Soon</div><div class="kpi-value" style="color:var(--warning);">{len(due_soon)}</div></div>
            <div class="kpi-card"><div class="kpi-title">Overdue Books</div><div class="kpi-value" style="color:var(--danger);">{len(overdue)}</div></div>
            <div class="kpi-card"><div class="kpi-title">Outstanding Fine</div><div class="kpi-value" style="color:var(--danger);">${outstanding_fine:.2f}</div></div>
        </div>

        <div class="card">
            <h2>Current Active Loans</h2>
            <table><thead><tr><th>Book Title</th><th>Barcode</th><th>Issue Date</th><th>Due Date</th><th>Status</th></tr></thead><tbody>{loan_rows or "<tr><td colspan='5' class='empty-state'>You currently have no active checkouts.</td></tr>"}</tbody></table>
        </div>
        '''

    def render_search(self, query):
        q = query.get("q", "")
        books, total = self.app.book_svc.search(BookFilter(query=q, limit=50))

        rows = "".join(f'''
            <tr>
                <td><code>{b.isbn}</code></td>
                <td><strong>{b.title}</strong><br><small style="color:var(--text-muted);">{b.subtitle or ''}</small></td>
                <td>{b.author_name or '-'}</td>
                <td>{b.category_name or '-'}</td>
                <td>Shelf {b.shelf_number}</td>
                <td><span class="badge badge-{'avail' if b.available_copies > 0 else 'overdue'}">{b.available_copies} of {b.total_copies} Available</span></td>
                <td>
                    <form method="POST" action="/member/dashboard" style="display:inline;">
                        <input type="hidden" name="action" value="reserve_book">
                        <input type="hidden" name="book_id" value="{b.book_id}">
                        <button type="submit" class="btn btn-sm {'btn-primary' if b.available_copies == 0 else 'btn-secondary'}">
                            {'Hold Queue' if b.available_copies == 0 else 'Reserve'}
                        </button>
                    </form>
                </td>
            </tr>
        ''' for b in books)

        return f'''
        <div class="header-row"><h1>Library Catalog Search</h1></div>
        <div class="card">
            <h2>Search & Filter Catalog ({total} Books)</h2>
            <form method="GET" action="/member/dashboard" class="search-bar">
                <input type="hidden" name="tab" value="search">
                <input type="text" name="q" value="{q}" placeholder="Search catalog by title, author, category, or ISBN...">
                <button type="submit" class="btn">Search</button>
            </form>
            <table><thead><tr><th>ISBN</th><th>Title</th><th>Author</th><th>Genre</th><th>Location</th><th>Availability</th><th>Action</th></tr></thead><tbody>{rows or "<tr><td colspan='7' class='empty-state'>No matching books found.</td></tr>"}</tbody></table>
        </div>
        '''

    def render_my_books(self, member):
        mid = member["member_id"]
        today = datetime.date.today().isoformat()

        active = self.app.db_manager.fetch_all("""
            SELECT b.*, bk.title, bk.isbn, c.barcode 
            FROM borrowings b 
            JOIN book_copies c ON b.copy_id = c.copy_id 
            JOIN books bk ON c.book_id = bk.book_id 
            WHERE b.member_id = ? AND b.status IN ('ISSUED', 'EXTENDED');
        """, (mid,))

        history = self.app.db_manager.fetch_all("""
            SELECT r.*, bk.title, c.barcode 
            FROM returns r 
            JOIN borrowings b ON r.borrowing_id = b.borrowing_id 
            JOIN book_copies c ON b.copy_id = c.copy_id 
            JOIN books bk ON c.book_id = bk.book_id 
            WHERE b.member_id = ? 
            ORDER BY r.return_id DESC LIMIT 20;
        """, (mid,))

        active_rows = "".join(f'''
            <tr>
                <td><strong>{a['title']}</strong></td>
                <td><code>{a['barcode']}</code></td>
                <td>{a['issue_date']}</td>
                <td><strong>{a['due_date']}</strong></td>
                <td>{a['renewal_count']} / 2</td>
                <td><span class="badge badge-{'overdue' if a['due_date'] < today else 'issued'}">{'OVERDUE' if a['due_date'] < today else 'ON LOAN'}</span></td>
                <td>
                    <form method="POST" action="/member/dashboard" style="display:inline;">
                        <input type="hidden" name="action" value="renew_book">
                        <input type="hidden" name="borrowing_id" value="{a['borrowing_id']}">
                        <button type="submit" class="btn btn-sm btn-secondary" {'disabled' if a['due_date'] < today or a['renewal_count'] >= 2 else ''}>
                            Renew Loan
                        </button>
                    </form>
                </td>
            </tr>
        ''' for a in active)

        history_rows = "".join(f'''
            <tr>
                <td><strong>{h['title']}</strong></td>
                <td><code>{h['barcode']}</code></td>
                <td>{h['returned_date']}</td>
                <td>{h['condition_on_return']}</td>
                <td>${h['fine_amount']:.2f}</td>
            </tr>
        ''' for h in history)

        return f'''
        <div class="header-row"><h1>My Books & Circulation Activity</h1></div>
        <div class="card">
            <h2>Currently Borrowed Items ({len(active)} Books)</h2>
            <table><thead><tr><th>Book Title</th><th>Barcode</th><th>Issue Date</th><th>Due Date</th><th>Renewals</th><th>Status</th><th>Action</th></tr></thead><tbody>{active_rows or "<tr><td colspan='7' class='empty-state'>No books currently checked out.</td></tr>"}</tbody></table>
        </div>
        <div class="card">
            <h2>Borrowing History (Past Returns)</h2>
            <table><thead><tr><th>Book Title</th><th>Barcode</th><th>Returned On</th><th>Condition</th><th>Fine</th></tr></thead><tbody>{history_rows or "<tr><td colspan='5' class='empty-state'>No return history yet.</td></tr>"}</tbody></table>
        </div>
        '''

    def render_reservations(self, member):
        mid = member["member_id"]
        holds = self.app.db_manager.fetch_all("""
            SELECT r.*, b.title, b.isbn 
            FROM reservations r JOIN books b ON r.book_id = b.book_id 
            WHERE r.member_id = ? 
            ORDER BY r.reservation_id DESC;
        """, (mid,))

        rows = "".join(f'''
            <tr>
                <td><strong>{h['title']}</strong></td>
                <td><code>{h['isbn']}</code></td>
                <td>{h['reservation_date']}</td>
                <td>Position #{h['queue_position']}</td>
                <td><span class="badge badge-{'avail' if h['status'] == 'READY' else 'pending'}">{h['status']}</span></td>
                <td>
                    {'<form method="POST" action="/member/dashboard" style="display:inline;"><input type="hidden" name="action" value="cancel_reservation"><input type="hidden" name="reservation_id" value="' + str(h['reservation_id']) + '"><button type="submit" class="btn btn-sm btn-danger">Cancel</button></form>' if h['status'] in ('PENDING', 'READY') else '-'}
                </td>
            </tr>
        ''' for h in holds)

        return f'''
        <div class="header-row"><h1>My Reservations & Book Holds</h1></div>
        <div class="card">
            <h2>Active Holds Queue & Status</h2>
            <table><thead><tr><th>Book Title</th><th>ISBN</th><th>Requested Date</th><th>Queue Position</th><th>Status</th><th>Action</th></tr></thead><tbody>{rows or "<tr><td colspan='6' class='empty-state'>No active hold reservations.</td></tr>"}</tbody></table>
        </div>
        '''

    def render_fines(self, member):
        mid = member["member_id"]
        fines = self.app.db_manager.fetch_all("SELECT * FROM fines WHERE member_id = ? ORDER BY fine_id DESC;", (mid,))
        unpaid = [f for f in fines if f['status'] != 'PAID']
        unpaid_opts = "".join(f"<option value='{f['fine_id']}'>Fine #{f['fine_id']}: ${f['balance_amount']:.2f} ({f['fine_type']})</option>" for f in unpaid)

        rows = "".join(f'''
            <tr>
                <td>#{f['fine_id']}</td>
                <td>{f['fine_type']}</td>
                <td>${f['amount']:.2f}</td>
                <td>${f['paid_amount']:.2f}</td>
                <td><strong style="color:var(--danger);">${f['balance_amount']:.2f}</strong></td>
                <td><span class="badge badge-{'avail' if f['status'] == 'PAID' else 'overdue'}">{f['status']}</span></td>
            </tr>
        ''' for f in fines)

        payments = self.app.db_manager.fetch_all("""
            SELECT p.* FROM payments p 
            JOIN fines f ON p.fine_id = f.fine_id 
            WHERE f.member_id = ? 
            ORDER BY p.payment_id DESC;
        """, (mid,))

        receipt_rows = "".join(f'''
            <tr>
                <td><code>{p['receipt_number']}</code></td>
                <td>{p['payment_date']}</td>
                <td>${p['amount']:.2f}</td>
                <td>{p['payment_method']}</td>
                <td><span class="badge badge-avail">{p['status']}</span></td>
            </tr>
        ''' for p in payments)

        return f'''
        <div class="header-row"><h1>My Fines & Online Fee Settlement</h1></div>

        <div class="card">
            <h2>?? Pay Fine Online (Instant Clearance)</h2>
            <form method="POST" action="/member/dashboard">
                <input type="hidden" name="action" value="pay_fine_online">
                <div class="form-grid">
                    <div class="form-group"><label>Select Unpaid Fine *</label><select name="fine_id">{unpaid_opts or "<option value=''>No outstanding fines</option>"}</select></div>
                    <div class="form-group"><label>Payment Amount ($) *</label><input type="number" step="0.50" name="amount" value="10.00" min="0.50"></div>
                    <div class="form-group"><label>Payment Method *</label>
                        <select name="payment_method">
                            <option value="UPI">UPI / QR Code</option>
                            <option value="CREDIT_CARD">Credit Card</option>
                            <option value="DEBIT_CARD">Debit Card</option>
                        </select>
                    </div>
                </div>
                <button type="submit" class="btn btn-success" {'disabled' if not unpaid else ''}>Pay Now Online</button>
            </form>
        </div>

        <div class="card">
            <h2>Fines Assessment History</h2>
            <table><thead><tr><th>Fine ID</th><th>Reason</th><th>Assessed</th><th>Paid</th><th>Outstanding</th><th>Status</th></tr></thead><tbody>{rows or "<tr><td colspan='6' class='empty-state'>No fines on your account.</td></tr>"}</tbody></table>
        </div>

        <div class="card">
            <h2>Payment Receipts</h2>
            <table><thead><tr><th>Receipt No</th><th>Date</th><th>Amount</th><th>Method</th><th>Status</th></tr></thead><tbody>{receipt_rows or "<tr><td colspan='5' class='empty-state'>No payment receipts yet.</td></tr>"}</tbody></table>
        </div>
        '''

    def render_notifications(self, user):
        notifs = self.app.db_manager.fetch_all("SELECT * FROM notifications WHERE user_id = ? ORDER BY notification_id DESC LIMIT 20;", (user["user_id"],))
        rows = "".join(f'''
            <tr>
                <td><small>{n['created_at']}</small></td>
                <td><strong>{n['title']}</strong></td>
                <td>{n['message']}</td>
            </tr>
        ''' for n in notifs)

        return f'''
        <div class="header-row"><h1>My Notifications & Reminders</h1></div>
        <div class="card">
            <h2>Inbox & Circulation Messages</h2>
            <table><thead><tr><th>Timestamp</th><th>Subject</th><th>Message</th></tr></thead><tbody>{rows or "<tr><td colspan='3' class='empty-state'>No notifications.</td></tr>"}</tbody></table>
        </div>
        '''

    def render_profile(self, member, user):
        return f'''
        <div class="header-row"><h1>My Patron Profile & Identification</h1></div>
        <div class="card" style="max-width: 600px; border-left: 6px solid var(--primary);">
            <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border);padding-bottom:1rem;margin-bottom:1.25rem;">
                <div>
                    <h2 style="border:none;margin:0;padding:0;">{member['first_name']} {member['last_name']}</h2>
                    <code style="font-size:1.1rem;color:var(--primary);">{member['member_code']}</code>
                </div>
                <span class="badge badge-member" style="font-size:0.9rem;padding:0.4rem 0.8rem;">{member['membership_type']} TIER</span>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;font-size:0.92rem;">
                <div><strong>Email:</strong> {user.get('email')}</div>
                <div><strong>Phone:</strong> {member['phone']}</div>
                <div><strong>Status:</strong> <span class="badge badge-avail">{member['status']}</span></div>
                <div><strong>Expires On:</strong> {member['expiry_date']}</div>
                <div style="grid-column: span 2;"><strong>Address:</strong> {member['address']}</div>
            </div>
        </div>
        '''

    def render_announcements(self):
        active = self.app.announce_svc.list_active_announcements()
        rows = "".join(f'''
            <div class="card" style="border-left: 4px solid var(--primary); margin-bottom:1rem;">
                <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                    <h3>{a.title}</h3>
                    <span class="badge badge-admin">{a.priority}</span>
                </div>
                <p style="margin-bottom:0.5rem;">{a.content}</p>
                <small style="color:var(--text-muted);">Posted on: {a.start_date}</small>
            </div>
        ''' for a in active)

        return f'''
        <div class="header-row"><h1>Campus Announcements & Library Bulletins</h1></div>
        {rows or "<div class='empty-state'>No announcements currently posted.</div>"}
        '''
