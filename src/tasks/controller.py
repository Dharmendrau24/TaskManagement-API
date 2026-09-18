from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.tasks.dtos import (
    TaskCreateSchema,
    TaskUpdateSchema,
)
from src.tasks.models import TaskModel
from src.user.models import UserModel


def create_task(
    body: TaskCreateSchema,
    db: Session,
    user: UserModel,
):
    new_task = TaskModel(
        title=body.title,
        description=body.description,
        is_completed=body.is_completed,
        priority=body.priority,
        due_date=body.due_date,
        user_id=user.id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_tasks(
    db: Session,
    user: UserModel,
    skip: int = 0,
    limit: int = 10,
    priority=None,
    is_completed: bool | None = None,
    sort_by=None,
    sort_order=None,
    search: str | None = None,
):
    query = (
        db.query(TaskModel)
        .filter(TaskModel.user_id == user.id)
    )

    # Search filter
    if search:
        search_term = search.strip()

        query = query.filter(
            TaskModel.title.ilike(f"%{search_term}%")
        )

    # Priority filter
    if priority:
        query = query.filter(
            TaskModel.priority == priority.value
        )

    # Completion filter
    if is_completed is not None:
        query = query.filter(
            TaskModel.is_completed == is_completed
        )

    # Allowed sorting fields
    allowed_sort_fields = {
        "created_at": TaskModel.created_at,
        "updated_at": TaskModel.updated_at,
        "due_date": TaskModel.due_date,
        "title": TaskModel.title,
        "priority": TaskModel.priority,
    }

    sort_column = allowed_sort_fields.get(
        sort_by.value if sort_by else "created_at"
    )

    if sort_order is not None and sort_order.value == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # Total matching records BEFORE pagination
    total = query.count()

    # Apply pagination
    tasks = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    page = (skip // limit) + 1
    has_previous = skip > 0
    has_next = skip + limit < total

    return {
        "total": total,
        "page": page,
        "skip": skip,
        "limit": limit,
        "has_next": has_next,
        "has_previous": has_previous,
        "tasks": tasks,
    }   

def get_one_task(
    task_id: int,
    db: Session,
    user: UserModel,
):
    task = (
        db.query(TaskModel)
        .filter(
            TaskModel.id == task_id,
            TaskModel.user_id == user.id,
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


def update_task(
    task_id: int,
    body: TaskUpdateSchema,
    db: Session,
    user: UserModel,
):
    task = (
        db.query(TaskModel)
        .filter(
            TaskModel.id == task_id,
            TaskModel.user_id == user.id,
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    update_data = body.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    task_id: int,
    db: Session,
    user: UserModel,
):
    task = (
        db.query(TaskModel)
        .filter(
            TaskModel.id == task_id,
            TaskModel.user_id == user.id,
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    db.delete(task)
    db.commit()