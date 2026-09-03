"""Data repository for system settings."""
from typing import Optional, List, Dict
from smartlib.database.connection import DatabaseManager
from smartlib.settings.models import SystemSetting

class SettingsRepository:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def get(self, key: str) -> Optional[SystemSetting]:
        sql = "SELECT * FROM system_settings WHERE setting_key = ?;"
        row = self.db_manager.fetch_one(sql, (key.strip(),))
        return SystemSetting(**dict(row)) if row else None

    def set(self, key: str, value: str, category: str = "GENERAL", description: Optional[str] = None) -> None:
        sql = """
        INSERT INTO system_settings (setting_key, setting_value, category, description)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(setting_key) DO UPDATE SET
            setting_value = excluded.setting_value,
            updated_at = CURRENT_TIMESTAMP;
        """
        self.db_manager.execute(sql, (key.strip(), str(value), category, description))
        self.db_manager.get_connection().commit()

    def list_all(self) -> List[SystemSetting]:
        rows = self.db_manager.fetch_all("SELECT * FROM system_settings ORDER BY category, setting_key;")
        return [SystemSetting(**dict(r)) for r in rows]
