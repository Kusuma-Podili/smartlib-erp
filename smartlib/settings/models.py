"""System setting domain model."""
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class SystemSetting:
    setting_id: Optional[int] = None
    setting_key: str = ""
    setting_value: str = ""
    category: str = "GENERAL"
    description: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "setting_id": self.setting_id,
            "setting_key": self.setting_key,
            "setting_value": self.setting_value,
            "category": self.category,
            "description": self.description,
            "updated_at": self.updated_at
        }
