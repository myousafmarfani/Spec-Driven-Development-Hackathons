from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from typing import List, Optional
from datetime import datetime

from models import Task, TaskCreate, TaskUpdate
from schemas import Task as TaskSchema, TaskListResponse
from db import get_session
from auth import get_current_user, verify_user_owns_token
from typing import Annotated

router = APIRouter(prefix="/api", tags=["tasks"])

# Create a dependency for the current user
CurrentUserDependency = Annotated[str, Depends(get_current_user)]
SessionDependency = Annotated[Session, Depends(get_session)]


@router.get("/{user_id}/tasks", response_model=List[TaskSchema])
async def get_tasks(
    user_id: str,
    status: Optional[str] = None,
    current_user_id: CurrentUserDependency = None,
    session: SessionDependency = None
):
    """
    Get all tasks for a specific user.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        status: Optional filter for task status ("all", "pending", "completed")
        current_user_id: The ID of the currently authenticated user
        session: Database session

    Returns:
        List of tasks for the specified user
    """
    # Verify that the user_id in the path matches the authenticated user
    verify_user_owns_token(user_id, current_user_id)

    # Build query based on optional status filter
    query = select(Task).where(Task.user_id == user_id)

    if status and status.lower() == "completed":
        query = query.where(Task.completed == True)
    elif status and status.lower() == "pending":
        query = query.where(Task.completed == False)

    # Order by creation date (newest first)
    query = query.order_by(Task.created_at.desc())

    tasks = session.exec(query).all()
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskSchema)
async def create_task(
    user_id: str,
    task_create: TaskCreate,
    current_user_id: CurrentUserDependency = None,
    session: SessionDependency = None
):
    """
    Create a new task for a specific user.

    Args:
        user_id: The ID of the user to create the task for
        task_create: Task creation data
        current_user_id: The ID of the currently authenticated user
        session: Database session

    Returns:
        The created task
    """
    # Verify that the user_id in the path matches the authenticated user
    verify_user_owns_token(user_id, current_user_id)

    # Calculate the next task_number for this user
    max_task_number_query = select(func.max(Task.task_number)).where(Task.user_id == user_id)
    max_task_number = session.exec(max_task_number_query).first()
    next_task_number = (max_task_number or 0) + 1

    # Create task instance with the user_id from the path
    now = datetime.now()
    task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=False,
        priority=task_create.priority or "medium",
        due_date=task_create.due_date,
        user_id=user_id,
        task_number=next_task_number,
        created_at=now,
        updated_at=now,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskSchema)
async def get_task(
    user_id: str,
    task_id: int,
    current_user_id: CurrentUserDependency = None,
    session: SessionDependency = None
):
    """
    Get a specific task by ID for a specific user.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to retrieve
        current_user_id: The ID of the currently authenticated user
        session: Database session

    Returns:
        The requested task
    """
    # Verify that the user_id in the path matches the authenticated user
    verify_user_owns_token(user_id, current_user_id)

    # Query for the task with both user_id and task_id
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskSchema)
async def update_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: CurrentUserDependency = None,
    session: SessionDependency = None
):
    """
    Update a specific task by ID for a specific user.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        task_update: Task update data
        current_user_id: The ID of the currently authenticated user
        session: Database session

    Returns:
        The updated task
    """
    # Verify that the user_id in the path matches the authenticated user
    verify_user_owns_token(user_id, current_user_id)

    # Query for the task with both user_id and task_id
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update the task with provided fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    # Update the updated_at timestamp
    task.updated_at = datetime.now()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: str,
    task_id: int,
    current_user_id: CurrentUserDependency = None,
    session: SessionDependency = None
):
    """
    Delete a specific task by ID for a specific user.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to delete
        current_user_id: The ID of the currently authenticated user
        session: Database session

    Returns:
        Success message
    """
    # Verify that the user_id in the path matches the authenticated user
    verify_user_owns_token(user_id, current_user_id)

    # Query for the task with both user_id and task_id
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskSchema)
async def toggle_task_complete(
    user_id: str,
    task_id: int,
    current_user_id: CurrentUserDependency = None,
    session: SessionDependency = None
):
    """
    Toggle the completion status of a specific task by ID for a specific user.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to toggle
        current_user_id: The ID of the currently authenticated user
        session: Database session

    Returns:
        The updated task with new completion status
    """
    # Verify that the user_id in the path matches the authenticated user
    verify_user_owns_token(user_id, current_user_id)

    # Query for the task with both user_id and task_id
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this task"
        )

    # Toggle the completed status
    task.completed = not task.completed
    task.updated_at = datetime.now()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task