from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    name: str = Field(nullable=False, max_length=100)


class User(UserBase, table=True):
    """
    User model representing a registered user in the system.
    """
    id: Optional[str] = Field(default=None, primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium", max_length=10)  # low, medium, high
    due_date: Optional[datetime] = Field(default=None)
    user_id: str = Field(foreign_key="user.id")


class Task(TaskBase, table=True):
    """
    Task model representing a todo item owned by a user.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)


class TaskPublic(TaskBase):
    """
    Public representation of a Task without internal fields.
    """
    id: int
    created_at: datetime
    updated_at: datetime


class TaskCreate(SQLModel):
    """
    Schema for creating a new Task.
    Only title and description come from the request body;
    user_id is taken from the URL path parameter.
    """
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: str = Field(default="medium", max_length=10)
    due_date: Optional[datetime] = Field(default=None)


class TaskUpdate(SQLModel):
    """
    Schema for updating an existing Task.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(default=None, max_length=10)
    due_date: Optional[datetime] = Field(default=None)