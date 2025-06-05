from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(BaseModel):
    status: TaskStatus
    title: str
    description: str | None = None
    due_date: datetime


class TaskResponse(Task):
    pass