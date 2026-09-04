"""
Admin Reports & Analytics Module for SmartLibrary ERP.

Provides:
- Main Navigation Tab: Reports & Analytics
- Section 1: 📈 Analytics Dashboard
  1. Borrowing Trends (Monthly borrowing trends bar chart)
  2. Issue vs Return Comparison (Issued vs Returned ratio & visual bars)
  3. Most Borrowed Books (Top circulated books ranking with live availability)
  4. Book Availability Analysis (Overall ratio & category breakdown bars)
  5. Member Activity (Active borrowers, tier distribution, top patrons)
  6. Fine Collection Trends (Assessed vs Collected vs Outstanding & efficiency)
- Section 2: 📑 Reports
  1. Book Inventory & Catalog Report (Total books, copies, available, issued, lost/damaged,
     breakdown by category/author/publisher, comprehensive search & filters)
  2. Overdue Borrowing Report (Member, book, issue/due dates, days overdue, fine amount,
     status, filters by date, member, book, status)
  3. Fine Collections & Financial Ledger Report (Total generated, collected, outstanding,
     member name, fine amount, payment date, status, payment history, filters)
All currencies rendered in Indian Rupee (₹).
"""

import html
import urllib.parse
from typing import Dict, Any, List

def _escape(val: Any) -> str:
    if val is None:
        return "-"
    return html.escape(str(val))

def _make_csv_data_uri(headers: List[str], rows: List[List[Any]]) -> str:
    """Generate a data:text/csv URI for immediate client-side download."""
    lines = [",".join(f'"{str(h).replace(chr(34), chr(34)+chr(34))}"' for h in headers)]
    for r in rows:
        lines.append(",".join(f'"{str(c).replace(chr(34), chr(34)+chr(34))}"' for c in r))
    csv_text = "\r\n".join(lines)
    return "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_text)

def render_admin_reports_and_analytics(app, query: Dict[str, str]) -> str:
    """Main entrypoint for Admin Reports & Analytics tab."""
    subtab = query.get("subtab", "analytics").strip().lower()
    if subtab not in ("analytics", "inventory", "overdue", "financial"):
        subtab = "analytics"

    # Navigation bar styling and markup
    custom_css = """
    <style>
        .report-header {
            margin-bottom: 1.5rem;
        }
        .report-nav {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1.75rem;
            background: #ffffff;
            padding: 0.6rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            border-top: 3px solid var(--accent);
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }
        .report-nav-item {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.55rem 1.1rem;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-muted);
            transition: all 0.2s ease;
        }
        .report-nav-item:hover {
            color: var(--text-main);
            background: var(--accent-subtle);
        }
        .report-nav-item.active {
            background: var(--primary);
            color: var(--text-main);
            font-weight: 700;
            border: 1px solid #E5B29F;
        }
        .filter-box {
            background: #FAF7FD;
            border: 1px solid var(--border);
            border-left: 4px solid var(--accent);
            border-radius: 8px;
            padding: 1rem 1.25rem;
            margin-bottom: 1.5rem;
        }
        .filter-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 0.85rem;
            align-items: end;
        }
        .chart-bar-row {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.65rem;
            font-size: 0.85rem;
        }
        .chart-bar-label {
            width: 95px;
            font-weight: 600;
            color: var(--text-muted);
            text-align: right;
            flex-shrink: 0;
        }
        .chart-bar-track {
            flex: 1;
            background: #e2e8f0;
            border-radius: 4px;
            height: 20px;
            overflow: hidden;
            display: flex;
        }
        .chart-bar-fill {
            background: var(--primary);
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s ease;
        }
        .chart-bar-val {
            width: 60px;
            font-weight: 700;
            color: var(--text-main);
            padding-left: 0.4rem;
            flex-shrink: 0;
        }
        .progress-multi {
            height: 14px;
            border-radius: 7px;
            background: #e2e8f0;
            display: flex;
            overflow: hidden;
            margin-top: 0.4rem;
        }
        .badge-rank-1 { background: #fef08a; color: #854d0e; font-weight: 800; border: 1px solid #facc15; }
        .badge-rank-2 { background: #e2e8f0; color: #334155; font-weight: 700; }
        .badge-rank-3 { background: #fed7aa; color: #9a3412; font-weight: 700; }
        .badge-rank-other { background: #f1f5f9; color: #64748b; }
        .stat-highlight {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
        }
        .stat-subtext {
            font-size: 0.8rem;
            color: var(--text-muted);
        }
        .btn-download {
            background: #059669;
            color: white;
            padding: 0.4rem 0.8rem;
            border-radius: 5px;
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
        }
        .btn-download:hover { background: #047857; }
    </style>
    """

    nav_html = f"""
    {custom_css}
    <div class="report-header">
        <div class="header-row">
            <div>
                <h1>📊 Reports & Analytics</h1>
                <p style="color:var(--text-muted); font-size:0.9rem; margin-top:0.25rem;">
                    Comprehensive enterprise oversight: circulation analytics, catalog inventory, overdue tracking, and financial ledgers.
                </p>
            </div>
            <div>
                <a href="/admin/dashboard?tab=reports&subtab={subtab}" class="btn btn-sm btn-secondary">&#x21bb; Refresh Data</a>
            </div>
        </div>
    </div>

    <div class="report-nav">
        <a href="/admin/dashboard?tab=reports&subtab=analytics" class="report-nav-item {'active' if subtab == 'analytics' else ''}">
            📈 Analytics Dashboard
        </a>
        <a href="/admin/dashboard?tab=reports&subtab=inventory" class="report-nav-item {'active' if subtab == 'inventory' else ''}">
            📚 Book Inventory & Catalog Report
        </a>
        <a href="/admin/dashboard?tab=reports&subtab=overdue" class="report-nav-item {'active' if subtab == 'overdue' else ''}">
            ⚠️ Overdue Borrowing Report
        </a>
        <a href="/admin/dashboard?tab=reports&subtab=financial" class="report-nav-item {'active' if subtab == 'financial' else ''}">
            💰 Fine Collections & Financial Ledger
        </a>
    </div>
    """

    if subtab == "analytics":
        body = _render_analytics_tab(app)
    elif subtab == "inventory":
        body = _render_inventory_tab(app, query)
    elif subtab == "overdue":
        body = _render_overdue_tab(app, query)
    elif subtab == "financial":
        body = _render_financial_tab(app, query)
    else:
        body = _render_analytics_tab(app)

    return nav_html + body

# ==============================================================================
# 1. 📈 ANALYTICS DASHBOARD
# ==============================================================================

def _render_analytics_tab(app) -> str:
    k = app.metrics.get_summary_kpis()

    # 1. Borrowing Trends (Monthly Borrowing Trends)
    monthly_trends = app.db_manager.fetch_all("""
        SELECT strftime('%Y-%m', issue_date) as month, COUNT(*) as count
        FROM borrowings
        GROUP BY month
        ORDER BY month ASC
        LIMIT 12;
    """)
    if not monthly_trends:
        import datetime
        cur_m = datetime.date.today().strftime("%Y-%m")
        monthly_trends = [{"month": cur_m, "count": 0}]

    max_m_count = max([r["count"] for r in monthly_trends] + [1])
    chart_bars = ""
    for r in monthly_trends:
        pct = max(6, int((r["count"] / max_m_count) * 100)) if r["count"] > 0 else 4
        chart_bars += f"""
        <div class="chart-bar-row">
            <div class="chart-bar-label">{r['month']}</div>
            <div class="chart-bar-track">
                <div class="chart-bar-fill" style="width: {pct}%;"></div>
            </div>
            <div class="chart-bar-val">{r['count']} loans</div>
        </div>
        """

    # 2. Issue vs Return Comparison
    issues_row = app.db_manager.fetch_one("SELECT COUNT(*) as cnt FROM borrowings;")
    returns_row = app.db_manager.fetch_one("SELECT COUNT(*) as cnt FROM returns;")
    total_issues = int(issues_row["cnt"]) if issues_row else 0
    total_returns = int(returns_row["cnt"]) if returns_row else 0
    active_loans = max(0, total_issues - total_returns)
    return_rate = (total_returns / total_issues * 100) if total_issues > 0 else 0.0
    issue_vs_return_bar = f"""
    <div style="margin-top:0.75rem;">
        <div style="display:flex; justify-content:space-between; font-size:0.85rem; font-weight:600; margin-bottom:0.25rem;">
            <span style="color:#2563eb;">Issued: {total_issues}</span>
            <span style="color:#16a34a;">Returned: {total_returns} ({return_rate:.1f}%)</span>
        </div>
        <div class="progress-multi">
            <div style="width:{return_rate:.1f}%; background:#16a34a;" title="Returned: {total_returns}"></div>
            <div style="width:{100.0 - return_rate:.1f}%; background:#2563eb;" title="Active Out: {active_loans}"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:var(--text-muted); margin-top:0.35rem;">
            <span>🟢 Returned: {total_returns}</span>
            <span>🔵 Currently Checked Out: {active_loans}</span>
        </div>
    </div>
    """

    # 3. Most Borrowed Books Ranking
    pop_books = app.db_manager.fetch_all("""
        SELECT b.book_id, b.title, b.isbn, a.name as author_name, c.name as category_name,
               b.available_copies, b.total_copies, COUNT(br.borrowing_id) as borrow_count
        FROM books b
        JOIN borrowings br ON b.book_id = br.book_id
        LEFT JOIN authors a ON b.author_id = a.author_id
        LEFT JOIN categories c ON b.category_id = c.category_id
        GROUP BY b.book_id
        ORDER BY borrow_count DESC
        LIMIT 5;
    """)
    pop_rows = ""
    for idx, b in enumerate(pop_books, start=1):
        rank_badge = f"badge-rank-{idx}" if idx <= 3 else "badge-rank-other"
        avail_badge = f"<span class='badge badge-avail'>{b['available_copies']} / {b['total_copies']} Available</span>" if b['available_copies'] > 0 else "<span class='badge badge-overdue'>Fully Issued</span>"
        pop_rows += f"""
        <tr>
            <td style="width:45px; text-align:center;"><span class="badge {rank_badge}">#{idx}</span></td>
            <td><strong>{_escape(b['title'])}</strong><br><small style="color:var(--text-muted);">{_escape(b['author_name'])} &bull; <code>{_escape(b['isbn'])}</code></small></td>
            <td>{_escape(b['category_name'])}</td>
            <td><strong style="color:var(--primary); font-size:1.05rem;">{b['borrow_count']}</strong> checkouts</td>
            <td>{avail_badge}</td>
        </tr>
        """
    if not pop_rows:
        pop_rows = "<tr><td colspan='5' class='empty-state'>No checkout records accumulated yet.</td></tr>"

    # 4. Book Availability Analysis (Category breakdown & ratios)
    total_c = max(1, k["total_copies"])
    avail_c = k["available_copies"]
    avail_pct = (avail_c / total_c) * 100.0
    issued_pct = (k["issued_copies"] / total_c) * 100.0
    lost_dmg_pct = ((k["lost_copies"] + k["damaged_copies"]) / total_c) * 100.0

    cat_breakdown = app.db_manager.fetch_all("""
        SELECT c.name as category_name, COUNT(b.book_id) as titles_count,
               COALESCE(SUM(b.total_copies), 0) as cat_total,
               COALESCE(SUM(b.available_copies), 0) as cat_avail,
               COALESCE(SUM(b.issued_copies), 0) as cat_issued
        FROM categories c
        LEFT JOIN books b ON c.category_id = b.category_id
        GROUP BY c.category_id
        HAVING cat_total > 0
        ORDER BY cat_total DESC
        LIMIT 6;
    """)
    cat_rows = ""
    for cat in cat_breakdown:
        ctot = max(1, cat["cat_total"])
        cpct = (cat["cat_avail"] / ctot) * 100.0
        cat_rows += f"""
        <div style="margin-bottom: 0.75rem;">
            <div style="display:flex; justify-content:space-between; font-size:0.85rem; font-weight:600;">
                <span>{_escape(cat['category_name'])} ({cat['titles_count']} titles)</span>
                <span>{cat['cat_avail']} / {cat['cat_total']} Avail ({cpct:.0f}%)</span>
            </div>
            <div class="progress-multi">
                <div style="width:{cpct:.1f}%; background:#16a34a;" title="Available"></div>
                <div style="width:{100.0 - cpct:.1f}%; background:#3b82f6;" title="Issued"></div>
            </div>
        </div>
        """

    # 5. Member Activity & Demographics
    active_patrons_cnt = app.db_manager.fetch_one("""
        SELECT COUNT(DISTINCT member_id) as cnt FROM borrowings WHERE status IN ('ACTIVE', 'OVERDUE');
    """)
    active_patrons = int(active_patrons_cnt["cnt"]) if active_patrons_cnt else 0

    tier_dist = app.db_manager.fetch_all("""
        SELECT membership_type, COUNT(*) as cnt FROM members GROUP BY membership_type;
    """)
    tier_badges = " ".join(f"<span class='badge badge-member' style='margin-right:0.3rem; margin-bottom:0.3rem;'>{t['membership_type']}: <strong>{t['cnt']}</strong></span>" for t in tier_dist)

    top_members = app.db_manager.fetch_all("""
        SELECT m.member_id, (m.first_name || ' ' || m.last_name) as full_name, m.member_code, m.membership_type,
               COUNT(br.borrowing_id) as total_borrows,
               SUM(CASE WHEN br.status IN ('ACTIVE', 'OVERDUE') THEN 1 ELSE 0 END) as active_loans
        FROM members m
        JOIN borrowings br ON m.member_id = br.member_id
        GROUP BY m.member_id
        ORDER BY total_borrows DESC
        LIMIT 4;
    """)
    top_member_rows = "".join(f"""
        <tr>
            <td><strong>{_escape(m['full_name'])}</strong><br><small><code>{_escape(m['member_code'])}</code> &bull; {m['membership_type']}</small></td>
            <td><strong style="color:var(--primary);">{m['total_borrows']}</strong> checkouts</td>
            <td><span class="badge badge-{'issued' if m['active_loans'] else 'avail'}">{m['active_loans']} active loans</span></td>
        </tr>
    """ for m in top_members)

    # 6. Fine Collection Trends
    tf = k["total_fines"]
    cf = k["collected_fines"]
    of = k["outstanding_fines"]
    coll_rate = (cf / tf * 100) if tf > 0 else 100.0

    return f"""
    <!-- Summary Cards -->
    <div class="grid-4" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));">
        <div class="kpi-card">
            <div class="kpi-title">Total Books</div>
            <div class="kpi-value">{k['total_books']}</div>
            <div class="stat-subtext">{k['total_copies']} Physical Copies</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Available Books</div>
            <div class="kpi-value" style="color:var(--success);">{k['available_copies']}</div>
            <div class="stat-subtext">{avail_pct:.1f}% In Shelf Stock</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Issued Books</div>
            <div class="kpi-value" style="color:var(--info);">{k['issued_copies']}</div>
            <div class="stat-subtext">{issued_pct:.1f}% Active Circulation</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Total Members</div>
            <div class="kpi-value">{k['total_members']}</div>
            <div class="stat-subtext">{active_patrons} Active Borrowers</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Overdue Books</div>
            <div class="kpi-value" style="color:var(--danger);">{k['overdue_books']}</div>
            <div class="stat-subtext">Requires Patron Follow-up</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Total Fines Assessed</div>
            <div class="kpi-value">₹{tf:.2f}</div>
            <div class="stat-subtext" style="color:var(--success);">₹{cf:.2f} Collected ({coll_rate:.0f}%)</div>
        </div>
    </div>

    <!-- Analytics Section Grid -->
    <div class="grid-2">
        <!-- 1. Borrowing Trends -->
        <div class="card">
            <h2>📈 Monthly Borrowing Trends</h2>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:1rem;">
                Historical loan volume and seasonal checkout momentum across calendar months.
            </p>
            {chart_bars}
        </div>

        <!-- 2. Issue vs Return Comparison -->
        <div class="card">
            <h2>🔄 Issue vs Return Comparison</h2>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">
                Circulation turnaround balance: tracking outbound checkouts vs returned items.
            </p>
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.75rem; text-align:center; margin-bottom:1rem;">
                <div style="background:#eff6ff; padding:0.75rem; border-radius:6px;">
                    <div style="font-size:0.75rem; color:#1e40af; font-weight:700;">TOTAL ISSUED</div>
                    <div style="font-size:1.3rem; font-weight:700; color:#1d4ed8;">{total_issues}</div>
                </div>
                <div style="background:#f0fdf4; padding:0.75rem; border-radius:6px;">
                    <div style="font-size:0.75rem; color:#166534; font-weight:700;">TOTAL RETURNED</div>
                    <div style="font-size:1.3rem; font-weight:700; color:#15803d;">{total_returns}</div>
                </div>
                <div style="background:#fffbeb; padding:0.75rem; border-radius:6px;">
                    <div style="font-size:0.75rem; color:#92400e; font-weight:700;">CIRCULATING</div>
                    <div style="font-size:1.3rem; font-weight:700; color:#b45309;">{active_loans}</div>
                </div>
            </div>
            {issue_vs_return_bar}
        </div>
    </div>

    <!-- 3. Most Borrowed Books Ranking -->
    <div class="card">
        <h2>🏆 Most Borrowed Books (Popularity Ranking)</h2>
        <table>
            <thead>
                <tr>
                    <th style="width:45px;">Rank</th>
                    <th>Book Title & Details</th>
                    <th>Category</th>
                    <th>Total Checkouts</th>
                    <th>Live Availability</th>
                </tr>
            </thead>
            <tbody>
                {pop_rows}
            </tbody>
        </table>
    </div>

    <div class="grid-2">
        <!-- 4. Book Availability Analysis -->
        <div class="card">
            <h2>📊 Book Availability Analysis</h2>
            <div style="margin-bottom:1rem;">
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; font-weight:700; margin-bottom:0.3rem;">
                    <span>Global Shelf Availability: {avail_pct:.1f}%</span>
                    <span>{avail_c} / {total_c} Copies Ready</span>
                </div>
                <div class="progress-multi" style="height:18px;">
                    <div style="width:{avail_pct:.1f}%; background:#16a34a;" title="Available: {avail_c}"></div>
                    <div style="width:{issued_pct:.1f}%; background:#2563eb;" title="Issued: {k['issued_copies']}"></div>
                    <div style="width:{lost_dmg_pct:.1f}%; background:#dc2626;" title="Lost/Damaged: {k['lost_copies'] + k['damaged_copies']}"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:var(--text-muted); margin-top:0.3rem;">
                    <span>🟢 Available: {k['available_copies']}</span>
                    <span>🔵 Issued: {k['issued_copies']}</span>
                    <span>🔴 Lost/Damaged: {k['lost_copies'] + k['damaged_copies']}</span>
                </div>
            </div>
            <h3 style="font-size:0.95rem; margin-top:1.25rem; margin-bottom:0.6rem; color:var(--text-muted); text-transform:uppercase;">Availability By Category</h3>
            {cat_rows or "<div class='empty-state'>No categories populated.</div>"}
        </div>

        <!-- 5. Member Activity -->
        <div class="card">
            <h2>👥 Member Activity & Patron Utilization</h2>
            <div style="display:flex; justify-content:space-between; align-items:center; background:#f8fafc; padding:0.75rem 1rem; border-radius:6px; margin-bottom:1rem; border:1px solid var(--border);">
                <div>
                    <div style="font-size:0.8rem; color:var(--text-muted); font-weight:600;">ACTIVE CIRCULATION PATRONS</div>
                    <div class="stat-highlight">{active_patrons} <span style="font-size:0.9rem; font-weight:500; color:var(--text-muted);">/ {k['total_members']} registered</span></div>
                </div>
                <div>
                    <span class="badge badge-avail">{((active_patrons / max(1, k['total_members'])) * 100):.0f}% Active</span>
                </div>
            </div>
            <div style="margin-bottom:0.85rem;">
                <div style="font-size:0.78rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-bottom:0.35rem;">Membership Tier Breakdown</div>
                {tier_badges}
            </div>
            <h3 style="font-size:0.95rem; margin-top:1.25rem; margin-bottom:0.6rem; color:var(--text-muted); text-transform:uppercase;">Top Active Borrowers</h3>
            <table>
                <thead><tr><th>Patron</th><th>Checkouts</th><th>Active Loans</th></tr></thead>
                <tbody>{top_member_rows or "<tr><td colspan='3' class='empty-state'>No borrower activity yet.</td></tr>"}</tbody>
            </table>
        </div>
    </div>

    <!-- 6. Fine Collection Trends -->
    <div class="card">
        <h2>💰 Fine Collection Trends & Revenue Recovery</h2>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:1rem; margin-bottom:1.25rem;">
            <div style="background:#f8fafc; border:1px solid var(--border); border-radius:6px; padding:1rem;">
                <div style="font-size:0.75rem; color:var(--text-muted); font-weight:700;">TOTAL FINES GENERATED</div>
                <div style="font-size:1.5rem; font-weight:700; color:var(--text-main);">₹{tf:.2f}</div>
            </div>
            <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:6px; padding:1rem;">
                <div style="font-size:0.75rem; color:#166534; font-weight:700;">TOTAL FINES COLLECTED</div>
                <div style="font-size:1.5rem; font-weight:700; color:#16a34a;">₹{cf:.2f}</div>
            </div>
            <div style="background:#fef2f2; border:1px solid #fecaca; border-radius:6px; padding:1rem;">
                <div style="font-size:0.75rem; color:#991b1b; font-weight:700;">OUTSTANDING UNCOLLECTED</div>
                <div style="font-size:1.5rem; font-weight:700; color:#dc2626;">₹{of:.2f}</div>
            </div>
            <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:6px; padding:1rem;">
                <div style="font-size:0.75rem; color:#1e40af; font-weight:700;">FINANCIAL RECOVERY RATE</div>
                <div style="font-size:1.5rem; font-weight:700; color:#2563eb;">{coll_rate:.1f}%</div>
            </div>
        </div>
        <div style="margin-top:0.5rem;">
            <div style="display:flex; justify-content:space-between; font-size:0.85rem; font-weight:600; margin-bottom:0.25rem;">
                <span style="color:#16a34a;">Collected: ₹{cf:.2f} ({coll_rate:.1f}%)</span>
                <span style="color:#dc2626;">Outstanding: ₹{of:.2f}</span>
            </div>
            <div class="progress-multi" style="height:16px;">
                <div style="width:{coll_rate:.1f}%; background:#16a34a;" title="Collected: ₹{cf:.2f}"></div>
                <div style="width:{100.0 - coll_rate:.1f}%; background:#dc2626;" title="Outstanding: ₹{of:.2f}"></div>
            </div>
        </div>
    </div>
    """

# ==============================================================================
# 2. 📚 BOOK INVENTORY & CATALOG REPORT
# ==============================================================================

def _render_inventory_tab(app, query: Dict[str, str]) -> str:
    # Query parameters for filtering
    search_q = query.get("q", "").strip()
    cat_id = query.get("category_id", "").strip()
    auth_id = query.get("author_id", "").strip()
    pub_id = query.get("publisher_id", "").strip()
    avail_filter = query.get("avail", "").strip().upper()

    # Dropdown options
    categories = app.db_manager.fetch_all("SELECT category_id, name FROM categories ORDER BY name ASC;")
    authors = app.db_manager.fetch_all("SELECT author_id, name FROM authors ORDER BY name ASC;")
    publishers = app.db_manager.fetch_all("SELECT publisher_id, name FROM publishers ORDER BY name ASC;")

    cat_options = "".join(f"<option value='{c['category_id']}' {'selected' if cat_id == str(c['category_id']) else ''}>{_escape(c['name'])}</option>" for c in categories)
    auth_options = "".join(f"<option value='{a['author_id']}' {'selected' if auth_id == str(a['author_id']) else ''}>{_escape(a['name'])}</option>" for a in authors)
    pub_options = "".join(f"<option value='{p['publisher_id']}' {'selected' if pub_id == str(p['publisher_id']) else ''}>{_escape(p['name'])}</option>" for p in publishers)

    # Build dynamic filter SQL
    where_clauses = ["1=1"]
    params = []

    if search_q:
        where_clauses.append("(b.title LIKE ? OR b.isbn LIKE ?)")
        params.extend([f"%{search_q}%", f"%{search_q}%"])
    if cat_id and cat_id.isdigit():
        where_clauses.append("b.category_id = ?")
        params.append(int(cat_id))
    if auth_id and auth_id.isdigit():
        where_clauses.append("b.author_id = ?")
        params.append(int(auth_id))
    if pub_id and pub_id.isdigit():
        where_clauses.append("b.publisher_id = ?")
        params.append(int(pub_id))
    if avail_filter == "AVAILABLE":
        where_clauses.append("b.available_copies > 0")
    elif avail_filter == "ISSUED_OUT":
        where_clauses.append("b.available_copies = 0")
    elif avail_filter == "DAMAGED_LOST":
        where_clauses.append("(b.lost_copies > 0 OR b.damaged_copies > 0)")

    sql = f"""
        SELECT b.book_id, b.isbn, b.title, b.edition, b.publication_year,
               b.shelf_number, b.rack_number, b.price,
               b.total_copies, b.available_copies, b.issued_copies, b.lost_copies, b.damaged_copies,
               a.name as author_name, c.name as category_name, p.name as publisher_name
        FROM books b
        LEFT JOIN authors a ON b.author_id = a.author_id
        LEFT JOIN categories c ON b.category_id = c.category_id
        LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
        WHERE {' AND '.join(where_clauses)}
        ORDER BY b.title ASC;
    """
    books = app.db_manager.fetch_all(sql, tuple(params) if params else ())

    # Overall totals (regardless of filter or filtered)
    tot_books = len(books)
    tot_copies = sum(b["total_copies"] for b in books)
    tot_avail = sum(b["available_copies"] for b in books)
    tot_issued = sum(b["issued_copies"] for b in books)
    tot_lost_dmg = sum(b["lost_copies"] + b["damaged_copies"] for b in books)

    # Breakdown queries for Category, Author, Publisher
    by_cat = app.db_manager.fetch_all("""
        SELECT c.name, COUNT(b.book_id) as cnt, SUM(b.total_copies) as copies
        FROM categories c JOIN books b ON c.category_id = b.category_id
        GROUP BY c.category_id ORDER BY cnt DESC LIMIT 5;
    """)
    by_auth = app.db_manager.fetch_all("""
        SELECT a.name, COUNT(b.book_id) as cnt, SUM(b.total_copies) as copies
        FROM authors a JOIN books b ON a.author_id = b.author_id
        GROUP BY a.author_id ORDER BY cnt DESC LIMIT 5;
    """)
    by_pub = app.db_manager.fetch_all("""
        SELECT p.name, COUNT(b.book_id) as cnt, SUM(b.total_copies) as copies
        FROM publishers p JOIN books b ON p.publisher_id = b.publisher_id
        GROUP BY p.publisher_id ORDER BY cnt DESC LIMIT 5;
    """)

    cat_chips = " ".join(f"<span class='badge' style='background:#f1f5f9; color:#334155; margin-bottom:0.25rem;'>{_escape(r['name'])}: <strong>{r['cnt']} books</strong></span>" for r in by_cat)
    auth_chips = " ".join(f"<span class='badge' style='background:#f1f5f9; color:#334155; margin-bottom:0.25rem;'>{_escape(r['name'])}: <strong>{r['cnt']} books</strong></span>" for r in by_auth)
    pub_chips = " ".join(f"<span class='badge' style='background:#f1f5f9; color:#334155; margin-bottom:0.25rem;'>{_escape(r['name'])}: <strong>{r['cnt']} books</strong></span>" for r in by_pub)

    # Prepare data for table and CSV download
    csv_headers = ["ISBN", "Title", "Author", "Category", "Publisher", "Shelf/Rack", "Total Copies", "Available Copies", "Issued Copies", "Lost/Damaged", "Price (INR)"]
    csv_rows = []

    table_rows = ""
    for b in books:
        lost_dmg = b["lost_copies"] + b["damaged_copies"]
        status_badge = "<span class='badge badge-avail'>AVAILABLE</span>" if b["available_copies"] > 0 else "<span class='badge badge-overdue'>ALL ISSUED</span>"
        if lost_dmg > 0 and b["available_copies"] == 0:
            status_badge = "<span class='badge badge-admin'>DEFICIT</span>"

        csv_rows.append([
            b["isbn"], b["title"], b["author_name"] or "-", b["category_name"] or "-", b["publisher_name"] or "-",
            f"Shelf {b['shelf_number']} / {b['rack_number']}", b["total_copies"], b["available_copies"], b["issued_copies"],
            lost_dmg, f"₹{b['price']:.2f}"
        ])

        table_rows += f"""
        <tr>
            <td><code>{_escape(b['isbn'])}</code></td>
            <td><strong>{_escape(b['title'])}</strong><br><small style="color:var(--text-muted);">{_escape(b['edition'])} ({b['publication_year']})</small></td>
            <td>{_escape(b['author_name'])}</td>
            <td>{_escape(b['category_name'])}</td>
            <td>{_escape(b['publisher_name'])}</td>
            <td><code>{_escape(b['shelf_number'])}-{_escape(b['rack_number'])}</code></td>
            <td style="font-weight:700;">{b['total_copies']}</td>
            <td><strong style="color:var(--success);">{b['available_copies']}</strong></td>
            <td><strong style="color:var(--info);">{b['issued_copies']}</strong></td>
            <td><span style="color:{'var(--danger)' if lost_dmg > 0 else 'var(--text-muted)'}; font-weight:600;">{lost_dmg}</span></td>
            <td>₹{b['price']:.2f}</td>
            <td>{status_badge}</td>
        </tr>
        """

    csv_uri = _make_csv_data_uri(csv_headers, csv_rows)

    return f"""
    <!-- Inventory Metrics Summary -->
    <div class="grid-4" style="grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));">
        <div class="kpi-card">
            <div class="kpi-title">Total Books</div>
            <div class="kpi-value">{tot_books}</div>
            <div class="stat-subtext">Catalog Titles</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Total Copies</div>
            <div class="kpi-value">{tot_copies}</div>
            <div class="stat-subtext">Physical Asset Count</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Available Copies</div>
            <div class="kpi-value" style="color:var(--success);">{tot_avail}</div>
            <div class="stat-subtext">Ready for Checkout</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Issued Copies</div>
            <div class="kpi-value" style="color:var(--info);">{tot_issued}</div>
            <div class="stat-subtext">Currently on Loan</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Lost / Damaged Copies</div>
            <div class="kpi-value" style="color:var(--danger);">{tot_lost_dmg}</div>
            <div class="stat-subtext">Deficit Physical Items</div>
        </div>
    </div>

    <!-- Search & Filter Options -->
    <div class="filter-box">
        <form method="GET" action="/admin/dashboard">
            <input type="hidden" name="tab" value="reports">
            <input type="hidden" name="subtab" value="inventory">
            <div class="filter-grid">
                <div class="form-group" style="margin-bottom:0;">
                    <label>Search Keyword</label>
                    <input type="text" name="q" value="{_escape(search_q)}" placeholder="Search Title or ISBN...">
                </div>
                <div class="form-group" style="margin-bottom:0;">
                    <label>Category</label>
                    <select name="category_id">
                        <option value="">All Categories</option>
                        {cat_options}
                    </select>
                </div>
                <div class="form-group" style="margin-bottom:0;">
                    <label>Author</label>
                    <select name="author_id">
                        <option value="">All Authors</option>
                        {auth_options}
                    </select>
                </div>
                <div class="form-group" style="margin-bottom:0;">
                    <label>Publisher</label>
                    <select name="publisher_id">
                        <option value="">All Publishers</option>
                        {pub_options}
                    </select>
                </div>
                <div class="form-group" style="margin-bottom:0;">
                    <label>Availability</label>
                    <select name="avail">
                        <option value="">All Statuses</option>
                        <option value="AVAILABLE" {'selected' if avail_filter == 'AVAILABLE' else ''}>Available Copies Only</option>
                        <option value="ISSUED_OUT" {'selected' if avail_filter == 'ISSUED_OUT' else ''}>All Copies Issued</option>
                        <option value="DAMAGED_LOST" {'selected' if avail_filter == 'DAMAGED_LOST' else ''}>Has Lost / Damaged</option>
                    </select>
                </div>
                <div style="display:flex; gap:0.5rem;">
                    <button type="submit" class="btn" style="flex:1;">Filter</button>
                    <a href="/admin/dashboard?tab=reports&subtab=inventory" class="btn btn-secondary">Reset</a>
                </div>
            </div>
        </form>
    </div>

    <!-- Catalog Breakdowns (Category, Author, Publisher) -->
    <div class="grid-4" style="grid-template-columns: 1fr 1fr 1fr; margin-bottom:1.25rem;">
        <div class="kpi-card" style="padding:1rem;">
            <div class="kpi-title" style="margin-bottom:0.4rem;">Books by Category</div>
            <div>{cat_chips or "<small class='text-muted'>No categories</small>"}</div>
        </div>
        <div class="kpi-card" style="padding:1rem;">
            <div class="kpi-title" style="margin-bottom:0.4rem;">Books by Author</div>
            <div>{auth_chips or "<small class='text-muted'>No authors</small>"}</div>
        </div>
        <div class="kpi-card" style="padding:1rem;">
            <div class="kpi-title" style="margin-bottom:0.4rem;">Books by Publisher</div>
            <div>{pub_chips or "<small class='text-muted'>No publishers</small>"}</div>
        </div>
    </div>

    <!-- Inventory Data Table -->
    <div class="card">
        <h2>
            <span>📚 Catalog Master Inventory ({tot_books} items)</span>
            <a href="{csv_uri}" download="book_inventory_report.csv" class="btn-download">
                📥 Export CSV Report
            </a>
        </h2>
        <div style="overflow-x:auto;">
            <table>
                <thead>
                    <tr>
                        <th>ISBN</th>
                        <th>Book Title</th>
                        <th>Author</th>
                        <th>Category</th>
                        <th>Publisher</th>
                        <th>Location</th>
                        <th>Total</th>
                        <th>Avail</th>
                        <th>Issued</th>
                        <th>Deficit</th>
                        <th>Unit Price (₹)</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows or "<tr><td colspan='12' class='empty-state'>No books found matching the search criteria.</td></tr>"}
                </tbody>
            </table>
        </div>
    </div>
    """

# ==============================================================================
# 3. ⚠️ OVERDUE BORROWING REPORT
# ==============================================================================

def _render_overdue_tab(app, query: Dict[str, str]) -> str:
    member_q = query.get("member_q", "").strip()
    book_q = query.get("book_q", "").strip()
    due_before = query.get("due_before", "").strip()
    status_filter = query.get("status", "OVERDUE").strip().upper()

    where_clauses = ["br.due_date < DATE('now')"]
    params = []

    if status_filter in ("OVERDUE", "ACTIVE"):
        where_clauses.append("br.status = ?")
        params.append(status_filter)
    else:
        where_clauses.append("br.status IN ('ACTIVE', 'OVERDUE')")

    if member_q:
        where_clauses.append("((m.first_name || ' ' || m.last_name) LIKE ? OR m.member_code LIKE ?)")
        params.extend([f"%{member_q}%", f"%{member_q}%"])

    if book_q:
        where_clauses.append("(b.title LIKE ? OR b.isbn LIKE ?)")
        params.extend([f"%{book_q}%", f"%{book_q}%"])

    if due_before:
        where_clauses.append("br.due_date <= ?")
        params.append(due_before)

    sql = f"""
        SELECT br.borrowing_id, (m.first_name || ' ' || m.last_name) as member_name, m.member_code, m.email,
               b.title as book_title, b.isbn, c.barcode, br.issue_date, br.due_date, br.status,
               CAST(ROUND(julianday('now') - julianday(br.due_date)) AS INTEGER) as days_overdue,
               COALESCE(f.amount, CAST(ROUND(julianday('now') - julianday(br.due_date)) AS INTEGER) * 10.00) as fine_amount
        FROM borrowings br
        JOIN members m ON br.member_id = m.member_id
        JOIN books b ON br.book_id = b.book_id
        JOIN book_copies c ON br.copy_id = c.copy_id
        LEFT JOIN fines f ON br.borrowing_id = f.borrowing_id
        WHERE {' AND '.join(where_clauses)}
        ORDER BY br.due_date ASC;
    """
    rows = app.db_manager.fetch_all(sql, tuple(params) if params else ())

    total_overdue = len(rows)
    total_fines = sum(float(r["fine_amount"]) for r in rows)
    max_days = max([int(r["days_overdue"]) for r in rows] + [0])

    csv_headers = ["Loan ID", "Member Name", "Member Code", "Email", "Book Title", "ISBN", "Barcode", "Issue Date", "Due Date", "Days Overdue", "Fine Amount (INR)", "Status"]
    csv_rows = []

    table_rows = ""
    for r in rows:
        days = max(1, int(r["days_overdue"]))
        fine_val = float(r["fine_amount"])
        csv_rows.append([
            r["borrowing_id"], r["member_name"], r["member_code"], r["email"], r["book_title"],
            r["isbn"], r["barcode"], r["issue_date"], r["due_date"], days, f"₹{fine_val:.2f}", r["status"]
        ])

        table_rows += f"""
        <tr>
            <td><code>#{r['borrowing_id']}</code></td>
            <td><strong>{_escape(r['member_name'])}</strong><br><small><code>{_escape(r['member_code'])}</code> &bull; {_escape(r['email'])}</small></td>
            <td><strong>{_escape(r['book_title'])}</strong><br><small><code>{_escape(r['isbn'])}</code> &bull; Barcode: {_escape(r['barcode'])}</small></td>
            <td>{r['issue_date']}</td>
            <td><strong style="color:var(--danger);">{r['due_date']}</strong></td>
            <td><span class="badge badge-overdue">{days} Days Late</span></td>
            <td><strong style="color:var(--danger); font-size:1rem;">₹{fine_val:.2f}</strong></td>
            <td><span class="badge badge-overdue">{r['status']}</span></td>
        </tr>
        """

    csv_uri = _make_csv_data_uri(csv_headers, csv_rows)

    return f"""
    <!-- Overdue KPI Summary -->
    <div class="grid-4" style="grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));">
        <div class="kpi-card">
            <div class="kpi-title">Overdue Borrowings</div>
            <div class="kpi-value" style="color:var(--danger);">{total_overdue}</div>
            <div class="stat-subtext">Active Defaulted Loans</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Accrued Overdue Fines</div>
            <div class="kpi-value" style="color:var(--danger);">₹{total_fines:.2f}</div>
            <div class="stat-subtext">Calculated Fine Liability</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Longest Overdue Period</div>
            <div class="kpi-value">{max_days} Days</div>
            <div class="stat-subtext">Maximum Default Duration</div>
        </div>
    </div>

    <!-- Filter Form -->
    <div class="filter-box">
        <form method="GET" action="/admin/dashboard">
            <input type="hidden" name="tab" value="reports">
            <input type="hidden" name="subtab" value="overdue">
            <div class="filter-grid">
                <div class="form-group" style="margin-bottom:0;">
                    <label>Filter by Member</label>
                    <input type="text" name="member_q" value="{_escape(member_q)}" placeholder="Member name or code...">
                </div>
                <div class="form-group" style="margin-bottom:0;">
                    <label>Filter by Book</label>
                    <input type="text" name="book_q" value="{_escape(book_q)}" placeholder="Book title or ISBN...">
                </div>
                <div class="form-group" style="margin-bottom:0;">
                    <label>Due On or Before</label>
                    <input type="date" name="due_before" value="{_escape(due_before)}">
                </div>
                <div class="form-group" style="margin-bottom:0;">
                    <label>Status</label>
                    <select name="status">
                        <option value="ALL">All Statuses</option>
                        <option value="OVERDUE" {'selected' if status_filter == 'OVERDUE' else ''}>OVERDUE Only</option>
                        <option value="ACTIVE" {'selected' if status_filter == 'ACTIVE' else ''}>ACTIVE Only</option>
                    </select>
                </div>
                <div style="display:flex; gap:0.5rem;">
                    <button type="submit" class="btn" style="flex:1;">Filter</button>
                    <a href="/admin/dashboard?tab=reports&subtab=overdue" class="btn btn-secondary">Reset</a>
                </div>
            </div>
        </form>
    </div>

    <!-- Overdue Table -->
    <div class="card">
        <h2>
            <span>⚠️ Overdue Circulation Ledger ({total_overdue} defaults)</span>
            <a href="{csv_uri}" download="overdue_borrowing_report.csv" class="btn-download">
                📥 Export CSV Report
            </a>
        </h2>
        <div style="overflow-x:auto;">
            <table>
                <thead>
                    <tr>
                        <th>Loan ID</th>
                        <th>Member Details</th>
                        <th>Book & Copy Details</th>
                        <th>Issue Date</th>
                        <th>Due Date</th>
                        <th>Days Overdue</th>
                        <th>Fine Amount (₹)</th>
                        <th>Current Status</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows or "<tr><td colspan='8' class='empty-state'>No overdue loans matching the criteria. Circulation is healthy!</td></tr>"}
                </tbody>
            </table>
        </div>
    </div>
    """

# ==============================================================================
# 4. 💰 FINE COLLECTIONS & FINANCIAL LEDGER REPORT
# ==============================================================================

def _render_financial_tab(app, query: Dict[str, str]) -> str:
    status_filter = query.get("status", "").strip().upper()
    member_q = query.get("member_q", "").strip()
    date_from = query.get("date_from", "").strip()
    date_to = query.get("date_to", "").strip()

    where_clauses = ["1=1"]
    params = []

    if status_filter and status_filter != "ALL":
        where_clauses.append("f.status = ?")
        params.append(status_filter)

    if member_q:
        where_clauses.append("((m.first_name || ' ' || m.last_name) LIKE ? OR m.member_code LIKE ?)")
        params.extend([f"%{member_q}%", f"%{member_q}%"])

    if date_from:
        where_clauses.append("date(f.created_at) >= ?")
        params.append(date_from)
    if date_to:
        where_clauses.append("date(f.created_at) <= ?")
        params.append(date_to)

    sql = f"""
        SELECT f.fine_id, f.fine_type, f.amount, f.paid_amount, f.balance_amount, f.status, f.reason, f.created_at,
               (m.first_name || ' ' || m.last_name) as member_name, m.member_code,
               p.payment_id, p.receipt_number, p.payment_method, p.amount as payment_amount, p.payment_date
        FROM fines f
        JOIN members m ON f.member_id = m.member_id
        LEFT JOIN payments p ON f.fine_id = p.fine_id
        WHERE {' AND '.join(where_clauses)}
        ORDER BY f.fine_id DESC, p.payment_id DESC;
    """
    raw_rows = app.db_manager.fetch_all(sql, tuple(params) if params else ())

    # Group by fine_id to present clean row with payment history
    fines_dict = {}
    for r in raw_rows:
        fid = r["fine_id"]
        if fid not in fines_dict:
            fines_dict[fid] = {
                "fine_id": r["fine_id"],
                "member_name": r["member_name"],
                "member_code": r["member_code"],
                "fine_type": r["fine_type"],
                "amount": float(r["amount"]),
                "paid_amount": float(r["paid_amount"]),
                "balance_amount": float(r["balance_amount"]),
                "status": r["status"],
                "reason": r["reason"] or "-",
                "created_at": r["created_at"],
                "payments": []
            }
        if r["payment_id"]:
            fines_dict[fid]["payments"].append({
                "receipt": r["receipt_number"],
                "method": r["payment_method"],
                "amount": float(r["payment_amount"]),
                "date": r["payment_date"]
            })

    total_gen = sum(f["amount"] for f in fines_dict.values())
    total_col = sum(f["paid_amount"] for f in fines_dict.values())
    total_bal = sum(f["balance_amount"] for f in fines_dict.values())
    rec_pct = (total_col / total_gen * 100) if total_gen > 0 else 100.0

    csv_headers = ["Fine ID", "Member Name", "Member Code", "Type", "Fine Amount (INR)", "Paid (INR)", "Balance (INR)", "Status", "Payment Date", "Payment History", "Assessed Date"]
    csv_rows = []

    table_rows = ""
    for f in fines_dict.values():
        p_history_str = "; ".join(f"Receipt #{p['receipt']} (₹{p['amount']:.2f} via {p['method']} on {p['date']})" for p in f["payments"]) if f["payments"] else "No payments recorded"
        latest_payment_date = f["payments"][0]["date"] if f["payments"] else "-"

        csv_rows.append([
            f["fine_id"], f["member_name"], f["member_code"], f["fine_type"],
            f"₹{f['amount']:.2f}", f"₹{f['paid_amount']:.2f}", f"₹{f['balance_amount']:.2f}",
            f["status"], latest_payment_date, p_history_str, f["created_at"]
        ])

        status_badge = "<span class='badge badge-avail'>PAID</span>" if f["status"] == "PAID" else "<span class='badge badge-overdue'>UNPAID</span>"
        if f["status"] == "PARTIALLY_PAID":
            status_badge = "<span class='badge badge-librarian'>PARTIAL</span>"

        p_history_html = "".join(f"<div style='font-size:0.75rem; color:var(--text-muted);'>🧾 <code>{p['receipt']}</code>: <strong>₹{p['amount']:.2f}</strong> ({p['method']} - {p['date']})</div>" for p in f["payments"]) if f["payments"] else "<small style='color:var(--text-muted);'>Pending payment</small>"

        table_rows += f"""
        <tr>
            <td><code>#{f['fine_id']}</code></td>
            <td><strong>{_escape(f['member_name'])}</strong><br><small><code>{_escape(f['member_code'])}</code></small></td>
            <td><span class="badge" style="background:#f1f5f9; color:#475569;">{_escape(f['fine_type'])}</span><br><small style="color:var(--text-muted);">{_escape(f['reason'])}</small></td>
            <td><strong>₹{f['amount']:.2f}</strong></td>
            <td><strong style="color:var(--success);">₹{f['paid_amount']:.2f}</strong></td>
            <td><strong style="color:{'var(--danger)' if f['balance_amount'] > 0 else 'var(--success)'}; font-size:0.95rem;">₹{f['balance_amount']:.2f}</strong></td>
            <td>{status_badge}</td>
            <td><small>{latest_payment_date}</small></td>
            <td>{p_history_html}</td>
        </tr>
        """

    csv_uri = _make_csv_data_uri(csv_headers, csv_rows)

    return f"""
    <!-- Financial Metrics Summary -->
    <div class="grid-4" style="grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));">
        <div class="kpi-card">
            <div class="kpi-title">Total Fines Generated</div>
            <div class="kpi-value">₹{total_gen:.2f}</div>
            <div class="stat-subtext">Total Incurred Fines</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Total Fines Collected</div>
            <div class="kpi-value" style="color:var(--success);">₹{total_col:.2f}</div>
            <div class="stat-subtext">Realized Revenue</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Outstanding Fines</div>
            <div class="kpi-value" style="color:var(--danger);">₹{total_bal:.2f}</div>
            <div class="stat-subtext">Uncollected Balances</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Collection Rate</div>
            <div class="kpi-value" style="color:var(--primary);">{rec_pct:.1f}%</div>
            <div class="stat-subtext">Financial Realization</div>
        </div>
    </div>

    <!-- Filter Form -->
    <div class="filter-box">
        <form method="GET" action="/admin/dashboard">
            <input type="hidden" name="tab" value="reports">
            <input type="hidden" name="subtab" value="financial">
            <div class="filter-grid">
                <div class="form-group" style="margin-bottom:0;">
                    <label>Payment Status</label>
                    <select name="status">
                        <option value="ALL">All Payment Statuses</option>
                        <option value="UNPAID" {'selected' if status_filter == 'UNPAID' else ''}>UNPAID Fines Only</option>
                        <option value="PAID" {'selected' if status_filter == 'PAID' else ''}>PAID Fines Only</option>
                        <option value="PARTIALLY_PAID" {'selected' if status_filter == 'PARTIALLY_PAID' else ''}>PARTIAL Fines Only</option>
                    </select>
                </div>
                <div class="form-group" style="margin-bottom:0;">
                    <label>Member Search</label>
                    <input type="text" name="member_q" value="{_escape(member_q)}" placeholder="Member name or code...">
                </div>
                <div class="form-group" style="margin-bottom:0;">
                    <label>From Date</label>
                    <input type="date" name="date_from" value="{_escape(date_from)}">
                </div>
                <div class="form-group" style="margin-bottom:0;">
                    <label>To Date</label>
                    <input type="date" name="date_to" value="{_escape(date_to)}">
                </div>
                <div style="display:flex; gap:0.5rem;">
                    <button type="submit" class="btn" style="flex:1;">Filter</button>
                    <a href="/admin/dashboard?tab=reports&subtab=financial" class="btn btn-secondary">Reset</a>
                </div>
            </div>
        </form>
    </div>

    <!-- Financial Ledger Table -->
    <div class="card">
        <h2>
            <span>💰 Fine Collections & Financial Ledger ({len(fines_dict)} records)</span>
            <a href="{csv_uri}" download="financial_ledger_report.csv" class="btn-download">
                📥 Export CSV Report
            </a>
        </h2>
        <div style="overflow-x:auto;">
            <table>
                <thead>
                    <tr>
                        <th>Fine ID</th>
                        <th>Member Details</th>
                        <th>Reason / Type</th>
                        <th>Assessed (₹)</th>
                        <th>Paid (₹)</th>
                        <th>Balance (₹)</th>
                        <th>Status</th>
                        <th>Payment Date</th>
                        <th>Payment History & Receipts</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows or "<tr><td colspan='9' class='empty-state'>No fine records found matching criteria.</td></tr>"}
                </tbody>
            </table>
        </div>
    </div>
    """
