"""
Seed data generator for default Administrator, Librarian, and Patron users,
membership tiers, and library policies.
"""

import logging
import datetime
from typing import Optional
from smartlib.database.connection import DatabaseManager
from smartlib.constants import UserRole, UserStatus, MembershipType, MembershipStatus

logger = logging.getLogger("smartlib.seeder")

class DatabaseSeeder:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def seed_all(self):
        """Seed roles, system settings, membership tiers, and standard default accounts."""
        logger.info("Seeding system tables...")
        self.seed_roles()
        self.seed_membership_tiers()
        self.seed_system_settings()
        self.seed_default_users()
        logger.info("Seeding completed successfully.")

    def seed_roles(self):
        roles = [
            ("ADMIN", "System Administrator with full management and oversight privileges"),
            ("LIBRARIAN", "Circulation Desk Staff managing books, loans, returns, and members"),
            ("MEMBER", "Library Patron with catalog search, loan viewing, hold requests, and fine history")
        ]
        for role, desc in roles:
            self.db_manager.execute(
                "INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?);",
                (role, desc)
            )
        self.db_manager.get_connection().commit()

    def seed_membership_tiers(self):
        tiers = [
            ("STUDENT", "Student Tier", 3, 14, 1, 2, 5.00, "Academic student enrolled in courses"),
            ("FACULTY", "Faculty Tier", 10, 60, 3, 4, 2.00, "Teaching and research faculty members"),
            ("STAFF", "Staff Tier", 5, 30, 2, 3, 5.00, "Administrative and support university staff"),
            ("GENERAL", "General Public", 2, 14, 1, 1, 10.00, "General community patron membership")
        ]
        for t in tiers:
            self.db_manager.execute(
                """
                INSERT OR IGNORE INTO membership_tiers 
                (tier_type, name, max_borrow_limit, loan_duration_days, grace_period_days, max_renewals, daily_fine_rate, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
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
                """
                INSERT OR IGNORE INTO system_settings (setting_key, setting_value, category, description)
                VALUES (?, ?, ?, ?);
                """,
                s
            )
        self.db_manager.get_connection().commit()

    def seed_default_users(self):
        # We import hasher inside method to prevent circular import
        from smartlib.authentication.hasher import PasswordHasher
        hasher = PasswordHasher()

        # 1. Admin: admin@library.com / Admin@123
        admin_pass, admin_salt = hasher.hash_password("Admin@123")
        self.db_manager.execute(
            """
            INSERT OR IGNORE INTO users (username, email, password_hash, salt, role, status)
            VALUES ('admin', 'admin@library.com', ?, ?, 'ADMIN', 'ACTIVE');
            """,
            (admin_pass, admin_salt)
        )

        # 2. Librarian: librarian@library.com / Librarian@123
        lib_pass, lib_salt = hasher.hash_password("Librarian@123")
        self.db_manager.execute(
            """
            INSERT OR IGNORE INTO users (username, email, password_hash, salt, role, status)
            VALUES ('librarian', 'librarian@library.com', ?, ?, 'LIBRARIAN', 'ACTIVE');
            """,
            (lib_pass, lib_salt)
        )
        lib_user = self.db_manager.fetch_one("SELECT user_id FROM users WHERE username = 'librarian';")
        if lib_user:
            self.db_manager.execute(
                """
                INSERT OR IGNORE INTO librarians (user_id, employee_code, full_name, phone, department, shift)
                VALUES (?, 'EMP-LIB-001', 'Alice Librarian', '+1-555-0101', 'Circulation Services', 'Morning');
                """,
                (lib_user["user_id"],)
            )

        # 3. Member: member@library.com / Member@123
        mem_pass, mem_salt = hasher.hash_password("Member@123")
        self.db_manager.execute(
            """
            INSERT OR IGNORE INTO users (username, email, password_hash, salt, role, status)
            VALUES ('member', 'member@library.com', ?, ?, 'MEMBER', 'ACTIVE');
            """,
            (mem_pass, mem_salt)
        )
        mem_user = self.db_manager.fetch_one("SELECT user_id FROM users WHERE username = 'member';")
        if mem_user:
            exp_date = (datetime.date.today() + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
            self.db_manager.execute(
                """
                INSERT OR IGNORE INTO members 
                (user_id, member_code, first_name, last_name, email, phone, address, membership_type, expiry_date, status)
                VALUES (?, 'MEM-2026-0001', 'John', 'Patron', 'member@library.com', '+1-555-0102', '100 University Ave', 'STUDENT', ?, 'ACTIVE');
                """,
                (mem_user["user_id"], exp_date)
            )
        self.db_manager.get_connection().commit()
