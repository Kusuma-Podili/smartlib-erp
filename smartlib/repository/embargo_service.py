"""Embargo Management and Timed Release Engine."""

from typing import List, Dict
import datetime
from .models import Bitstream, AccessType


class EmbargoService:
    """Controls access restrictions and automatically releases expired embargoes."""

    def __init__(self):
        self.embargoed_bitstreams: List[Bitstream] = []

    def set_embargo(self, bitstream: Bitstream, release_date: datetime.date):
        bitstream.access_type = AccessType.EMBARGOED
        bitstream.embargo_until = release_date
        self.embargoed_bitstreams.append(bitstream)

    def release_expired_embargoes(self) -> int:
        today = datetime.date.today()
        released_count = 0
        active_remaining = []
        for bs in self.embargoed_bitstreams:
            if bs.embargo_until and bs.embargo_until <= today:
                bs.access_type = AccessType.OPEN_ACCESS
                bs.embargo_until = None
                released_count += 1
            else:
                active_remaining.append(bs)
        self.embargoed_bitstreams = active_remaining
        return released_count
