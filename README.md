# smartlib-erp

# SmartLibrary ERP

**SmartLibrary ERP** is an enterprise-grade Library Enterprise Resource Planning System built entirely in Python. It provides comprehensive automation for modern academic, public, and enterprise library management across Admin, Librarian, and Patron tiers.

## Core Modules & Features
- **Identity & Access**: Secure authentication, PBKDF2/bcrypt hashing, cryptographic session management, role-based access control (Admin, Librarian, Member).
- **Patron Management**: Multi-tier patron registration (Student, Faculty, Staff, General), quota management, automated expiration checks, membership card generation.
- **Master Catalog**: Comprehensive bibliographic control (MARC21/Dublin Core metadata, ISBN-10/13 validation, author bibliographies, Dewey Decimal & genre classification, publishers).
- **Inventory & Copy Tracking**: Item-level barcode tracking (BC-{ISBN}-{NUM}), condition ratings (New, Good, Fair, Damaged), shelf & rack location indexing, maintenance routing.
- **Circulation Desk Engine**: High-throughput book checkout, check-in, loan duration calculators, tier-specific loan quotas, renewals with conflict detection.
- **Reservation Hold Queues**: Automated FIFO reservation queues with hold-slotting and notification upon book return.
- **Financial Ledger & Fine Engine**: Automated overdue penalty calculations, lost/damage charge assessments, cashier desk payments with serialized receipts (REC-YYYY-XXXXX).
- **Communication Center**: In-app event alerts, book due reminders, hold notifications, broadcast announcements.
- **Business Intelligence & Reporting**: Real-time KPI dashboard, monthly circulation trends, genre popularity metrics, multi-format reporting (CSV, JSON, HTML).
- **Compliance & Audit**: Granular audit logging tracking entity diffs, operational events, and administrative actions.
- **System Settings**: Configurable loan periods, grace periods, daily penalty rates, renewal caps.

## Technology Stack
- **Language**: Python 3.10+
- **Architecture**: Domain-Driven Design (DDD), Repository Pattern, Unit of Work
- **Database**: SQLite / Enterprise Relational SQL with foreign key constraints & indexes
- **Security**: Cryptographic password hashing, RBAC route guards, session revocation
- **Testing**: Comprehensive automated test suites with unittest & pytest
