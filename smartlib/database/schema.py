"""
Enterprise Relational DDL Schema definitions for SmartLibrary ERP.
Contains tables, foreign keys, unique indices, and check constraints for all 22 domain models.
"""

SCHEMA_DDL = """
-- 1. Roles Table
CREATE TABLE IF NOT EXISTS roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Permissions Table
CREATE TABLE IF NOT EXISTS permissions (
    permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Role-Permissions Junction Table
CREATE TABLE IF NOT EXISTS role_permissions (
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(permission_id) ON DELETE CASCADE
);

-- 4. Users Table (Core Identity)
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(64) NOT NULL,
    role VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE' NOT NULL,
    failed_login_attempts INTEGER DEFAULT 0 NOT NULL,
    locked_until TIMESTAMP NULL,
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 5. Sessions Table
CREATE TABLE IF NOT EXISTS user_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_token VARCHAR(128) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_revoked BOOLEAN DEFAULT 0 NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 6. Librarians Table (Staff Metadata)
CREATE TABLE IF NOT EXISTS librarians (
    librarian_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    employee_code VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(30),
    department VARCHAR(100) DEFAULT 'General Library',
    shift VARCHAR(30) DEFAULT 'Morning',
    desk_location VARCHAR(50) DEFAULT 'Circulation Desk 1',
    hire_date DATE DEFAULT (DATE('now')),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 7. Membership Tiers Table
CREATE TABLE IF NOT EXISTS membership_tiers (
    tier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tier_type VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    max_borrow_limit INTEGER DEFAULT 3 NOT NULL,
    loan_duration_days INTEGER DEFAULT 14 NOT NULL,
    grace_period_days INTEGER DEFAULT 1 NOT NULL,
    max_renewals INTEGER DEFAULT 2 NOT NULL,
    daily_fine_rate DECIMAL(10,2) DEFAULT 10.00 NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 8. Members Table (Patron Profiles)
CREATE TABLE IF NOT EXISTS members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    member_code VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(30),
    address TEXT,
    membership_type VARCHAR(50) NOT NULL,
    registration_date DATE DEFAULT (DATE('now')) NOT NULL,
    expiry_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE' NOT NULL,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 9. Authors Table
CREATE TABLE IF NOT EXISTS authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) NOT NULL,
    biography TEXT,
    nationality VARCHAR(100),
    birth_year INTEGER,
    death_year INTEGER,
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 10. Categories Table (Dewey Decimal / Genre)
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    dewey_decimal_class VARCHAR(50),
    parent_category_id INTEGER NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (parent_category_id) REFERENCES categories(category_id) ON DELETE SET NULL
);

-- 11. Publishers Table
CREATE TABLE IF NOT EXISTS publishers (
    publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) UNIQUE NOT NULL,
    contact_email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    website VARCHAR(255),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 12. Books Master Table
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    subtitle VARCHAR(255),
    author_id INTEGER NOT NULL,
    publisher_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    edition VARCHAR(50) DEFAULT '1st Edition',
    publication_year INTEGER,
    language VARCHAR(50) DEFAULT 'English',
    description TEXT,
    shelf_number VARCHAR(50) DEFAULT 'A1',
    rack_number VARCHAR(50) DEFAULT 'R1',
    price DECIMAL(10,2) DEFAULT 0.00 NOT NULL,
    total_copies INTEGER DEFAULT 0 NOT NULL,
    available_copies INTEGER DEFAULT 0 NOT NULL,
    issued_copies INTEGER DEFAULT 0 NOT NULL,
    lost_copies INTEGER DEFAULT 0 NOT NULL,
    damaged_copies INTEGER DEFAULT 0 NOT NULL,
    status VARCHAR(30) DEFAULT 'AVAILABLE' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE RESTRICT,
    FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id) ON DELETE RESTRICT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT
);

-- 13. Book Physical Copies Table
CREATE TABLE IF NOT EXISTS book_copies (
    copy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    copy_number VARCHAR(50) UNIQUE NOT NULL,
    barcode VARCHAR(100) UNIQUE NOT NULL,
    condition VARCHAR(30) DEFAULT 'GOOD' NOT NULL,
    status VARCHAR(30) DEFAULT 'AVAILABLE' NOT NULL,
    acquisition_date DATE DEFAULT (DATE('now')),
    acquisition_cost DECIMAL(10,2) DEFAULT 0.00,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
);

-- 14. Borrowing Records Table
CREATE TABLE IF NOT EXISTS borrowings (
    borrowing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    copy_id INTEGER NOT NULL,
    issued_by_librarian_id INTEGER,
    issue_date DATE DEFAULT (DATE('now')) NOT NULL,
    due_date DATE NOT NULL,
    renewal_count INTEGER DEFAULT 0 NOT NULL,
    max_renewals_allowed INTEGER DEFAULT 2 NOT NULL,
    status VARCHAR(30) DEFAULT 'ACTIVE' NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE RESTRICT,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE RESTRICT,
    FOREIGN KEY (copy_id) REFERENCES book_copies(copy_id) ON DELETE RESTRICT,
    FOREIGN KEY (issued_by_librarian_id) REFERENCES librarians(librarian_id) ON DELETE SET NULL
);

-- 15. Return Records Table
CREATE TABLE IF NOT EXISTS returns (
    return_id INTEGER PRIMARY KEY AUTOINCREMENT,
    borrowing_id INTEGER UNIQUE NOT NULL,
    returned_date DATE DEFAULT (DATE('now')) NOT NULL,
    received_by_librarian_id INTEGER,
    overdue_days INTEGER DEFAULT 0 NOT NULL,
    fine_amount DECIMAL(10,2) DEFAULT 0.00 NOT NULL,
    condition_on_return VARCHAR(30) DEFAULT 'GOOD' NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (borrowing_id) REFERENCES borrowings(borrowing_id) ON DELETE CASCADE,
    FOREIGN KEY (received_by_librarian_id) REFERENCES librarians(librarian_id) ON DELETE SET NULL
);

-- 16. Renewal Records Table
CREATE TABLE IF NOT EXISTS renewals (
    renewal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    borrowing_id INTEGER NOT NULL,
    requested_by_member_id INTEGER NOT NULL,
    approved_by_librarian_id INTEGER,
    previous_due_date DATE NOT NULL,
    new_due_date DATE NOT NULL,
    renewal_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (borrowing_id) REFERENCES borrowings(borrowing_id) ON DELETE CASCADE,
    FOREIGN KEY (requested_by_member_id) REFERENCES members(member_id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by_librarian_id) REFERENCES librarians(librarian_id) ON DELETE SET NULL
);

-- 17. Reservations Table
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    reservation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    queue_position INTEGER NOT NULL,
    status VARCHAR(30) DEFAULT 'PENDING' NOT NULL,
    available_since TIMESTAMP NULL,
    hold_expiry_date DATE NULL,
    fulfilled_at TIMESTAMP NULL,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- 18. Fines Table
CREATE TABLE IF NOT EXISTS fines (
    fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    borrowing_id INTEGER NULL,
    fine_type VARCHAR(30) DEFAULT 'OVERDUE' NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    paid_amount DECIMAL(10,2) DEFAULT 0.00 NOT NULL,
    balance_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(30) DEFAULT 'UNPAID' NOT NULL,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE RESTRICT,
    FOREIGN KEY (borrowing_id) REFERENCES borrowings(borrowing_id) ON DELETE SET NULL
);

-- 19. Payments Table
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fine_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    processed_by_librarian_id INTEGER,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(30) DEFAULT 'CASH' NOT NULL,
    receipt_number VARCHAR(100) UNIQUE NOT NULL,
    transaction_reference VARCHAR(100),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    notes TEXT,
    FOREIGN KEY (fine_id) REFERENCES fines(fine_id) ON DELETE RESTRICT,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE RESTRICT,
    FOREIGN KEY (processed_by_librarian_id) REFERENCES librarians(librarian_id) ON DELETE SET NULL
);

-- 20. Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'GENERAL_ANNOUNCEMENT' NOT NULL,
    is_read BOOLEAN DEFAULT 0 NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 21. Announcements Table
CREATE TABLE IF NOT EXISTS announcements (
    announcement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_by_user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    priority VARCHAR(20) DEFAULT 'NORMAL' NOT NULL,
    is_published BOOLEAN DEFAULT 1 NOT NULL,
    start_date DATE DEFAULT (DATE('now')),
    end_date DATE NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (created_by_user_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

-- 22. Audit Logs Table
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NULL,
    username VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(50),
    description TEXT,
    old_values TEXT,
    new_values TEXT,
    ip_address VARCHAR(45),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 23. System Settings Table
CREATE TABLE IF NOT EXISTS system_settings (
    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'GENERAL' NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_books_isbn ON books(isbn);
CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
CREATE INDEX IF NOT EXISTS idx_books_author ON books(author_id);
CREATE INDEX IF NOT EXISTS idx_books_category ON books(category_id);
CREATE INDEX IF NOT EXISTS idx_copies_barcode ON book_copies(barcode);
CREATE INDEX IF NOT EXISTS idx_copies_book ON book_copies(book_id);
CREATE INDEX IF NOT EXISTS idx_members_code ON members(member_code);
CREATE INDEX IF NOT EXISTS idx_members_email ON members(email);
CREATE INDEX IF NOT EXISTS idx_borrowings_member ON borrowings(member_id);
CREATE INDEX IF NOT EXISTS idx_borrowings_copy ON borrowings(copy_id);
CREATE INDEX IF NOT EXISTS idx_borrowings_status ON borrowings(status);
CREATE INDEX IF NOT EXISTS idx_reservations_book ON reservations(book_id);
CREATE INDEX IF NOT EXISTS idx_fines_member ON fines(member_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id, is_read);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token);
"""
