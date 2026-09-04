"""5-Field Cron Expression Parser and Task Scheduler."""

import datetime
from typing import List, Callable, Optional
from dataclasses import dataclass


@dataclass
class ScheduledJob:
    id: str
    cron_expr: str
    name: str
    job_func: Callable[[], None]
    last_run: Optional[datetime.datetime] = None


class CronScheduler:
    """Parses standard minute, hour, dom, month, dow cron expressions."""

    def __init__(self):
        self.jobs: List[ScheduledJob] = []

    def _matches_field(self, pattern: str, val: int) -> bool:
        if pattern == "*":
            return True
        if "/" in pattern:
            base, step = pattern.split("/", 1)
            return (val % int(step)) == 0
        if "," in pattern:
            return val in [int(x) for x in pattern.split(",")]
        return val == int(pattern)

    def matches(self, cron_expr: str, dt: datetime.datetime) -> bool:
        fields = cron_expr.split()
        if len(fields) != 5:
            return False
        m, h, dom, mon, dow = fields
        # dow: 0=Sunday in cron, dt.isoweekday() 7=Sunday
        cron_dow = 0 if dt.isoweekday() == 7 else dt.isoweekday()
        return (
            self._matches_field(m, dt.minute) and
            self._matches_field(h, dt.hour) and
            self._matches_field(dom, dt.day) and
            self._matches_field(mon, dt.month) and
            self._matches_field(dow, cron_dow)
        )

    def schedule(self, cron_expr: str, name: str, func: Callable[[], None]):
        job = ScheduledJob(id=f"JOB-{len(self.jobs)+1:03d}", cron_expr=cron_expr, name=name, job_func=func)
        self.jobs.append(job)

    def tick(self, now: Optional[datetime.datetime] = None):
        if now is None:
            now = datetime.datetime.now()
        for job in self.jobs:
            if self.matches(job.cron_expr, now):
                job.last_run = now
                try:
                    job.job_func()
                except Exception:
                    pass
