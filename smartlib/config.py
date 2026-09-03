"""
Configuration loader and runtime settings for SmartLibrary ERP.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class DatabaseConfig:
    db_path: str = os.getenv("SMARTLIB_DB_PATH", "smartlib.db")
    echo_sql: bool = os.getenv("SMARTLIB_ECHO_SQL", "False").lower() in ("true", "1")
    timeout_seconds: float = float(os.getenv("SMARTLIB_DB_TIMEOUT", "30.0"))
    wal_mode: bool = True
    foreign_keys: bool = True

@dataclass
class SecurityConfig:
    secret_key: str = os.getenv("SMARTLIB_SECRET_KEY", "default-insecure-secret-key-change-in-prod")
    password_hash_iterations: int = int(os.getenv("SMARTLIB_HASH_ITERATIONS", "100000"))
    salt_bytes: int = 32
    session_timeout_minutes: int = int(os.getenv("SMARTLIB_SESSION_TIMEOUT", "60"))
    max_failed_attempts: int = int(os.getenv("SMARTLIB_MAX_FAILED_LOGIN", "5"))
    lockout_minutes: int = int(os.getenv("SMARTLIB_LOCKOUT_MINUTES", "15"))
    require_special_char: bool = True
    require_uppercase: bool = True
    require_digit: bool = True
    min_password_length: int = 8

@dataclass
class CirculationConfig:
    default_loan_period_days: int = 14
    default_fine_per_day: float = 10.0
    grace_period_days: int = 1
    max_renewals: int = 2
    reservation_hold_days: int = 3
    lost_book_fee_multiplier: float = 1.5
    damaged_book_fee_percent: float = 0.50

@dataclass
class AppConfig:
    app_name: str = "SmartLibrary ERP"
    version: str = "1.0.0"
    environment: str = os.getenv("SMARTLIB_ENV", "production")
    host: str = os.getenv("SMARTLIB_HOST", "127.0.0.1")
    port: int = int(os.getenv("SMARTLIB_PORT", "8000"))
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    circulation: CirculationConfig = field(default_factory=CirculationConfig)

    @classmethod
    def get_default(cls) -> "AppConfig":
        return cls()

    @classmethod
    def get_test_config(cls) -> "AppConfig":
        cfg = cls()
        cfg.environment = "testing"
        cfg.database.db_path = ":memory:"
        cfg.security.password_hash_iterations = 1000  # Fast testing hashes
        return cfg
