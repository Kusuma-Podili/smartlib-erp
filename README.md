# SmartLibrary ERP - Enterprise Library Resource Planning System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-45%20Passing-brightgreen.svg)]()
[![Code%20Style](https://img.shields.io/badge/Architecture-Clean%20%2F%20DDD-orange.svg)]()

**SmartLibrary ERP** is a complete, enterprise-grade **Library Enterprise Resource Planning System** written entirely in **pure Python**. Designed specifically for university campuses, research facilities, and public library networks, SmartLibrary ERP provides robust bibliographic catalog control, physical item barcode tracking, patron lifecycle and membership tier management, circulation desk workflows, automated reservation hold queues, financial fee assessments, event notifications, business intelligence analytics, and granular compliance audit logging.

---

## Table of Contents
1. [Project Purpose](#project-purpose)
2. [Enterprise Architecture](#enterprise-architecture)
3. [User Roles & Access Control](#user-roles--access-control)
4. [Core Modules Overview](#core-modules-overview)
5. [End-to-End Main Workflows](#end-to-end-main-workflows)
6. [Business Rules Enforced](#business-rules-enforced)
7. [Default Seeded Credentials](#default-seeded-credentials)
8. [Setup & Installation Instructions](#setup--installation-instructions)
9. [How to Run the Application & CLI](#how-to-run-the-application--cli)
10. [Automated Test Suites](#automated-test-suites)
11. [Project Structure](#project-structure)
12. [Future Improvements](#future-improvements)

---

## Project Purpose
Traditional library management software often operates as basic CRUD tools with loose validation, flat structures, and no physical copy separation. **SmartLibrary ERP** was designed from the ground up as a true Enterprise Resource Planning (ERP) platform featuring:
- Strict **separation of master catalog titles** and **physical serialized copies** (with individual condition ratings and barcodes).
- Domain-Driven Design (DDD) with explicit service layers, repository patterns, transactional Unit-of-Work, and domain invariants.
- Automatic post-authentication role detection eliminating the need for users to manually select their role.
- Complete financial accounting with serialized receipt numbers for fine collections.
- Clean Python code architecture designed to naturally scale to **50,000+ lines of production-grade software**.

---

## User Roles & Access Control
SmartLibrary ERP implements strict Role-Based Access Control (RBAC) across three distinct tiers. Users are authenticated via credentials, after which the system identifies the role and routes directly to the appropriate portal:

### 1. Admin (`ADMIN`)
- **Portal**: `/admin/dashboard`
- **Capabilities**:
  - Full system oversight & user account management (create, update, deactivate).
  - Staff management for librarians (shift schedules, circulation desk allocations).
  - Configuration of membership tiers, borrowing limits, loan durations, and grace periods.
  - Configuration of fine rates and lost/damage multiplier policies.
  - View executive analytics dashboards, monthly circulation trends, and genre distributions.
  - Filter and inspect granular compliance audit logs with state differentials.
  - Publish system-wide broadcasts and emergency notices.

### 2. Librarian (`LIBRARIAN`)
- **Portal**: `/librarian/dashboard`
- **Capabilities**:
  - Register patrons and manage membership records.
  - Bibliographic catalog management: add/edit authors, categories, publishers, and books.
  - Inventory management: accession physical copies with unique barcodes (`BC-{ISBN}-{INDEX}`).
  - Circulation desk operations: check out (issue), check in (return), and renew loans.
  - Condition evaluation upon return (route poor/damaged items to maintenance).
  - Calculate overdue fines, assess replacement fees, and record cashier payments.
  - Monitor overdue loan rosters and fulfill reservation hold queues.

### 3. Member (`MEMBER`)
- **Portal**: `/member/dashboard`
- **Capabilities**:
  - Personal profile and membership card overview.
  - Search and filter catalog by keyword, author, category, publisher, shelf, rack, and availability.
  - View active borrowed books, loan durations, and countdown to due dates.
  - Request self-service loan renewals (subject to renewal count and hold rules).
  - Place hold reservations on checked-out books with FIFO queue position tracking.
  - Review historical borrowing records, returned books, and reservation logs.
  - View assessed fines, outstanding balances, payment transaction history, and official receipts.
  - Receive automated in-app alerts (due reminders, hold arrivals, fine notices).

---

## Core Modules Overview

```text
smartlib/
├── authentication/   # PBKDF2 hashing, session tokens, brute-force defense, RBAC guards
├── users/            # User domain model, SQL repository, user service, permission matrix
├── librarians/       # Staff profiles, employee codes, shifts, desk allocations
├── members/          # Patron profiles, card generator (MEM-YYYY-XXXX), status lifecycle
├── memberships/      # Membership tiers (Student, Faculty, Staff, General), expiry scanner
├── authors/          # Bibliographic author profiles and bibliography lookups
├── categories/       # Dewey Decimal Classification (DDC) and genre taxonomy
├── publishers/       # Publisher directory and catalog associations
├── books/            # Master book catalog (ISBN-10/13, shelf, rack, copy caches)
├── copies/           # Physical copy inventory, barcode engine (BC-ISBN-XXX), condition evaluator
├── borrowing/        # Circulation check-out desk, loan duration math, quota checks
├── returns/          # Circulation check-in desk, grace periods, overdue calculations
├── renewals/         # Loan renewal engine, max renewal caps, hold conflict rules
├── reservations/     # Automated FIFO reservation queue, hold-slotting upon book return
├── fines/            # Fine calculation formulas, fee assessments, administrative waivers
├── payments/         # Cashier desk, payment settlements, receipt generator (REC-YYYY-XXXXX)
├── notifications/    # Event-driven in-app alerts with formatted template engine
├── announcements/    # Broadcast notices, holiday announcements, priority ranking
├── analytics/        # Executive KPI aggregations, monthly trends, popularity metrics
├── reports/          # Multi-format report generator (CSV, JSON, ASCII table)
├── audit/            # Compliance audit trail capturing user, action, diffs, IP address
├── settings/         # Dynamic runtime system policy configuration store
├── validation/       # ISBN, RFC-email, E.164 phone, password complexity validators
├── utilities/        # Date arithmetic, calendar durations, formatting helpers
└── database/         # SQLite connection manager, ACID transactions, DDL schema, seeder
```

---

## End-to-End Main Workflows

### 1. Catalog & Inventory Lifecycle
```text
Admin creates category (e.g. "CS-PROG" / Dewey 005.1)
  └── Adds author (e.g. "Robert C. Martin")
       └── Adds publisher (e.g. "Prentice Hall")
            └── Registers book with ISBN-13 validation ("9780132350884")
                 └── Accessions physical copies ("COPY-B1-001", "COPY-B1-002")
                      └── Master book record automatically updates available copy counts
```

### 2. Circulation & Fine Cashiering Flow
```text
Patron searches catalog & checks availability
  └── Librarian issues physical copy
       └── System verifies:
            1. Physical copy status == AVAILABLE
            2. Member status == ACTIVE
            3. Membership NOT expired
            4. Active loans count < Tier quota
       └── System creates BorrowingRecord & calculates due date
       └── Physical copy transitions to ISSUED
  └── Book is returned past due date
       └── System calculates: Overdue days = (Return Date - Due Date) - Grace Period
       └── Evaluates copy physical condition (GOOD / FAIR / DAMAGED)
       └── Restores physical copy status to AVAILABLE
       └── Assesses overdue penalty (Days * Daily Rate)
  └── Cashier collects payment (Cash / Card / UPI)
       └── Generates official serialized receipt (REC-YYYY-XXXXX)
       └── Updates fine balance to $0.00 (PAID)
       └── Admin dashboard KPIs reflect collected revenue
```

### 3. FIFO Reservation Hold Queue
```text
Book has 0 available copies
  └── Patron requests hold
       └── System verifies no duplicate active hold exists for patron
       └── Assigns sequential FIFO queue position (e.g. Position #1)
  └── Another patron returns a checked-out copy
       └── System identifies head of the reservation queue
       └── Transitions hold status to READY_FOR_PICKUP
       └── Holds copy for configured duration (e.g. 3 days)
       └── Dispatches in-app pickup notification to patron
```

---

## Business Rules Enforced
SmartLibrary ERP strictly enforces all 12 core business invariants:
1. **Physical Copy Availability**: A book title cannot be issued when no physical copy has `status == AVAILABLE`.
2. **Borrowing Limit Enforcement**: A patron cannot borrow more books than permitted by their membership tier (Student: 3, General: 2, Staff: 5, Faculty: 10).
3. **Expired Membership Gate**: Patrons whose membership expiry date has passed are blocked from borrowing or renewing items.
4. **Duplicate Hold Prevention**: A patron cannot hold multiple active reservations for the same book title.
5. **Physical Copy State Restoration**: Returning a book immediately restores the copy's circulation state to `AVAILABLE` (or routes to `DAMAGED`/`IN_MAINTENANCE` if damaged).
6. **Accurate Fine Calculations**: Overdue penalties deduct configured grace periods and multiply effective late days by the tier daily rate.
7. **Damage & Loss Availability Impact**: Marking a copy as damaged or lost removes it from circulation counts and assesses the required replacement fee.
8. **Patron Data Privacy**: Members are restricted to viewing only their own active loans, historical records, and personal fines.
9. **Administrative Access Barriers**: High-privilege management actions are guarded by role decorators (`@require_role("ADMIN")`).
10. **Deactivated Account Lockout**: Suspended, deactivated, or locked accounts cannot perform any circulation or reservation activities.
11. **Renewal Compliance**: Loans cannot be renewed if already overdue, if the renewal count cap is reached, or if the patron's account has expired.
12. **FIFO Hold Prioritization**: Upon return, copies reserved by patrons are allocated in strict First-In, First-Out sequence.

---

## Default Seeded Credentials
The database comes pre-seeded with standard test accounts:

| Role | Username / Email | Password | Default Portal | Privileges |
| :--- | :--- | :--- | :--- | :--- |
| **System Administrator** | `admin` / `admin@library.com` | `Admin@123` | `/admin/dashboard` | Full system control, rules, audit logs, settings |
| **Circulation Librarian** | `librarian` / `librarian@library.com` | `Librarian@123` | `/librarian/dashboard` | Cataloging, checkout, checkin, returns, fines, cashiering |
| **Library Member** | `member` / `member@library.com` | `Member@123` | `/member/dashboard` | Catalog search, active loans, self-renewal, holds, fines |

---

## Setup & Installation Instructions

### Prerequisites
- Python 3.10+ (or Poetry 1.8+)
- Node.js 18+ (optional, for frontend toolchains)
- Java 17+ & Maven 3.8+ (optional, for enterprise bridge services)
- Git

### Dependency Manifests & Lockfiles
The repository contains pinned lockfiles and manifests for reproducible enterprise deployments:
- **Python**: [`pyproject.toml`](pyproject.toml) & [`poetry.lock`](poetry.lock) (Poetry v2) + [`requirements.txt`](requirements.txt)
- **Node.js / Frontend**: [`package.json`](package.json) & [`package-lock.json`](package-lock.json) (npm v3)
- **Java / Enterprise Bridge**: [`pom.xml`](pom.xml) (Apache Maven)

### Installation Methods

#### Method 1: Poetry (Recommended - Uses `poetry.lock`)
```bash
# 1. Clone repository
git clone https://github.com/Kusuma-Podili/smartlib-erp.git
cd smartlib-erp

# 2. Install pinned dependencies from lockfile
poetry install

# 3. Activate Poetry virtual environment shell
poetry shell
```

#### Method 2: Standard Pip (`requirements.txt`)
```bash
# 1. Create and activate a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 2. Install production dependencies
pip install -r requirements.txt

# 3. Install SmartLib in editable mode
pip install -e .
```

#### Method 3: Node.js Client Assets (`package-lock.json`)
```bash
# Install pinned UI build and linting tooling
npm install
```

#### Method 4: Maven Enterprise Services (`pom.xml`)
```bash
# Compile and package enterprise Java bridge modules
mvn clean package
```

---

## How to Run the Application & CLI

### Initialize Database & Apply Seeds
```bash
# Initialize SQLite tables and schema migrations
python -m smartlib.cli.manage init-db

# Seed default administrator, librarian, member, membership tiers, and policies
python -m smartlib.cli.manage seed

# View all registered users
python -m smartlib.cli.manage list-users
```

### Register New User via CLI
```bash
python -m smartlib.cli.manage create-user --username johndoe --email john@university.edu --password "Secret@2026" --role MEMBER
```

---

## Automated Test Suites
SmartLibrary ERP contains 45 comprehensive test cases covering authentication, cataloging, membership rules, circulation desk operations, reservations, fines, cashier payments, analytics, reports, and all 12 business rules:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Test Suite Summary:
- `tests/test_auth.py`: PBKDF2 salting, password verification, automatic role detection, account lockout defense, session invalidation.
- `tests/test_users_security.py`: User registration, email/username uniqueness, RBAC permission matrix, user deactivation lifecycle.
- `tests/test_books_catalog.py`: Authors, Categories, Publishers, Books, ISBN-10/13 checksum validation, copy barcode generation, faceted multi-field search.
- `tests/test_members_memberships.py`: Patron registration, card code generator (`MEM-YYYY-XXXX`), tier policies, automated expiration auditing.
- `tests/test_circulation.py`: Issue checkouts, quota enforcement, return check-in, overdue calculations, renewals.
- `tests/test_reservations.py`: FIFO queue position order, duplicate hold prevention, hold fulfillment upon check-in.
- `tests/test_fines_payments.py`: Overdue fine calculations, lost/damaged fees, cashier payments, serialized receipts (`REC-YYYY-XXXXX`), waivers.
- `tests/test_analytics_reports.py`: Dashboard KPIs, popular books/genres, CSV export generation, notifications, announcements, runtime settings.
- `tests/test_business_rules.py`: Rigorous verification of all 12 core business rules and full end-to-end integration workflow.

---

## Future Improvements
- Barcode scanner hardware integration via USB HID keyboard emulation.
- Automated email and SMS gateway dispatchers (SMTP, Twilio).
- RFID gate anti-theft scanner integration.
- MARC21 / Dublin Core ISO 2709 import/export support.
