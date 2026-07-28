from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from enum import Enum



class PriorityEnum(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
        
        
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    
    class Config:
        from_attributes = True
        
        
class LoginRequest(BaseModel):
    email:EmailStr
    password: str
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
    
class TaskCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=100
    )
    description: str = Field(
        min_length=5,
        max_length=500
    )
    priority: PriorityEnum = PriorityEnum.MEDIUM
    
    
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: PriorityEnum
    completed: bool
    owner_id: int
    class Config:
        from_attributes = True
        
class TaskUpdate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=100
    )
    description: str = Field(
        min_length=5,
        max_length=500
    )
    priority: PriorityEnum
    completed: bool
    
    
