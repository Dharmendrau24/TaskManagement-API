from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.tasks import controller
from src.tasks.dtos import (
    TaskCreateSchema,
    TaskResponseSchema,
    TaskUpdateSchema,
    TaskPriority,
    TaskSortBy,
    TaskSortOrder,
    TaskListResponseSchema,
)
from src.user.models import UserModel
from src.utils.db import get_db
from src.utils.helpers import is_authenticated


task_routes = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_routes.post(
    "",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    body: TaskCreateSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated),
):
    return controller.create_task(body, db, user)


@task_routes.get(
    "",
    response_model=TaskListResponseSchema,
    status_code=status.HTTP_200_OK,
)

def get_tasks(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    priority: TaskPriority | None = None,
    is_completed: bool | None = None,
    sort_by: TaskSortBy = Query(default=TaskSortBy.CREATED_AT),
    sort_order: TaskSortOrder = Query(default=TaskSortOrder.DESC),
    search: str | None = Query(default=None, min_length=1, max_length=100),
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated),
):
    return controller.get_tasks(
        db,
        user,
        skip,
        limit,
        priority,
        is_completed,
        sort_by,
        sort_order,
        search,
    )


@task_routes.get(
    "/{task_id}",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_200_OK,
)
def get_one_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated),
):
    return controller.get_one_task(task_id, db, user)


@task_routes.put(
    "/{task_id}",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_200_OK,
)
def update_task(
    task_id: int,
    body: TaskUpdateSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated),
):
    return controller.update_task(task_id, body, db, user)


@task_routes.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated),
):
    controller.delete_task(task_id, db, user)