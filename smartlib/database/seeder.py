"""
Enterprise database seeder for SmartLibrary ERP.
Populates complete, realistic demonstration data across:
- Roles & Permissions
- System Policies & Rules
- Membership Tiers
- Users (Admin, Librarians, Patrons)
- Authors, Categories (Dewey Decimal), Publishers
- Master Books Catalog (11 high-impact software/science books)
- Serialized Physical Book Copies with barcodes
- Active Loans, Overdue Loans, and Historical Returns
- Assessed Fines and Cashier Payment Transactions
- FIFO Reservations and Broadcast Announcements
"""

import datetime
from typing import Optional
from smartlib.database.connection import DatabaseManager
from smartlib.constants import (
    UserRole, UserStatus, MembershipType, MembershipStatus,
    BookCopyStatus, BookCopyCondition, BorrowingStatus,
    ReservationStatus, FineType, FineStatus, PaymentMethod,
    AnnouncementPriority
)

class DatabaseSeeder:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def seed_all(self, include_demo: bool = False):
        self.seed_roles()
        self.seed_membership_tiers()
        self.seed_system_settings()
        self.seed_users_and_staff(include_extra_patrons=include_demo)
        if include_demo:
            self.seed_catalog_and_inventory()
            self.seed_circulation_and_fines()
            self.seed_announcements()

    def seed_roles(self):
        roles = [
            ("ADMIN", "System Administrator with full oversight and rule management"),
            ("LIBRARIAN", "Circulation Desk Staff handling loans, checkins, and cashiering"),
            ("MEMBER", "Patron accessing self-service catalog, loans, and holds")
        ]
        for r, d in roles:
            self.db_manager.execute("INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?);", (r, d))
        self.db_manager.get_connection().commit()

    def seed_membership_tiers(self):
        tiers = [
            ("STUDENT", "Student Academic Tier", 3, 14, 1, 2, 5.00, "Enrolled undergraduate and graduate students"),
            ("FACULTY", "Faculty & Research Tier", 10, 60, 3, 4, 2.00, "Teaching, research, and professorial faculty"),
            ("STAFF", "Institutional Staff Tier", 5, 30, 2, 3, 5.00, "University and organizational staff members"),
            ("GENERAL", "General Community Tier", 2, 14, 1, 1, 10.00, "Public community patrons and external visitors")
        ]
        for t in tiers:
            self.db_manager.execute(
                """INSERT OR IGNORE INTO membership_tiers 
                (tier_type, name, max_borrow_limit, loan_duration_days, grace_period_days, max_renewals, daily_fine_rate, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
                t
            )
        self.db_manager.get_connection().commit()

    def seed_system_settings(self):
        settings = [
            ("library_name", "SmartLibrary Enterprise", "GENERAL", "Official library name"),
            ("library_email", "support@smartlibrary.erp", "GENERAL", "Contact email address"),
            ("library_phone", "+1-800-555-0199", "GENERAL", "Main library telephone number"),
            ("default_fine_per_day", "10.00", "CIRCULATION", "Daily overdue fine amount in currency units"),
            ("max_borrowing_limit_default", "5", "CIRCULATION", "Default item borrow limit across all tiers"),
            ("max_renewals_default", "2", "CIRCULATION", "Default maximum renewal count per borrowed copy"),
            ("reservation_hold_days", "3", "CIRCULATION", "Number of days a reserved copy is held on arrival"),
            ("lost_book_charge_multiplier", "1.5", "FINES", "Multiplier applied to book replacement price for lost books")
        ]
        for s in settings:
            self.db_manager.execute(
                """INSERT OR IGNORE INTO system_settings (setting_key, setting_value, category, description)
                VALUES (?, ?, ?, ?);""",
                s
            )
        self.db_manager.get_connection().commit()

    def seed_users_and_staff(self, include_extra_patrons: bool = False):
        from smartlib.authentication.hasher import PasswordHasher
        hasher = PasswordHasher(iterations=1000)

        users_data = [
            # Admins
            ("admin", "admin@library.com", "Admin@123", "ADMIN"),
            # Librarians
            ("librarian", "librarian@library.com", "Librarian@123", "LIBRARIAN"),
            # Members
            ("member", "member@library.com", "Member@123", "MEMBER"),
        ]
        if include_extra_patrons:
            users_data.extend([
                ("bob_staff", "bob@library.com", "Librarian@123", "LIBRARIAN"),
                ("ada_lovelace", "ada@library.com", "Member@123", "MEMBER"),
                ("grace_hopper", "grace@library.com", "Member@123", "MEMBER"),
                ("alan_turing", "alan@library.com", "Member@123", "MEMBER"),
                ("margaret_h", "margaret@library.com", "Member@123", "MEMBER")
            ])

        for uname, email, pwd, role in users_data:
            phash, salt = hasher.hash_password(pwd)
            self.db_manager.execute(
                """INSERT OR IGNORE INTO users (username, email, password_hash, salt, role, status)
                VALUES (?, ?, ?, ?, ?, 'ACTIVE');""",
                (uname, email, phash, salt, role)
            )

        # Librarians metadata
        lib_meta = [
            ("librarian", "EMP-LIB-001", "Alice Librarian", "+1-555-0101", "Circulation Services", "Morning", "Desk 1")
        ]
        if include_extra_patrons:
            lib_meta.append(("bob_staff", "EMP-LIB-002", "Bob Jenkins", "+1-555-0102", "Technical Services", "Evening", "Desk 2"))

        for uname, code, name, phone, dept, shift, desk in lib_meta:
            u = self.db_manager.fetch_one("SELECT user_id FROM users WHERE username = ?;", (uname,))
            if u:
                self.db_manager.execute(
                    """INSERT OR IGNORE INTO librarians (user_id, employee_code, full_name, phone, department, shift, desk_location)
                    VALUES (?, ?, ?, ?, ?, ?, ?);""",
                    (u["user_id"], code, name, phone, dept, shift, desk)
                )

        # Members metadata
        today = datetime.date.today()
        exp_active = (today + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        members_meta = [
            ("member", "MEM-2026-0001", "John", "Patron", "member@library.com", "+1-555-0201", "100 University Ave", "STUDENT", exp_active)
        ]
        if include_extra_patrons:
            members_meta.extend([
                ("ada_lovelace", "MEM-2026-0002", "Ada", "Lovelace", "ada@library.com", "+1-555-0202", "12 Babbage St", "FACULTY", exp_active),
                ("grace_hopper", "MEM-2026-0003", "Grace", "Hopper", "grace@library.com", "+1-555-0203", "45 Arlington Way", "FACULTY", exp_active),
                ("alan_turing", "MEM-2026-0004", "Alan", "Turing", "alan@library.com", "+1-555-0204", "8 Bletchley Park", "STAFF", exp_active),
                ("margaret_h", "MEM-2026-0005", "Margaret", "Hamilton", "margaret@library.com", "+1-555-0205", "Apollo Hall 3", "STUDENT", exp_active)
            ])

        for uname, code, fn, ln, email, phone, addr, mtype, expiry in members_meta:
            u = self.db_manager.fetch_one("SELECT user_id FROM users WHERE username = ?;", (uname,))
            if u:
                self.db_manager.execute(
                    """INSERT OR IGNORE INTO members 
                    (user_id, member_code, first_name, last_name, email, phone, address, membership_type, expiry_date, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'ACTIVE');""",
                    (u["user_id"], code, fn, ln, email, phone, addr, mtype, expiry)
                )

        self.db_manager.get_connection().commit()

    def seed_catalog_and_inventory(self):
        # 1. Authors
        authors = [
            ("Robert C. Martin", "Author of Clean Code and agile engineering pioneer", "American", 1952),
            ("Martin Fowler", "Chief Scientist at ThoughtWorks, author of Refactoring", "British", 1963),
            ("Joshua Bloch", "Java language architect and author of Effective Java", "American", 1961),
            ("Kent Beck", "Creator of Extreme Programming and Test-Driven Development", "American", 1961),
            ("Andrew Hunt & David Thomas", "Authors of The Pragmatic Programmer", "American", 1964),
            ("Donald Knuth", "Computer scientist and creator of TeX", "American", 1938),
            ("Steve McConnell", "Software engineering expert, author of Code Complete", "American", 1962),
            ("Martin Kleppmann", "Researcher in distributed systems at Cambridge", "German", 1983)
        ]
        for name, bio, nat, byear in authors:
            self.db_manager.execute(
                "INSERT OR IGNORE INTO authors (name, biography, nationality, birth_year) VALUES (?, ?, ?, ?);",
                (name, bio, nat, byear)
            )

        # 2. Categories (Dewey Decimal Classification)
        categories = [
            ("CS-PROG", "Computer Programming", "005.1", "Software development, languages, and coding paradigms"),
            ("CS-ARCH", "Software Architecture", "005.12", "System design, enterprise patterns, and scalability"),
            ("CS-ALG", "Algorithms & Data Structures", "005.13", "Mathematical analysis, algorithms, and complexity"),
            ("CS-DATA", "Distributed Systems & Databases", "005.74", "Database engines, consistency, and storage systems"),
            ("CS-AI", "Artificial Intelligence", "006.3", "Machine learning, neural networks, and automated reasoning")
        ]
        for code, name, ddc, desc in categories:
            self.db_manager.execute(
                "INSERT OR IGNORE INTO categories (code, name, dewey_decimal_class, description) VALUES (?, ?, ?, ?);",
                (code, name, ddc, desc)
            )

        # 3. Publishers
        publishers = [
            ("Prentice Hall", "contact@prenhall.com", "+1-800-282-0693", "Upper Saddle River, NJ", "USA"),
            ("Addison-Wesley", "orders@pearson.com", "+1-800-922-0579", "Boston, MA", "USA"),
            ("O'Reilly Media", "support@oreilly.com", "+1-800-889-8969", "Sebastopol, CA", "USA"),
            ("Microsoft Press", "mspress@microsoft.com", "+1-800-642-7676", "Redmond, WA", "USA")
        ]
        for name, email, phone, addr, country in publishers:
            self.db_manager.execute(
                "INSERT OR IGNORE INTO publishers (name, contact_email, phone, address, country) VALUES (?, ?, ?, ?, ?);",
                (name, email, phone, addr, country)
            )
        self.db_manager.get_connection().commit()

        # 4. Master Books
        books = [
            ("9780132350884", "Clean Code: A Handbook of Agile Software Craftsmanship", "A Handbook of Agile Software Craftsmanship", 1, 1, 1, "1st Edition", 2008, "A1", "R1", 45.00),
            ("9780134494166", "Clean Architecture: A Craftsman's Guide to Software Structure", "A Craftsman's Guide", 1, 1, 2, "1st Edition", 2017, "A1", "R2", 48.00),
            ("9780134757599", "Refactoring: Improving the Design of Existing Code", "Second Edition", 2, 2, 1, "2nd Edition", 2018, "A2", "R1", 52.00),
            ("9780134685991", "Effective Java", "Best Practices for the Java Platform", 3, 2, 1, "3rd Edition", 2017, "A2", "R2", 49.99),
            ("9780321146533", "Test-Driven Development: By Example", "TDD Practices", 4, 2, 1, "1st Edition", 2002, "A3", "R1", 39.95),
            ("9780201616224", "The Pragmatic Programmer: Your Journey to Mastery", "20th Anniversary Edition", 5, 2, 1, "2nd Edition", 2019, "A3", "R2", 55.00),
            ("9780735619678", "Code Complete: A Practical Handbook of Software Construction", "Second Edition", 7, 4, 1, "2nd Edition", 2004, "B1", "R1", 50.00),
            ("9781449373320", "Designing Data-Intensive Applications", "The Big Ideas Behind Reliable Systems", 8, 3, 4, "1st Edition", 2017, "B2", "R1", 54.99),
            ("9780201896831", "The Art of Computer Programming: Volume 1", "Fundamental Algorithms", 6, 2, 3, "3rd Edition", 1997, "C1", "R1", 75.00)
        ]
        for isbn, title, sub, aid, pid, cid, ed, yr, shelf, rack, price in books:
            self.db_manager.execute(
                """INSERT OR IGNORE INTO books 
                (isbn, title, subtitle, author_id, publisher_id, category_id, edition, publication_year, shelf_number, rack_number, price, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'AVAILABLE');""",
                (isbn, title, sub, aid, pid, cid, ed, yr, shelf, rack, price)
            )
        self.db_manager.get_connection().commit()

        # 5. Physical Book Copies
        all_books = self.db_manager.fetch_all("SELECT book_id, isbn FROM books;")
        for b in all_books:
            bid = b["book_id"]
            isbn = b["isbn"]
            # Add 3 physical copies per book
            for idx in range(1, 4):
                cnum = f"COPY-B{bid}-{idx:03d}"
                bcode = f"BC-{isbn}-{idx:03d}"
                self.db_manager.execute(
                    """INSERT OR IGNORE INTO book_copies (book_id, copy_number, barcode, condition, status, acquisition_cost)
                    VALUES (?, ?, ?, 'GOOD', 'AVAILABLE', 40.00);""",
                    (bid, cnum, bcode)
                )

            # Update book count caches
            self.db_manager.execute(
                """UPDATE books 
                SET total_copies = 3, available_copies = 3, issued_copies = 0, status = 'AVAILABLE' 
                WHERE book_id = ?;""",
                (bid,)
            )
        self.db_manager.get_connection().commit()

    def seed_circulation_and_fines(self):
        john = self.db_manager.fetch_one("SELECT member_id FROM members WHERE member_code = 'MEM-2026-0001';")
        ada = self.db_manager.fetch_one("SELECT member_id FROM members WHERE member_code = 'MEM-2026-0002';")
        grace = self.db_manager.fetch_one("SELECT member_id FROM members WHERE member_code = 'MEM-2026-0003';")
        lib = self.db_manager.fetch_one("SELECT librarian_id FROM librarians LIMIT 1;")

        john_id = john["member_id"] if john else 1
        ada_id = ada["member_id"] if ada else john_id
        grace_id = grace["member_id"] if grace else john_id
        lib_id = lib["librarian_id"] if lib else 1

        # 1. Issue a book to John Patron (due in 7 days - ACTIVE)
        today = datetime.date.today()
        due_active = (today + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        due_overdue = (today - datetime.timedelta(days=4)).strftime("%Y-%m-%d")
        issue_past = (today - datetime.timedelta(days=18)).strftime("%Y-%m-%d")

        # Loan 1: Clean Code to John Patron (Active, On Time)
        self.db_manager.execute(
            """INSERT OR IGNORE INTO borrowings 
            (borrowing_id, member_id, book_id, copy_id, issued_by_librarian_id, issue_date, due_date, renewal_count, status)
            VALUES (1, ?, 1, 1, ?, ?, ?, 0, 'ACTIVE');""",
            (john_id, lib_id, today.strftime("%Y-%m-%d"), due_active)
        )
        self.db_manager.execute("UPDATE book_copies SET status = 'ISSUED' WHERE copy_id = 1;")
        self.db_manager.execute("UPDATE books SET available_copies = available_copies - 1, issued_copies = issued_copies + 1 WHERE book_id = 1;")

        # Loan 2: Designing Data-Intensive Apps to John Patron (OVERDUE by 4 days)
        self.db_manager.execute(
            """INSERT OR IGNORE INTO borrowings 
            (borrowing_id, member_id, book_id, copy_id, issued_by_librarian_id, issue_date, due_date, renewal_count, status)
            VALUES (2, ?, 8, 22, ?, ?, ?, 0, 'OVERDUE');""",
            (john_id, lib_id, issue_past, due_overdue)
        )
        self.db_manager.execute("UPDATE book_copies SET status = 'ISSUED' WHERE copy_id = 22;")
        self.db_manager.execute("UPDATE books SET available_copies = available_copies - 1, issued_copies = issued_copies + 1 WHERE book_id = 8;")

        # Loan 3: Refactoring to Ada Lovelace (Active)
        self.db_manager.execute(
            """INSERT OR IGNORE INTO borrowings 
            (borrowing_id, member_id, book_id, copy_id, issued_by_librarian_id, issue_date, due_date, renewal_count, status)
            VALUES (3, ?, 3, 7, ?, ?, ?, 0, 'ACTIVE');""",
            (ada_id, lib_id, today.strftime("%Y-%m-%d"), due_active)
        )
        self.db_manager.execute("UPDATE book_copies SET status = 'ISSUED' WHERE copy_id = 7;")
        self.db_manager.execute("UPDATE books SET available_copies = available_copies - 1, issued_copies = issued_copies + 1 WHERE book_id = 3;")

        # Seed an overdue fine for John Patron ($15.00 unpaid)
        self.db_manager.execute(
            """INSERT OR IGNORE INTO fines 
            (fine_id, member_id, borrowing_id, fine_type, amount, paid_amount, balance_amount, status, reason)
            VALUES (1, ?, 2, 'OVERDUE', 15.00, 0.00, 15.00, 'UNPAID', '4 days overdue on Designing Data-Intensive Applications');""",
            (john_id,)
        )

        # Seed a paid fine with receipt for Grace Hopper
        self.db_manager.execute(
            """INSERT OR IGNORE INTO fines 
            (fine_id, member_id, borrowing_id, fine_type, amount, paid_amount, balance_amount, status, reason)
            VALUES (2, ?, NULL, 'PROCESSING_FEE', 10.00, 10.00, 0.00, 'PAID', 'Library Card Replacement Processing Fee');""",
            (grace_id,)
        )
        self.db_manager.execute(
            """INSERT OR IGNORE INTO payments 
            (payment_id, fine_id, member_id, processed_by_librarian_id, amount, payment_method, receipt_number)
            VALUES (1, 2, ?, ?, 10.00, 'UPI', 'REC-2026-00001');""",
            (grace_id, lib_id)
        )

        # Seed a reservation on Effective Java
        self.db_manager.execute(
            """INSERT OR IGNORE INTO reservations 
            (reservation_id, book_id, member_id, queue_position, status)
            VALUES (1, 4, ?, 1, 'PENDING');""",
            (john_id,)
        )

        self.db_manager.get_connection().commit()

    def seed_announcements(self):
        today = datetime.date.today().strftime("%Y-%m-%d")
        end = (datetime.date.today() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        announcements = [
            (1, "Welcome to the New Academic Year 2026", "The library hours are now 8:00 AM - 10:00 PM daily. Enjoy our enhanced collection of digital and physical software engineering literature.", "NORMAL", today, end),
            (1, "Scheduled Maintenance Notice", "Self-service kiosk systems will undergo brief maintenance on Sunday from 2:00 AM to 4:00 AM.", "LOW", today, end),
            (1, "Holiday Closure Announcement", "The main library and study halls will be closed next Monday for institutional holiday.", "HIGH", today, end)
        ]
        for uid, title, content, priority, sdate, edate in announcements:
            self.db_manager.execute(
                """INSERT OR IGNORE INTO announcements (created_by_user_id, title, content, priority, is_published, start_date, end_date)
                VALUES (?, ?, ?, ?, 1, ?, ?);""",
                (uid, title, content, priority, sdate, edate)
            )
        self.db_manager.get_connection().commit()
