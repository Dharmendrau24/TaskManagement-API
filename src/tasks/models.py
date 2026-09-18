from datetime import datetime, UTC

from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, DateTime

from src.utils.db import Base


class TaskModel(Base):
    __tablename__ = "user_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String, nullable=False)

    description = Column(String, nullable=False)

    is_completed = Column(Boolean, default=False, nullable=False)

    priority = Column(String, default="medium", nullable=False)

    due_date = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    user_id = Column(
        Integer,
        ForeignKey("user_table.id", ondelete="CASCADE"),
        nullable=False,
    )