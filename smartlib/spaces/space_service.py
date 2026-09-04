"""Study Room and Facility Reservation Service."""

from typing import List, Dict, Optional
import datetime
from .models import SpaceRoom, SpaceReservation, SpaceType


class SpaceReservationService:
    """Manages room availability, patron quotas, and reservations."""

    def __init__(self):
        self.rooms: Dict[str, SpaceRoom] = {}
        self.reservations: List[SpaceReservation] = []

    def add_room(self, room: SpaceRoom):
        self.rooms[room.id] = room

    def is_room_available(self, room_id: str, start_time: datetime.datetime, end_time: datetime.datetime) -> bool:
        if room_id not in self.rooms or not self.rooms[room_id].is_available:
            return False
        for res in self.reservations:
            if res.room_id == room_id and not res.cancelled:
                # Check overlap: (start1 < end2) and (end1 > start2)
                if (start_time < res.end_time) and (end_time > res.start_time):
                    return False
        return True

    def reserve_room(self, room_id: str, patron_id: str, start_time: datetime.datetime,
                     duration_hours: int = 2, party_size: int = 1) -> Optional[SpaceReservation]:
        end_time = start_time + datetime.timedelta(hours=duration_hours)
        if not self.is_room_available(room_id, start_time, end_time):
            return None

        res_id = f"RES-SP-{len(self.reservations)+1:05d}"
        res = SpaceReservation(
            id=res_id,
            room_id=room_id,
            patron_id=patron_id,
            start_time=start_time,
            end_time=end_time,
            party_size=party_size
        )
        self.reservations.append(res)
        return res
