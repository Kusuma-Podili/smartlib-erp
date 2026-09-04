"""CSS styling for SmartLibrary ERP Web Portal."""

APP_CSS = """
:root {
    --primary: #F6C7B6;            /* 🍑 Pastel Peach - buttons, active navigation, important actions */
    --primary-hover: #EEB39E;      /* Deeper Peach hover */
    --accent: #D8C9E8;             /* 💜 Pastel Lavender - sidebar accents, secondary cards, highlights */
    --accent-hover: #C6B3DC;       /* Deeper Lavender hover */
    --accent-subtle: #F5EEFC;      /* Soft Lavender tint for table headers & highlights */
    --bg-main: #FFFDF9;            /* Off-white main background */
    --bg-card: #FFFFFF;            /* Clean card background */
    --text-main: #3F3A3A;          /* Dark charcoal primary text */
    --text-muted: #6B6262;         /* Charcoal secondary/muted text */
    --border: #E8DFD8;             /* Warm soft border */
    --border-accent: #D8C9E8;      /* Lavender highlight border */
    --sidebar-bg: #352F31;         /* Deep charcoal sidebar */
    --sidebar-text: #E5DCED;       /* Soft lavender-tinted text */
    --sidebar-hover: #453E41;      /* Subtle hover */
    --sidebar-active: #F6C7B6;     /* Pastel Peach active navigation */
    --sidebar-accent: #D8C9E8;     /* Pastel Lavender sidebar accent */
    --success: #6CA676;            /* Soft sage green */
    --warning: #D8984E;            /* Soft amber */
    --danger: #D66858;             /* Soft coral */
    --info: #8B9FD8;               /* Soft periwinkle */
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg-main); color: var(--text-main); display: flex; flex-direction: column; min-height: 100vh; }
.navbar { background: #352F31; color: #FFFDF9; padding: 0.85rem 1.75rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid var(--primary); box-shadow: 0 2px 8px rgba(53, 47, 49, 0.15); }
.navbar-brand { font-size: 1.25rem; font-weight: 700; color: var(--primary); text-decoration: none; display: flex; align-items: center; gap: 0.5rem; letter-spacing: 0.02em; }
.navbar-user { display: flex; align-items: center; gap: 1rem; font-size: 0.9rem; color: #E5DCED; }
.navbar-user a { color: var(--text-main); text-decoration: none; padding: 0.4rem 0.85rem; border-radius: 6px; background: var(--primary); font-weight: 600; transition: all 0.2s; }
.navbar-user a:hover { background: var(--primary-hover); }
.app-layout { display: flex; flex: 1; }
.sidebar { width: 250px; background: var(--sidebar-bg); color: var(--sidebar-text); padding: 1.5rem 0; flex-shrink: 0; border-right: 1px solid rgba(216, 201, 232, 0.15); }
.sidebar-heading { padding: 0 1.25rem 0.65rem; font-size: 0.76rem; text-transform: uppercase; font-weight: 700; color: var(--sidebar-accent); letter-spacing: 0.08em; border-bottom: 1px solid rgba(216, 201, 232, 0.15); margin-bottom: 0.75rem; }
.sidebar-menu { list-style: none; margin-bottom: 1.5rem; }
.sidebar-menu li a { display: block; padding: 0.75rem 1.25rem; color: var(--sidebar-text); text-decoration: none; font-size: 0.92rem; font-weight: 500; border-left: 4px solid transparent; transition: all 0.18s ease; }
.sidebar-menu li a:hover { background: var(--sidebar-hover); color: #FFFDF9; border-left-color: var(--sidebar-accent); }
.sidebar-menu li.active a { background: var(--primary); color: var(--text-main); font-weight: 700; border-left: 4px solid var(--accent); box-shadow: inset 0 0 0 1px rgba(0,0,0,0.05); }
.main-content { flex: 1; padding: 2rem; overflow-y: auto; background: var(--bg-main); }
.header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.header-row h1 { font-size: 1.6rem; color: var(--text-main); font-weight: 700; }
.grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.25rem; margin-bottom: 1.5rem; }
.grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem; margin-bottom: 1.5rem; }
.kpi-card { background: var(--bg-card); border: 1px solid var(--border); border-left: 4px solid var(--accent); border-radius: 10px; padding: 1.25rem; box-shadow: 0 2px 6px rgba(63, 58, 58, 0.04); }
.kpi-title { font-size: 0.8rem; text-transform: uppercase; color: var(--text-muted); font-weight: 600; letter-spacing: 0.04em; }
.kpi-value { font-size: 1.85rem; font-weight: 800; color: var(--text-main); margin-top: 0.35rem; }
.card { background: var(--bg-card); border: 1px solid var(--border); border-top: 3px solid var(--accent); border-radius: 10px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(63, 58, 58, 0.04); margin-bottom: 1.5rem; }
.card h2 { font-size: 1.2rem; margin-bottom: 1rem; color: var(--text-main); display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }
table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; }
th, td { text-align: left; padding: 0.75rem 0.85rem; border-bottom: 1px solid var(--border); font-size: 0.88rem; color: var(--text-main); }
th { background: var(--accent-subtle); color: var(--text-main); font-weight: 700; border-bottom: 2px solid var(--accent); }
.badge { display: inline-block; padding: 0.25rem 0.6rem; border-radius: 5px; font-size: 0.75rem; font-weight: 700; }
.badge-admin { background: #FDE8E5; color: #8F2218; border: 1px solid #F6C7B6; }
.badge-librarian { background: #F6E6DA; color: #8C4724; border: 1px solid #F6C7B6; }
.badge-member { background: #EDE4F7; color: #513673; border: 1px solid #D8C9E8; }
.badge-avail { background: #E2F2E4; color: #235F2B; }
.badge-issued { background: #EDE4F7; color: #513673; }
.badge-overdue { background: #FDE8E5; color: #8F2218; }
.badge-pending { background: #FFF1DF; color: #8F520B; }
.btn { display: inline-block; background: var(--primary); color: var(--text-main); padding: 0.55rem 1.15rem; border-radius: 8px; text-decoration: none; font-size: 0.9rem; font-weight: 600; border: 1px solid #E5B29F; cursor: pointer; transition: all 0.18s ease; box-shadow: 0 2px 4px rgba(246, 199, 182, 0.35); }
.btn:hover { background: var(--primary-hover); color: #2B2526; transform: translateY(-1px); }
.btn-sm { padding: 0.35rem 0.75rem; font-size: 0.82rem; }
.btn-success { background: var(--primary); color: var(--text-main); border: 1px solid #E5B29F; }
.btn-success:hover { background: var(--primary-hover); }
.btn-secondary { background: var(--accent); color: var(--text-main); border: 1px solid #C5B0DC; box-shadow: 0 2px 4px rgba(216, 201, 232, 0.35); }
.btn-secondary:hover { background: var(--accent-hover); }
.btn-danger { background: #FDD5D0; color: #8F2218; border: 1px solid #F7A8A0; }
.btn-danger:hover { background: #FBBBB3; }
.btn-warning { background: #FFE8CC; color: #8F520B; border: 1px solid #FCD19C; }
.alert { padding: 0.85rem 1.25rem; border-radius: 8px; margin-bottom: 1.25rem; font-size: 0.92rem; font-weight: 500; }
.alert-error { background: #FDE8E5; color: #8F2218; border: 1px solid #F6C7B6; }
.alert-success { background: #EAF6EC; color: #1D5E29; border: 1px solid #BEE4C5; }
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-bottom: 1rem; }
.form-group { margin-bottom: 0.85rem; }
.form-group label { display: block; font-size: 0.84rem; font-weight: 600; color: var(--text-main); margin-bottom: 0.3rem; }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 0.55rem 0.8rem; border: 1px solid var(--border); border-radius: 7px; font-size: 0.92rem; font-family: inherit; color: var(--text-main); background: #FFFFFF; }
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px rgba(216, 201, 232, 0.35); }
.search-bar { display: flex; gap: 0.75rem; margin-bottom: 1.25rem; }
.search-bar input { flex: 1; padding: 0.6rem 0.9rem; border: 1px solid var(--border); border-radius: 7px; font-size: 0.92rem; background: #FFFFFF; color: var(--text-main); }
.empty-state { text-align: center; padding: 2rem; color: var(--text-muted); font-size: 0.9rem; }
footer { text-align: center; padding: 1.5rem; color: var(--text-muted); font-size: 0.85rem; border-top: 1px solid var(--border); background: var(--bg-main); }
"""

def render_shell(title, user, menu_items, active_tab, content, msg="", msg_type="success"):
    # Render clean sidebar navigation links without icons as requested
    menu_html = "".join(f'''
        <li class="{"active" if active_tab == tab_id else ""}">
            <a href="{url}">{name}</a>
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
        <a href="/" class="navbar-brand">SmartLibrary ERP</a>
        <div class="navbar-user">
            <span><strong>{user.get("username")}</strong> ({role_badge})</span>
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
