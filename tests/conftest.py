"""
Test fixtures: In-memory SQLite database configuration, isolated state resets, and seeders.
"""

import unittest
import os
from smartlib.config import AppConfig
from smartlib.database.connection import DatabaseManager
from smartlib.database.migrations import MigrationManager
from smartlib.database.seeder import DatabaseSeeder

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # Reset database manager to use in-memory database
        DatabaseManager.reset_instance()
        self.config = AppConfig.get_test_config()
        self.db_manager = DatabaseManager.get_instance(self.config.database)
        self.migrator = MigrationManager(self.db_manager)
        self.migrator.apply_initial_schema()
        self.seeder = DatabaseSeeder(self.db_manager)
        self.seeder.seed_all()

    def tearDown(self):
        DatabaseManager.reset_instance()
