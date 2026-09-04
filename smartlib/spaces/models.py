"""Spaces and Equipment data models."""

from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
import datetime


class SpaceType(Enum):
    QUIET_STUDY_ROOM = "quiet_study_room"
    GROUP_STUDY_ROOM = "group_study_room"
    CONFERENCE_HALL = "conference_hall"
    MEDIA_RECORDING_LAB = "media_recording_lab"
    COMPUTER_CLASSROOM = "computer_classroom"


class EquipmentCategory(Enum):
    LAPTOP = "laptop"
    TABLET = "tablet"
    PROJECTOR = "projector"
    CAMERA = "camera"
    AUDIO_RECORDER = "audio_recorder"
    HEADPHONES = "headphones"
    GRAPHICS_TABLET = "graphics_tablet"


@dataclass
class SpaceRoom:
    id: str
    room_number: str
    name: str
    space_type: SpaceType
    capacity: int
    has_projector: bool = False
    has_whiteboard: bool = True
    is_available: bool = True


@dataclass
class SpaceReservation:
    id: str
    room_id: str
    patron_id: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    purpose: str = "Group Study"
    party_size: int = 1
    checked_in: bool = False
    cancelled: bool = False


@dataclass
class EquipmentItem:
    id: str
    barcode: str
    name: str
    category: EquipmentCategory
    model: str
    serial_number: str
    condition_rating: int = 5  # 1-5 scale
    is_checked_out: bool = False


@dataclass
class EquipmentLoan:
    id: str
    equipment_id: str
    patron_id: str
    loaned_at: datetime.datetime
    due_at: datetime.datetime
    returned_at: Optional[datetime.datetime] = None
    accessories_included: List[str] = field(default_factory=list)
