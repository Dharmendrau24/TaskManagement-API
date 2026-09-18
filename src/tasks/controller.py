from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException, status
from src.user.models import UserModel
def create_task(body: TaskSchema, db: Session, user: UserModel):
    data = body.model_dump()
    new_task = TaskModel(title = data['title'], description = data['description'], 
    is_completed = data['is_completed'],
    user_id = user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks(db: Session, user: UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all()
    return tasks

def get_one_task(task_id: int, db: Session, user: UserModel):
    one_task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user.id).first()
    if not one_task:
        raise HTTPException(404, detail="Task Id is incorrect")
    return one_task

def update_task(task_id: int, body: TaskSchema, db: Session, user: UserModel):
    data = body.model_dump()
    one_task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user.id).first()
    if not one_task:
        raise HTTPException(404, detail="Task Id is incorrect")
    for field, value in data.items():
        setattr(one_task, field, value)
    db.add(one_task)
    db.commit()
    db.refresh(one_task)
    return one_task

def delete_task(task_id: int, db: Session, user: UserModel): 
    one_task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user.id).first()
    if not one_task:
        raise HTTPException(404, detail="Task Id is incorrect")
    db.delete(one_task)
    db.commit()
    return None