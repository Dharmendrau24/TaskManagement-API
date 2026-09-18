from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskSortBy(str, Enum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    DUE_DATE = "due_date"
    TITLE = "title"
    PRIORITY = "priority"

class TaskSortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    is_completed: bool = False
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = None


class TaskUpdateSchema(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, min_length=1)
    is_completed: bool | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None


class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool
    priority: TaskPriority
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime
    user_id: int

    model_config = {
        "from_attributes": True
    }

class TaskListResponseSchema(BaseModel):
    total: int
    page: int
    skip: int
    limit: int
    has_next: bool
    has_previous: bool
    tasks: list[TaskResponseSchema]