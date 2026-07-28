from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import models
from app import crud, schemas
from app.dependencies import get_db, get_current_user
from fastapi import HTTPException

from app.routers.auth import(
    verify_password,
    create_access_token
    
)



router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
    
)

@router.post("/",response_model = schemas.UserResponse)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(db = db, user=user)



@router.post(
    "/login",
    response_model=schemas.Token
)
def login(
    user: schemas.LoginRequest,
    db: Session = Depends(get_db)
):

    db_user = crud.get_user_by_email(
        db,
        user.email
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
        
@router.get("/me")
def get_me(
    current_user: models.User = Depends(get_current_user)
    
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }