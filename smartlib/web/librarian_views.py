"""Librarian / Employee Portal Views and Handlers for SmartLibrary ERP."""
import datetime
from smartlib.web.css import render_shell
from smartlib.members.models import MemberDTO
from smartlib.books.models import BookFilter
from smartlib.copies.models import BookCopyDTO
from smartlib.constants import BookCopyCondition, PaymentMethod

LIBRARIAN_MENU = [
    ("overview", "Overview", "&#128202;", "/librarian/dashboard?tab=overview"),
    ("members", "Member Management", "&#128101;", "/librarian/dashboard?tab=members"),
    ("books", "Book Management", "&#128218;", "/librarian/dashboard?tab=books"),
    ("transactions", "Transactions", "&#128257;", "/librarian/dashboard?tab=transactions"),
    ("fines", "Fine Management", "&#128176;", "/librarian/dashboard?tab=fines"),
    ("notifications", "Notifications", "&#128276;", "/librarian/dashboard?tab=notifications"),
    ("reports", "Daily Reports", "&#128196;", "/librarian/dashboard?tab=reports"),
]

class LibrarianViews:
    def __init__(self, app):
        self.app = app

    def handle_request(self, environ, start_response, path, method, user):
        query = self.app.parse_query(environ)
        tab = query.get("tab", "overview")
        msg = query.get("msg", "")
        msg_type = query.get("msg_type", "success")

        if method == "POST":
            params = self.app.parse_body(environ)
            action = params.get("action", "")

            # 1. Add Member
            if action == "add_member":
                try:
                    fn = params.get("first_name").strip()
                    ln = params.get("last_name").strip()
                    em = params.get("email").strip().lower()
                    ph = params.get("phone").strip()
                    addr = params.get("address", "Campus Housing")
                    tier = params.get("tier", "STUDENT")
                    
                    mdto = MemberDTO(
                        first_name=fn,
                        last_name=ln,
                        email=em,
                        phone=ph,
                        address=addr,
                        membership_type=tier,
                        password="Member@123"
                    )
                    created_member = self.app.member_svc.register_member(mdto, actor_username=user["username"])
                    return self.app.redirect(start_response, "/librarian/dashboard?tab=members", f"Member created! Code: {created_member.member_code}")
                except Exception as e:
                    return self.app.redirect(start_response, "/librarian/dashboard?tab=members", str(e), "error")

            # 2. Issue Book
            elif action == "issue_book":
                try:
                    member_id = int(params.get("member_id"))
                    copy_id = int(params.get("copy_id"))
                    loan = self.app.issue_svc.issue_book(copy_id=copy_id, member_id=member_id, actor_username=user["username"])
                    return self.app.redirect(start_response, "/librarian/dashboard?tab=transactions", f"Book issued! Due Date: {loan.due_date}")
                except Exception as e:
                    return self.app.redirect(start_response, "/librarian/dashboard?tab=transactions", str(e), "error")

            # 3. Return Book
            elif action == "return_book":
                try:
                    borrowing_id = int(params.get("borrowing_id"))
                    cond_str = params.get("condition", "GOOD")
                    condition = BookCopyCondition[cond_str]
                    res = self.app.return_svc.return_book(borrowing_id=borrowing_id, condition=condition, actor_username=user["username"])
                    fine_msg = f" (Overdue fine assessed: ${res.fine_amount:.2f})" if res.fine_amount > 0 else " (No overdue fine)"
                    return self.app.redirect(start_response, "/librarian/dashboard?tab=transactions", f"Book returned successfully!{fine_msg}")
                except Exception as e:
                    return self.app.redirect(start_response, "/librarian/dashboard?tab=transactions", str(e), "error")

            # 4. Renew Book
            elif action == "renew_book":
                try:
                    borrowing_id = int(params.get("borrowing_id"))
                    renewal = self.app.renew_svc.renew_loan(borrowing_id=borrowing_id, actor_username=user["username"])
                    return self.app.redirect(start_response, "/librarian/dashboard?tab=transactions", f"Loan extended! New Due Date: {renewal.new_due_date}")
                except Exception as e:
                    return self.app.redirect(start_response, "/librarian/dashboard?tab=transactions", str(e), "error")

            # 5. Record Fine Payment
            elif action == "record_payment":
                try:
                    fine_id = int(params.get("fine_id"))
                    amount = float(params.get("amount"))
                    pm = params.get("payment_method", "CASH")
                    method = PaymentMethod[pm]
                    payment = self.app.payment_svc.process_payment(fine_id=fine_id, amount=amount, payment_method=method, cashier_username=user["username"], actor_username=user["username"])
                    return self.app.redirect(start_response, "/librarian/dashboard?tab=fines", f"Payment recorded! Receipt #{payment.receipt_number}")
                except Exception as e:
                    return self.app.redirect(start_response, "/librarian/dashboard?tab=fines", str(e), "error")

            # 6. Add Copy
            elif action == "add_copy":
                try:
                    book_id = int(params.get("book_id"))
                    cost = float(params.get("cost") or 40.0)
                    copy = self.app.copy_svc.add_copy(BookCopyDTO(book_id=book_id, acquisition_cost=cost), actor_username=user["username"])
                    return self.app.redirect(start_response, "/librarian/dashboard?tab=books", f"Copy added! Barcode: {copy.barcode}")
                except Exception as e:
                    return self.app.redirect(start_response, "/librarian/dashboard?tab=books", str(e), "error")

        content = ""
        if tab == "overview": content = self.render_overview()
        elif tab == "members": content = self.render_members(query)
        elif tab == "books": content = self.render_books(query)
        elif tab == "transactions": content = self.render_transactions()
        elif tab == "fines": content = self.render_fines()
        elif tab == "notifications": content = self.render_notifications()
        elif tab == "reports": content = self.render_reports()
        else: content = self.render_overview()

        html = render_shell("Librarian Operations Portal", user, LIBRARIAN_MENU, tab, content, msg, msg_type)
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [html.encode("utf-8")]

    def render_overview(self):
        k = self.app.metrics.get_summary_kpis()
        today = datetime.date.today().isoformat()
        today_issues = len(self.app.db_manager.fetch_all("SELECT borrowing_id FROM borrowings WHERE issue_date = ?;", (today,)))
        today_returns = len(self.app.db_manager.fetch_all("SELECT return_id FROM returns WHERE returned_date = ?;", (today,)))
        pending_fines = len(self.app.db_manager.fetch_all("SELECT fine_id FROM fines WHERE status != 'PAID';"))
        active_loans = self.app.issue_svc.borrow_repo.list_all_active()[:5]

        loan_rows = "".join(f"<tr><td>#{l.borrowing_id}</td><td><strong>{l.book_title}</strong></td><td><code>{l.barcode}</code></td><td>{l.member_name}</td><td><strong>{l.due_date}</strong></td><td><span class='badge badge-{'overdue' if l.is_overdue() else 'issued'}'>{l.status}</span></td></tr>" for l in active_loans)

        return f'''
        <div class="header-row">
            <h1>Librarian Operational Overview</h1>
            <div>
                <a href="/librarian/dashboard?tab=transactions" class="btn btn-sm">+ Issue / Return</a>
                <a href="/librarian/dashboard?tab=members" class="btn btn-sm btn-secondary">+ Add Member</a>
            </div>
        </div>
        <div class="grid-4">
            <div class="kpi-card"><div class="kpi-title">Today's Issues</div><div class="kpi-value">{today_issues}</div></div>
            <div class="kpi-card"><div class="kpi-title">Today's Returns</div><div class="kpi-value" style="color:var(--success);">{today_returns}</div></div>
            <div class="kpi-card"><div class="kpi-title">Pending Reservations</div><div class="kpi-value" style="color:var(--warning);">{k['pending_reservations']}</div></div>
            <div class="kpi-card"><div class="kpi-title">Overdue Loans</div><div class="kpi-value" style="color:var(--danger);">{k['overdue_books']}</div></div>
        </div>
        <div class="grid-4">
            <div class="kpi-card"><div class="kpi-title">Pending Fines</div><div class="kpi-value" style="color:var(--danger);">{pending_fines}</div></div>
            <div class="kpi-card"><div class="kpi-title">Available Copies</div><div class="kpi-value" style="color:var(--success);">{k['available_copies']}</div></div>
            <div class="kpi-card"><div class="kpi-title">Total Patrons</div><div class="kpi-value">{k['total_members']}</div></div>
            <div class="kpi-card"><div class="kpi-title">Collected Revenue</div><div class="kpi-value" style="color:var(--success);">${k['collected_fines']:.2f}</div></div>
        </div>
        <div class="card">
            <h2>Current Active Checkouts</h2>
            <table><thead><tr><th>Loan ID</th><th>Book Title</th><th>Barcode</th><th>Patron</th><th>Due Date</th><th>Status</th></tr></thead><tbody>{loan_rows or "<tr><td colspan='6' class='empty-state'>No active checkouts.</td></tr>"}</tbody></table>
        </div>
        '''

    def render_members(self, query):
        q = query.get("q", "")
        members = self.app.db_manager.fetch_all("""
            SELECT m.*, u.username, u.email, u.status as user_status 
            FROM members m JOIN users u ON m.user_id = u.user_id
            WHERE m.first_name LIKE ? OR m.last_name LIKE ? OR m.member_code LIKE ?
            ORDER BY m.member_id DESC;
        """, (f"%{q}%", f"%{q}%", f"%{q}%"))

        member_rows = "".join(f'''
            <tr>
                <td><code>{m['member_code']}</code></td>
                <td><strong>{m['first_name']} {m['last_name']}</strong></td>
                <td>{m['email']}</td>
                <td>{m['phone']}</td>
                <td><span class="badge badge-member">{m['membership_type']}</span></td>
                <td>{m['expiry_date']}</td>
                <td><span class="badge badge-{'avail' if m['status'] == 'ACTIVE' else 'overdue'}">{m['status']}</span></td>
            </tr>
        ''' for m in members)

        return f'''
        <div class="header-row"><h1>Member Management & Patron Registry</h1></div>
        <div class="card">
            <h2>? Add New Library Member</h2>
            <form method="POST" action="/librarian/dashboard">
                <input type="hidden" name="action" value="add_member">
                <div class="form-grid">
                    <div class="form-group"><label>First Name *</label><input type="text" name="first_name" required placeholder="Jane"></div>
                    <div class="form-group"><label>Last Name *</label><input type="text" name="last_name" required placeholder="Doe"></div>
                    <div class="form-group"><label>Email *</label><input type="email" name="email" required placeholder="jane.doe@university.edu"></div>
                </div>
                <div class="form-grid">
                    <div class="form-group"><label>Phone Number *</label><input type="text" name="phone" required placeholder="+1 555-0199"></div>
                    <div class="form-group"><label>Membership Tier *</label>
                        <select name="tier">
                            <option value="STUDENT">STUDENT (Quota: 3, 14 Days)</option>
                            <option value="FACULTY">FACULTY (Quota: 10, 30 Days)</option>
                            <option value="STAFF">STAFF (Quota: 5, 21 Days)</option>
                            <option value="GENERAL">GENERAL (Quota: 2, 7 Days)</option>
                        </select>
                    </div>
                    <div class="form-group"><label>Address</label><input type="text" name="address" value="Campus West Dormitory"></div>
                </div>
                <button type="submit" class="btn btn-success">+ Register Member & Issue Card</button>
            </form>
        </div>

        <div class="card">
            <h2>?? Registered Patrons Directory</h2>
            <form method="GET" action="/librarian/dashboard" class="search-bar">
                <input type="hidden" name="tab" value="members">
                <input type="text" name="q" value="{q}" placeholder="Search member by name or code (e.g. MEM-2026)...">
                <button type="submit" class="btn">Search</button>
            </form>
            <table><thead><tr><th>Card Code</th><th>Full Name</th><th>Email</th><th>Phone</th><th>Tier</th><th>Expiration</th><th>Status</th></tr></thead><tbody>{member_rows or "<tr><td colspan='7' class='empty-state'>No members found.</td></tr>"}</tbody></table>
        </div>
        '''

    def render_books(self, query):
        q = query.get("q", "")
        books, total = self.app.book_svc.search(BookFilter(query=q, limit=50))
        book_select_opts = "".join(f"<option value='{b.book_id}'>{b.title} (ISBN: {b.isbn})</option>" for b in books)

        rows = "".join(f'''
            <tr>
                <td><code>{b.isbn}</code></td>
                <td><strong>{b.title}</strong></td>
                <td>{b.author_name or '-'}</td>
                <td>{b.category_name or '-'}</td>
                <td>Shelf {b.shelf_number}</td>
                <td>{b.total_copies}</td>
                <td><span class="badge badge-{'avail' if b.available_copies > 0 else 'overdue'}">{b.available_copies} Available</span></td>
                <td>${b.price:.2f}</td>
            </tr>
        ''' for b in books)

        return f'''
        <div class="header-row"><h1>Book Inventory & Availability Verification</h1></div>
        <div class="card">
            <h2>? Add Physical Copy to Title</h2>
            <form method="POST" action="/librarian/dashboard" style="display:flex;gap:1rem;align-items:flex-end;">
                <input type="hidden" name="action" value="add_copy">
                <div class="form-group" style="flex:1;"><label>Select Book</label><select name="book_id">{book_select_opts}</select></div>
                <div class="form-group" style="width:150px;"><label>Acquisition Cost ($)</label><input type="number" step="0.50" name="cost" value="40.00"></div>
                <button type="submit" class="btn btn-success" style="margin-bottom:0.85rem;">+ Add Copy & Barcode</button>
            </form>
        </div>

        <div class="card">
            <h2>?? Master Book Catalog ({total} Books)</h2>
            <form method="GET" action="/librarian/dashboard" class="search-bar">
                <input type="hidden" name="tab" value="books">
                <input type="text" name="q" value="{q}" placeholder="Search books by title, author, or ISBN...">
                <button type="submit" class="btn">Search</button>
            </form>
            <table><thead><tr><th>ISBN</th><th>Title</th><th>Author</th><th>Genre</th><th>Shelf</th><th>Total</th><th>Status</th><th>Price</th></tr></thead><tbody>{rows or "<tr><td colspan='8' class='empty-state'>No books found.</td></tr>"}</tbody></table>
        </div>
        '''

    def render_transactions(self):
        active_loans = self.app.issue_svc.borrow_repo.list_all_active()
        members = self.app.db_manager.fetch_all("SELECT member_id, member_code, first_name, last_name FROM members WHERE status = 'ACTIVE';")
        copies = self.app.db_manager.fetch_all("""
            SELECT c.copy_id, c.barcode, b.title, b.isbn 
            FROM book_copies c JOIN books b ON c.book_id = b.book_id 
            WHERE c.status = 'AVAILABLE';
        """)

        member_opts = "".join(f"<option value='{m['member_id']}'>{m['first_name']} {m['last_name']} ({m['member_code']})</option>" for m in members)
        copy_opts = "".join(f"<option value='{c['copy_id']}'>{c['title']} - Barcode: {c['barcode']}</option>" for c in copies)
        loan_opts = "".join(f"<option value='{l.borrowing_id}'>#{l.borrowing_id}: {l.book_title} -> {l.member_name} (Due: {l.due_date})</option>" for l in active_loans)

        loan_rows = "".join(f'''
            <tr>
                <td>#{l.borrowing_id}</td>
                <td><strong>{l.book_title}</strong></td>
                <td><code>{l.barcode}</code></td>
                <td>{l.member_name} ({l.member_code})</td>
                <td>{l.issue_date}</td>
                <td><strong>{l.due_date}</strong></td>
                <td><span class="badge badge-{'overdue' if l.is_overdue() else 'issued'}">{l.status}</span></td>
                <td>
                    <form method="POST" action="/librarian/dashboard" style="display:inline;">
                        <input type="hidden" name="action" value="renew_book">
                        <input type="hidden" name="borrowing_id" value="{l.borrowing_id}">
                        <button type="submit" class="btn btn-sm btn-secondary">Renew</button>
                    </form>
                </td>
            </tr>
        ''' for l in active_loans)

        return f'''
        <div class="header-row"><h1>Circulation Transactions Desk</h1></div>

        <div class="grid-2">
            <div class="card">
                <h2>?? Issue Book (Checkout)</h2>
                <form method="POST" action="/librarian/dashboard">
                    <input type="hidden" name="action" value="issue_book">
                    <div class="form-group"><label>Patron Member *</label><select name="member_id">{member_opts}</select></div>
                    <div class="form-group"><label>Available Physical Copy *</label><select name="copy_id">{copy_opts}</select></div>
                    <button type="submit" class="btn btn-success">Issue Book to Patron</button>
                </form>
            </div>

            <div class="card">
                <h2>?? Return Book (Checkin)</h2>
                <form method="POST" action="/librarian/dashboard">
                    <input type="hidden" name="action" value="return_book">
                    <div class="form-group"><label>Active Loan *</label><select name="borrowing_id">{loan_opts}</select></div>
                    <div class="form-group"><label>Inspected Physical Condition *</label>
                        <select name="condition">
                            <option value="GOOD">GOOD (No damage fees)</option>
                            <option value="FAIR">FAIR (Minor wear, no fee)</option>
                            <option value="POOR">POOR (Noticeable wear)</option>
                            <option value="DAMAGED">DAMAGED (Auto assesses repair fee)</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">Process Return & Inspect</button>
                </form>
            </div>
        </div>

        <div class="card">
            <h2>Active Circulation Checkouts ({len(active_loans)} Loans)</h2>
            <table><thead><tr><th>Loan ID</th><th>Book Title</th><th>Barcode</th><th>Patron</th><th>Issued</th><th>Due Date</th><th>Status</th><th>Action</th></tr></thead><tbody>{loan_rows or "<tr><td colspan='8' class='empty-state'>No active loans.</td></tr>"}</tbody></table>
        </div>
        '''

    def render_fines(self):
        fines = self.app.db_manager.fetch_all("""
            SELECT f.*, (m.first_name || ' ' || m.last_name) as member_name, m.member_code 
            FROM fines f JOIN members m ON f.member_id = m.member_id 
            ORDER BY f.fine_id DESC;
        """)

        unpaid_fines = [f for f in fines if f['status'] != 'PAID']
        unpaid_opts = "".join(f"<option value='{f['fine_id']}'>Fine #{f['fine_id']}: {f['member_name']} - ${f['balance_amount']:.2f} ({f['fine_type']})</option>" for f in unpaid_fines)

        fine_rows = "".join(f'''
            <tr>
                <td>#{f['fine_id']}</td>
                <td><strong>{f['member_name']}</strong> ({f['member_code']})</td>
                <td>{f['fine_type']}</td>
                <td>${f['amount']:.2f}</td>
                <td>${f['paid_amount']:.2f}</td>
                <td><strong style="color:var(--danger);">${f['balance_amount']:.2f}</strong></td>
                <td><span class="badge badge-{'avail' if f['status'] == 'PAID' else 'overdue'}">{f['status']}</span></td>
            </tr>
        ''' for f in fines)

        return f'''
        <div class="header-row"><h1>Fine Management & Cashiering Desk</h1></div>

        <div class="card">
            <h2>?? Record Fine Payment & Issue Receipt</h2>
            <form method="POST" action="/librarian/dashboard">
                <input type="hidden" name="action" value="record_payment">
                <div class="form-grid">
                    <div class="form-group"><label>Outstanding Fine *</label><select name="fine_id">{unpaid_opts or "<option value=''>No outstanding unpaid fines</option>"}</select></div>
                    <div class="form-group"><label>Payment Amount ($) *</label><input type="number" step="0.50" name="amount" value="10.00" min="0.50"></div>
                    <div class="form-group"><label>Payment Method *</label>
                        <select name="payment_method">
                            <option value="CASH">CASH</option>
                            <option value="UPI">UPI / Digital QR</option>
                            <option value="CREDIT_CARD">CREDIT CARD</option>
                            <option value="DEBIT_CARD">DEBIT CARD</option>
                        </select>
                    </div>
                </div>
                <button type="submit" class="btn btn-success">Process Payment & Generate Receipt</button>
            </form>
        </div>

        <div class="card">
            <h2>Fines & Fee Ledger</h2>
            <table><thead><tr><th>Fine ID</th><th>Patron</th><th>Type</th><th>Assessed</th><th>Paid</th><th>Outstanding</th><th>Status</th></tr></thead><tbody>{fine_rows or "<tr><td colspan='7' class='empty-state'>No fines recorded.</td></tr>"}</tbody></table>
        </div>
        '''

    def render_notifications(self):
        notifications = self.app.db_manager.fetch_all("""
            SELECT n.*, u.username 
            FROM notifications n JOIN users u ON n.user_id = u.user_id 
            ORDER BY n.notification_id DESC LIMIT 20;
        """)

        rows = "".join(f'''
            <tr>
                <td><small>{n['created_at']}</small></td>
                <td><code>{n['username']}</code></td>
                <td><strong>{n['title']}</strong></td>
                <td>{n['message']}</td>
                <td><span class="badge badge-{'avail' if n['is_read'] else 'pending'}">{'READ' if n['is_read'] else 'UNREAD'}</span></td>
            </tr>
        ''' for n in notifications)

        return f'''
        <div class="header-row"><h1>Notifications & Circulation Alerts</h1></div>
        <div class="card">
            <h2>System Alerts & Patron Reminders</h2>
            <table><thead><tr><th>Timestamp</th><th>Recipient</th><th>Title</th><th>Message</th><th>Status</th></tr></thead><tbody>{rows or "<tr><td colspan='5' class='empty-state'>No notifications.</td></tr>"}</tbody></table>
        </div>
        '''

    def render_reports(self):
        od = self.app.reports.generate_overdue_report()
        fin = self.app.reports.generate_financial_ledger_report()
        return f'''
        <div class="header-row"><h1>Daily Operations Reports</h1></div>
        <div class="card">
            <h2>?? Daily Overdue Summary</h2>
            <textarea readonly style="width:100%;height:130px;font-family:monospace;font-size:0.82rem;padding:0.5rem;background:#f8fafc;">{od['csv']}</textarea>
        </div>
        <div class="card">
            <h2>?? Daily Cashier & Financial Ledger</h2>
            <textarea readonly style="width:100%;height:130px;font-family:monospace;font-size:0.82rem;padding:0.5rem;background:#f8fafc;">{fin['csv']}</textarea>
        </div>
        '''
