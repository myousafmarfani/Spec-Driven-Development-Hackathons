"""Task manager for the Todo Application."""

from typing import List, Optional, Dict, Any
from src.models.task import Task
from src.storage.task_storage import TaskStorage


class TaskManager:
    """Manages business logic for tasks."""

    def __init__(self):
        """Initialize the task manager with storage."""
        self.storage = TaskStorage()

    def create_task(self, title: str, description: str = "") -> Dict[str, Any]:
        """
        Create a new task with validation.

        Args:
            title (str): Title of the task (1-200 characters)
            description (str): Optional description (max 1000 characters)

        Returns:
            Dict[str, Any]: Result dictionary with task info and success status
        """
        try:
            # Validate title (required field)
            if not title or not title.strip():
                return {
                    "success": False,
                    "message": "Title is required",
                    "task": None
                }

            # Validate title length
            if len(title) < 1 or len(title) > 200:
                return {
                    "success": False,
                    "message": f"Title must be between 1 and 200 characters, got {len(title)}",
                    "task": None
                }

            # Validate description length
            if len(description) > 1000:
                return {
                    "success": False,
                    "message": f"Description must be no more than 1000 characters, got {len(description)}",
                    "task": None
                }

            # Create the task
            task_id = self.storage._generate_next_id()
            task = Task(task_id, title.strip(), description.strip())

            added_id = self.storage.add(task)

            return {
                "success": True,
                "message": "Task created successfully",
                "task": task.to_dict()
            }
        except ValueError as e:
            return {
                "success": False,
                "message": str(e),
                "task": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"An error occurred while creating task: {str(e)}",
                "task": None
            }

    def list_tasks(self) -> Dict[str, Any]:
        """
        List all tasks with their status.

        Returns:
            Dict[str, Any]: Result dictionary with tasks and success status
        """
        try:
            tasks = self.storage.get_all()
            task_dicts = [task.to_dict() for task in tasks]

            return {
                "success": True,
                "message": f"Retrieved {len(tasks)} tasks",
                "tasks": task_dicts,
                "has_tasks": len(tasks) > 0
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"An error occurred while listing tasks: {str(e)}",
                "tasks": [],
                "has_tasks": False
            }

    def update_task(self, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
        """
        Update an existing task.

        Args:
            task_id (int): ID of the task to update
            title (str, optional): New title
            description (str, optional): New description

        Returns:
            Dict[str, Any]: Result dictionary with update status
        """
        try:
            # Validate if title is provided
            if title is not None:
                if len(title) < 1 or len(title) > 200:
                    return {
                        "success": False,
                        "message": f"Title must be between 1 and 200 characters, got {len(title)}",
                        "task": None
                    }

            # Validate if description is provided
            if description is not None:
                if len(description) > 1000:
                    return {
                        "success": False,
                        "message": f"Description must be no more than 1000 characters, got {len(description)}",
                        "task": None
                    }

            # Check if task exists
            existing_task = self.storage.get_by_id(task_id)
            if not existing_task:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} does not exist",
                    "task": None
                }

            # Perform update
            success = self.storage.update(task_id, title, description)
            if success:
                updated_task = self.storage.get_by_id(task_id)

                return {
                    "success": True,
                    "message": f"Task {task_id} updated successfully",
                    "task": updated_task.to_dict()
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to update task {task_id}",
                    "task": None
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"An error occurred while updating task: {str(e)}",
                "task": None
            }

    def delete_task(self, task_id: int) -> Dict[str, Any]:
        """
        Delete a task by ID.

        Args:
            task_id (int): ID of the task to delete

        Returns:
            Dict[str, Any]: Result dictionary with deletion status
        """
        try:
            # Check if task exists
            existing_task = self.storage.get_by_id(task_id)
            if not existing_task:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} does not exist",
                    "task": None
                }

            # Perform deletion
            success = self.storage.delete(task_id)
            if success:
                return {
                    "success": True,
                    "message": f"Task {task_id} deleted successfully",
                    "task": None
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to delete task {task_id}",
                    "task": None
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"An error occurred while deleting task: {str(e)}",
                "task": None
            }

    def toggle_complete(self, task_id: int) -> Dict[str, Any]:
        """
        Toggle the completion status of a task.

        Args:
            task_id (int): ID of the task to toggle

        Returns:
            Dict[str, Any]: Result dictionary with toggle status
        """
        try:
            # Check if task exists
            existing_task = self.storage.get_by_id(task_id)
            if not existing_task:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} does not exist",
                    "task": None
                }

            # Toggle completion status
            new_status = not existing_task.completed
            success = self.storage.update(task_id, completed=new_status)

            if success:
                updated_task = self.storage.get_by_id(task_id)

                status_text = "completed" if updated_task.completed else "incomplete"
                return {
                    "success": True,
                    "message": f"Task {task_id} marked as {status_text}",
                    "task": updated_task.to_dict()
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to toggle completion status for task {task_id}",
                    "task": None
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"An error occurred while toggling task completion: {str(e)}",
                "task": None
            }