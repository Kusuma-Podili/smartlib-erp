"""Library Workshop, Author Reading, and Community Event Service."""

from typing import List, Dict, Optional
import datetime
from dataclasses import dataclass, field


@dataclass
class LibraryEvent:
    id: str
    title: str
    presenter: str
    room_id: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    capacity: int
    registered_patron_ids: List[str] = field(default_factory=list)
    waitlist_patron_ids: List[str] = field(default_factory=list)


class LibraryEventService:
    """Manages library workshops, events, registration, and waitlists."""

    def __init__(self):
        self.events: Dict[str, LibraryEvent] = {}

    def create_event(self, title: str, presenter: str, room_id: str,
                     start_time: datetime.datetime, end_time: datetime.datetime, capacity: int = 30) -> LibraryEvent:
        e_id = f"EVT-{len(self.events)+1:04d}"
        ev = LibraryEvent(
            id=e_id, title=title, presenter=presenter, room_id=room_id,
            start_time=start_time, end_time=end_time, capacity=capacity
        )
        self.events[e_id] = ev
        return ev

    def register_patron(self, event_id: str, patron_id: str) -> str:
        ev = self.events.get(event_id)
        if not ev:
            return "NOT_FOUND"

        if patron_id in ev.registered_patron_ids:
            return "ALREADY_REGISTERED"

        if len(ev.registered_patron_ids) < ev.capacity:
            ev.registered_patron_ids.append(patron_id)
            return "CONFIRMED"
        else:
            if patron_id not in ev.waitlist_patron_ids:
                ev.waitlist_patron_ids.append(patron_id)
            return "WAITLISTED"
