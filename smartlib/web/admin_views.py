"""Admin Portal Views and Handlers for SmartLibrary ERP."""
from smartlib.web.css import render_shell
from smartlib.books.models import BookDTO, BookFilter
from smartlib.categories.models import CategoryDTO
from smartlib.authors.models import AuthorDTO
from smartlib.copies.models import BookCopyDTO
from smartlib.users.models import UserDTO

ADMIN_MENU = [
    ("overview", "Overview", "&#128202;", "/admin/dashboard?tab=overview"),
    ("books", "Book Management", "&#128218;", "/admin/dashboard?tab=books"),
    ("users", "User Management", "&#128101;", "/admin/dashboard?tab=users"),
    ("operations", "Library Operations", "&#128214;", "/admin/dashboard?tab=operations"),
    ("reports", "Reports & Analytics", "&#128200;", "/admin/dashboard?tab=reports"),
    ("announcements", "Announcements", "&#128276;", "/admin/dashboard?tab=announcements"),
    ("settings", "Settings", "&#9881;", "/admin/dashboard?tab=settings"),
    ("audits", "Audit Logs", "&#128221;", "/admin/dashboard?tab=audits"),
]

class AdminViews:
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

            # 1. Add Book
            if action == "add_book":
                try:
                    dto = BookDTO(
                        isbn=params.get("isbn"), title=params.get("title"), subtitle=params.get("subtitle") or None,
                        author_id=int(params.get("author_id")), publisher_id=int(params.get("publisher_id")),
                        category_id=int(params.get("category_id")), edition=params.get("edition") or "1st Edition",
                        publication_year=int(params.get("publication_year") or 2026), shelf_number=params.get("shelf_number") or "A1",
                        rack_number=params.get("rack_number") or "R1", price=float(params.get("price") or 40.0)
                    )
                    created_book = self.app.book_svc.add_book(dto, actor_username=user["username"])
                    copies_count = int(params.get("copies_count") or 2)
                    self.app.copy_svc.add_multiple_copies(created_book.book_id, count=copies_count, cost=dto.price, actor_username=user["username"])
                    return self.app.redirect(start_response, "/admin/dashboard?tab=books", f"Book '{created_book.title}' added with {copies_count} copies!")
                except Exception as e:
                    return self.app.redirect(start_response, "/admin/dashboard?tab=books", str(e), "error")

            # 2. Add Category
            elif action == "add_category":
                try:
                    cdto = CategoryDTO(code=params.get("code").strip().upper(), name=params.get("name").strip())
                    self.app.category_svc.add_category(cdto, actor_username=user["username"])
                    return self.app.redirect(start_response, "/admin/dashboard?tab=books", f"Category '{cdto.name}' created!")
                except Exception as e:
                    return self.app.redirect(start_response, "/admin/dashboard?tab=books", str(e), "error")

            # 3. Add Author
            elif action == "add_author":
                try:
                    adto = AuthorDTO(name=params.get("name").strip(), nationality=params.get("nationality") or None)
                    self.app.author_svc.add_author(adto, actor_username=user["username"])
                    return self.app.redirect(start_response, "/admin/dashboard?tab=books", f"Author '{adto.name}' added!")
                except Exception as e:
                    return self.app.redirect(start_response, "/admin/dashboard?tab=books", str(e), "error")

            # 4. Add Physical Copy
            elif action == "add_copy":
                try:
                    book_id = int(params.get("book_id"))
                    cost = float(params.get("cost") or 40.0)
                    copy = self.app.copy_svc.add_copy(BookCopyDTO(book_id=book_id, acquisition_cost=cost), actor_username=user["username"])
                    return self.app.redirect(start_response, "/admin/dashboard?tab=books", f"Copy added! Barcode: {copy.barcode}")
                except Exception as e:
                    return self.app.redirect(start_response, "/admin/dashboard?tab=books", str(e), "error")

            # 5. Add Employee
            elif action == "add_employee":
                try:
                    uname = params.get("username").strip().lower()
                    email = params.get("email").strip().lower()
                    pwd = params.get("password") or "Librarian@123"
                    name = params.get("name").strip()
                    shift = params.get("shift", "Morning")
                    desk = params.get("desk", "Desk 1")
                    dept = params.get("department", "Circulation Services")
                    
                    u = self.app.user_svc.register_user(
                        UserDTO(username=uname, email=email, password=pwd, role="LIBRARIAN"),
                        actor_username=user["username"]
                    )
                    self.app.db_manager.execute(
                        "INSERT INTO librarians (user_id, employee_code, full_name, shift, desk_location, department) VALUES (?, ?, ?, ?, ?, ?);",
                        (u.user_id, f"EMP-{u.user_id:03d}", name, shift, desk, dept)
                    )
                    self.app.db_manager.get_connection().commit()
                    return self.app.redirect(start_response, "/admin/dashboard?tab=users", f"Employee {name} registered!")
                except Exception as e:
                    return self.app.redirect(start_response, "/admin/dashboard?tab=users", str(e), "error")

            # 6. Toggle User Status
            elif action == "toggle_user":
                try:
                    uid = int(params.get("user_id"))
                    target_status = params.get("target_status")
                    if target_status == "DEACTIVATE":
                        self.app.user_svc.deactivate_user(uid, actor_username=user["username"])
                        return self.app.redirect(start_response, "/admin/dashboard?tab=users", "User deactivated.")
                    else:
                        self.app.user_svc.activate_user(uid, actor_username=user["username"])
                        return self.app.redirect(start_response, "/admin/dashboard?tab=users", "User activated.")
                except Exception as e:
                    return self.app.redirect(start_response, "/admin/dashboard?tab=users", str(e), "error")

            # 7. Publish Announcement
            elif action == "publish_announcement":
                try:
                    self.app.announce_svc.publish_announcement(user["user_id"], params.get("title"), params.get("content"), params.get("priority", "NORMAL"), actor_username=user["username"])
                    return self.app.redirect(start_response, "/admin/dashboard?tab=announcements", "Announcement published!")
                except Exception as e:
                    return self.app.redirect(start_response, "/admin/dashboard?tab=announcements", str(e), "error")

            # 8. Update Settings
            elif action == "update_settings":
                try:
                    self.app.settings_svc.update_setting("default_fine_per_day", params.get("daily_fine_rate"), actor_username=user["username"])
                    self.app.settings_svc.update_setting("max_renewals_default", params.get("max_renewals"), actor_username=user["username"])
                    self.app.settings_svc.update_setting("reservation_hold_days", params.get("hold_days"), actor_username=user["username"])
                    return self.app.redirect(start_response, "/admin/dashboard?tab=settings", "Settings updated!")
                except Exception as e:
                    return self.app.redirect(start_response, "/admin/dashboard?tab=settings", str(e), "error")

        content = ""
        if tab == "overview": content = self.render_overview()
        elif tab == "books": content = self.render_books(query)
        elif tab == "users": content = self.render_users()
        elif tab == "operations": content = self.render_operations()
        elif tab == "reports": content = self.render_reports()
        elif tab == "announcements": content = self.render_announcements()
        elif tab == "settings": content = self.render_settings()
        elif tab == "audits": content = self.render_audits()
        else: content = self.render_overview()

        html = render_shell("Admin Dashboard", user, ADMIN_MENU, tab, content, msg, msg_type)
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [html.encode("utf-8")]

    def render_overview(self):
        k = self.app.metrics.get_summary_kpis()
        emp_cnt = len(self.app.db_manager.fetch_all("SELECT user_id FROM users WHERE role = 'LIBRARIAN';"))
        pop = self.app.trends.get_popular_books(limit=5)
        aud = self.app.audit_svc.get_recent_activity(limit=5)

        pop_rows = "".join(f"<tr><td><strong>{b['title']}</strong></td><td>{b.get('author_name') or '-'}</td><td><code>{b['isbn']}</code></td><td><span class='badge badge-avail'>{b['borrow_count']} Checkouts</span></td></tr>" for b in pop)
        aud_rows = "".join(f"<tr><td><small>{a.timestamp}</small></td><td><code>{a.username}</code></td><td><span class='badge badge-admin'>{a.action}</span></td><td>{a.description}</td></tr>" for a in aud)

        return f'''
        <div class="header-row">
            <h1>Library Overview & Executive Dashboard</h1>
            <div>
                <a href="/admin/dashboard?tab=books" class="btn btn-sm">+ Add Book</a>
                <a href="/admin/dashboard?tab=reports" class="btn btn-sm btn-secondary">Reports</a>
            </div>
        </div>
        <div class="grid-4">
            <div class="kpi-card"><div class="kpi-title">Total Books</div><div class="kpi-value">{k['total_books']}</div></div>
            <div class="kpi-card"><div class="kpi-title">Total Members</div><div class="kpi-value">{k['total_members']}</div></div>
            <div class="kpi-card"><div class="kpi-title">Total Employees</div><div class="kpi-value">{emp_cnt}</div></div>
            <div class="kpi-card"><div class="kpi-title">Issued Books</div><div class="kpi-value" style="color:var(--primary);">{k['issued_copies']}</div></div>
        </div>
        <div class="grid-4">
            <div class="kpi-card"><div class="kpi-title">Available Books</div><div class="kpi-value" style="color:var(--success);">{k['available_copies']}</div></div>
            <div class="kpi-card"><div class="kpi-title">Overdue Books</div><div class="kpi-value" style="color:var(--danger);">{k['overdue_books']}</div></div>
            <div class="kpi-card"><div class="kpi-title">Total Fines</div><div class="kpi-value">${k['total_fines']:.2f}</div></div>
            <div class="kpi-card"><div class="kpi-title">Collected Revenue</div><div class="kpi-value" style="color:var(--success);">${k['collected_fines']:.2f}</div></div>
        </div>
        <div class="card">
            <h2>Most Popular Books</h2>
            <table><thead><tr><th>Title</th><th>Author</th><th>ISBN</th><th>Checkouts</th></tr></thead><tbody>{pop_rows or "<tr><td colspan='4' class='empty-state'>No data yet.</td></tr>"}</tbody></table>
        </div>
        <div class="card">
            <h2>Recent System Activity</h2>
            <table><thead><tr><th>Time</th><th>User</th><th>Action</th><th>Details</th></tr></thead><tbody>{aud_rows or "<tr><td colspan='4' class='empty-state'>No events.</td></tr>"}</tbody></table>
        </div>
        '''

    def render_books(self, query):
        q = query.get("q", "")
        books, total = self.app.book_svc.search(BookFilter(query=q, limit=50))
        authors = self.app.author_svc.repo.list_all()
        categories = self.app.category_svc.repo.list_all()
        publishers = self.app.publisher_svc.repo.list_all()

        author_opts = "".join(f"<option value='{a.author_id}'>{a.name}</option>" for a in authors)
        cat_opts = "".join(f"<option value='{c.category_id}'>{c.name} ({c.code})</option>" for c in categories)
        pub_opts = "".join(f"<option value='{p.publisher_id}'>{p.name}</option>" for p in publishers)
        book_select_opts = "".join(f"<option value='{b.book_id}'>{b.title}</option>" for b in books)

        rows = "".join(f"<tr><td><code>{b.isbn}</code></td><td><strong>{b.title}</strong></td><td>{b.author_name or '-'}</td><td>{b.category_name or '-'}</td><td>Shelf {b.shelf_number}</td><td>{b.total_copies}</td><td><span class='badge badge-avail'>{b.available_copies}</span></td><td>${b.price:.2f}</td></tr>" for b in books)

        return f'''
        <div class="header-row"><h1>Book Management</h1></div>
        <div class="card">
            <h2>Add Book to Catalog</h2>
            <form method="POST" action="/admin/dashboard">
                <input type="hidden" name="action" value="add_book">
                <div class="form-grid">
                    <div class="form-group"><label>Title *</label><input type="text" name="title" required placeholder="Clean Code"></div>
                    <div class="form-group"><label>Subtitle</label><input type="text" name="subtitle" placeholder="A Handbook..."></div>
                    <div class="form-group"><label>ISBN *</label><input type="text" name="isbn" required placeholder="9780132350884"></div>
                </div>
                <div class="form-grid">
                    <div class="form-group"><label>Author *</label><select name="author_id">{author_opts}</select></div>
                    <div class="form-group"><label>Publisher *</label><select name="publisher_id">{pub_opts}</select></div>
                    <div class="form-group"><label>Category *</label><select name="category_id">{cat_opts}</select></div>
                </div>
                <div class="form-grid">
                    <div class="form-group"><label>Price ($) *</label><input type="number" step="0.01" name="price" value="45.00"></div>
                    <div class="form-group"><label>Physical Copies *</label><input type="number" name="copies_count" value="2" min="1" max="20"></div>
                    <div class="form-group"><label>Shelf</label><input type="text" name="shelf_number" value="A1"></div>
                    <div class="form-group"><label>Rack</label><input type="text" name="rack_number" value="R1"></div>
                </div>
                <button type="submit" class="btn btn-success">+ Save Book & Generate Copies</button>
            </form>
        </div>

        <div class="grid-2">
            <div class="card">
                <h2>Manage Categories</h2>
                <form method="POST" action="/admin/dashboard">
                    <input type="hidden" name="action" value="add_category">
                    <div class="form-group"><label>Category Code *</label><input type="text" name="code" required placeholder="CS-PROG"></div>
                    <div class="form-group"><label>Category Name *</label><input type="text" name="name" required placeholder="Computer Programming"></div>
                    <button type="submit" class="btn btn-sm btn-success">+ Add Category</button>
                </form>
            </div>
            <div class="card">
                <h2>Manage Authors</h2>
                <form method="POST" action="/admin/dashboard">
                    <input type="hidden" name="action" value="add_author">
                    <div class="form-group"><label>Author Name *</label><input type="text" name="name" required placeholder="Robert C. Martin"></div>
                    <div class="form-group"><label>Nationality</label><input type="text" name="nationality" placeholder="American"></div>
                    <button type="submit" class="btn btn-sm btn-success">+ Add Author</button>
                </form>
            </div>
        </div>

        <div class="card">
            <h2>Add Physical Copies to Existing Title</h2>
            <form method="POST" action="/admin/dashboard" style="display:flex;gap:1rem;align-items:flex-end;">
                <input type="hidden" name="action" value="add_copy">
                <div class="form-group" style="flex:1;"><label>Select Book Title</label><select name="book_id">{book_select_opts}</select></div>
                <div class="form-group" style="width:150px;"><label>Unit Cost ($)</label><input type="number" step="0.50" name="cost" value="40.00"></div>
                <button type="submit" class="btn btn-success" style="margin-bottom:0.85rem;">+ Add Physical Copy</button>
            </form>
        </div>

        <div class="card">
            <h2>Master Catalog Titles ({total} Books)</h2>
            <form method="GET" action="/admin/dashboard" class="search-bar">
                <input type="hidden" name="tab" value="books">
                <input type="text" name="q" value="{q}" placeholder="Search books by title, ISBN, or author...">
                <button type="submit" class="btn">Search</button>
            </form>
            <table>
                <thead><tr><th>ISBN</th><th>Title</th><th>Author</th><th>Genre</th><th>Location</th><th>Total</th><th>Avail</th><th>Price</th></tr></thead>
                <tbody>{rows or "<tr><td colspan='8' class='empty-state'>No books found.</td></tr>"}</tbody>
            </table>
        </div>
        '''

    def render_users(self):
        users = self.app.user_svc.repo.list_all()
        librarians = self.app.db_manager.fetch_all("SELECT * FROM librarians;")

        user_rows = "".join(f'''
            <tr>
                <td>#{u.user_id}</td>
                <td><code>{u.username}</code></td>
                <td>{u.email}</td>
                <td><span class="badge badge-{u.role.lower()}">{u.role}</span></td>
                <td><span class="badge badge-{'avail' if u.status == 'ACTIVE' else 'overdue'}">{u.status}</span></td>
                <td>
                    <form method="POST" action="/admin/dashboard" style="display:inline;">
                        <input type="hidden" name="action" value="toggle_user">
                        <input type="hidden" name="user_id" value="{u.user_id}">
                        <input type="hidden" name="target_status" value="{'DEACTIVATE' if u.status == 'ACTIVE' else 'ACTIVATE'}">
                        <button type="submit" class="btn btn-sm {'btn-danger' if u.status == 'ACTIVE' else 'btn-success'}">
                            {'Deactivate' if u.status == 'ACTIVE' else 'Activate'}
                        </button>
                    </form>
                </td>
            </tr>
        ''' for u in users)

        emp_rows = "".join(f"<tr><td><code>{l['employee_code']}</code></td><td><strong>{l['full_name']}</strong></td><td>{l['department']}</td><td>{l['shift']}</td><td>{l['desk_location']}</td></tr>" for l in librarians)

        return f'''
        <div class="header-row"><h1>User & Employee Management</h1></div>

        <div class="card">
            <h2>Add New Librarian / Employee</h2>
            <form method="POST" action="/admin/dashboard">
                <input type="hidden" name="action" value="add_employee">
                <div class="form-grid">
                    <div class="form-group"><label>Full Name *</label><input type="text" name="name" required placeholder="e.g. Sarah Jenkins"></div>
                    <div class="form-group"><label>Username *</label><input type="text" name="username" required placeholder="sarah_j"></div>
                    <div class="form-group"><label>Email *</label><input type="email" name="email" required placeholder="sarah@library.com"></div>
                </div>
                <div class="form-grid">
                    <div class="form-group"><label>Default Password</label><input type="text" name="password" value="Librarian@123"></div>
                    <div class="form-group"><label>Shift</label><select name="shift"><option value="Morning">Morning</option><option value="Evening">Evening</option><option value="Night">Night</option></select></div>
                    <div class="form-group"><label>Desk Location</label><input type="text" name="desk" value="Desk 1"></div>
                </div>
                <button type="submit" class="btn btn-success">+ Register Employee</button>
            </form>
        </div>

        <div class="card">
            <h2>Registered Employees (Librarians)</h2>
            <table><thead><tr><th>Code</th><th>Name</th><th>Department</th><th>Shift</th><th>Desk</th></tr></thead><tbody>{emp_rows}</tbody></table>
        </div>

        <div class="card">
            <h2>System User Accounts & Activation Toggle</h2>
            <table><thead><tr><th>ID</th><th>Username</th><th>Email</th><th>Role</th><th>Status</th><th>Action</th></tr></thead><tbody>{user_rows}</tbody></table>
        </div>
        '''

    def render_operations(self):
        active = self.app.issue_svc.borrow_repo.list_all_active()
        reservations = self.app.db_manager.fetch_all("""
            SELECT r.*, b.title as book_title, (m.first_name || ' ' || m.last_name) as member_name, m.member_code 
            FROM reservations r JOIN books b ON r.book_id = b.book_id JOIN members m ON r.member_id = m.member_id 
            WHERE r.status = 'PENDING';
        """)
        fines = self.app.db_manager.fetch_all("""
            SELECT f.*, (m.first_name || ' ' || m.last_name) as member_name, m.member_code 
            FROM fines f JOIN members m ON f.member_id = m.member_id ORDER BY f.fine_id DESC LIMIT 15;
        """)

        loan_rows = "".join(f"<tr><td>#{l.borrowing_id}</td><td><strong>{l.book_title}</strong></td><td><code>{l.barcode}</code></td><td>{l.member_name} ({l.member_code})</td><td>{l.issue_date}</td><td><strong>{l.due_date}</strong></td><td><span class='badge badge-{'overdue' if l.is_overdue() else 'issued'}'>{l.status}</span></td></tr>" for l in active)
        res_rows = "".join(f"<tr><td>#{r['reservation_id']}</td><td><strong>{r['book_title']}</strong></td><td>{r['member_name']} ({r['member_code']})</td><td>Queue #{r['queue_position']}</td><td><span class='badge badge-pending'>{r['status']}</span></td></tr>" for r in reservations)
        fine_rows = "".join(f"<tr><td>#{f['fine_id']}</td><td>{f['member_name']}</td><td>{f['fine_type']}</td><td>${f['amount']:.2f}</td><td>${f['paid_amount']:.2f}</td><td><strong style='color:var(--danger);'>${f['balance_amount']:.2f}</strong></td><td><span class='badge badge-{'avail' if f['status'] == 'PAID' else 'overdue'}'>{f['status']}</span></td></tr>" for f in fines)

        return f'''
        <div class="header-row"><h1>Library Operations & Circulation Logs</h1></div>
        <div class="card">
            <h2>Active Loans & Circulation</h2>
            <table><thead><tr><th>Loan ID</th><th>Book Title</th><th>Barcode</th><th>Patron</th><th>Issued</th><th>Due Date</th><th>Status</th></tr></thead><tbody>{loan_rows or "<tr><td colspan='7' class='empty-state'>No active loans.</td></tr>"}</tbody></table>
        </div>
        <div class="card">
            <h2>Hold Reservations Queue</h2>
            <table><thead><tr><th>Hold ID</th><th>Book Title</th><th>Patron</th><th>Queue Pos</th><th>Status</th></tr></thead><tbody>{res_rows or "<tr><td colspan='5' class='empty-state'>No active reservations.</td></tr>"}</tbody></table>
        </div>
        <div class="card">
            <h2>Financial Penalties & Fines</h2>
            <table><thead><tr><th>Fine ID</th><th>Patron</th><th>Type</th><th>Assessed</th><th>Paid</th><th>Balance</th><th>Status</th></tr></thead><tbody>{fine_rows or "<tr><td colspan='7' class='empty-state'>No fines.</td></tr>"}</tbody></table>
        </div>
        '''

    def render_reports(self):
        inv = self.app.reports.generate_books_inventory_report()
        od = self.app.reports.generate_overdue_report()
        fin = self.app.reports.generate_financial_ledger_report()
        return f'''
        <div class="header-row"><h1>Reports & Analytics</h1></div>
        <div class="card">
            <h2>Book Inventory & Catalog Report</h2>
            <textarea readonly style="width:100%;height:110px;font-family:monospace;font-size:0.82rem;padding:0.5rem;background:#f8fafc;">{inv['csv']}</textarea>
        </div>
        <div class="card">
            <h2>Overdue Borrowing Report</h2>
            <textarea readonly style="width:100%;height:110px;font-family:monospace;font-size:0.82rem;padding:0.5rem;background:#f8fafc;">{od['csv']}</textarea>
        </div>
        <div class="card">
            <h2>Fine Collections & Financial Ledger Report</h2>
            <textarea readonly style="width:100%;height:110px;font-family:monospace;font-size:0.82rem;padding:0.5rem;background:#f8fafc;">{fin['csv']}</textarea>
        </div>
        '''

    def render_announcements(self):
        active = self.app.announce_svc.list_active_announcements()
        rows = "".join(f"<tr><td><strong>{a.title}</strong></td><td>{a.content}</td><td><span class='badge badge-admin'>{a.priority}</span></td><td>{a.start_date}</td><td>{a.end_date or 'Indefinite'}</td></tr>" for a in active)
        return f'''
        <div class="header-row"><h1>Notifications & Announcements</h1></div>
        <div class="card">
            <h2>Publish Announcement</h2>
            <form method="POST" action="/admin/dashboard">
                <input type="hidden" name="action" value="publish_announcement">
                <div class="form-grid">
                    <div class="form-group"><label>Title *</label><input type="text" name="title" required placeholder="Announcement Title"></div>
                    <div class="form-group"><label>Priority</label><select name="priority"><option value="NORMAL">NORMAL</option><option value="HIGH">HIGH</option><option value="CRITICAL">CRITICAL</option></select></div>
                </div>
                <div class="form-group"><label>Content *</label><textarea name="content" rows="3" required placeholder="Broadcast message..."></textarea></div>
                <button type="submit" class="btn btn-success">Publish Announcement</button>
            </form>
        </div>
        <div class="card">
            <h2>Active Bulletins</h2>
            <table><thead><tr><th>Title</th><th>Message</th><th>Priority</th><th>Start Date</th><th>End Date</th></tr></thead><tbody>{rows or "<tr><td colspan='5' class='empty-state'>No announcements.</td></tr>"}</tbody></table>
        </div>
        '''

    def render_settings(self):
        fine = self.app.settings_svc.get_setting_value("default_fine_per_day", "10.00")
        ren = self.app.settings_svc.get_setting_value("max_renewals_default", "2")
        hold = self.app.settings_svc.get_setting_value("reservation_hold_days", "3")
        return f'''
        <div class="header-row"><h1>Library Policy & System Settings</h1></div>
        <div class="card">
            <h2>Operational Policies</h2>
            <form method="POST" action="/admin/dashboard">
                <input type="hidden" name="action" value="update_settings">
                <div class="form-grid">
                    <div class="form-group"><label>Daily Fine Rate ($)</label><input type="number" step="0.50" name="daily_fine_rate" value="{fine}"></div>
                    <div class="form-group"><label>Max Renewals Limit</label><input type="number" name="max_renewals" value="{ren}"></div>
                    <div class="form-group"><label>Reservation Hold (Days)</label><input type="number" name="hold_days" value="{hold}"></div>
                </div>
                <button type="submit" class="btn btn-success">Save System Settings</button>
            </form>
        </div>
        '''

    def render_audits(self):
        audits = self.app.audit_svc.get_recent_activity(limit=100)
        rows = "".join(f"<tr><td><small>{a.timestamp}</small></td><td><code>{a.username}</code></td><td><span class='badge badge-admin'>{a.action}</span></td><td>{a.entity_type} #{a.entity_id or '-'}</td><td>{a.description}</td></tr>" for a in audits)
        return f'''
        <div class="header-row"><h1>Compliance Audit Logs</h1></div>
        <div class="card">
            <h2>Audit Log Trail</h2>
            <table><thead><tr><th>Timestamp</th><th>User</th><th>Action</th><th>Target</th><th>Details</th></tr></thead><tbody>{rows or "<tr><td colspan='5' class='empty-state'>No audit events.</td></tr>"}</tbody></table>
        </div>
        '''
