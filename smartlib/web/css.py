"""CSS styling for SmartLibrary ERP Web Portal."""

APP_CSS = """
:root {
    --primary: #1e3a8a;
    --primary-hover: #1d4ed8;
    --sidebar-bg: #0f172a;
    --sidebar-text: #94a3b8;
    --sidebar-hover: #1e293b;
    --sidebar-active: #2563eb;
    --bg-main: #f8fafc;
    --bg-card: #ffffff;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --border: #e2e8f0;
    --success: #16a34a;
    --warning: #d97706;
    --danger: #dc2626;
    --info: #0284c7;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg-main); color: var(--text-main); display: flex; flex-direction: column; min-height: 100vh; }
.navbar { background: var(--primary); color: white; padding: 0.85rem 1.5rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.navbar-brand { font-size: 1.25rem; font-weight: 700; color: white; text-decoration: none; display: flex; align-items: center; gap: 0.5rem; }
.navbar-user { display: flex; align-items: center; gap: 1rem; font-size: 0.9rem; }
.navbar-user a { color: white; text-decoration: none; padding: 0.35rem 0.75rem; border-radius: 4px; background: rgba(255,255,255,0.15); }
.navbar-user a:hover { background: rgba(255,255,255,0.25); }
.app-layout { display: flex; flex: 1; }
.sidebar { width: 250px; background: var(--sidebar-bg); color: var(--sidebar-text); padding: 1.5rem 0; flex-shrink: 0; }
.sidebar-heading { padding: 0 1.25rem 0.5rem; font-size: 0.75rem; text-transform: uppercase; font-weight: 700; color: #64748b; letter-spacing: 0.05em; }
.sidebar-menu { list-style: none; margin-bottom: 1.5rem; }
.sidebar-menu li a { display: flex; align-items: center; gap: 0.75rem; padding: 0.7rem 1.25rem; color: var(--sidebar-text); text-decoration: none; font-size: 0.9rem; font-weight: 500; transition: all 0.15s ease; }
.sidebar-menu li a:hover { background: var(--sidebar-hover); color: white; }
.sidebar-menu li.active a { background: var(--sidebar-active); color: white; }
.main-content { flex: 1; padding: 2rem; overflow-y: auto; }
.header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.header-row h1 { font-size: 1.6rem; color: var(--text-main); font-weight: 700; }
.grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.25rem; margin-bottom: 1.5rem; }
.grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem; margin-bottom: 1.5rem; }
.kpi-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.kpi-title { font-size: 0.8rem; text-transform: uppercase; color: var(--text-muted); font-weight: 600; }
.kpi-value { font-size: 1.8rem; font-weight: 700; color: var(--primary); margin-top: 0.25rem; }
.card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 1.5rem; }
.card h2 { font-size: 1.15rem; margin-bottom: 1rem; color: var(--text-main); display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }
table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; }
th, td { text-align: left; padding: 0.75rem 0.85rem; border-bottom: 1px solid var(--border); font-size: 0.88rem; }
th { background: #f8fafc; color: var(--text-muted); font-weight: 600; }
.badge { display: inline-block; padding: 0.2rem 0.55rem; border-radius: 4px; font-size: 0.75rem; font-weight: 700; }
.badge-admin { background: #fee2e2; color: #991b1b; }
.badge-librarian { background: #fef3c7; color: #92400e; }
.badge-member { background: #dcfce7; color: #166534; }
.badge-avail { background: #dcfce7; color: #166534; }
.badge-issued { background: #e0e7ff; color: #3730a3; }
.badge-overdue { background: #fee2e2; color: #991b1b; }
.badge-pending { background: #fef3c7; color: #92400e; }
.btn { display: inline-block; background: var(--primary); color: white; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; font-size: 0.9rem; font-weight: 500; border: none; cursor: pointer; }
.btn:hover { background: var(--primary-hover); }
.btn-sm { padding: 0.3rem 0.65rem; font-size: 0.8rem; }
.btn-success { background: var(--success); }
.btn-success:hover { background: #15803d; }
.btn-danger { background: var(--danger); }
.btn-danger:hover { background: #b91c1c; }
.btn-warning { background: var(--warning); }
.btn-secondary { background: var(--text-muted); }
.alert { padding: 0.75rem 1.25rem; border-radius: 6px; margin-bottom: 1.25rem; font-size: 0.9rem; }
.alert-error { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }
.alert-success { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-bottom: 1rem; }
.form-group { margin-bottom: 0.85rem; }
.form-group label { display: block; font-size: 0.82rem; font-weight: 600; color: var(--text-main); margin-bottom: 0.25rem; }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 0.5rem 0.75rem; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; font-family: inherit; }
.search-bar { display: flex; gap: 0.75rem; margin-bottom: 1.25rem; }
.search-bar input { flex: 1; padding: 0.55rem 0.85rem; border: 1px solid var(--border); border-radius: 6px; font-size: 0.92rem; }
.empty-state { text-align: center; padding: 2rem; color: var(--text-muted); font-size: 0.9rem; }
footer { text-align: center; padding: 1.5rem; color: var(--text-muted); font-size: 0.85rem; border-top: 1px solid var(--border); }
"""

def render_shell(title, user, menu_items, active_tab, content, msg="", msg_type="success"):
    menu_html = "".join(f'''
        <li class="{"active" if active_tab == tab_id else ""}">
            <a href="{url}">{icon} {name}</a>
        </li>
    ''' for tab_id, name, icon, url in menu_items)
    banner = f'<div class="alert alert-{msg_type}">{msg}</div>' if msg else ""
    role_badge = f'<span class="badge badge-{user["role"].lower()}">{user["role"]}</span>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title} - SmartLibrary ERP</title>
    <style>{APP_CSS}</style>
</head>
<body>
    <header class="navbar">
        <a href="/" class="navbar-brand">📚 SmartLibrary ERP</a>
        <div class="navbar-user">
            <span>👤 <strong>{user.get("username")}</strong> ({role_badge})</span>
            <a href="/logout">Sign Out</a>
        </div>
    </header>
    <div class="app-layout">
        <aside class="sidebar">
            <div class="sidebar-heading">{user["role"]} Navigation</div>
            <ul class="sidebar-menu">{menu_html}</ul>
        </aside>
        <main class="main-content">
            {banner}
            {content}
        </main>
    </div>
    <footer>&copy; 2026 SmartLibrary ERP &bull; Enterprise Library Resource Planning &bull; Pure Python</footer>
</body>
</html>'''
