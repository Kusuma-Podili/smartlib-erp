"""Priority Task Queue with Retry Backoff and Dead-Letter Queue."""

import heapq
import time
from enum import Enum, auto
from typing import Callable, Any, Optional, Dict, List
from dataclasses import dataclass, field


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"


@dataclass(order=True)
class PriorityTask:
    priority: int  # Lower number = higher priority
    task_id: str = field(compare=False)
    name: str = field(compare=False)
    handler: Callable[..., Any] = field(compare=False)
    args: tuple = field(default_factory=tuple, compare=False)
    kwargs: dict = field(default_factory=dict, compare=False)
    max_retries: int = field(default=3, compare=False)
    retry_count: int = field(default=0, compare=False)
    status: TaskStatus = field(default=TaskStatus.PENDING, compare=False)
    error_message: Optional[str] = field(default=None, compare=False)


class TaskQueue:
    """Thread-safe priority worker queue."""

    def __init__(self):
        self._heap: List[PriorityTask] = []
        self._dead_letter: List[PriorityTask] = []
        self._completed: List[PriorityTask] = []

    def enqueue(self, task_id: str, name: str, handler: Callable[..., Any],
                priority: int = 10, *args, **kwargs) -> PriorityTask:
        task = PriorityTask(
            priority=priority, task_id=task_id, name=name,
            handler=handler, args=args, kwargs=kwargs
        )
        heapq.heappush(self._heap, task)
        return task

    def process_next(self) -> Optional[PriorityTask]:
        if not self._heap:
            return None
        task = heapq.heappop(self._heap)
        task.status = TaskStatus.RUNNING
        try:
            task.handler(*task.args, **task.kwargs)
            task.status = TaskStatus.COMPLETED
            self._completed.append(task)
            return task
        except Exception as e:
            task.error_message = str(e)
            task.retry_count += 1
            if task.retry_count <= task.max_retries:
                task.status = TaskStatus.PENDING
                heapq.heappush(self._heap, task)
            else:
                task.status = TaskStatus.DEAD_LETTER
                self._dead_letter.append(task)
            return task
