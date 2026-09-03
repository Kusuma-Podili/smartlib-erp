"""
Librarian staff domain model.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Librarian:
    librarian_id: Optional[int] = None
    user_id: int = 0
    employee_code: str = ""
    full_name: str = ""
    phone: Optional[str] = None
    department: str = "General Library"
    shift: str = "Morning"
    desk_location: str = "Circulation Desk 1"
    hire_date: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "librarian_id": self.librarian_id,
            "user_id": self.user_id,
            "employee_code": self.employee_code,
            "full_name": self.full_name,
            "phone": self.phone,
            "department": self.department,
            "shift": self.shift,
            "desk_location": self.desk_location,
            "hire_date": self.hire_date
        }
