from sqlalchemy.orm import Session
from app import schemas
from app.routers.auth import hash_password
from db import models
from typing import Optional


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name = user.name,
        email = user.email,
        password = hash_password(user.password)
        
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def get_user_by_email(db: Session, email: str):
    return(
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )
    
    
def create_task(db:Session, task: schemas.TaskCreate, owner_id: int):
    db_task = models.Task(
        title = task.title,
        description = task.description,
        priority = task.priority,
        owner_id = owner_id
        
    )
    
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    
    return db_task


def get_tasks(
    db:Session, 
    owner_id:int,
    skip: int =0,
    limit: int = 10,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None
    ):
    query = db.query(models.Task).filter(
        models.Task.owner_id == owner_id
    )

    if completed is not None:
        query = query.filter(models.Task.completed == completed)

    if priority:
        query = query.filter(models.Task.priority == priority)

    if search:
        query = query.filter(
            models.Task.title.ilike(f"%{search}%")
        )

    return query.offset(skip).limit(limit).all()
    
    
def get_task_by_id(db:Session, task_id:int, owner_id: int):
    return(
        db.query(models.Task)
        .filter(
            models.Task.id == task_id, 
            models.Task.owner_id == owner_id
        )
        .first()
    )
    
    
    
def update_task(
    db:Session,
    task_id : int, 
    owner_id: int,
    updated_task: schemas.TaskUpdate
    
):
    
    task = get_task_by_id(db, task_id, owner_id)
    
    
    if task is None:
        return None
    
    task.title = updated_task.title
    task.description = updated_task.description
    task.priority = updated_task.priority
    task.completed = updated_task.completed
    
    
    db.commit()
    db.refresh(task)
    
    
    return task

def delete_task(
    db:Session,
    task_id: int, 
    owner_id: int
):
    task = get_task_by_id(db, task_id, owner_id)
    
    
    if task is None:
        return None
    
    db.delete(task)
    db.commit()
    
    return task

    