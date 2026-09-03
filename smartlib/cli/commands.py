"""
Implementations of administrative CLI commands.
"""

import sys
from smartlib.database.connection import DatabaseManager
from smartlib.database.migrations import MigrationManager
from smartlib.database.seeder import DatabaseSeeder
from smartlib.users.user_service import UserService
from smartlib.users.models import UserDTO
from smartlib.utilities.formatting import format_table

class CLICommands:
    @staticmethod
    def init_db():
        print("[+] Initializing database tables and schema migrations...")
        migrator = MigrationManager()
        migrator.apply_initial_schema()
        print("[OK] Database initialized successfully.")

    @staticmethod
    def seed_data():
        print("[+] Seeding default roles, policies, and system credentials...")
        seeder = DatabaseSeeder()
        seeder.seed_all()
        print("[OK] Seed data applied successfully.")

    @staticmethod
    def list_users():
        user_svc = UserService()
        users = user_svc.list_users(limit=100)
        headers = ["ID", "Username", "Email", "Role", "Status", "Last Login"]
        rows = [
            [u.user_id, u.username, u.email, u.role, u.status, u.last_login_at or "Never"]
            for u in users
        ]
        print(format_table(headers, rows))

    @staticmethod
    def create_user(username, email, password, role="MEMBER"):
        user_svc = UserService()
        dto = UserDTO(username=username, email=email, password=password, role=role)
        u = user_svc.register_user(dto, actor_username="CLI_ADMIN")
        print(f"[OK] Created user: ID={u.user_id}, Username='{u.username}', Role='{u.role}'")
