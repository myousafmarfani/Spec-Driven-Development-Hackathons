"""Task storage implementation for the Todo Application."""

from typing import List, Optional
from src.models.task import Task


class TaskStorage:
    """Manages in-memory storage of tasks."""

    def __init__(self):
        """Initialize the in-memory task storage."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add(self, task: Task) -> int:
        """
        Add a task to the storage.

        Args:
            task (Task): Task to add

        Returns:
            int: ID of the added task
        """
        if not isinstance(task, Task):
            raise TypeError("Only Task instances can be added to storage")

        # Set a unique ID if the task doesn't have one or has ID 0
        if task.id == 0 or not hasattr(task, 'id'):
            task.id = self._generate_next_id()

        # If the ID already exists, update it to the next available
        if self.get_by_id(task.id):
            task.id = self._generate_next_id()

        self._tasks.append(task)
        return task.id

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id (int): ID of the task to retrieve

        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def get_all(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            List[Task]: List of all tasks
        """
        return self._tasks.copy()  # Return a copy to prevent external modification

    def update(self, task_id: int, title: str = None, description: str = None, completed: bool = None) -> bool:
        """
        Update a task's properties.

        Args:
            task_id (int): ID of the task to update
            title (str, optional): New title
            description (str, optional): New description
            completed (bool, optional): New completion status

        Returns:
            bool: True if task was updated, False if task not found
        """
        task = self.get_by_id(task_id)
        if not task:
            return False

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        return True

    def delete(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id (int): ID of the task to delete

        Returns:
            bool: True if task was deleted, False if task not found
        """
        task = self.get_by_id(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False

    def _generate_next_id(self) -> int:
        """
        Generate the next unique ID for a task.

        Returns:
            int: Next unique ID
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id