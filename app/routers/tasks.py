from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from db import models
from app.dependencies import get_db, get_current_user
from typing import List, Optional

router = APIRouter(
    prefix = "/tasks",
    tags = ["Tasks"]
)




@router.post("/", response_model = schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
    
    
):
    return crud.create_task(
        db = db, 
        task = task,
        owner_id = current_user.id
    )
    
    
@router.get("/", response_model=list[schemas.TaskResponse])
def get_my_tasks(
    skip: int = 0,
    limit: int = 10,
    completed: Optional[bool] = None,
    priority: Optional[schemas.PriorityEnum] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_tasks(
        db=db,
        owner_id=current_user.id,
        skip=skip,
        limit=limit,
        completed=completed,
        priority=priority.value if priority else None,
        search=search,
    )
    
    
@router.get("/{task_id}", response_model = schemas.TaskResponse)
def get_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
    
):
    task = crud.get_task_by_id(
        db = db,
        task_id = task_id,
        owner_id = current_user.id
    )
    
    if task is None:
        raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
        
    return task


@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    updated = crud.update_task(
        db=db,
        task_id=task_id,
        owner_id=current_user.id,
        updated_task=task
    )

    if updated is None:
        raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

    return updated



@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task = crud.delete_task(
        db=db,
        task_id=task_id,
        owner_id=current_user.id
    )

    if task is None:
        raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

    return {
        "message": "Task deleted successfully"
    }