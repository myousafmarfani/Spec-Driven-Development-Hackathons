from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for token data payload.
    """
    username: Optional[str] = None


class UserBase(BaseModel):
    """
    Base user schema with common fields.
    """
    email: str
    name: str


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str


class User(UserBase):
    """
    Schema for user response.
    """
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    """
    Base task schema with common fields.
    """
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None

    class Config:
        # Allow ORM mode for SQLModel compatibility
        from_attributes = True


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None


class Task(TaskBase):
    """
    Schema for task response.
    """
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """
    Schema for task list response.
    """
    tasks: List[Task]
    total_count: int


class UserAuthResponse(BaseModel):
    """
    Schema for user authentication response.
    """
    user: User
    token: str


class TaskToggleComplete(BaseModel):
    """
    Schema for toggling task completion status.
    """
    completed: bool