"""Task data model for the Todo Application."""

from datetime import datetime
from typing import Dict, Any


class Task:
    """Represents a single task in the todo application."""

    def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False):
        """
        Initialize a new Task instance.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Title of the task (required, 1-200 characters)
            description (str): Optional description of the task (max 1000 characters)
            completed (bool): Whether the task is completed (default: False)

        Raises:
            ValueError: If title or description do not meet validation requirements
        """
        self._validate_title(title)
        self._validate_description(description)

        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = datetime.now()

    @staticmethod
    def _validate_title(title: str) -> None:
        """
        Validate the title according to requirements (1-200 characters).

        Args:
            title (str): Title to validate

        Raises:
            ValueError: If title does not meet requirements
        """
        if not isinstance(title, str):
            raise ValueError("Title must be a string")
        if len(title) < 1 or len(title) > 200:
            raise ValueError(f"Title must be between 1 and 200 characters, got {len(title)}")

    @staticmethod
    def _validate_description(description: str) -> None:
        """
        Validate the description according to requirements (max 1000 characters).

        Args:
            description (str): Description to validate

        Raises:
            ValueError: If description does not meet requirements
        """
        if not isinstance(description, str):
            raise ValueError("Description must be a string")
        if len(description) > 1000:
            raise ValueError(f"Description must be no more than 1000 characters, got {len(description)}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Task instance to a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary representation of the task
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }

    def __str__(self) -> str:
        """
        Return a string representation of the task.

        Returns:
            str: String representation of the task
        """
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}: {self.title}"

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the task.

        Returns:
            str: Detailed string representation of the task
        """
        return f"Task(id={self.id}, title='{self.title}', completed={self.completed})"