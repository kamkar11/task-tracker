from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task:
    status: TaskStatus
    title: str
    description: str | None
    due_date: datetime


class TaskResponse(Task):
    pass