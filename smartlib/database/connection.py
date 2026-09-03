"""
Thread-safe SQLite connection manager with WAL mode, foreign key enforcement, and Unit-of-Work transactions.
"""

import sqlite3
import threading
from contextlib import contextmanager
from typing import Generator, Optional, Any, List, Tuple
from smartlib.config import DatabaseConfig

class DatabaseManager:
    _instance: Optional["DatabaseManager"] = None
    _lock = threading.Lock()

    def __init__(self, config: Optional[DatabaseConfig] = None):
        self.config = config or DatabaseConfig()
        self._local = threading.local()

    @classmethod
    def get_instance(cls, config: Optional[DatabaseConfig] = None) -> "DatabaseManager":
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(config)
            return cls._instance

    @classmethod
    def reset_instance(cls):
        with cls._lock:
            if cls._instance:
                cls._instance.close_all()
                cls._instance = None

    def get_connection(self) -> sqlite3.Connection:
        """Return a thread-local SQLite connection with optimized PRAGMAs."""
        if not hasattr(self._local, "connection") or self._local.connection is None:
            conn = sqlite3.connect(
                self.config.db_path,
                timeout=self.config.timeout_seconds,
                check_same_thread=False
            )
            conn.row_factory = sqlite3.Row
            # Enforce Foreign Keys & enable Write-Ahead Logging
            cursor = conn.cursor()
            if self.config.foreign_keys:
                cursor.execute("PRAGMA foreign_keys = ON;")
            if self.config.wal_mode and self.config.db_path != ":memory:":
                cursor.execute("PRAGMA journal_mode = WAL;")
            cursor.execute("PRAGMA synchronous = NORMAL;")
            cursor.close()
            self._local.connection = conn
        return self._local.connection

    @contextmanager
    def transaction(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager providing atomic ACID transactional block with auto-commit/rollback."""
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def execute(self, sql: str, params: Tuple[Any, ...] = ()) -> sqlite3.Cursor:
        """Execute a single SQL command."""
        conn = self.get_connection()
        return conn.execute(sql, params)

    def execute_script(self, sql_script: str) -> None:
        """Execute multi-statement SQL script."""
        conn = self.get_connection()
        conn.executescript(sql_script)
        conn.commit()

    def fetch_all(self, sql: str, params: Tuple[Any, ...] = ()) -> List[sqlite3.Row]:
        """Execute query and fetch all rows as sqlite3.Row."""
        cursor = self.execute(sql, params)
        return cursor.fetchall()

    def fetch_one(self, sql: str, params: Tuple[Any, ...] = ()) -> Optional[sqlite3.Row]:
        """Execute query and fetch single row."""
        cursor = self.execute(sql, params)
        return cursor.fetchone()

    def close_all(self):
        """Close thread connection."""
        if hasattr(self._local, "connection") and self._local.connection is not None:
            try:
                self._local.connection.close()
            except Exception:
                pass
            self._local.connection = None

class UnitOfWork:
    """Unit of Work pattern encapsulating transactional integrity across multiple repositories."""
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()
        self.conn: Optional[sqlite3.Connection] = None

    def __enter__(self) -> "UnitOfWork":
        self.conn = self.db_manager.get_connection()
        self.conn.execute("BEGIN IMMEDIATE;")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            if self.conn:
                self.conn.rollback()
            return False
        else:
            if self.conn:
                self.conn.commit()
            return True

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()
