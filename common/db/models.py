from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from common.db import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column()
    due_date: Mapped[datetime] = mapped_column(nullable=True)