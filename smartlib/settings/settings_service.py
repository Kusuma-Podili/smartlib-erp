"""Service managing system policies and runtime parameters."""
from typing import Optional, List, Dict, Any
from smartlib.settings.models import SystemSetting
from smartlib.settings.repository import SettingsRepository
from smartlib.audit.audit_service import AuditService
from smartlib.constants import AuditAction

class SettingsService:
    def __init__(self, repo: Optional[SettingsRepository] = None, audit_svc: Optional[AuditService] = None):
        self.repo = repo or SettingsRepository()
        self.audit_svc = audit_svc or AuditService()

    def get_setting_value(self, key: str, default: str = "") -> str:
        s = self.repo.get(key)
        return s.setting_value if s else default

    def update_setting(self, key: str, value: Any, actor_username: str = "admin") -> None:
        val_str = str(value)
        self.repo.set(key, val_str)
        self.audit_svc.log(
            action=AuditAction.SETTING_UPDATE.value,
            entity_type="SystemSetting",
            entity_id=key,
            username=actor_username,
            description=f"Updated setting '{key}' to '{val_str}'."
        )

    def list_all_settings(self) -> List[SystemSetting]:
        return self.repo.list_all()
