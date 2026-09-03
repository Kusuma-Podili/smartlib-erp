"""
Database migration runner and schema version management.
"""

import logging
from typing import Optional
from smartlib.database.connection import DatabaseManager
from smartlib.database.schema import SCHEMA_DDL

logger = logging.getLogger("smartlib.migrations")

class MigrationManager:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def ensure_migration_table(self):
        """Ensure the schema_migrations table exists."""
        sql = """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT
        );
        """
        self.db_manager.execute(sql)

    def get_current_version(self) -> int:
        """Get the highest applied migration version."""
        self.ensure_migration_table()
        row = self.db_manager.fetch_one("SELECT MAX(version) as max_v FROM schema_migrations;")
        if row and row["max_v"] is not None:
            return int(row["max_v"])
        return 0

    def apply_initial_schema(self) -> None:
        """Execute full DDL schema if version is 0."""
        current_v = self.get_current_version()
        if current_v < 1:
            logger.info("Applying initial schema migration (v1)...")
            self.db_manager.execute_script(SCHEMA_DDL)
            self.db_manager.execute(
                "INSERT INTO schema_migrations (version, description) VALUES (1, 'Initial ERP Schema (23 tables)');"
            )
            self.db_manager.get_connection().commit()
            logger.info("Schema migration v1 applied successfully.")
        else:
            logger.info("Database schema is up to date (version %d).", current_v)
